package main

import (
	"database/sql"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/google/uuid"
)

func SaveLog(db *sql.DB, payload LogPayload) error {
	namespaceStr := os.Getenv("UUID_NAMESPACE")
	namespace, err := uuid.Parse(namespaceStr)
	if err != nil {
		namespace = uuid.NameSpaceOID
	}

	uniqueName := fmt.Sprintf("%s-%s-%d", payload.ClientIP, payload.Route, time.Now().UnixNano())
	logID := uuid.NewSHA1(namespace, []byte(uniqueName))
	
	query := `
		INSERT INTO audit_logs (id, client_ip, professional_id, http_method, route, status_code, processing_time_ms, created_at)
		VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
	`
	_, err = db.Exec(query,
		logID.String(),
		payload.ClientIP,
		payload.ProfessionalID,
		payload.HTTPMethod,
		payload.Route,
		payload.StatusCode,
		payload.ProcessingTimeMS,
		payload.CreatedAt,
	)
	if err != nil {
		log.Printf("Database execution error: %v\n", err)
		return err
	}
	return nil
}