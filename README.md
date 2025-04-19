# 投票開票紀錄系統

這是一個用於記錄投票和開票過程的系統，可以設定候選人、投票人數，並記錄開票過程。

## 功能特點

- 設定候選人和投票人數
- 設定當選條件（總票數的百分比或過半）
- 開票過程中記錄每一票（加票或減票）
- 達到當選條件時自動提醒
- 儲存開票結果
- 匯出開票紀錄為Excel格式

## 技術棧

- **後端**：Flask
- **前端**：HTML, CSS, jQuery, Bootstrap
- **資料庫**：PostgreSQL
- **容器化**：Docker

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

1. **建立新投票**：
   - 設定投票標題
   - 設定總投票人數
   - 選擇當選條件（百分比或過半）
   - 新增候選人

2. **開票過程**：
   - 點擊 `+1` 為候選人增加一票
   - 點擊 `-1` 為候選人減少一票
   - 每次投票都需要確認
   - 達到當選條件時系統會提醒

3. **儲存結果**：
   - 點擊「儲存結果」將記錄當前開票狀態
   - 儲存後不可再進行投票操作

4. **匯出記錄**：
   - 點擊「匯出結果」將開票記錄匯出為Excel檔案
   - Excel檔案包含開票結果和詳細的投票記錄