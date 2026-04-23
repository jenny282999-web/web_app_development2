# 流程圖設計 (FLOWCHART) - 漫畫推薦系統

## 1. 使用者流程圖 (User Flow)

描述使用者從進入首頁到完成閱讀與留言的操作路徑。

```mermaid
flowchart TD
    Start([使用者進入網站]) --> Home[首頁 - 排行榜與推薦]
    
    Home --> Search[書名搜尋]
    Search --> Results[搜尋結果列表]
    Results --> Detail[漫畫詳細資訊頁]
    
    Home --> Category[分類篩選]
    Category --> MangaList[分類漫畫列表]
    MangaList --> Detail
    
    Detail --> Reader[進入閱讀器]
    Reader --> Mode{切換閱讀模式?}
    Mode -->|下拉式| Scroll[卷軸滾動閱讀]
    Mode -->|翻頁式| Flip[點擊/滑動翻頁]
    
    Scroll --> End[章節末尾]
    Flip --> End
    
    End --> Comment[查看與發表留言]
    Comment --> Finish([完成閱讀])
```

---

## 2. 系統序列圖 (Sequence Diagram)

以「發表留言」為例，描述資料在各元件之間的傳遞流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant DB as SQLite 資料庫

    User->>Browser: 在留言區輸入內容並點擊提交
    Browser->>Flask: POST /manga/<id>/comment (JSON 或 Form Data)
    
    rect rgb(240, 240, 240)
        Note over Flask, DB: 資料處理階段
        Flask->>DB: INSERT INTO comments (user_id, manga_id, content)
        DB-->>Flask: 回傳執行成功
    end
    
    Flask-->>Browser: 302 重導向 (或返回成功訊息)
    Browser->>User: 重新整理頁面，顯示新留言
```

---

## 3. 功能清單對照表

| 功能名稱 | URL 路徑 | HTTP 方法 | 說明 |
| :--- | :--- | :--- | :--- |
| 首頁 (排行榜) | `/` | GET | 顯示各類別 Top 10 |
| 搜尋結果 | `/search` | GET | 根據關鍵字過濾漫畫 |
| 分類篩選 | `/category/<type>` | GET | 顯示特定分類的漫畫列表 |
| 漫畫詳情 | `/manga/<id>` | GET | 顯示簡介與章節列表 |
| 閱讀器 | `/manga/<id>/read` | GET | 核心閱讀介面 (含模式切換) |
| 發表留言 | `/manga/<id>/comment` | POST | 儲存使用者心得 |

---

## 說明
- **使用者流程圖**：確保了使用者可以透過多種途徑（搜尋或分類）抵達目標內容，並能順利進入核心的閱讀與互動環節。
- **序列圖**：展示了 Flask 作為中介，如何處理來自前端的互動並確保數據持久化到 SQLite。
- **對照表**：為後續的路由設計（API Design）提供了明確的藍圖。
