.PHONY: db-up db-down core-install core login logs-install logs up down

# Variáveis de diretório
CORE_DIR = backend/core
LOGIN_DIR = backend/login
LOGS_DIR = backend/logs

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
	cd $(CORE_DIR) && python -m venv .venv
	cd $(CORE_DIR) && .venv/bin/pip install -r requirements.txt

core:
	cd $(CORE_DIR) && .venv/bin/uvicorn main:app --reload --port 8000

# ==========================================
# LOGIN (GO)
# ==========================================
login:
	cd $(LOGIN_DIR) && go run main.go

# ==========================================
# LOGS (TYPESCRIPT)
# ==========================================
logs-install:
	cd $(LOGS_DIR) && npm install

logs:
	cd $(LOGS_DIR) && npm run dev

# ==========================================
# COMANDOS GLOBAIS
# ==========================================
up: db-up core login logs