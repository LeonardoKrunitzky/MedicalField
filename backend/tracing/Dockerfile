FROM golang:1.25-alpine AS builder
WORKDIR /app

COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download

COPY . .
RUN --mount=type=cache,target=/root/.cache/go-build \
    --mount=type=cache,target=/go/pkg/mod \
    go build -o tracings-service .

FROM alpine:latest
WORKDIR /app

COPY --from=builder /app/tracings-service .
COPY --from=builder /app/.env .

EXPOSE 8081
CMD ["./tracings-service"]
