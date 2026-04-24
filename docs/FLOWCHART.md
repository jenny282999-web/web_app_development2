# 流程圖設計 (FLOWCHART) - 漫遊索引系統

## 1. 使用者流程圖 (User Flow)

描述讀者從進入網站到使用各項核心功能的的操作路徑。

```mermaid
flowchart TD
    Start([開啟漫遊索引系統]) --> Landing{是否已登入？}
    Landing -- 否 --> Login[登入 / 註冊頁]
    Login --> Home[首頁 - 推薦與概覽]
    Landing -- 是 --> Home

    Home --> SearchChoice{想看什麼？}
    
    %% 搜尋與推薦流程
    SearchChoice -->|AI 情感推薦| AIReq[輸入心情標籤]
    AIReq --> AIResult[顯示媒合漫畫清單]
    SearchChoice -->|畫風搜尋| ArtUpload[上傳漫畫截圖]
    ArtUpload --> ArtResult[顯示相似畫風作品]
    
    AIResult --> Detail[漫畫詳情頁]
    ArtResult --> Detail

    %% 書櫃管理流程
    SearchChoice -->|查看我的書櫃| Lib[書櫃列表]
    Lib --> EditProg[更新閱讀進度]
    EditProg --> Lib
    
    Detail --> AddLib[加入書櫃]
    AddLib --> Lib

    %% 社群與評論流程
    Detail --> Comm[查看評論與雷點標籤]
    Comm --> AddComm[發表評論並標註雷點]
    AddComm --> Detail
    
    Home --> Room[漫話室 - 熱門討論]
    Room --> Detail
```

---

## 2. 系統序列圖 (Sequence Diagram)

描述「將漫畫加入跨平台書櫃」的完整資料流轉過程。

```mermaid
sequenceDiagram
    actor Reader as 讀者
    participant Browser as 瀏覽器
    participant Route as Flask Route (/library/add)
    participant Model as Progress Model
    participant DB as SQLite DB

    Reader->>Browser: 點擊「加入書櫃」
    Browser->>Route: POST /library/add (comic_id, platform)
    Route->>Model: 檢查是否已存在
    Model->>DB: SELECT * FROM progress WHERE user_id=? AND comic_id=?
    DB-->>Model: 回傳結果
    
    alt 尚未加入
        Route->>Model: 建立新進度紀錄
        Model->>DB: INSERT INTO progress (user_id, comic_id, platform, status)
        DB-->>Model: 儲存成功
        Model-->>Route: 回傳 Success
        Route-->>Browser: 重導向至 /library (書櫃頁)
        Browser-->>Reader: 顯示「已成功加入書櫃」
    else 已在書櫃中
        Route-->>Browser: 提示「此作品已在書櫃中」
        Browser-->>Reader: 顯示錯誤訊息
    end
```

---

## 3. 功能清單對照表

| 功能模組 | URL 路徑 | HTTP 方法 | 說明 |
| :--- | :--- | :--- | :--- |
| **首頁** | `/` | GET | 顯示推薦作品與系統公告 |
| **登入/註冊** | `/auth/login` | GET, POST | 用戶身份驗證 |
| **情感搜尋** | `/search/ai` | GET, POST | 處理心情標籤並回傳推薦清單 |
| **畫風搜尋** | `/search/art` | POST | 接收圖片上傳並進行視覺分析 |
| **書櫃首頁** | `/library` | GET | 列出用戶收藏的所有漫畫 |
| **加入書櫃** | `/library/add` | POST | 將作品加入個人書櫃 |
| **更新進度** | `/library/update`| POST | 記錄讀者在不同平台的最新進度 |
| **漫畫詳情** | `/comic/<int:id>`| GET | 顯示作品介紹、標籤與評論 |
| **發表評論** | `/comic/<int:id>/comment`| POST | 提交評論內容與雷點標籤 |

---

## 4. 接下來的步驟
- 根據流程圖與功能對照表，開始 **Phase 4: 資料庫設計 (Database Design)**。
- 定義 User, Comic, Progress, Comment 等資料表的欄位關聯。
