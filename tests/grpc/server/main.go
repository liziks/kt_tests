package server

import (
	"context"
	"fmt"
	pb "grpc_test/auth"
	"log"
	"net"
	"sync"
	"time"

	"github.com/golang-jwt/jwt/v4"
	"golang.org/x/crypto/bcrypt"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

var jwtSecret = []byte("jwt_secret_key")

type User struct {
	Username       string
	HashedPassword string
}

type authServer struct {
	pb.UnimplementedAuthServiceServer
	users map[string]User
	mu    sync.Mutex
}

func NewAuthServer() *authServer {
	return &authServer{
		users: make(map[string]User),
	}
}

type Claims struct {
	jwt.RegisteredClaims
	Username string `json:"username"`
}

func generateToken(username string) (string, error) {
	expirationTime := time.Now().Add(24 * time.Hour)
	claims := &Claims{
		Username: username,
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(expirationTime),
			IssuedAt:  jwt.NewNumericDate(time.Now()),
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	tokenString, err := token.SignedString(jwtSecret)
	if err != nil {
		return "", err
	}
	return tokenString, nil
}

func (s *authServer) Register(
	ctx context.Context,
	req *pb.RegisterRequest,
) (*pb.AuthResponse, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	if len(req.Password) < 8 {
		return nil, status.Errorf(
			codes.InvalidArgument,
			"Пароль должен быть не менее %d символов",
			8,
		)
	}

	if _, exists := s.users[req.Username]; exists {
		return nil, status.Errorf(
			codes.AlreadyExists,
			"Пользователь с таким именем уже существует",
		)
	}

	hashedPassword, err := bcrypt.GenerateFromPassword(
		[]byte(req.Password),
		bcrypt.DefaultCost,
	)
	if err != nil {
		log.Printf("Ошибка хеширования пароля: %v", err)
		return nil, status.Errorf(codes.Internal, "Ошибка сервера при регистрации")
	}

	s.users[req.Username] = User{
		Username:       req.Username,
		HashedPassword: string(hashedPassword),
	}

	token, err := generateToken(req.Username)
	if err != nil {
		log.Printf("Ошибка генерации токена: %v", err)
		return nil, status.Errorf(
			codes.Internal,
			"Ошибка сервера при генерации токена",
		)
	}

	log.Printf("Пользователь %s зарегистрирован", req.Username)
	return &pb.AuthResponse{Token: token}, nil
}

func (s *authServer) Login(
	ctx context.Context,
	req *pb.LoginRequest,
) (*pb.AuthResponse, error) {
	s.mu.Lock()
	user, exists := s.users[req.Username]
	s.mu.Unlock()

	if !exists {
		return nil, status.Errorf(codes.NotFound, "Пользователь не найден")
	}

	err := bcrypt.CompareHashAndPassword(
		[]byte(user.HashedPassword),
		[]byte(req.Password),
	)
	if err != nil {
		return nil, status.Errorf(codes.Unauthenticated, "Неверный пароль")
	}

	token, err := generateToken(req.Username)
	if err != nil {
		log.Printf("Ошибка генерации токена: %v", err)
		return nil, status.Errorf(
			codes.Internal,
			"Ошибка сервера при генерации токена",
		)
	}

	log.Printf("Пользователь %s вошел в систему", req.Username)
	return &pb.AuthResponse{Token: token}, nil
}

func (s *authServer) ValidateToken(
	ctx context.Context,
	req *pb.ValidateTokenRequest,
) (*pb.ValidateTokenResponse, error) {
	claims := &Claims{}

	token, err := jwt.ParseWithClaims(
		req.Token,
		claims,
		func(token *jwt.Token) (interface{}, error) {
			if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
				return nil, fmt.Errorf(
					"неожиданный метод подписи: %v",
					token.Header["alg"],
				)
			}
			return jwtSecret, nil
		},
	)

	if err != nil {
		if err == jwt.ErrSignatureInvalid {
			return &pb.ValidateTokenResponse{Valid: false}, nil
		}
		return &pb.ValidateTokenResponse{Valid: false}, nil
	}

	if !token.Valid {
		return &pb.ValidateTokenResponse{Valid: false}, nil
	}

	log.Printf("Токен для пользователя %s валиден", claims.Username)
	return &pb.ValidateTokenResponse{Valid: true, Username: claims.Username}, nil
}

func main() {
	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatalf("Не удалось начать слушать порт: %v", err)
	}

	grpcServer := grpc.NewServer()
	authSrv := NewAuthServer()
	pb.RegisterAuthServiceServer(grpcServer, authSrv)

	log.Printf("Сервер запущен на порту %s", lis.Addr().String())
	if err := grpcServer.Serve(lis); err != nil {
		log.Fatalf("Не удалось запустить сервер: %v", err)
	}
}
