FROM golang:1.25-alpine AS builder
WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN go build -o tracings-service .

FROM alpine:latest
WORKDIR /app

COPY --from=builder /app/tracings-service .
COPY --from=builder /app/.env .

EXPOSE 8081
CMD ["./tracings-service"]
