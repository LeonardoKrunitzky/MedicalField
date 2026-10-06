.PHONY: project-up project-down core-install core tracing communication-install communication up

# Variáveis de diretório
CORE_DIR = backend/core
COMMUNICATION_DIR = backend/communication
TRACING_DIR = backend/tracing

# ==========================================
# DOCKER & DATABASES (Postgres e SQLite via compose)
# ==========================================
project-up:
	docker-compose up -d --build

project-down:
	docker-compose down

# ==========================================
# BACKEND CORE (PYTHON / UVICORN)
# ==========================================
core-install:
	cd $(CORE_DIR) && uv sync

core:
	cd $(CORE_DIR) && uv run uvicorn main:app --reload --port 8000

# ==========================================
# TRACING (GO)
# ==========================================
tracing:
	cd $(TRACING_DIR) && go run main.go

# ==========================================
# COMMUNICATION (TS / NODE)
# ==========================================
communication-install:
	cd $(COMMUNICATION_DIR) && npm install

communication:
	cd $(COMMUNICATION_DIR) && npm run dev

# ==========================================
# COMANDOS GLOBAIS
# ==========================================
# Para rodar isso, use: make -j 4 up
up: project-up core tracing communication