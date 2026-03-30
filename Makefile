SITE     ?= dev.localhost
ADMIN_PW ?= admin
DB_PW    ?= admin123
IMAGE    := smart-management-system-dev

COMPOSE_CMD := docker compose \
	-f docker/compose.yaml \
	-f docker/compose.dev.yaml \
	--env-file docker/.env.dev

.PHONY: dev-build dev-up dev-down create-site install-apps import-translations logs restart-backend

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

## 第四步：安裝模組（依序安裝 erpnext → hrms → healthcare）並匯入繁體中文翻譯
install-apps:
	$(COMPOSE_CMD) exec backend bench --site $(SITE) install-app erpnext
	$(COMPOSE_CMD) exec backend bench --site $(SITE) install-app hrms
	$(COMPOSE_CMD) exec backend bench --site $(SITE) install-app healthcare
	$(MAKE) import-translations

## 匯入 zh-TW 繁體中文翻譯（可單獨執行以更新翻譯）
## - import-translations：更新後端 CSV 翻譯快取
## - compile-po-to-mo：編譯前端 .po → .mo（重建 image 時會自動執行）
import-translations:
	$(COMPOSE_CMD) exec backend bench --site $(SITE) import-translations zh-TW /home/frappe/frappe-bench/apps/frappe/frappe/locale/zh_TW.po
	$(COMPOSE_CMD) exec backend bench --site $(SITE) import-translations zh-TW /home/frappe/frappe-bench/apps/erpnext/erpnext/locale/zh_TW.po
	$(COMPOSE_CMD) exec backend bench --site $(SITE) import-translations zh-TW /home/frappe/frappe-bench/apps/hrms/hrms/locale/zh_TW.po
	$(COMPOSE_CMD) exec backend bench --site $(SITE) import-translations zh-TW /home/frappe/frappe-bench/apps/healthcare/healthcare/locale/zh_TW.po
	$(COMPOSE_CMD) exec backend bench compile-po-to-mo --app healthcare --locale zh_TW

## 修改 Python 程式碼後重啟 backend（讓變更生效）
restart-backend:
	$(COMPOSE_CMD) restart backend queue-short queue-long scheduler

## 查看即時 log
logs:
	$(COMPOSE_CMD) logs -f

## 執行資料庫 migration（修改 DocType schema 後執行）
migrate:
	$(COMPOSE_CMD) exec backend bench --site $(SITE) migrate
