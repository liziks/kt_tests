package client

import (
	"context"
	"log"
	"net"
	"os"
	"sync"
	"testing"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/grpc/status"

	pb "grpc_test/auth"
	"grpc_test/server"
)

var (
	testServerAddr string
	once           sync.Once
)

type authServerForTest struct {
	pb.UnimplementedAuthServiceServer
	mu    sync.Mutex
	users map[string]server.User
}

func NewAuthServerForTest() *authServerForTest {
	return &authServerForTest{
		users: make(map[string]server.User),
	}
}

func setupTestServer(tb testing.TB) (
	client pb.AuthServiceClient,
	closer func(),
) {
	once.Do(func() {
		lis, err := net.Listen("tcp", "localhost:0")
		if err != nil {
			log.Fatalf("Не удалось начать слушать порт: %v", err)
		}
		testServerAddr = lis.Addr().String()
		log.Printf("Тестовый сервер запущен на %s", testServerAddr)

		grpcServer := grpc.NewServer()

		authSrvInstance := server.NewAuthServer()
		pb.RegisterAuthServiceServer(grpcServer, authSrvInstance)

		go func() {
			if err := grpcServer.Serve(lis); err != nil {
				if err != grpc.ErrServerStopped && err.Error() != "accept tcp [::]:0: use of closed network connection" {
					log.Printf("Ошибка тестового сервера: %v", err)
				}
			}
		}()
		closer = func() {
			grpcServer.Stop()
			lis.Close()
			log.Println("Тестовый сервер остановлен")
		}
	})

	conn, err := grpc.Dial(
		testServerAddr,
		grpc.WithTransportCredentials(insecure.NewCredentials()),
	)
	if err != nil {
		tb.Fatalf("Не удалось подключиться к тестовому серверу: %v", err)
	}
	client = pb.NewAuthServiceClient(conn)

	clientCloser := func() {
		conn.Close()
	}
	tb.Cleanup(clientCloser)

	return client, closer
}

func TestMain(m *testing.M) {
	code := m.Run()
	os.Exit(code)
}

func TestAuthService_Register_Successful(t *testing.T) {
	client, _ := setupTestServer(t)

	ctx, cancel := context.WithTimeout(
		context.Background(),
		time.Second,
	)
	defer cancel()

	resp, err := client.Register(ctx, &pb.RegisterRequest{
		Username: "testuser1",
		Password: "password123",
	})

	if err != nil {
		t.Fatalf("Register() failed: %v", err)
	}
	if resp.Token == "" {
		t.Errorf("Register()_Successful: ожидался токен, получен пустой")
	}
}

func TestAuthService_Register_ShortPassword(t *testing.T) {
	client, _ := setupTestServer(t)
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	_, err := client.Register(ctx, &pb.RegisterRequest{
		Username: "shortpassuser",
		Password: "short",
	})

	if err == nil {
		t.Fatal("Register()_ShortPassword: ожидалась ошибка, но ее не было")
	}

	st, ok := status.FromError(err)
	if !ok {
		t.Fatalf("Register()_ShortPassword: не удалось получить статус из ошибки: %v", err)
	}
	if st.Code() != codes.InvalidArgument {
		t.Errorf("Register()_ShortPassword: ожидался код ошибки InvalidArgument, получен %s", st.Code())
	}
	t.Logf("Register_ShortPassword: Получена ожидаемая ошибка: %v", err)
}

func TestAuthService_Login_Successful(t *testing.T) {
	client, _ := setupTestServer(t)
	ctx, cancel := context.WithTimeout(context.Background(), time.Second*2)
	defer cancel()

	regUsername := "logintestuser"
	regPassword := "loginpassword123"
	_, err := client.Register(ctx, &pb.RegisterRequest{
		Username: regUsername,
		Password: regPassword,
	})
	if err != nil {
		st, ok := status.FromError(err)
		if !ok || st.Code() != codes.AlreadyExists {
			t.Fatalf(
				"Login_Successful: Ошибка при предварительной регистрации: %v",
				err,
			)
		}
	}

	resp, err := client.Login(ctx, &pb.LoginRequest{
		Username: regUsername,
		Password: regPassword,
	})

	if err != nil {
		t.Fatalf("Login()_Successful failed: %v", err)
	}
	if resp.Token == "" {
		t.Errorf("Login()_Successful: ожидался токен, получен пустой")
	}
	t.Logf("Login_Successful: Token: %s", resp.Token)
}

func TestAuthService_Login_IncorrectPassword(t *testing.T) {
	client, _ := setupTestServer(t)
	ctx, cancel := context.WithTimeout(context.Background(), time.Second*2)
	defer cancel()

	regUsername := "wrongpasstestuser"
	regPassword := "correctpassword123"
	_, err := client.Register(ctx, &pb.RegisterRequest{
		Username: regUsername,
		Password: regPassword,
	})
	if err != nil {
		st, ok := status.FromError(err)
		if !ok || st.Code() != codes.AlreadyExists {
			t.Fatalf(
				"Login_IncorrectPassword: Ошибка при предварительной регистрации: %v",
				err,
			)
		}
	}

	_, err = client.Login(ctx, &pb.LoginRequest{
		Username: regUsername,
		Password: "incorrectpassword",
	})

	if err == nil {
		t.Fatal("Login()_IncorrectPassword: ожидалась ошибка, но ее не было")
	}

	st, ok := status.FromError(err)
	if !ok {
		t.Fatalf("Login()_IncorrectPassword: не удалось получить статус из ошибки: %v", err)
	}
	if st.Code() != codes.Unauthenticated {
		t.Errorf("Login()_IncorrectPassword: ожидался код ошибки Unauthenticated, получен %s", st.Code())
	}
	t.Logf("Login_IncorrectPassword: Получена ожидаемая ошибка: %v", err)
}

func TestAuthService_ValidateToken_Successful(t *testing.T) {
	client, _ := setupTestServer(t)
	ctx, cancel := context.WithTimeout(context.Background(), time.Second*2)
	defer cancel()

	regUsername := "validatetokenuser"
	regPassword := "validtokenpass123"
	regResp, err := client.Register(ctx, &pb.RegisterRequest{
		Username: regUsername,
		Password: regPassword,
	})
	if err != nil {
		st, ok := status.FromError(err)
		if !ok || st.Code() != codes.AlreadyExists {
			t.Fatalf("ValidateToken_Successful: Ошибка при предварительной регистрации: %v", err)
		}
		if st.Code() == codes.AlreadyExists {
			logResp, loginErr := client.Login(ctx, &pb.LoginRequest{Username: regUsername, Password: regPassword})
			if loginErr != nil {
				t.Fatalf("ValidateToken_Successful: Ошибка при логине для получения токена: %v", loginErr)
			}
			regResp = logResp
		}
	}
	if regResp == nil || regResp.Token == "" {
		t.Fatal("ValidateToken_Successful: Не удалось получить токен для теста")
	}

	valResp, err := client.ValidateToken(ctx, &pb.ValidateTokenRequest{Token: regResp.Token})
	if err != nil {
		t.Fatalf("ValidateToken()_Successful failed: %v", err)
	}

	if !valResp.Valid {
		t.Errorf("ValidateToken()_Successful: ожидалась валидность токена true, получено false.")
	}
	if valResp.Username != regUsername {
		t.Errorf("ValidateToken()_Successful: ожидался username '%s', получен '%s'", regUsername, valResp.Username)
	}
	t.Logf("ValidateToken_Successful: Valid: %t, Username: %s", valResp.Valid, valResp.Username)
}

func TestAuthService_ValidateToken_InvalidToken(t *testing.T) {
	client, _ := setupTestServer(t)
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	invalidToken := "this.is.not.a.valid.jwt.token"
	valResp, err := client.ValidateToken(ctx, &pb.ValidateTokenRequest{Token: invalidToken})

	if err != nil {
		t.Fatalf("ValidateToken()_InvalidToken unexpectedly failed: %v", err)
	}

	if valResp.Valid {
		t.Errorf("ValidateToken()_InvalidToken: ожидалась валидность токена false, получено true")
	}
	if valResp.Username != "" {
		t.Errorf("ValidateToken()_InvalidToken: ожидался пустой username, получен '%s'", valResp.Username)
	}
	t.Logf("ValidateToken_InvalidToken: Valid: %t", valResp.Valid)
}
