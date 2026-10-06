package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/joho/godotenv"
	_ "github.com/lib/pq"
)

// Representa a carga de auditoria enviada pelo Core ou pelo cliente offline[cite: 1, 4]
type LogPayload struct {
	ClientIP         string `json:"client_ip"`
	ProfessionalID   int    `json:"professional_id"`
	HTTPMethod       string `json:"http_method"`
	Route            string `json:"route"`
	StatusCode       int    `json:"status_code"`
	ProcessingTimeMS int    `json:"processing_time_ms"`
}

var db *sql.DB

func getEnv(key, fallback string) string {
	if val := os.Getenv(key); val != "" {
		return val
	}
	return fallback
}

func initDB() {
	var err error
	host := getEnv("DB_HOST", "127.0.0.1")
	port := getEnv("DB_PORT", "5432")
	user := getEnv("DB_USER", "postgres")
	password := getEnv("DB_PASSWORD", "postgres")
	dbname := getEnv("DB_NAME", "medicalfield")

	connStr := fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=disable",
		host, port, user, password, dbname)

	db, err = sql.Open("postgres", connStr)
	if err != nil {
		log.Fatalf("Erro ao registrar driver do Postgres: %v", err)
	}

	if err = db.Ping(); err != nil {
		log.Fatalf("Erro ao conectar no PostgreSQL: %v", err)
	}

	log.Println("Conexão com PostgreSQL estabelecida com sucesso!")
}

func logHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Método não permitido", http.StatusMethodNotAllowed)
		return
	}

	var payload LogPayload
	if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
		http.Error(w, "JSON inválido: "+err.Error(), http.StatusBadRequest)
		return
	}

	// Insere na tabela audit_logs[cite: 2, 9]
	query := `
		INSERT INTO audit_logs (id, client_ip, professional_id, http_method, route, status_code, processing_time_ms)
		VALUES ($1, $2, $3, $4, $5, $6, $7)
	`
	_, err := db.Exec(query,
		getEnv("UUID_NAMESPACE", "0"),
		payload.ClientIP,
		getEnv("UUID_NAMESPACE", "0"),
		payload.HTTPMethod,
		payload.Route,
		payload.StatusCode,
		payload.ProcessingTimeMS,
	)
	if err != nil {
		log.Printf("Erro ao salvar log no banco: %v", err)
		http.Error(w, "Erro ao gravar log", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)
	w.Write([]byte(`{"message": "Log registrado com sucesso"}`))
}

func main() {
	// Carrega as credenciais a partir do arquivo .env local
	if err := godotenv.Load(); err != nil {
		log.Println("Aviso: arquivo .env não encontrado, utilizando variáveis do sistema.")
	}

	initDB()
	defer db.Close()

	port := getEnv("PORT", "8081")
	http.HandleFunc("/post_tracing", logHandler) // Rota POST /log exigida no roteiro[cite: 1, 5]

	log.Printf("Serviço de logs em Go rodando na porta %s...", port)
	if err := http.ListenAndServe(":"+port, nil); err != nil {
		log.Fatalf("Falha no servidor HTTP: %v", err)
	}
}