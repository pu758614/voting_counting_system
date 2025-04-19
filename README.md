# 投票開票紀錄系統

這是一個用於記錄投票和開票過程的系統，可以設定候選人、投票人數，並記錄開票過程。

## 功能特點

- 設定候選人和投票人數
- 設定當選條件（總票數的百分比或過半）
- 開票過程中記錄每一票（加票或減票）
- 達到當選條件時自動提醒
- 儲存開票結果
- 匯出開票紀錄為Excel格式
- 帳號登入認證機制

## 技術棧

- **後端**：Flask
- **前端**：HTML, CSS, jQuery, Bootstrap
- **資料庫**：PostgreSQL / SQLite
- **容器化**：Docker
- **部署**：Fly.io

## 安裝與運行

### 使用 Docker Compose 運行

1. 確保已安裝 Docker 和 Docker Compose

2. 克隆本倉庫：
   ```bash
   git clone [repository-url]
   cd [repository-directory]
   ```

3. 啟動服務：
   ```bash
   docker-compose up --build
   ```

   首次運行時，可能需要等待一段時間讓數據庫初始化完成。如果看到網頁服務連接錯誤，請嘗試重新啟動容器：
   ```bash
   docker-compose down
   docker-compose up
   ```

4. 在瀏覽器中訪問：
   ```
   http://localhost:5000
   ```

5. 使用預設帳號密碼登入：
   ```
   帳號: admin
   密碼: 1234567891
   ```

### 常見問題排解

如果遇到數據庫連接問題，可以嘗試：

1. 刪除舊的 volume 並重新創建：
   ```bash
   docker-compose down -v
   docker-compose up --build
   ```

2. 確認 PostgreSQL 容器正常運行：
   ```bash
   docker-compose ps
   ```

## 系統使用方法

1. **登入系統**：
   - 使用提供的帳號密碼登入系統（預設為 admin/1234567891）

2. **建立新投票**：
   - 設定投票標題
   - 設定總投票人數
   - 選擇當選條件（百分比或過半）
   - 新增候選人

3. **開票過程**：
   - 點擊 `+1` 為候選人增加一票
   - 點擊 `-1` 為候選人減少一票
   - 每次投票都需要確認
   - 達到當選條件時系統會提醒

4. **儲存結果**：
   - 點擊「儲存結果」將記錄當前開票狀態
   - 儲存後不可再進行投票操作

5. **匯出記錄**：
   - 點擊「匯出結果」將開票記錄匯出為Excel檔案
   - Excel檔案包含開票結果和詳細的投票記錄

## 部署到 Fly.io

本系統可以輕鬆部署到 Fly.io 雲平台上。以下是部署步驟：

### 準備工作

1. 註冊 [Fly.io](https://fly.io) 帳號
2. 安裝 Fly CLI
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex

   # MacOS/Linux
   curl -L https://fly.io/install.sh | sh
   ```
3. 登入 Fly.io
   ```bash
   fly auth login
   ```

### 部署步驟

1. 確保專案中有下列檔案：
   - `fly.toml` (Fly.io 配置檔)
   - `Dockerfile` (容器配置檔)
   - `requirements.txt` (Python 依賴)
   - `wsgi.py` (WSGI 入口點)

2. 創建 Fly.io 應用程式
   ```bash
   fly apps create voting-counting-system
   ```

3. 為 SQLite 數據庫創建持久化卷
   ```bash
   fly volumes create sqlite_data --size 1 --app voting-counting-system --region sin
   ```

4. 部署應用程式
   ```bash
   fly deploy
   ```

5. 查看部署日誌
   ```bash
   fly logs
   ```

6. 開啟應用程式
   ```bash
   fly open
   ```

現在你的應用程式已經成功部署到 Fly.io，可以通過以下網址訪問：
```
https://voting-counting-system.fly.dev
```

### 更新應用程式

當你需要更新應用程式時，只需修改代碼後重新部署：
```bash
fly deploy
```

### 常見問題

1. **數據持久化**：應用程式使用 Fly.io 的 volumes 功能來保存 SQLite 數據庫，確保數據不會在部署之間丟失。

2. **自定義域名**：如需使用自定義域名，請參考 [Fly.io 文檔](https://fly.io/docs/app-guides/custom-domains-with-fly/)。

3. **伸縮應用**：可以使用 `fly scale` 命令調整應用程式的資源配置。