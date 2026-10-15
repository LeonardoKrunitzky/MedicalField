package main

import (
	"database/sql"
	"encoding/json"
	"log"
	"net/http"
	"github.com/google/uuid"
)

type LogPayload struct {
	ClientIP         string `json:"client_ip"`
	ProfessionalID   uuid.UUID    `json:"professional_id"`
	HTTPMethod       string `json:"http_method"`
	Route            string `json:"route"`
	StatusCode       int    `json:"status_code"`
	ProcessingTimeMS int    `json:"processing_time_ms"`
}

func LogHandler(db *sql.DB) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		var payload LogPayload
		if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
			log.Printf("Payload Decode Error: %v", err)
			http.Error(w, "Invalid JSON", http.StatusBadRequest)
			return
		}

		if err := SaveLog(db, payload); err != nil {
			http.Error(w, "Internal Server Error", http.StatusInternalServerError)
			return
		}

		log.Println("Log saved successfully")
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusCreated)
		w.Write([]byte(`{"message": "Created"}`))
	}
}