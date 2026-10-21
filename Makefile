.PHONY: up down install-deps run-core run-tracing run-communication

# Variáveis de diretório
CORE_DIR = backend/core
COMMUNICATION_DIR = backend/communication
TRACING_DIR = backend/tracing
FRONTEND_DIR = frontend

# ==========================================
# DOCKER & DATABASES (Postgres e SQLite via compose)
# ==========================================
up:
	docker-compose up -d --build

down:
	docker-compose down

# ==========================================
# BACKEND CORE (PYTHON / UVICORN)
# ==========================================
run-core:
	cd $(CORE_DIR) && PYTHONPATH=src uv run uvicorn routes.server:app \
		--reload \
		--host 0.0.0.0 \
		--port 8080

# ==========================================
# TRACING (GO)
# ==========================================
run-tracing:
	cd $(TRACING_DIR) && go run .

# ==========================================
# COMMUNICATION (TS / NODE)
# ==========================================
run-communication:
	cd $(COMMUNICATION_DIR) && npm run dev

# ==========================================
# COMANDOS GLOBAIS
# ==========================================
install-deps:
	cd $(CORE_DIR) && uv sync
	cd $(TRACING_DIR) && go mod tidy && go test ./... && go build
	cd $(COMMUNICATION_DIR) && npm install
	cd $(FRONTEND_DIR) && npm install