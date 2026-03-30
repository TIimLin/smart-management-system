# 智慧化管理系統

基於 [Frappe Healthcare (Marley)](https://github.com/earthians/marley) 的智慧化管理系統，整合 ERPNext、HRMS 與 Healthcare 模組，透過 Docker 一鍵部署。

## 版本資訊

| 套件 | 版本 |
|------|------|
| Frappe Framework | version-16 |
| ERPNext | version-16 |
| Frappe HRMS | version-16 |
| Healthcare (Marley) | version-16 |
| Python | 3.14.x |
| Node.js | 24.x |

## 專案架構

```
smart-management-system/
├── healthcare/              # Frappe App 模組（主要開發目錄）
├── patient_portal/          # 病患入口模組
├── apps.json                # 額外安裝的 Frappe apps 清單（不含 frappe 本身）
├── Dockerfile               # 自訂 Docker image 建置
├── Makefile                 # 常用開發指令
├── pyproject.toml           # Python 套件設定
├── docker/
│   ├── compose.yaml         # Docker Compose 主設定
│   ├── compose.dev.yaml     # 本機開發 override（掛載本地程式碼）
│   ├── .env.example         # 生產環境變數範本
│   ├── resources/           # Nginx 設定資源
│   └── overrides/           # HTTPS 等環境 override 設定
└── .github/workflows/
    └── build-push.yml       # CI/CD：自動建置並推送映像至 ghcr.io
```

---

## 本機開發環境（推薦）

本機開發使用 `compose.dev.yaml`，**本地 `healthcare/` 程式碼直接掛載進 container**，修改後不需重新 build image。

### 前置需求

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- WSL2（Windows 用戶）或 Linux / macOS
- Make（Windows 用戶可在 WSL 執行以下所有指令）

### 首次安裝

**Step 1：建置 Docker image**（需要下載 Frappe / ERPNext / HRMS，約 20~40 分鐘）

```bash
make dev-build
```

**Step 2：啟動所有服務**

```bash
make dev-up
```

**Step 3：建立 Frappe site**

```bash
make create-site
```

**Step 4：安裝模組**（依序安裝 erpnext → hrms → healthcare）

```bash
# 安裝 ERPNext
docker compose -f docker/compose.yaml -f docker/compose.dev.yaml --env-file docker/.env.dev \
  exec backend bench --site dev.localhost install-app erpnext

# 安裝 HRMS
docker compose -f docker/compose.yaml -f docker/compose.dev.yaml --env-file docker/.env.dev \
  exec backend bench --site dev.localhost install-app hrms

# 安裝 Healthcare
docker compose -f docker/compose.yaml -f docker/compose.dev.yaml --env-file docker/.env.dev \
  exec backend bench --site dev.localhost install-app healthcare
```

**Step 5：開啟瀏覽器**

```
http://localhost:8080
帳號：Administrator
密碼：admin
```

### 日常開發指令

| 指令 | 說明 |
|------|------|
| `make dev-up` | 啟動服務 |
| `make dev-down` | 停止服務 |
| `make restart-backend` | 修改 Python 程式碼後重載 |
| `make migrate` | 修改 DocType schema 後執行 migration |
| `make logs` | 查看即時 log |

> **何時需要重新 `make dev-build`？**
> 只有修改 `Dockerfile` 或 `apps.json`（新增/移除第三方 app）時才需要。
> 日常修改 `healthcare/` Python 程式碼只需 `make restart-backend`。

---

## CI/CD 工作流程（生產部署）

```
修改 healthcare/ 程式碼
    ↓
git push origin main
    ↓
GitHub Actions 自動建置 Docker image
    ↓
ghcr.io/tiimlin/smart-management-system:latest 更新
    ↓
伺服器執行 docker compose pull && docker compose up -d
```

### 生產環境快速部署

**Step 1：複製設定檔**

```bash
cd docker/
cp .env.example .env
# 編輯 .env，至少設定 DB_PASSWORD
```

**Step 2：啟動服務**

```bash
docker compose up -d
```

**Step 3：建立站台並安裝模組**

```bash
docker compose exec backend bench new-site mysite.local \
  --mariadb-root-password <DB_PASSWORD> \
  --admin-password <ADMIN_PASSWORD> \
  --mariadb-user-host-login-scope='%'

docker compose exec backend bench --site mysite.local install-app erpnext
docker compose exec backend bench --site mysite.local install-app hrms
docker compose exec backend bench --site mysite.local install-app healthcare
```

**Step 4：設定 site header**

在 `docker/.env` 設定：
```
FRAPPE_SITE_NAME_HEADER=mysite.local
```

重啟 frontend：
```bash
docker compose restart frontend
```

### 更新部署

```bash
docker compose pull
docker compose up -d --force-recreate
# 若有 schema 異動
docker compose exec backend bench --site all migrate
```

---

## Windows 注意事項

在 Windows 環境 clone 專案時，請確認 git 換行符號設定正確，否則所有檔案會顯示為已修改：

```powershell
git config --global core.autocrlf true
```

---

## License

MIT
