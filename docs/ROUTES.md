# 路由設計 (ROUTES) - 漫遊索引系統

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁** | GET | `/` | `index.html` | 顯示熱門漫畫與情緒推薦入口 |
| **註冊頁面** | GET | `/auth/register` | `auth/register.html` | 顯示註冊表單 |
| **執行註冊** | POST | `/auth/register` | — | 建立用戶，重導向至登入 |
| **登入頁面** | GET | `/auth/login` | `auth/login.html` | 顯示登入表單 |
| **執行登入** | POST | `/auth/login` | — | 驗證身份，重導向至首頁 |
| **登出** | GET | `/auth/logout` | — | 清除 Session，重導向至首頁 |
| **情感推薦搜尋** | GET | `/search/ai` | `search/ai.html` | 顯示情緒標籤選擇介面 |
| **執行情感推薦** | POST | `/search/ai` | `search/results.html` | 根據標籤媒合作品並顯示結果 |
| **畫風搜尋頁面** | GET | `/search/art` | `search/art.html` | 顯示圖片上傳介面 |
| **執行畫風搜尋** | POST | `/search/art` | `search/results.html` | 分析圖片特徵並推薦相似畫風 |
| **我的書櫃** | GET | `/library` | `library/index.html` | 顯示使用者收藏的所有漫畫進度 |
| **加入書櫃** | POST | `/library/add` | — | 將作品加入收藏，重導向至書櫃 |
| **更新閱讀進度** | POST | `/library/update` | — | 修改章節或狀態，重導向至書櫃 |
| **移除收藏** | POST | `/library/delete` | — | 從書櫃中移除作品 |
| **漫畫詳情頁** | GET | `/comic/<int:id>` | `comic/detail.html` | 顯示作品細節、情緒標籤與評論 |
| **發表評論** | POST | `/comic/<int:id>/comment` | — | 提交評論與雷點標籤，重導向至詳情頁 |

---

## 2. 每個路由的詳細說明

### 2.1 搜尋模組 (Search)
- **情感推薦 (`POST /search/ai`)**
  - **輸入**：表單欄位 `emotion_tags` (多選)。
  - **處理**：呼叫 `ComicModel.get_by_tag()`。
  - **輸出**：渲染 `search/results.html` 顯示符合的作品。
  - **錯誤處理**：若未選取標籤，顯示警告訊息。

- **畫風搜尋 (`POST /search/art`)**
  - **輸入**：上傳檔案 `style_image`。
  - **處理**：儲存檔案至 `static/uploads/`，呼叫 `ai_logic.analyze_style()`。
  - **輸出**：渲染 `search/results.html`。

### 2.2 書櫃模組 (Library)
- **更新進度 (`POST /library/update`)**
  - **輸入**：`progress_id`, `current_chapter`, `status`, `platform`。
  - **處理**：呼叫 `ProgressModel.create_or_update()`。
  - **重導向**：`/library`。

---

## 3. Jinja2 模板清單

所有模板皆繼承自 `templates/base.html`。

- `base.html`: 包含導覽列 (首頁、搜尋、書櫃、登入/登出狀態)。
- `index.html`: 首頁 Hero section 與熱門展示。
- `auth/login.html`: 登入表單。
- `auth/register.html`: 註冊表單。
- `search/ai.html`: 情緒標籤選擇器 (Chip 樣式)。
- `search/art.html`: 圖片拖放上傳區。
- `search/results.html`: 漫畫卡片列表。
- `library/index.html`: 書櫃清單，含更新進度的彈出視窗 (Modal)。
- `comic/detail.html`: 詳細資訊、雷點標籤雲、評論列表。

---

## 4. 接下來的步驟
- 根據路由骨架，開始 **Phase 6: 程式碼實作 (Implementation)**。
- 優先建立 `app/routes/` 檔案並定義 `Blueprint`。
