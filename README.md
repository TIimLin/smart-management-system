# 智慧化管理系統

基於 [Frappe Healthcare (Marley)](https://github.com/earthians/marley) 的智慧化管理系統，整合 Docker 部署設定，讓你可以在原始碼層級開發並自動打包為 Docker image。

## 專案架構

```
smart-management-system/
├── healthcare/              # Frappe App 模組（主要開發目錄）
├── patient_portal/          # 病患入口模組
├── apps.json                # Frappe apps 安裝清單
├── Dockerfile               # 自訂 Docker image 建置
├── pyproject.toml           # Python 套件設定
├── docker/
│   ├── compose.yaml         # Docker Compose 主設定
│   ├── .env.example         # 環境變數範本
│   ├── resources/           # Nginx 設定資源
│   └── overrides/           # 環境 override 設定
└── .github/workflows/
    └── build-push.yml       # CI/CD：自動建置並推送映像
```

## 開發工作流程

```
修改 healthcare/ 程式碼
    ↓
git add . && git commit -m "feat: ..."
    ↓
git push origin main
    ↓
GitHub Actions 自動建置 Docker image
    ↓
ghcr.io/tiimlin/smart-management-system:latest 更新
    ↓
伺服器執行 docker compose pull && docker compose up -d
```

## 快速開始

### 1. 複製設定檔

```bash
cd docker/
cp .env.example .env
# 編輯 .env，至少設定 DB_PASSWORD
```

### 2. 啟動服務

```bash
cd docker/
docker compose up -d
```

### 3. 建立站台

```bash
docker compose exec backend bench new-site mysite.local \
  --mariadb-root-password <DB_ROOT_PASSWORD> \
  --admin-password <ADMIN_PASSWORD>

docker compose exec backend bench --site mysite.local install-app healthcare
```

### 4. 設定網站名稱（本機開發）

在 `docker/.env` 加入：
```
FRAPPE_SITE_NAME_HEADER=mysite.local
```

然後重啟 frontend：
```bash
docker compose restart frontend
```

瀏覽器開啟 http://localhost:8080

## 本機開發（不需 Docker）

若要在本機直接修改 `healthcare/` 並即時測試：

```bash
# 安裝至本機 Frappe bench
bench get-app https://github.com/TIimLin/smart-management-system
bench --site mysite install-app healthcare
```

## 手動建置 Docker Image

```bash
APPS_JSON_BASE64=$(base64 -w 0 apps.json)

docker build \
  --build-arg APPS_JSON_BASE64="${APPS_JSON_BASE64}" \
  --build-arg FRAPPE_BRANCH=version-16 \
  -t smart-management-system:local \
  .
```

## 更新部署

```bash
cd docker/
docker compose pull
docker compose up -d --force-recreate
# 若有 schema 異動
docker compose exec backend bench --site all migrate
```

## 版本資訊

- Frappe Framework: version-16
- Marley (Healthcare): version-16（基於 [earthians/marley](https://github.com/earthians/marley)）
- Node.js: 18.x
- Python: 3.11

## License

MIT
