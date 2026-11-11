# 更新紀錄

版號寫在 `VERSION`。日期是 commit 日期。

## 1.13.0（2026-11-11）

- `live-panel-demo.html` 加「上游範例」：上游 live-panel-skill 的 12 個範例各一頁（`up-*.html`），簡體轉為繁體（臺灣用語），含 excalidraw 手繪、sketchboard 說明板、loop、ring、funnel、框線面板。
- 新增 `examples/live-panel/build_upstream.py`：從 `live-panel/examples/*/config.json` 重建上游範例頁，先用 OpenCC 轉繁體，手繪字型依頁面用字裁切後內嵌。

## 1.12.0（2026-11-11）

- 新增 `examples/drawio-arch/svg2drawio.py`：把報告頁的線路圖轉回可編輯的 drawio。
- 新增範例 `examples/drawio-arch/demo-arch.drawio`。
- `references/drawio.md` 加「反向：線路圖轉回 drawio」一節。
- 新增本檔。

## 1.11.0（2026-11-11）

- 新增 drawio 轉檔步驟 `references/drawio.md`。
- 新增 `examples/drawio-arch/`：`drawio_tool.py`（原圖畫成 PNG、列出框與線）、`build_arch.py`（畫圖函式與範例頁）。

## 1.10.0（2026-10-25）

- MR !1 review 修正：STE 檢查路徑、自檢例外、目標管理系統 細節移到 `references/web-app-embed.md`。
- 示範頁：Atlas 導覽列、淡色立體版、Harbor 淺色範例區塊、Harbor 章節導覽列。

## 1.9.1（2026-10-24）

- 撤回 SeeCode。

## 1.9.0（2026-10-24）

- 內建 SeeCode，Harbor 範例加送簽收序列圖（已在 1.9.1 撤回）。

## 1.8.0（2026-10-24）

- live-panel 加 16:9 監控牆風格。

## 1.6.0（2026-10-24）

- live-panel 展示頁：loop、ring、funnel、終端機面板。

## 1.5.0（2026-10-24）

- 內建 live-panel。Paper 示範改用 loop 動態圖。

## 1.4.0（2026-10-24）

- jira 使用說明三版示範：Paper、Harbor、Atlas。

## 1.3.0（2026-10-24）

- 新增風格 C：Atlas 計畫版。架構圖改為四選一。

## 1.2.0 – 1.2.2（2026-10-24）

- 定位為內部報告 HTML 的設計與發布工具。
- 加入 static.example.com 發布：`scripts/publish.sh`、`scripts/delete.sh`。
- 加入 ASD-STE100 文案段，以及來源與交叉引用段。

## 1.1.0（2026-10-24）

- 兩種風格：Paper 極簡、Harbor 深藍。架構圖可選 Mermaid 或 live-panel。

## 1.0.0（2026-10-24）

- 第一版：Radix Colors 色系、11 條 UI 設計規範、套用流程、自檢清單。
