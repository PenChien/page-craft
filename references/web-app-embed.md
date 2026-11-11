# 目標管理系統 套版參考

目標管理系統（React、antd、refine）專屬的細節。通則在 `SKILL.md`「套進既有網頁程式」。

- 外層留白：寬螢幕 24px、窄螢幕（≤575px）12px。所以封面用 `.momo{margin:-24px}` 貼齊左右邊。
- 預覽站：`http://192.0.2.10/preview/`。
- 建置：前端用 `VITE_API_BASE_URL=/preview/api/v1 npx vite build --base /preview/`，把 `dist` 的 `index.html` 與 `assets` 複製到預覽目錄。
- 少了 `VITE_API_BASE_URL` 會打到正式站後端。

來源：2026-10-24 目標管理系統「如何開專案」、Q&A、個人頁套版。
