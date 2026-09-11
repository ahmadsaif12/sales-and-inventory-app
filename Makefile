.PHONY: help install migrate makemigrations createapp register superuser createuser run shell test collectstatic check lint format build up down down-volumes logs exec clean

PYTHON := python3
MANAGE := $(PYTHON) manage.py

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	$(PYTHON) -m pip install -r requirements.txt

migrate: ## Run database migrations
	$(MANAGE) migrate

makemigrations: ## Create new migrations
	$(MANAGE) makemigrations

createapp: ## Create a new Django app (usage: make createapp accounts)
	@$(MANAGE) startapp $(filter-out $@,$(MAKECMDGOALS))

register: ## Create and register app (usage: make register APP=accounts)
	@if [ -z "$(APP)" ]; then \
		echo "Usage: make register APP=accounts"; \
		exit 1; \
	fi
	$(PYTHON) register_app.py $(APP)

superuser: ## Create a Django superuser
	$(MANAGE) createsuperuser

createuser: ## Create a default admin user
	$(MANAGE) shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" 2>/dev/null || echo "User may already exist"

run: ## Run the development server
	$(MANAGE) runserver

shell: ## Open the Django shell
	$(MANAGE) shell

test: ## Run the test suite
	$(MANAGE) test

collectstatic: ## Collect static files
	$(MANAGE) collectstatic --noinput

check: ## Run Django system checks
	$(MANAGE) check

lint: ## Run linting
	flake8 .
	isort --check-only --diff .

format: ## Auto-format code
	black .
	isort .

build: ## Build Docker containers
	docker compose build

up: ## Start Docker containers
	docker compose up -d

down: ## Stop Docker containers
	docker compose down

down-volumes: ## Stop Docker containers and remove volumes
	docker compose down -v

logs: ## View Docker logs
	docker compose logs -f

exec: ## Open a shell in the web container
	docker compose exec web bash

clean: ## Remove Python cache files and staticfiles
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf staticfiles