# page-craft

內部報告 HTML 的**設計 + 發布工具**。把寫好的報告內容，套成一致的視覺風格，發布到 static.example.com，並做版本控制。

## 示範（線上）

首頁：https://penchien.github.io/page-craft-demo/

| 頁面 | 風格 | 架構圖 | 網址 |
|---|---|---|---|
| jira 使用說明 | Paper 極簡 | live-panel 動態圖 | https://penchien.github.io/page-craft-demo/jira-paper.html |
| jira 使用說明 | Harbor 深藍 | inline SVG 泳道 | https://penchien.github.io/page-craft-demo/jira-harbor.html |
| jira 使用說明 | Atlas 計畫版 | CSS 流程框 | https://penchien.github.io/page-craft-demo/jira-atlas.html |
| Atlas 元件示範 | Atlas 計畫版 | 三種並列 | https://penchien.github.io/page-craft-demo/atlas-demo.html |
| live-panel 示範 | live-panel | loop、ring、funnel、終端機面板、16:9 監控牆 | https://penchien.github.io/page-craft-demo/live-panel-demo.html |

原始檔在 `examples/` 與 `assets/`。

## 能做什麼

1. **設計**：三種可選風格 — Paper 極簡、Harbor 深藍、Atlas 計畫版。色票、表格、彩色卡片、架構圖四選一。
2. **發布**：上傳到 static.example.com portal，預覽到正式，cmp 逐 byte 驗證，刪預覽。
3. **版控**：commit 推 GitLab，rollback 備份。

## 用法

Claude Code 載入後，說「改 UI」「美化報告」「發布到 space」「Paper」「Harbor」「Atlas」「架構圖」即觸發。規範與流程全文見 `SKILL.md`。

## 三種風格

| 風格 | 個性 | 適合 |
|---|---|---|
| Paper 極簡 | sand 中性、0.5px、低對比、守 11 條 | 資料密集、要中性專業 |
| Harbor 深藍 | #1f4e79、標題左線、善用表格、彩色卡片 | 說明文件、要引導閱讀 |
| Atlas 計畫版 | 深藍封面、灰底白卡、章節 chip、進度條、狀態 pill | 季度計畫、OKR 進度、roadmap |

三者不同取捨，內文不要混用；頁首與導覽列可沿用 Atlas。動手前問使用者要哪種。Atlas 的 CSS 與示範頁在 `assets/`（`atlas.css`、`atlas-demo.html`）。

## 文案：ASD-STE100 寫法

報告文字照 ASD-STE100（簡化技術英文）的原則寫：一句一事、短句、同詞同義。三種風格都適用。

| 規則 | 內容 |
|---|---|
| R1 句長 | 一句不超過 25 字。英文詞、數字、單號、日期各算 1 字。 |
| R2 模糊詞 | 不用「優化、處理、調整、改善、相關、已完成、已確認」。「協助」「支援」後面要接具體動詞。 |
| R3 縮寫 | 第一次出現寫全名，例：SC-1（成功指標第 1 條）。 |

| 不要這樣寫 | 要這樣寫 |
|---|---|
| 已完成防火牆相關設定調整 | Casey Ho 於 2026-06-01 新增 policy 123。 |
| 效能大幅提升 | 開機時間從 2 分 05 秒降到 6 秒。 |
| 6/1 下午 | 2026-06-01 14:33 Asia/Taipei |

送出前跑檢查（腳本在 jira skill 內）：

```
python3 "$(find ~/.claude/skills -name ste_check.py | head -1)" <檔>
# 路徑依安裝方式而定：
#   直接安裝 ~/.claude/skills/jira/scripts/ste_check.py
#   整個 repo clone ~/.claude/skills/jira/skills/jira/scripts/ste_check.py
```

同一個概念全文用同一個詞。Paper 風格另外不用中點「·」當分隔。

## 發布（static.example.com）

- API 與流程見 `SKILL.md`「發布」段。
- 腳本在 `scripts/`：
  - `publish.sh <site> <本機檔> <線上名> [--index]`：上傳 + cmp 驗證 + 可選設首頁。
  - `delete.sh <site> <path>`：刪線上檔。
- token 放 `~/.config/space-portal.env`（`SPACE_TOKEN=<token>`，chmod 600）。腳本讀、不印、不進對話。
- 流程：套樣式 → 發預覽（`<名>-preview.html`）→ 使用者確認 → 覆蓋正式 → 刪預覽 → 可選推 GitLab。

## 架構圖（四選一）

- Mermaid：有分支、節點 5–7 個、與文章同寬。
- CSS 流程框：`.flow` / `.vflow` / `.lc` / `.uloop`，3–6 步線性流程，純 HTML，手機自動轉直。
- inline SVG 泳道：多角色、要精確排版；泳道虛線框、白底彩邊節點、箭頭依語意分色。
- live-panel：一直在跑的動態架構圖，已內建在 `live-panel/`（MIT，上游 ythx-101/live-panel-skill）。

選法：線性 → CSS 流程框；分支 → Mermaid；泳道 → inline SVG；展示面板 → live-panel。

示範：`examples/jira/` 用 jira 使用說明做三版（Paper＋live-panel、Harbor＋SVG 泳道、Atlas＋CSS 流程框），`build.py` 可重建。

drawio 轉檔：把 drawio 架構圖重繪成 inline SVG 線路圖，也能用 `svg2drawio.py` 把線路圖轉回可編輯的 drawio。步驟見 `references/drawio.md`，範例在 `examples/drawio-arch/`。

## 第三方元件

`live-panel/` 來自 https://github.com/ythx-101/live-panel-skill（MIT）。字型為 SIL OFL 1.1，Lucide 圖示為 ISC，授權檔與 NOTICE 照原樣保留。上游版本記在 `live-panel/UPSTREAM`。

## 更新

`update-skills`（讀 `SKILL.md` 的 `source` 欄位 git pull）。

各版改了什麼見 `CHANGELOG.md`。

## 正本

GitLab：https://git.example.com/skills/page-craft
