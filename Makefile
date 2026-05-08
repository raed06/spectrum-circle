.PHONY: help setup install db-start db-stop run run-all test lint clean

# Default target
help:
	@echo ""
	@echo "  SpectrumCircle - Available Commands"
	@echo "  ===================================="
	@echo ""
	@echo "  Setup"
	@echo "    make setup       Full setup for new contributors (venv + deps + .env)"
	@echo "    make install     Install Python dependencies only"
	@echo ""
	@echo "  Database"
	@echo "    make db-start    Start PostgreSQL via Docker"
	@echo "    make db-stop     Stop PostgreSQL container"
	@echo ""
	@echo "  Run"
	@echo "    make run         Start the main FastAPI server"
	@echo "    make run-all     Start FastAPI + Crisis MCP server"
	@echo ""
	@echo "  Quality"
	@echo "    make test        Run the test suite"
	@echo "    make lint        Check code for syntax errors"
	@echo ""
	@echo "  Cleanup"
	@echo "    make clean       Remove virtual environment and cache files"
	@echo ""

# ─── Setup ────────────────────────────────────────────────────────────────────

setup: install
	@echo "⚙️  Setting up environment..."
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "📄 .env file created from .env.example — fill in your API keys!"; \
	else \
		echo "📄 .env already exists, skipping."; \
	fi
	@echo ""
	@echo "✅ Setup complete! Next steps:"
	@echo "   1. Edit .env and add your API keys"
	@echo "   2. Run: make db-start"
	@echo "   3. Run: make run"
	@echo ""

install:
	@echo "📦 Creating virtual environment..."
	@python3 -m venv .venv
	@echo "📦 Installing dependencies..."
	@.venv/bin/pip install --upgrade pip -q
	@.venv/bin/pip install -r backend/requirements.txt
	@echo "✅ Dependencies installed."

# ─── Database ─────────────────────────────────────────────────────────────────

db-start:
	@echo "🐳 Starting PostgreSQL..."
	@cd docker/postgres && docker-compose up -d
	@echo "✅ PostgreSQL is running on port 5432."

db-stop:
	@echo "🐳 Stopping PostgreSQL..."
	@cd docker/postgres && docker-compose down
	@echo "✅ PostgreSQL stopped."

# ─── Run ──────────────────────────────────────────────────────────────────────

run:
	@echo "🚀 Starting SpectrumCircle API..."
	@.venv/bin/uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000

run-all:
	@echo "🚀 Starting FastAPI + Crisis MCP server..."
	@trap 'kill 0' SIGINT; \
	.venv/bin/uvicorn backend.api.main:app --reload --port 8000 & \
	.venv/bin/python mcp/crisis_mcp_server.py & \
	wait
	@echo "✅ All servers running. Press Ctrl+C to stop all."

# ─── Quality ──────────────────────────────────────────────────────────────────

test:
	@echo "🧪 Running tests..."
	@.venv/bin/pytest tests/ -v --tb=short

lint:
	@echo "🔍 Checking for syntax errors..."
	@.venv/bin/pip install pyflakes -q
	@.venv/bin/python -m pyflakes backend/ mcp/
	@echo "✅ No syntax errors found."

# ─── Cleanup ──────────────────────────────────────────────────────────────────

clean:
	@echo "🧹 Cleaning up..."
	@rm -rf .venv
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Cleaned."
