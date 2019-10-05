include .env

.DEFAULT_GOAL=help

APP = docker-compose exec app
FLASK = $(APP) flask

CD_NGINX = cd docker/nginx
CD_REDIS = cd docker/redis


# Targets
help:
	@echo "Targets:"
	@echo "  Container:"
	@echo "    => build"
	@echo "    => up"
	@echo "    => build_up"
	@echo "    => down"
	@echo "    => logs"
	@echo "    => clean"
	@echo ""
	@echo "  Bundle Command:"
	@echo "    => bundle_install"
	@echo "    => bundle_remove"
	@echo ""
	@echo "  Rails Command:"
	@echo "    => rails_console"
	@echo "    => rails_routes"
	@echo "    => rspec"
	@echo "    => rubocop"
	@echo ""
	@echo "  DB Command:"
	@echo "    => db_create"
	@echo "    => db_migrate"
	@echo "    => db_seed"


# コンテナ操作コマンド
.PHONY: bundle up build_up down logs clean test
build:
	$(DC) build
up:
	$(DC) up -d
build_up:
	$(DC) up -d --build
restart:
	$(DC) restart
force_restart:
	@make down
	@make build_up
down:
	$(DC) down
logs:
	$(DC) logs -f
clean:
	@docker image prune
	@docker volume prune
test:
	$(APP) pytest

# DB関連コマンド
.PHONY: db_migrate db_upgrade
db_migrate:
	@$(FLASK) db migrate
db_upgrade:
	@$(FLASK) db upgrade
db_downgrade:
	@$(FLASK) db downgrade
