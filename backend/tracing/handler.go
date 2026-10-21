package main

import (
	"context"
	"database/sql"
	"log"
	"net/http"

	"github.com/danielgtaylor/huma/v2"
	"github.com/google/uuid"
)

type LogPayload struct {
	ClientIP         string    `json:"client_ip" example:"127.0.0.1" doc:"Client IP address"`
	ProfessionalID   uuid.UUID `json:"professional_id" example:"550e8400-e29b-41d4-a716-446655440000" doc:"Professional UUID"`
	HTTPMethod       string    `json:"http_method" example:"POST" doc:"HTTP Method"`
	Route            string    `json:"route" example:"/appointments" doc:"Request route"`
	StatusCode       int       `json:"status_code" example:"201" doc:"HTTP Status Code"`
	ProcessingTimeMS int       `json:"processing_time_ms" example:"45" doc:"Processing time in milliseconds"`
	CreatedAt        string     `json:"created_at" example:"1640995200" doc:"Timestamp in seconds"`
}

type LogInput struct {
	Body LogPayload
}

type LogOutput struct {
	Status int
	Body   struct {
		Message string `json:"message" example:"Created"`
	}
}

func LogHandler(db *sql.DB) func(ctx context.Context, input *LogInput) (*LogOutput, error) {
	return func(ctx context.Context, input *LogInput) (*LogOutput, error) {
		if err := SaveLog(db, input.Body); err != nil {
			log.Printf("Database Error: %v", err)
			return nil, huma.Error500InternalServerError("Internal Server Error", err)
		}

		log.Println("Log saved successfully")
		resp := &LogOutput{}
		resp.Status = http.StatusCreated
		resp.Body.Message = "Created"
		return resp, nil
	}
}