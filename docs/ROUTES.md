# 路由設計 (ROUTES) - 漫畫推薦系統

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁 (排行榜) | GET | `/` | `index.html` | 顯示各類別 Top 10 與熱門推薦 |
| 搜尋結果 | GET | `/search` | `search.html` | 根據書名關鍵字顯示過濾結果 |
| 分類清單 | GET | `/categories` | `categories.html` | 顯示所有分類選項 |
| 分類篩選結果 | GET | `/category` | `manga_list.html` | 根據語言/內容/性別篩選作品 |
| 漫畫詳情 | GET | `/manga/<id>` | `manga_detail.html` | 顯示簡介與章節列表 |
| 閱讀器 | GET | `/manga/<id>/read/<num>` | `reader.html` | 核心閱讀介面 (含模式切換) |
| 發表留言 | POST | `/manga/<id>/comment` | — | 接收留言表單，存入 DB 後重導向 |

---

## 2. 每個路由的詳細說明

### 2.1 首頁 (`/`)
- **處理邏輯**：呼叫 `Ranking.get_top_n()` 獲取不同類別的排行榜。
- **輸出**：渲染 `index.html`。

### 2.2 搜尋 (`/search`)
- **輸入**：URL 參數 `q` (關鍵字)。
- **處理邏輯**：呼叫 `Manga.search(q)`。
- **輸出**：渲染 `search.html`。

### 2.3 分類篩選 (`/category`)
- **輸入**：URL 參數 `lang`, `type`, `gender`。
- **處理邏輯**：呼叫 `Manga.filter(lang, type, gender)`。
- **輸出**：渲染 `manga_list.html`。

### 2.4 漫畫詳情 (`/manga/<id>`)
- **處理邏輯**：
    - 呼叫 `Manga.get_by_id(id)` 獲取漫畫資訊。
    - 呼叫 `Chapter.get_by_manga(id)` 獲取章節清單。
- **輸出**：渲染 `manga_detail.html`。若不存在則返回 404。

### 2.5 閱讀器 (`/manga/<id>/read/<num>`)
- **處理邏輯**：
    - 呼叫 `Chapter.get_by_manga(id)` 並找到第 `num` 章。
    - 呼叫 `Comment.get_by_chapter(chapter_id)` 獲取該章留言。
- **輸出**：渲染 `reader.html`。

### 2.6 發表留言 (`/manga/<id>/comment`)
- **輸入**：表單欄位 `user_name`, `content`, `chapter_id`。
- **處理邏輯**：呼叫 `Comment.create()`。
- **輸出**：重導向回 `manga_detail` 或 `reader` 頁面。

---

## 3. Jinja2 模板清單

| 檔案名稱 | 說明 | 繼承自 |
| :--- | :--- | :--- |
| `layout.html` | 基礎佈局 (導覽列、頁尾、搜尋欄) | — |
| `index.html` | 首頁與排行榜 | `layout.html` |
| `search.html` | 搜尋結果頁 | `layout.html` |
| `categories.html` | 分類索引頁 | `layout.html` |
| `manga_list.html` | 分類篩選後的漫畫列表 | `layout.html` |
| `manga_detail.html` | 漫畫詳細資訊與章節清單 | `layout.html` |
| `reader.html` | 漫畫閱讀介面 (全屏/無導覽列) | — (或獨立 CSS) |

---

## 4. 路由骨架程式碼

規劃在以下檔案中：
- `app/routes/main.py`: 首頁、搜尋、分類。
- `app/routes/manga.py`: 詳情、留言、閱讀器。
