.PHONY: help up down down-volumes build rebuild logs ps test test-integration clean status check-docker

# Цвета для вывода (опционально, для красоты)
GREEN := \033[0;32m
RED := \033[0;31m
NC := \033[0m # No Color

# Ищем Makefile-ы сервисов
SERVICES_DIR := services
SERVICES := $(shell find $(SERVICES_DIR) -maxdepth 1 -type d ! -path $(SERVICES_DIR) -exec basename {} \;)
# Проверяет, есть ли в Makefile сервиса указанная цель
define has_target
$(shell grep -q "^$(1):" $(SERVICES_DIR)/$(2)/Makefile 2>/dev/null && echo yes)
endef

# Сервисы с возможностью запуска тестов (есть цель test)
SERVICES_WITH_TEST := $(foreach service,$(SERVICES), \
	$(if $(call has_target,test,$(service)),$(service),))

help: ## Показать справку по всем командам
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

install-tools-linux: ## Установить Docker, Docker Compose V2 и Make на Linux
	@echo "🐧 Установка Docker, Docker Compose V2 и Make..."
	# Устанавливаем Make
	sudo apt update
	sudo apt install -y make
	# Устанавливаем Docker и Docker Compose V2 (официальный скрипт)
	curl -fsSL https://get.docker.com -o get-docker.sh
	sudo sh get-docker.sh
	# Добавляем пользователя в группу docker
	sudo usermod -aG docker $$USER
	# Удаляем установочный скрипт
	rm get-docker.sh
	@echo ""
	@echo "✅ Готово!"
	@echo "👉 Перезайдите в систему"

up: ## Запустить все сервисы (фоновый режим)
	@echo "$(GREEN)🚀 Запуск всех микросервисов...$(NC)"
	cd deploy && docker compose up -d
	@echo "$(GREEN)✅ Все сервисы запущены. Проверьте: docker compose ps$(NC)"

down: ## Остановить все сервисы
	@echo "$(RED)🛑 Остановка всех сервисов...$(NC)"
	cd deploy && docker compose down
	@echo "$(GREEN)✅ Все сервисы остановлены$(NC)"

down-volumes: ## Полностью остановить и удалить все данные (volumes)
	@echo "$(RED)⚠️  ВНИМАНИЕ: Это удалит все данные из баз данных!$(NC)"
	read -p "Вы уверены? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		cd deploy && docker compose down -v; \
		echo "$(GREEN)✅ Данные удалены$(NC)"; \
	else \
		echo "$(RED)❌ Операция отменена$(NC)"; \
	fi

build: ## Собрать Docker-образы для всех сервисов
	@echo "$(GREEN)🏗️  Сборка образов...$(NC)"
	cd deploy && docker compose build --parallel
	@echo "$(GREEN)✅ Образы собраны$(NC)"

rebuild: down build up ## Полная пересборка (остановить -> пересобрать -> запустить)

logs: ## Показать логи всех сервисов (Ctrl+C для выхода)
	cd deploy && docker compose logs -f

ps: ## Показать статус контейнеров
	cd deploy && docker compose ps

# ------------------------------------------------------------
# ТЕСТИРОВАНИЕ
# ------------------------------------------------------------

test: ## Запустить тесты во всех сервисах где есть make test, локально, без Docker
	@echo "$(GREEN)🧪 Запуск тестов во всех сервисах...$(NC)"
	@FAILED=0; \
	for service in $(SERVICES_WITH_TEST); do \
		echo "$(GREEN)--- Тестируем $$service ---$(NC)"; \
		cd $(SERVICES_DIR)/$$service && $(MAKE) test; \
		if [ $$? -ne 0 ]; then \
			echo "$(RED)❌ $$service: тесты провалены$(NC)"; \
			FAILED=1; \
		else \
			echo "$(GREEN)✅ $$service: тесты пройдены$(NC)"; \
		fi; \
		echo ""; \
	done; \
	if [ $$FAILED -eq 1 ]; then \
		echo "$(RED)❌ Некоторые тесты не прошли$(NC)"; \
		exit 1; \
	else \
		echo "$(GREEN)✅ Все тесты успешно пройдены!$(NC)"; \
	fi

test-integration: ## Запустить интеграционные тесты через pytest (требуют запущенных контейнеров)
	@echo "$(GREEN)🔗 Запуск интеграционных тестов...$(NC)"
	@for service in $(SERVICES_WITH_TEST); do \
		echo "$(GREEN)--- Интеграционные тесты для $$service ---$(NC)"; \
		cd deploy && docker compose exec -T $$service pytest tests/integration/ 2>/dev/null || \
		echo "$(YELLOW)⚠️  $$service: нет интеграционных тестов или сервис не запущен$(NC)"; \
	done

# ------------------------------------------------------------
# УТИЛИТЫ
# ------------------------------------------------------------

clean: ## Очистить кеш Python, временные файлы и Docker
	@echo "$(GREEN)🧹 Очистка...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	cd deploy && docker compose down -v --rmi local 2>/dev/null || true
	docker system prune -f
	@echo "$(GREEN)✅ Очистка завершена$(NC)"

status: ## Показать статус всех сервисов и их здоровье
	@cd deploy && docker compose ps
	@echo ""
	@echo "🌐 Доступные эндпоинты:"
	@echo "  - API: http://localhost"
	@echo "  - Auth Service health: http://localhost/health"
	@echo "  - Swagger UI: http://localhost/docs"

# Вспомогательная команда для проверки наличия Docker
check-docker:
	@command -v docker >/dev/null 2>&1 || { echo "$(RED)❌ Docker не установлен$(NC)" >&2; exit 1; }
	@command -v docker compose >/dev/null 2>&1 || { echo "$(RED)❌ Docker Compose не установлен$(NC)" >&2; exit 1; }