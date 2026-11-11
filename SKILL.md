---
name: skill-html
source: https://git.example.com/skills/skill-html.git
description: skill-html（舊名 skill-ui）。Alex 的內部報告 HTML 設計與發布工具。三種風格(Radix 極簡、Ocean 深藍、Momo 計畫版)套樣式，內建 live-panel 動態架構圖，發布到 static.example.com(預覽→正式、cmp 驗證)，GitLab 版控。含色票、表格與彩色卡片、架構圖四選一(Mermaid / CSS 流程框 / inline SVG 泳道 / live-panel)、發布腳本、rollback 與自檢。觸發於 改 UI / 美化報告 / 發布到 space / 界面優化 / Radix / Ocean / Momo / restyle / redesign / 架構圖 / 流程圖 / 計畫頁 / OKR 頁。
triggers: ui, live-panel, 動態架構圖, 改ui, 美化, 介面, 界面, radix, ocean, momo, 設計規範, skill-html, skill-html-demo, html, restyle, redesign, 優化介面, 架構圖, 流程圖, 泳道, 流程框, 計畫頁, okr, 卡片, 風格, 發布, space, portal, 報告
metadata:
  type: reference
---

# skill-html：內部報告 HTML 設計與發布

舊名 skill-ui，2026-10-24 正名為 skill-html。

內部報告 HTML 的**設計 + 發布工具**。把寫好的報告內容，套成一致的視覺風格，發布到 static.example.com，並做版本控制。三件事：
1. **設計**：三種可選風格 — Radix 極簡、Ocean 深藍、Momo 計畫版。動手前先問使用者要哪一種，或沿用既有。
2. **發布**：上傳到 static.example.com，預覽到正式，cmp 逐 byte 驗證。見下方「發布」段。
3. **版控**：commit 推 GitLab，rollback 備份。

## 何時用

- 使用者說：改 UI、美化、界面優化、套用設計規範、Radix、Ocean、Momo、restyle、redesign。
- 既有 HTML、報告、工具要重新設計視覺。

## 先決：一定要能 rollback

1. 檔在 git：記下 commit（`git rev-parse --short HEAD`），還原用 `git checkout HEAD -- <檔>`。
2. 另存一份 `.bak` 到 git 外的目錄。
3. 改完先發**預覽版**（不同檔名），使用者確認再覆蓋正式。不要直接覆蓋正式。
4. 不確定風格時，可兩種各發一個預覽，讓使用者並排比較。

## 選風格

| 風格 | 個性 | 適合 |
|---|---|---|
| Radix 極簡 | 安靜、克制、低對比、少裝飾 | 資料密集、要中性專業的報告；守 11 條 |
| Ocean 深藍 | 深藍主色、標題左線、表格組織、彩色卡片；層次鮮明、一眼抓重點 | 說明文件、流程、要引導閱讀的報告 |
| Momo 計畫版 | 深藍封面、灰底白卡、章節 chip、進度條、狀態 pill、CSS 流程框；像一頁式簡報 | 季度計畫、OKR 進度、roadmap、要給主管一眼看完的頁 |

不確定就問使用者。三者是不同取捨，內文不要混用。例如 Radix 的 0.5px 不配 Ocean 的 6px 左線，Momo 的圓角陰影不配 Radix。
例外：**頁首與導覽列可沿用 Momo，內文維持一種風格**。頁首指封面加黏頂章節列。2026-10-24 目標管理系統「如何開專案」用 Momo 頁首包 Ocean 內文，Alex 接受。

---

## 風格 A：Radix 極簡

全部顏色用 [Radix Colors](https://www.radix-ui.com/colors)。中性 sand、強調 orange、成功 green。
分階：1-2 底、2-3 面、6-7 線、9 實色、11 文字。

```
:root{
  --bg:#fdfdfc;--surface:#f9f9f8;--surface2:#f1f0ef;
  --line:#dad9d6;--line-strong:#cfceca;--mut:#63635e;--fg:#21201c;
  --acc:#f76b15;--acc-text:#cc4e00;--ok:#30a46c;--ok-text:#218358;--on-acc:#fff;
}
@media (prefers-color-scheme:dark){:root{
  --bg:#111110;--surface:#191918;--surface2:#222221;
  --line:#3b3a37;--line-strong:#494844;--mut:#b5b3ad;--fg:#eeeeec;
  --acc:#f76b15;--acc-text:#ffa057;--ok:#30a46c;--ok-text:#3dd68c;--on-acc:#fff;
}}
```
- 底 step1、面 step2、巢狀面 step3；邊框 step6，較強 step7。
- 次要文字 step11、主文字 step12；實色（bar、按鈕底）step9，強調文字 step11。
- step9 配字：多數白；amber/yellow/lime/mint/sky 配深字，orange 配白。

### Radix 的 11 條規則

1. 不用中點「·」作分隔。改空格或頓號「、」。
2. 不加冗餘的解釋性描述，別弄髒界面。
3. review 文案：符合受眾、好懂、不口語、不冗餘、不造詞。
4. 顏色全用 Radix，照其語意分階。
5. 光學對齊；巢狀處同心圓角。
6. 線條邊框用 0.5px。
7. 少動畫；要用就 ease-out、250ms。
8. 字級 4 種以內（最好 3），最小 12px。不夠用字重、顏色、間距分層。
9. 少需要判斷的交互；依信息優先級有秩序地組織。
10. 少圓角、陰影，尤其**卡片左邊緣彩色線**。
11. 少 Eyebrow / Overline，不加與主標題語義重複的裝飾小標題。

**適用範圍（2026-10-24 Alex 評價）**：清單列用 Radix 好看，例：個人頁「手上的工作」。狀態卡、檢核卡用 Radix 被評「很醜」，例：Team Status，已還原。
**第 10 條的例外**：清單列前端的狀態色條要保留，Alex 明確要求。色條 3px，顏色同燈號。拿掉後狀態一眼看不出來。

---

## 風格 B：Ocean 深藍

來源：jira 使用說明的風格。深藍 `#1f4e79` 主色、標題帶左粗線、善用表格、彩色卡片、深色程式碼區。

```
:root{
  --bg:#fff;--surface:#f3f6fa;--surface2:#fafafa;
  --line:#d5dee8;--line-tbl:#ccc;--mut:#666;--fg:#1a1a1a;
  --acc:#1f4e79;--ok:#2e7d32;--no:#c62828;--on-acc:#fff;
}
@media (prefers-color-scheme:dark){:root{
  --bg:#13161a;--surface:#1a2230;--surface2:#1e1e1e;
  --line:#2b3a4d;--line-tbl:#3a4556;--mut:#9fb0c2;--fg:#e8edf2;
  --acc:#7aa7d6;--ok:#6fbf73;--no:#e57373;--on-acc:#13161a;
}}
h1{border-bottom:3px solid var(--acc);padding-bottom:6px}
h2{color:var(--acc);border-left:6px solid var(--acc);padding-left:10px}
a,.xref{color:var(--acc)}
th,td{border:1px solid var(--line-tbl);padding:6px 9px} th{background:var(--surface);font-weight:700}
pre{background:#1e1e1e;color:#e6e6e6;border-radius:6px;padding:12px 14px}
```

### Ocean 的兩個重點

1. **善用表格。** 這是 Ocean 最好的地方。資訊不進表格就會散亂。能列成表（項目對值、現況對目標、比較）的，一律用表格。
2. **彩色卡片分提示類型。** 不同語意用不同顏色的卡片：

```
.box {background:#f3f6fa;border:1px solid #d5dee8;padding:12px 16px;border-radius:6px}       /* 一般框 藍 */
.rule{background:#e8f4ea;border-left:5px solid #2e7d32;padding:8px 14px}                      /* 規則、正例 綠 */
.warn{background:#fff8e1;border-left:5px solid #f0b400;padding:8px 14px}                      /* 注意 黃 */
.no  {background:#fdecea;border-left:5px solid #c62828;padding:8px 14px}                      /* 禁止、錯誤 紅 */
.tag {display:inline-block;font-size:12px;padding:0 7px;border-radius:3px;font-weight:bold;color:#fff}
.b1{background:#1f4e79}.b2{background:#2e7d32}.b3{background:#6a1b9a}.b4{background:#bf360c}.b5{background:#555}
```
- 卡片左彩線在 Ocean 是刻意用的（和 Radix 第 10 條相反）。用來標示提示的語意類型，不要只為裝飾。
- 標籤 `.tag` 配 `.b1`-`.b5` 做彩色小標（藍、綠、紫、橙、灰）。

**公式、定義區塊不要用深色 pre**（2026-10-24 Alex：黑底不好看）。深色只留給真正的程式碼。卡片裡的公式改淺色，並貼在卡片底部，左右兩張卡才會對齊：
```
.qa{display:flex;flex-direction:column}
.qa pre{margin-top:auto;background:#f3f6fa;color:#1f3550;border:1px solid #d5dee8;border-left:4px solid #1f4e79;border-radius:4px;padding:8px 12px;white-space:pre-wrap}
```
章節之間要拉開：每節上方留 44px，加一條 1px 分隔線。否則章節看起來黏在一起。

---

## 風格 C：Momo 計畫版

來源：Data Team 2026 Q4 計畫頁（`data-team-plan-2026q4.html`）。一頁式簡報的讀法：封面深藍 → sticky 膠囊導覽 → 灰底 → 章節 chip 標題 → 白卡 `.blk` → 卡內灰卡 `.card`。

完整 CSS 在 `assets/momo.css`（亮色加深色，含三種架構圖）。示範頁 `assets/momo-demo.html`，每個元件各一個例子，複製就能用。

```
:root{
  --bg:#eef1f5;--surface:#fff;--surface2:#f5f6f8;
  --line:#e5e7eb;--mut:#8a8985;--fg2:#52514e;--fg:#0b0b0b;
  --acc:#2a78d6;--link:#1b4f9c;--navy:#0f2747;
  --ok:#1f6b3a;--ok-bg:#e6f2ea;--no:#9a1f1f;--no-bg:#f7d9d9;
  --shadow:0 1px 2px rgba(15,39,71,.06),0 6px 20px rgba(15,39,71,.05);
}
@media (prefers-color-scheme:dark){:root{
  --bg:#0f1115;--surface:#171a21;--surface2:#1e222b;
  --line:#2a2f3a;--mut:#8b949e;--fg2:#b6bdc8;--fg:#e8eaf0;
  --acc:#5b9cf0;--link:#8ab4f8;--navy:#0b1c33;
  --ok:#6fcf8f;--ok-bg:#15301f;--no:#f08a8a;--no-bg:#3a1a1a;--shadow:none;
}}
.cover{background:var(--navy);color:#fff;padding:88px 48px 64px}.cover h1{border-left:6px solid var(--acc);padding-left:20px;font-size:36px}
.divider{margin:72px 0 18px;font-size:24px;font-weight:800;color:var(--navy)}.divider span{background:var(--acc);color:#fff;font-size:12px;padding:3px 9px;border-radius:4px;margin-right:10px}
.blk{background:var(--surface);border-radius:14px;padding:26px 30px;margin:22px 0;box-shadow:var(--shadow)}
.card{background:var(--surface2);border-radius:10px;padding:14px 18px}.card .lab{color:var(--acc);font-weight:700;font-size:13px}
.bar{height:8px;background:var(--line);border-radius:4px;overflow:hidden}.fill{height:100%;background:var(--acc)}.fill.risk{background:var(--no)}
```

### Momo 的四個重點

1. **三層底色分層次。** 頁底灰 `--bg` → 白卡 `.blk`（14px 圓角、柔和陰影）→ 卡內灰卡 `.card`。不要再加邊框，層次靠底色。
2. **章節用 chip 標題。** `.divider` 是「藍 chip + 一句話標題」，chip 寫章節短名（現況、觀察、10–12 月），標題寫這章要回答的問題。
3. **進度與狀態可視化。** 標題旁 `.pct` 進度百分比加 `.bar` 進度條，落後用 `.fill.risk` 紅。新增項目用 `.new` 綠字加【新增】。狀態 pill 四種：`.st-done` 綠、`.st-prog` 藍、`.st-wait` 黃、`.st-todo` 灰。
4. **類別標籤四組固定色。** `.pill.o1` 藍、`.o2` 橙、`.o3` 綠、`.o4` 紫，對應 OKR 或類別，整份一致。階梯卡 `.lc-card.o1`–`.o4` 的頂線用同四色。

其他元件：`.stats` 四格大數字、`.hero` 深藍標語塊、`.callout` 綠色原則框、`table.t` 灰表頭、`pre` 深藍程式碼區。手機（≤800px）流程框自動轉直、四格變兩格。

### Momo 淡色立體版（2026-10-24 Alex 選定）

Alex 看過預設 Momo 後要求「顏色淡一點、更有質感、立體點」。差異只在下面幾項，其餘照 Momo。完整檔 `assets/momo-soft.css`，接在 `momo.css` 後面，只改亮色、深色維持原 Momo；示範 `examples/jira/jira-momo.html`：
```
.cover{background:linear-gradient(135deg,#eaf2fc 0%,#f4f8fd 55%,#e6eef9 100%);color:#0f2747;border-bottom:1px solid #dbe5f1}
.cover p{color:#4a6283}
.divider span{background:linear-gradient(180deg,#4b92e6,#2a78d6);box-shadow:0 2px 6px rgba(42,120,214,.28)}
.blk{background:linear-gradient(180deg,#fff,#fbfcfe);border:1px solid #edf1f6;box-shadow:0 1px 2px rgba(15,39,71,.05),0 10px 30px rgba(15,39,71,.07)}
.card{background:linear-gradient(180deg,#fff,#f7f9fc);border:1px solid #e9eef4;box-shadow:0 1px 2px rgba(15,39,71,.05),0 4px 12px rgba(15,39,71,.05),inset 0 1px 0 #fff;transition:transform .2s ease-out,box-shadow .2s ease-out}
.card:hover{transform:translateY(-2px);box-shadow:0 2px 4px rgba(15,39,71,.06),0 10px 24px rgba(15,39,71,.09),inset 0 1px 0 #fff}
.pill.o1{background:linear-gradient(180deg,#eaf2fc,#dbe8f9);box-shadow:inset 0 1px 0 #fff}
pre{background:#f3f7fc;color:#24426b;border:1px solid #e3ebf5;box-shadow:inset 0 1px 3px rgba(15,39,71,.08)}
```
這版的卡片有細邊框，和第 1 點「不加邊框」不同。淡色底上不加邊框，卡片會糊在一起。

### Momo 章節導覽列（2026-10-24 Alex 逐輪指正）

- **整條橫列鋪滿畫面寬，黏在頂端**。不要做成懸浮的圓角框（Alex：「變成懸浮的，我不要」）。
- **封面文字、導覽按鈕、內文左緣對齊同一條線**。單檔報告整塊置中（2026-10-25 Alex）；嵌在網頁程式裡（例 目標管理系統）才靠左、右側留白。
- **導覽按鈕與封面文字跟下面內容同寬**：外層橫列鋪滿。裡面包一層容器，max-width 同內文；單檔報告 `margin:0 auto`，嵌在網頁程式裡 `margin:0`。
- **捲到哪章亮哪章，每章一種顏色**：按鈕前加一個彩色小圓點；目前章節的按鈕換成該章顏色的淡底、邊框、文字並加粗。
- 監聽捲動用捕捉階段 `document.addEventListener("scroll", fn, true)`。頁面放在網頁程式裡時，捲動的是內層元素，掛在 window 上收不到。
- 現成實作：`assets/momo.css` 的 `nav.mnav`，加上 `assets/momo-nav.js`。Ocean 也可用同一支 js，導覽列配色改單一深藍，見 `examples/jira/jira-ocean.html`。判定線是導覽列底緣再往下 24px：比 scroll-padding 多留 16px，點錨點跳過去時才不會差一點沒過線而亮成上一章。深色模式下亮起的文字要調亮，章節色在深底上太暗。
```
.mnav{position:sticky;top:0;z-index:9;background:rgba(255,255,255,.94);backdrop-filter:blur(6px);border-bottom:1px solid #e3e9f0}
.mnav .mw{max-width:<內文寬>;margin:0;display:flex;gap:6px;flex-wrap:wrap}
.mnav a i{width:7px;height:7px;border-radius:50%;background:var(--c)}
.mnav a.on{background:color-mix(in srgb,var(--c) 14%,#fff);border:1px solid color-mix(in srgb,var(--c) 35%,#fff);color:var(--c);font-weight:700}
```

---

## 文案：ASD-STE100 寫法

報告文字用 ASD-STE100 原則：一句一事、短句、同詞同義。三種風格都適用。
三條核心（與 jira 的 `ste_check.py` 一致）：
- 一句不超過 25 字。英文詞、數字、單號、日期各算 1 字。
- 不用模糊詞：優化、處理、調整、改善、相關、已完成、已確認。「協助」「支援」後要接具體動詞。
- 縮寫第一次出現寫全名，例：SC-1（成功指標第 1 條）。

可重用檢查（jira skill 內）：`python3 "$(find ~/.claude/skills -name ste_check.py | head -1)" <檔>`。報告文字送出前先跑。
路徑依安裝方式而定：直接安裝是 `~/.claude/skills/jira/scripts/ste_check.py`；整個 repo clone 進去是 `~/.claude/skills/jira/skills/jira/scripts/ste_check.py`。

## 架構圖（四種選擇，提醒使用者）

畫架構圖、流程圖時，先問使用者要哪一種。不確定就依「適合」欄選，並說明為什麼。

| 選擇 | 樣子 | 適合 | 備註 |
|---|---|---|---|
| Mermaid | 報告內嵌的流程圖、架構圖 | 有分支、節點 5–7 個的一般報告 | 直式、與文章同寬、不要外擴；三種風格都能用 |
| CSS 流程框 | `.flow` 橫向一排框加 → 箭頭；`.vflow` 直向；`.lc` 四格階梯卡；`.uloop` 虛線迴圈 | 3–6 步的線性流程、階段對照 | 不用繪圖庫，純 HTML；手機自動轉直；CSS 在 `assets/momo.css`，例子在 `assets/momo-demo.html` |
| inline SVG 泳道 | 手繪 SVG：虛線泳道框 + 彩色小標、白底彩邊節點、pill 在節點上方、箭頭依語意分色 | 多角色（人 / agent / 系統）、要精確排版的架構圖 | `viewBox` 固定、`width:100%`、`min-width:720px` 窄螢幕橫向捲動；SVG 固定亮色，深色模式下包在 `.fig` 白框 |
| live-panel | 一直在跑的動態架構圖：固定版面、線上流動的封包、判斷點與回環；`terminal-dark` 或 `light-pastel` 兩種主題 | 展示型、要「活的」流程或架構面板 | 已內建在 `live-panel/`（MIT，上游 ythx-101/live-panel-skill）；JSON config 產生單檔 HTML 或 mp4 |

選法：線性步驟 → CSS 流程框；有分支 → Mermaid；泳道、多角色 → inline SVG；要動態展示、有判斷與回環 → live-panel。

**完整示範**：`examples/jira/` 用同一份 jira 使用說明做三版，每版一種流程圖，方便並排比較。

| 檔案 | 風格 | 流程圖 |
|---|---|---|
| `jira-radix.html` | Radix 極簡 | live-panel loop 視圖（`jira-loop.html`，設定檔 `jira-loop.config.json`） |
| `jira-ocean.html` | Ocean 深藍 | inline SVG 泳道（主管、執行者、簽收者） |
| `jira-momo.html` | Momo 計畫版 | CSS 流程框（開案到關單七步） |

來源頁更新後重跑：`python3 examples/jira/build.py <jira-使用說明.html>`。三頁 CSS 全內嵌，單檔就能發布。

**drawio 轉檔**：使用者給 drawio、要轉成報告用的線路圖時，用 inline SVG。步驟與判讀原圖的坑見 `references/drawio.md`；範例 `examples/drawio-arch/`（`drawio_tool.py` 畫原圖、列框與線；`build_arch.py` 產生重繪頁；`svg2drawio.py` 把重繪頁轉回可編輯的 drawio）。

### live-panel（內建）

上游完整說明在 `live-panel/SKILL.md`，動手前先讀。這裡只記在本機跑通的做法。

**展示頁**：`examples/live-panel/live-panel-demo.html`，五種畫法各一個例子：loop、ring、funnel、scaffold 終端機面板、16:9 監控牆。每個都附 config 和「何時用」。線上版 https://penchien.github.io/skill-html-demo/live-panel-demo.html 。

```
cd ~/.claude/skills/skill-html/live-panel
CH=~/.cache/ms-playwright/chromium-1234/chrome-linux64/chrome
# 1. 檢查：文字溢出、重疊、連線穿過節點；--repeat 證明回放逐像素相同。exit 0 才往下
python3 -I scripts/check_frames.py --config <cfg>.json --out-dir /tmp/frames --chrome $CH --no-sandbox --png 4 --repeat
# 2. 輸出單檔 HTML（mp4 只是副產品，可用很短的 duration 帶過）
python3 -I scripts/render.py --config <cfg>.json --out /tmp/x.mp4 --duration 1 --fps 5 --chrome $CH --no-sandbox --html-out <name>.html
```
- 視圖選法：有判斷與回環 → `loop`；循環 → `ring`；逐段流失 → `funnel`；任意框線 → 不用 view，照上游例子手排。
- **16:9 監控牆風格**（投螢幕、電視）：terminal-dark、1920x1080、`fontSize` 22。左欄主管值班（`triggers` 狀態機 + `tarrow`），右邊由上往下一層一層的框（Epic → 基準量測 → Story ×4 → 簽收 → 送簽收 → 使用統計），層間 `flow` 封包，底部 `log`。範本 `examples/live-panel/wall.config.json`（與 192.0.2.10:8088/live-panel.html 同內容；用內建 live-panel 重產，截圖逐 byte 相同）。改內容時複製這份 config，改框內文字與 `machines`，座標照抄。
- 報告內嵌：`<iframe src="<name>.html" style="width:100%;aspect-ratio:<W>/<H>;border:0">`。頁面會依視窗等比縮放，HTML 要和報告一起上傳。
- 主題配風格：Radix、Momo 用 `light-pastel`；要終端機監控感才用 `terminal-dark`。
- loop 視圖的 `period` 必須是 `ambientPeriod` 的整數倍，`canvas.duration` 必須是 `period` 的整數倍。每跳至少 1.25 秒。
- 連線穿過說明框時，`check_frames.py` 會報 `edge … passes through node`。把 note 移到沒有連線經過的欄。
- 數字沒有真實來源就在 `credit` 寫「示意」。上游的 credit 規則照守。
- `scaffold.py` 在 `lang:"zh"` 時會補簡體字固定字串（最近建议、调用、唤起）。產生後在 config 裡改成繁體，再跑一次檢查。

### Mermaid

```
<pre class="mermaid">
flowchart TD
  A["開案<br>八項必填"] --> B{"現值待量？"}
  B -- 是 --> C["基準量測"]
  B -- 否 --> D["任務"]
  C --> D
</pre>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js"></script>
<script>if(window.mermaid){var d=matchMedia('(prefers-color-scheme: dark)').matches;
mermaid.initialize({startOnLoad:true,theme:'base',themeVariables:d?{primaryColor:'#222221',primaryTextColor:'#eeeeec',lineColor:'#b5b3ad'}:{primaryColor:'#f9f9f8',primaryTextColor:'#21201c',lineColor:'#63635e'}})}</script>
```
- 節點文字用 `<br>` 自己斷行：「標題<br>一句說明」。不斷的話 Mermaid 在約 200px 自動換行，會斷在「P0–」與「P4」中間。
- 顏色用 `theme:'base'` 加 `themeVariables`，依 `matchMedia` 切亮暗。色票取該風格的 token。
- CDN 讀不到時 `<pre class="mermaid">` 會留下原始文字，不會整塊空白。內網不能出網時，把 mermaid.min.js 放同站目錄改相對路徑。

### CSS 流程框

```
<div class="flow">
  <div class="bx"><b>票進來</b><span>維運、新資料源</span></div><div class="arr">→</div>
  <div class="bx"><b>負責人開做</b><span>各自實作</span></div><div class="arr">→</div>
  <div class="bx bad"><b>沒有人看到全貌</b><span>一個人掌握不了</span></div>
</div>
<div class="uloop red"><span class="uarr">↑</span><span class="ulab">回到起點</span></div>
```
- 框色三種語意：`.bx` 一般灰、`.bx.good` 綠（正確做法）、`.bx.bad` 紅（問題）、`.bx.dark` 深藍（強調）。
- 每框兩行：`<b>` 一句名稱、`<span>` 一句說明。超過兩行就改表格。
- 迴圈 `.uloop` 放在 `.flow` 下方，`.red` 表示惡性循環。

### inline SVG 泳道

```
<div class="fig"><svg viewBox="0 0 1090 300" role="img" aria-label="…">
  <defs><marker id="a-main" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#52514e"/></marker></defs>
  <!-- 泳道 -->
  <rect x="20" y="40" width="250" height="230" rx="12" fill="#f3faf5" stroke="#1baf7a" stroke-dasharray="5 4"/>
  <text x="32" y="60" font-size="12.5" font-weight="650" fill="#1baf7a">人</text>
  <!-- 節點：白底彩邊，標題 13.5 粗、說明 11 -->
  <rect x="50" y="120" width="190" height="70" rx="8" fill="#fff" stroke="#1b4f9c" stroke-width="1.6"/>
  <text x="145" y="152" text-anchor="middle" font-size="13.5" font-weight="800" fill="#0b0b0b">節點名</text>
  <text x="145" y="172" text-anchor="middle" font-size="11" fill="#52514e">一句說明</text>
  <!-- pill 在節點上方 -->
  <rect x="123" y="96" width="44" height="18" rx="9" fill="#dbe8f9"/><text x="145" y="109" text-anchor="middle" font-size="11" font-weight="800" fill="#1b4f9c">OKR1</text>
  <!-- 箭頭 -->
  <line x1="240" y1="155" x2="316" y2="155" stroke="#52514e" stroke-width="1.6" marker-end="url(#a-main)"/>
</svg></div>
```
- 泳道色：人 綠 `#1baf7a/#f3faf5`、workflow 黃 `#c98500/#fffcf3`、資料 藍 `#2a78d6/#f4f8fd`、共用 青 `#0e8a8a/#f0fafa`。
- 箭頭依語意分色：主流程灰 `#52514e`、參照紫 `#4a3aa7`、迴圈橙 `#eb6834`（虛線）、錯誤紅 `#d03b3b`、詢問青 `#0e8a8a`（虛線）。每種各一個 `<marker>`。
- 字級以 viewBox 單位算：標題 13.5、說明 11、泳道標 12.5。小於 10.5 在 1090 寬的 viewBox 縮到手機會看不清。
- 位置用整數座標手算，節點寬 170–190、高 56–70、間距 30–80。完整例子見 `assets/momo-demo.html` 的「C 手繪 inline SVG 泳道」。

## 套進既有網頁程式（不是單檔 HTML）

例：目標管理系統（React、antd、refine）的頁面。和單檔報告不同的地方：
- **樣式包在頁面根層 class 下**，例 `.ocean`、`.momo`。不要寫在 `:root` 或裸元素上，否則會改到其他頁。
- **封面要貼齊左右邊**，得用負 margin 抵銷外層留白。margin 值等於外層的留白，例 `.momo{margin:-24px}`。
- **預覽不是發 space**，照該網頁程式自己的預覽流程。
- 目標管理系統 的外層留白、預覽站與建置指令見 `references/web-app-embed.md`。
- 改之前把原檔另存到 git 外，記下 commit，使用者確認後才 commit。

## 發布到 static.example.com portal

報告做好後發布到內部靜態站 static.example.com。

- API：`https://portal.static.example.com/api/v1`，Bearer token `<token>`（放 `~/.config/space-portal.env` 的 `SPACE_TOKEN=`，腳本讀、不印、不進對話）。
- 上傳：`POST /sites/<site>/files`，multipart `files=@檔;filename=<線上名>`（同名覆蓋；`filename=dir/x` 放子目錄）。
- 設首頁：`PUT /sites/<site>/index {"file":"<名>"}`。站網址 `https://<site>.static.example.com`。
- 刪除：`DELETE /sites/<site>/files/<path>`。
- 上傳後**一定 cmp 驗證**：下載線上檔和本機逐 byte 比對。大檔要重試幾次，portal 處理有延遲。

腳本（skill 的 `scripts/`）：
- `publish.sh <site> <本機檔> <線上名> [--index]`：上傳 + cmp 驗證 + 可選設首頁。
- `delete.sh <site> <path>`：刪線上檔。

**發布流程**：套樣式 → `publish.sh <site> <檔> <名>-preview.html`（發預覽）→ 使用者確認 → `publish.sh` 覆蓋正式名 → `delete.sh` 刪預覽 → 可選 commit 推 GitLab 版控。正式檔可能已被連結或工單引用，所以先預覽、確認、再覆蓋。

## 來源與交叉引用（GitLab / DocHub / Jira）

報告不是孤立的檔。做報告時把它和這三個來源交叉引用，方便追溯。

- **GitLab**：報告原始碼進 repo；commit 訊息、MR 標題帶 Jira 票號（例 DEMO-3213）；repo README 放 Jira 對應表。歷史不可含密碼，發布副本用 `git fast-export | sed 同長度取代 | fast-import` 清洗後再推。
- **DocHub**（wiki.example.com）：文件正本可放 DocHub，與 GitLab 同等計分。DocHub 開頁當正本，portal HTML 當可分享的視覺版。
- **Jira**：報告網址貼進對應工單的留言；票號寫進報告與 commit，Jira 開發區塊才連得起來。留言、送簽收、關單走 jira skill。
- **Toolbridge 閘道**（toolbridge.example.com，HTTPS）：Jira `/jira/mcp`、GitLab `/gitlab/mcp`、DocHub `/dochub/mcp`。接上後用 mcp 工具直接讀寫，不手動貼。設定見 reference-toolbridge。

做報告時順手問：這份連哪張 Jira？正本放 DocHub 還是 GitLab？發布後網址回貼工單了嗎？

## 套用流程

1. 問使用者要 Radix、Ocean 還是 Momo（或沿用既有）。
2. 備份加 rollback 點。
3. 重寫 `<style>` 的 `:root` token 成該風格（亮色加深色）。Momo 直接貼 `assets/momo.css`。
4. 元件依風格調：Radix 走極簡（0.5px、無左線、字級≤4）；Ocean 走藍色主調：左線標題、表格、彩色卡片；程式碼深色，公式淺色；Momo 走簡報式（封面、chip 標題、白卡灰卡、進度條、pill）。
5. 文案三風格都做：移除中點、刪冗餘、精簡副標題。
6. 架構圖四選一：Mermaid、CSS 流程框、inline SVG 泳道、live-panel。依場景或問使用者。
7. 跑自檢；發預覽；使用者確認後覆蓋正式。

## 自檢清單

- 風格一致：沒有混用兩套（grep 殘留的舊色）。
- 中點「·」= 0。
- Radix：字級≤4、最小 12px、邊框 0.5px、無卡片左彩線。
- Ocean：主色 #1f4e79 一致、資訊有進表格、卡片顏色對應語意。程式碼 pre 深色，公式區塊淺色且貼底。
- Momo：頁底 #eef1f5、每章有 chip 標題、白卡內不加邊框（淡色立體版例外：卡片加細邊框）、進度條與狀態 pill 顏色對應語意、類別 pill 四色整份一致。
- 架構圖：CSS 流程框每框兩行以內；inline SVG 有 `viewBox`、`aria-label`、字級 ≥ 10.5；手機寬（400px）看過一次。
- 標籤（tag）平衡；實色上文字對比足。

## gotcha（實作教訓）

- **sticky 導覽 active 高亮**：判定當前章節的閾值用導覽列**實際高度**（`nav.offsetHeight`），不要用固定值；多排 wrap 時固定值會高亮錯節。並設 `document.documentElement.style.scrollPaddingTop = nav.offsetHeight + 8`，讓錨點連結對齊。
- **字級收斂（Radix）**：用字重、顏色、間距分層，不靠增加字級。
- **Radix step9 配字**：多數白；amber/yellow/lime/mint/sky 配深字，orange 配白。
- **先發預覽再覆蓋正式**：正式檔可能已被連結或工單引用。大改先發預覽，保留 rollback。
- **內聯底色在深色模式會刺眼**：來源頁常有 `style="background:#e3f1f5"` 這種表格列底色。改成 class，深色另給一組色。
- **iframe 用相對路徑的區塊**：換主機發布就會失效（例：jira 說明頁的 live-panel）。改版時換成內嵌圖，或改絕對網址。
- **流程框與節點文字先截圖再交**：中文說明超過約 7 字就會在 7 格的 `.flow` 裡換行；SVG 的標籤別放在線的正中央。
- **pill 類別色不要寫成裸 class**：`.o1{background…}` 會連 `.lc-card.o1` 的底色一起蓋掉。寫成 `.pill.o1`，階梯卡的頂線色另寫 `.lc-card.o1`。
- **inline SVG 在深色模式**：SVG 內是固定色碼，不吃 CSS 變數。包在 `.fig` 白底框內，別讓深色底直接貼 SVG。
- **標題不能截斷**：清單列、卡片標題寫 `white-space:normal` 讓它換行。單號與層級標籤跟在標題後面。Alex 看到截斷就會退。
- **兩張表並排用 CSS grid**：`display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr))`。用 `inline-block` 加百分比寬，會被前後文字擠歪而跑版。
- **展開的明細要和清單分開**：放在內縮的深底面板裡。面板底部加邊線，下一列前留間距。否則會和下一列黏在一起。
- **機器上沒有無頭瀏覽器時**：自檢做不了。交付時明說「我看不到畫面」，請使用者看預覽站。並寫出最可能出錯的地方，例如 SVG 文字重疊、封面負 margin。
- **無頭瀏覽器驗證**：`~/.cache/ms-playwright/chromium_headless_shell-*/…/chrome-headless-shell --headless --no-sandbox --screenshot=x.png --window-size=1280,2400 file:///…` 可截圖。深色模式用 `--force-dark-mode` 無效；把 `prefers-color-scheme:dark` 區塊抽出來無條件套進一份暫存 HTML 再截。
