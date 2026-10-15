package main

import (
	"context"
	"database/sql"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/danielgtaylor/huma/v2"
	"github.com/danielgtaylor/huma/v2/adapters/humago"
	"github.com/joho/godotenv"
	_ "github.com/lib/pq"
)

type GreetingOutput struct {
	Body struct {
		Message string `json:"message" example:"Hello, Go!" doc:"Greeting message"`
	}
}

func getEnv(key, fallback string) string {
	if val := os.Getenv(key); val != "" {
		return val
	}
	return fallback
}

func initDB() *sql.DB {
	host := getEnv("DB_HOST", "127.0.0.1")
	port := getEnv("DB_PORT", "5432")
	user := getEnv("DB_USER", "postgres")
	password := getEnv("DB_PASSWORD", "postgres")
	dbname := getEnv("DB_NAME", "medicalfield")

	connStr := fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=disable",
		host, port, user, password, dbname)

	db, err := sql.Open("postgres", connStr)
	if err != nil || db.Ping() != nil {
		log.Fatalf("Failed to connect to database: %v", err)
	}

	log.Println("Database connection established!")
	return db
}

func GetGreeting(ctx context.Context, input *struct{}) (*GreetingOutput, error) {
	resp := &GreetingOutput{}
	resp.Body.Message = "Hello, Go!"
	return resp, nil
}

func main() {
	godotenv.Load()
	db := initDB()
	defer db.Close()

	mux := http.NewServeMux()
	api := humago.New(mux, huma.DefaultConfig("Tracing Service API", "1.0.0"))

	huma.Post(api, "/post_tracing", LogHandler(db))

	port := getEnv("PORT", "8081")
	log.Printf("Go tracing service running on port %s (Docs at http://localhost:%s/docs)...", port, port)

	if err := http.ListenAndServe(":"+port, mux); err != nil {
		log.Fatalf("HTTP server failed: %v", err)
	}
}