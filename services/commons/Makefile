.PHONY: venv test run migrate migrate-down lint clean

SERVICE_NAME := content_service
SERVICE_PORT := 8000
VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

venv: ## Создать виртуальное окружение
	python3.12 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install pytest pytest-cov httpx

test: ## Запустить тесты
	$(PYTHON) -m pytest tests/ -v

run: ## Запустить сервис локально (не в Docker)
	$(PYTHON) -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

migrate: ## Применить миграции Alembic
	$(PYTHON) -m alembic upgrade head

migrate-down: ## Откатить последнюю миграцию
	$(PYTHON) -m alembic downgrade -1

lint: ## Проверить код (flake8, mypy)
	$(PYTHON) -m flake8 app/
	$(PYTHON) -m mypy app/

clean: ## Очистить временные файлы
	rm -rf __pycache__ .pytest_cache htmlcov .coverage
	rm -rf $(VENV)

# ------------------------------------------------------------
# DOCKER-КОМАНДЫ
# ------------------------------------------------------------
.PHONY: docker-build docker-run docker-stop docker-restart docker-clean docker-logs docker-test docker-build-test

DOCKER_IMAGE := AlGoBotat/$(SERVICE_NAME):latest
DOCKER_CONTAINER := AlGoBotat-$(SERVICE_NAME)

docker-build: ## Собрать Docker-образ
	docker build -t $(DOCKER_IMAGE) .
	@echo "✅ Образ $(DOCKER_IMAGE) собран"

docker-run: ## Запустить контейнер (локально, с переменными из .env)
	docker run -d \
		--name $(DOCKER_CONTAINER) \
		-p $(SERVICE_PORT):8000 \
		--env-file .env \
		$(DOCKER_IMAGE)
	@echo "✅ Контейнер $(DOCKER_CONTAINER) запущен на порту $(SERVICE_PORT)"

docker-stop: ## Остановить контейнер
	@docker stop $(DOCKER_CONTAINER) 2>/dev/null || true
	@docker rm $(DOCKER_CONTAINER) 2>/dev/null || true
	@echo "✅ Контейнер $(DOCKER_CONTAINER) остановлен и удалён"

docker-restart: docker-stop docker-run ## Перезапустить контейнер

docker-clean: docker-stop ## Полностью удалить образ
	-docker rmi $(DOCKER_IMAGE) 2>/dev/null || true
	@echo "✅ Образ $(DOCKER_IMAGE) удалён"

docker-logs: ## Показать логи контейнера
	docker logs -f $(DOCKER_CONTAINER)

docker-test: ## Запустить тесты ВНУТРИ контейнера (после сборки)
	@echo "🧪 Запуск тестов внутри контейнера..."
	docker run --rm \
		--name $(DOCKER_CONTAINER)-test \
		--env-file .env.test \
		$(DOCKER_IMAGE) \
		pytest tests/ -v

docker-build-test: docker-build docker-test ## Собрать образ и запустить тесты внутри него
