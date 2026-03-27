SITE     ?= dev.localhost
ADMIN_PW ?= admin
DB_PW    ?= admin123
IMAGE    := smart-management-system-dev

COMPOSE_CMD := docker compose \
	-f docker/compose.yaml \
	-f docker/compose.dev.yaml \
	--env-file docker/.env.dev

.PHONY: dev-build dev-up dev-down create-site install-apps logs restart-backend

## 第一步：打包本地 Docker image（首次或有 Dockerfile/依賴異動時執行）
dev-build:
	docker build \
		--progress=plain \
		--build-arg APPS_JSON_BASE64=$(shell tr -d '\r' < apps.json | base64 -w 0) \
		-t $(IMAGE):latest \
		.

## 第二步：啟動所有服務
dev-up:
	$(COMPOSE_CMD) up -d

## 停止所有服務
dev-down:
	$(COMPOSE_CMD) down

## 第三步：建立 Frappe site（首次執行）
create-site:
	$(COMPOSE_CMD) exec backend \
		bench new-site $(SITE) \
		--mariadb-root-password $(DB_PW) \
		--admin-password $(ADMIN_PW) \
		--no-mariadb-socket

## 第四步：安裝 healthcare 與 hrms 模組
install-apps:
	$(COMPOSE_CMD) exec backend bench --site $(SITE) install-app healthcare
	$(COMPOSE_CMD) exec backend bench --site $(SITE) install-app hrms

## 修改 Python 程式碼後重啟 backend（讓變更生效）
restart-backend:
	$(COMPOSE_CMD) restart backend queue-short queue-long scheduler

## 查看即時 log
logs:
	$(COMPOSE_CMD) logs -f

## 執行資料庫 migration（修改 DocType schema 後執行）
migrate:
	$(COMPOSE_CMD) exec backend bench --site $(SITE) migrate
