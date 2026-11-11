#!/usr/bin/env python3
"""用 jira 使用說明產生三種風格的示範頁，每頁一種流程圖。

  Radix 極簡  + live-panel（loop 視圖，嵌 jira-loop.html）
  Ocean 深藍  + inline SVG 泳道
  Momo 計畫版 + CSS 流程框

用法：python3 build.py <jira-使用說明.html> [輸出目錄]
來源頁的 live-panel iframe 用相對路徑，換主機會失效，所以換成各版的流程圖。
內容不改寫，只換樣式與流程圖。CSS 全部內嵌，每頁單檔可發布。
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MOMO_CSS = HERE.parent.parent / "assets" / "momo.css"
MOMO_SOFT = HERE.parent.parent / "assets" / "momo-soft.css"   # 淡色立體版（只改亮色）
MOMO_NAV_JS = HERE.parent.parent / "assets" / "momo-nav.js"

LIVE_START = "<p><b>動態版</b>"
LIVE_END = "<p>動態圖是 v1.1 版，畫的是四種 Sub-task，還沒有文件。</p>"

FLOW_INTRO = "<h3>流程圖：一張 Story 從開案到關單</h3>"

# ---------- 共用：讀來源 ----------

def load_body(src: Path) -> str:
    h = src.read_text(encoding="utf-8")
    m = re.search(r"<body>(.*)</body>", h, re.S)
    if not m:
        sys.exit(f"找不到 <body>：{src}")
    body = m.group(1)
    i, j = body.find(LIVE_START), body.find(LIVE_END)
    if i < 0 or j < 0:
        sys.exit("找不到 live-panel 區塊；來源頁改版了，請更新 LIVE_START / LIVE_END")
    body = body[:i] + "@@FLOW@@" + body[j + len(LIVE_END):]
    # 5a 的表格漏了 class
    body = body.replace("<table><tr><th>等級</th>", '<table class="g"><tr><th>等級</th>')
    # 內聯的淺色列底色在深色模式會刺眼，改成 class
    # 例二表格第一欄太窄，「使用統計」會斷行
    body = body.replace('<th style="width:11%">層級</th>', '<th style="width:14%">層級</th>')
    body = body.replace('style="background:#e3f1f5"', 'class="lv-epic"')
    body = body.replace('style="background:#fff8e1"', 'class="lv-base"')
    body = body.replace('style="background:#e8f0fb"', 'class="lv-story"')
    # 按鈕連到 live-panel 的那行已隨區塊移除
    return body


def switcher(cur: str) -> str:
    items = [("radix", "Radix 極簡＋live-panel"), ("ocean", "Ocean 深藍＋SVG 泳道"), ("momo", "Momo 計畫版＋CSS 流程框")]
    out = []
    for k, label in items:
        if k == cur:
            out.append(f"<b>{label}</b>")
        else:
            out.append(f'<a href="jira-{k}.html">{label}</a>')
    return '<div class="demo-switch">示範版本：' + "　".join(out) + "</div>"


def page(title: str, css: str, body: str, tail: str = "") -> str:
    return (
        '<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>{title}</title><style>{css}</style></head><body>{body}{tail}</body></html>\n"
    )

# ---------- A. Radix 極簡 + live-panel ----------

RADIX_CSS = r"""
:root{
  --bg:#fdfdfc;--surface:#f9f9f8;--surface2:#f1f0ef;--line:#dad9d6;--line-strong:#cfceca;--mut:#63635e;--fg:#21201c;
  --acc:#f76b15;--acc-text:#cc4e00;
  --g-bg:#f4fbf6;--g-line:#adddc0;--g-text:#218358;
  --a-bg:#fefbe9;--a-line:#f3d673;--a-text:#ab6400;
  --r-bg:#fff7f7;--r-line:#fdbdbe;--r-text:#ce2c31;
  --t1-bg:#e6f4fe;--t1:#0d74ce;--t2-bg:#e6f6eb;--t2:#218358;--t3-bg:#f4f0fe;--t3:#6550b9;--t4-bg:#fff1e7;--t4:#cc4e00;--t5-bg:#f1f0ef;--t5:#63635e;
  --code-bg:#f1f0ef;
}
@media (prefers-color-scheme:dark){:root{
  --bg:#111110;--surface:#191918;--surface2:#222221;--line:#3b3a37;--line-strong:#494844;--mut:#b5b3ad;--fg:#eeeeec;
  --acc:#f76b15;--acc-text:#ffa057;
  --g-bg:#121b17;--g-line:#20573e;--g-text:#3dd68c;
  --a-bg:#1d180f;--a-line:#5c3d05;--a-text:#ffca16;
  --r-bg:#201314;--r-line:#72232d;--r-text:#ff9592;
  --t1-bg:#0d2847;--t1:#70b8ff;--t2-bg:#132d21;--t2:#3dd68c;--t3-bg:#291f43;--t3:#baa7ff;--t4-bg:#331e0b;--t4:#ffa057;--t5-bg:#2a2a28;--t5:#b5b3ad;
  --code-bg:#222221;
}}
*{box-sizing:border-box}
body{margin:0 auto;max-width:960px;padding:24px 20px 48px;background:var(--bg);color:var(--fg);
  font-family:"Noto Sans TC","PingFang TC","Microsoft JhengHei",-apple-system,sans-serif;font-size:15px;line-height:1.75}
h1{font-size:24px;line-height:1.4;margin:16px 0 12px}
h2{font-size:17px;margin:44px 0 8px;padding-top:20px;border-top:0.5px solid var(--line)}
h3{font-size:15px;margin:22px 0 6px}
a{color:var(--acc-text);text-decoration:none}a:hover{text-decoration:underline}
code{font-size:13px;background:var(--surface2);padding:1px 5px;border-radius:4px}
.demo-switch{font-size:13px;color:var(--mut);padding-bottom:10px;border-bottom:0.5px solid var(--line)}
.demo-switch a,.demo-switch b{margin-left:4px}
.box{background:var(--surface);border:0.5px solid var(--line);padding:12px 16px;border-radius:6px;margin:12px 0}
.rule{background:var(--g-bg);border:0.5px solid var(--g-line);padding:10px 14px;border-radius:6px;margin:12px 0}
.rule>b:first-child{color:var(--g-text)}
.warn{background:var(--a-bg);border:0.5px solid var(--a-line);padding:10px 14px;border-radius:6px;margin:12px 0}
.no{background:var(--r-bg);border:0.5px solid var(--r-line);padding:10px 14px;border-radius:6px;margin:12px 0}
.no>b:first-child{color:var(--r-text)}
table.g{border-collapse:collapse;width:100%;margin:8px 0;font-size:13px}
table.g th,table.g td{border:0.5px solid var(--line);padding:6px 9px;text-align:left;vertical-align:top}
table.g th{background:var(--surface);color:var(--mut);font-weight:600}
tr.lv-epic td{background:var(--surface2);font-weight:600}tr.lv-base td,tr.lv-story td{background:var(--surface)}
.tblw{overflow-x:auto}
pre{background:var(--code-bg);color:var(--fg);border:0.5px solid var(--line);padding:12px 14px;border-radius:6px;font-size:13px;line-height:1.6;overflow-x:auto;white-space:pre-wrap}
.tree{font-family:Consolas,Menlo,monospace;font-size:13px;background:var(--surface);border:0.5px solid var(--line);padding:12px 16px;border-radius:6px;white-space:pre;overflow-x:auto;line-height:1.6}
.tag{display:inline-block;font-size:13px;padding:0 7px;border-radius:4px;margin-right:4px;font-weight:600}
.b1{background:var(--t1-bg);color:var(--t1)}.b2{background:var(--t2-bg);color:var(--t2)}.b3{background:var(--t3-bg);color:var(--t3)}.b4{background:var(--t4-bg);color:var(--t4)}.b5{background:var(--t5-bg);color:var(--t5)}
ol li,ul li{margin:4px 0}.steps li{margin:8px 0}
footer{margin-top:40px;color:var(--mut);font-size:13px;border-top:0.5px solid var(--line);padding-top:10px}
.flowfig{border:0.5px solid var(--line);border-radius:6px;padding:12px;margin:10px 0;background:var(--surface)}
.flowfig iframe.lp{display:block;width:100%;aspect-ratio:1200/1360;border:0;border-radius:4px;background:#fdfdfc}
.flowfig .note{font-size:13px;color:var(--mut);margin:6px 0 0}
"""

RADIX_FLOW = FLOW_INTRO + """
<div class="flowfig"><iframe class="lp" src="jira-loop.html" title="jira 一張 Story 的生命週期（live-panel 動態圖）" loading="lazy"></iframe>
<p class="note">動態圖：live-panel 的 loop 視圖，一直在跑。路徑與輪次為示意。<a href="jira-loop.html" target="_blank">單獨開啟</a>。設定檔 jira-loop.config.json。</p></div>
"""

RADIX_TAIL = ""


def build_radix(body: str) -> str:
    b = body.replace("@@FLOW@@", RADIX_FLOW)
    b = b.replace('<table class="g">', '<div class="tblw"><table class="g">').replace("</table>", "</table></div>")
    return page("jira 使用說明（Radix 示範）", RADIX_CSS, switcher("radix") + b, RADIX_TAIL)

# ---------- B. Ocean 深藍 + inline SVG 泳道 ----------

OCEAN_CSS = r"""
:root{
  --bg:#fff;--surface:#f3f6fa;--surface2:#fafafa;--line:#d5dee8;--line-tbl:#ccc;--mut:#666;--fg:#1a1a1a;
  --acc:#1f4e79;--ok:#2e7d32;--no:#c62828;--warnc:#f0b400;--on-acc:#fff;
  --rule-bg:#e8f4ea;--warn-bg:#fff8e1;--no-bg:#fdecea;--th:#eef2f7;
  --lv-epic:#e3f1f5;--lv-base:#fff8e1;--lv-story:#e8f0fb;--pre-fg:#1f3550;
}
@media (prefers-color-scheme:dark){:root{
  --bg:#13161a;--surface:#1a2230;--surface2:#1e1e1e;--line:#2b3a4d;--line-tbl:#3a4556;--mut:#9fb0c2;--fg:#e8edf2;
  --acc:#7aa7d6;--ok:#6fbf73;--no:#e57373;--warnc:#e0b84a;--on-acc:#13161a;
  --rule-bg:#16261a;--warn-bg:#2a2410;--no-bg:#2c1718;--th:#1d2633;
  --lv-epic:#15262c;--lv-base:#2a2410;--lv-story:#17223a;--pre-fg:#cfe0f2;
}}
*{box-sizing:border-box}
body{font-family:"Noto Sans TC","Microsoft JhengHei",Arial,sans-serif;margin:0;
  background:var(--bg);color:var(--fg);line-height:1.75;font-size:15px}
html{scroll-behavior:smooth}
.page{max-width:1000px;margin:0 auto;padding:16px 20px 24px}
/* 章節導覽列：鋪滿畫面寬、黏頂；按鈕與內文同寬置中；目前章節深藍底白字 */
nav.mnav{position:sticky;top:0;z-index:9;background:color-mix(in srgb,var(--bg) 94%,transparent);backdrop-filter:blur(6px);border-bottom:1px solid var(--line)}
nav.mnav .mw{max-width:1000px;margin:0 auto;padding:8px 20px;display:flex;gap:4px;flex-wrap:wrap;font-size:13px}
nav.mnav a{color:var(--mut);text-decoration:none;padding:2px 9px;border-radius:4px;border:1px solid transparent;white-space:nowrap}
nav.mnav a b{color:var(--acc);margin-right:3px}
nav.mnav a:hover{background:var(--surface);color:var(--fg)}
nav.mnav a.on{background:var(--acc);color:var(--on-acc);font-weight:700}
nav.mnav a.on b{color:var(--on-acc)}
h1{font-size:24px;border-bottom:3px solid var(--acc);padding-bottom:6px}
h2{font-size:19px;color:var(--acc);margin-top:44px;border-left:6px solid var(--acc);padding-left:10px}
h3{font-size:15.5px;margin:20px 0 6px;color:var(--fg)}
a{color:var(--acc)}
.demo-switch{font-size:13px;color:var(--mut);background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:6px 12px}
.demo-switch a,.demo-switch b{margin-left:4px}
.box{background:var(--surface);border:1px solid var(--line);padding:12px 16px;border-radius:6px;margin:10px 0}
.rule{background:var(--rule-bg);border-left:5px solid var(--ok);padding:8px 14px;margin:10px 0}
.warn{background:var(--warn-bg);border-left:5px solid var(--warnc);padding:8px 14px;margin:10px 0}
.no{background:var(--no-bg);border-left:5px solid var(--no);padding:8px 14px;margin:10px 0}
table.g{border-collapse:collapse;width:100%;margin:8px 0}
table.g th,table.g td{border:1px solid var(--line-tbl);padding:6px 9px;text-align:left;vertical-align:top}
table.g th{background:var(--th)}
tr.lv-epic td{background:var(--lv-epic)}tr.lv-base td{background:var(--lv-base)}tr.lv-story td{background:var(--lv-story)}
.tblw{overflow-x:auto}
pre{background:var(--surface);color:var(--pre-fg);border:1px solid var(--line);border-left:4px solid var(--acc);border-radius:4px;padding:8px 12px;font-size:13px;line-height:1.55;overflow-x:auto;white-space:pre-wrap}
pre.code{background:#1e1e1e;color:#e6e6e6;border:0;border-radius:6px;padding:12px 14px}
hr.sec{border:0;border-top:1px solid var(--line);margin:44px 0 0}
hr.sec+h2{margin-top:24px}
.tree{font-family:Consolas,Menlo,monospace;font-size:13.5px;background:var(--surface2);border:1px solid var(--line);padding:12px 16px;border-radius:6px;white-space:pre;overflow-x:auto;line-height:1.6}
.tag{display:inline-block;font-size:12px;padding:0 7px;border-radius:3px;margin-right:4px;font-weight:bold;color:#fff}
.b1{background:#1f4e79}.b2{background:#2e7d32}.b3{background:#6a1b9a}.b4{background:#bf360c}.b5{background:#555}
ol li,ul li{margin:4px 0}.steps li{margin:8px 0}
footer{margin-top:40px;color:var(--mut);font-size:13px;border-top:1px solid var(--line-tbl);padding-top:10px}
.fig{background:#fff;border:1px solid var(--line);border-radius:6px;padding:8px;overflow-x:auto;margin:10px 0}
.fig svg{display:block;width:100%;min-width:720px;height:auto}
.fig-note{font-size:13px;color:var(--mut);margin:4px 0 0}
"""

# 泳道：主管 / 執行者 / 簽收者（對方部門）。座標手算，viewBox 1000x350。
OCEAN_SVG = """
<div class="fig"><svg viewBox="0 0 1000 350" role="img" aria-label="一張 Story 的泳道流程：主管開案，執行者量測、實作、自測，簽收者在服務台關單，主管關單"
 style="font-family:'Noto Sans TC','Microsoft JhengHei',Arial,sans-serif">
<defs>
 <marker id="oc-main" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#1f4e79"/></marker>
 <marker id="oc-back" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#c62828"/></marker>
</defs>
<rect width="1000" height="350" fill="#fff"/>
<!-- 泳道 -->
<rect x="10" y="20" width="980" height="96" rx="6" fill="#f3f6fa" stroke="#d5dee8"/>
<rect x="10" y="126" width="980" height="96" rx="6" fill="#e8f4ea" stroke="#c5e1c8"/>
<rect x="10" y="232" width="980" height="96" rx="6" fill="#fff8e1" stroke="#f3dfa0"/>
<rect x="10" y="20" width="84" height="96" rx="6" fill="#1f4e79"/>
<rect x="10" y="126" width="84" height="96" rx="6" fill="#2e7d32"/>
<rect x="10" y="232" width="84" height="96" rx="6" fill="#b07800"/>
<text x="52" y="73" text-anchor="middle" font-size="15" font-weight="700" fill="#fff">主管</text>
<text x="52" y="179" text-anchor="middle" font-size="15" font-weight="700" fill="#fff">執行者</text>
<text x="52" y="276" text-anchor="middle" font-size="15" font-weight="700" fill="#fff">簽收者</text>
<text x="52" y="296" text-anchor="middle" font-size="11" fill="#fff">對方部門</text>
<!-- 節點：寬 150、高 56 -->
<rect x="110" y="40" width="150" height="56" rx="6" fill="#fff" stroke="#1f4e79" stroke-width="1.6"/>
<text x="185" y="64" text-anchor="middle" font-size="14" font-weight="700" fill="#1a1a1a">開案</text>
<text x="185" y="83" text-anchor="middle" font-size="11.5" fill="#555">八項必填、定 P0–P4</text>

<rect x="290" y="146" width="150" height="56" rx="6" fill="#fff" stroke="#2e7d32" stroke-width="1.6" stroke-dasharray="5 4"/>
<text x="365" y="170" text-anchor="middle" font-size="14" font-weight="700" fill="#1a1a1a">基準量測</text>
<text x="365" y="189" text-anchor="middle" font-size="11.5" fill="#555">現值待量才建</text>

<rect x="470" y="146" width="150" height="56" rx="6" fill="#fff" stroke="#2e7d32" stroke-width="1.6"/>
<text x="545" y="170" text-anchor="middle" font-size="14" font-weight="700" fill="#1a1a1a">任務、文件</text>
<text x="545" y="189" text-anchor="middle" font-size="11.5" fill="#555">一件事一張、文件交接</text>

<rect x="650" y="146" width="150" height="56" rx="6" fill="#fff" stroke="#2e7d32" stroke-width="1.6"/>
<text x="725" y="170" text-anchor="middle" font-size="14" font-weight="700" fill="#1a1a1a">留【自測】</text>
<text x="725" y="189" text-anchor="middle" font-size="11.5" fill="#555">同量法、附件掛上</text>

<rect x="650" y="252" width="150" height="56" rx="6" fill="#fff" stroke="#b07800" stroke-width="1.6"/>
<text x="725" y="276" text-anchor="middle" font-size="14" font-weight="700" fill="#1a1a1a">請簽收單</text>
<text x="725" y="295" text-anchor="middle" font-size="11.5" fill="#555">在自己的服務台關單</text>

<rect x="830" y="40" width="150" height="56" rx="6" fill="#fff" stroke="#1f4e79" stroke-width="1.6"/>
<text x="905" y="64" text-anchor="middle" font-size="14" font-weight="700" fill="#1a1a1a">關單</text>
<text x="905" y="83" text-anchor="middle" font-size="11.5" fill="#555">SC 結果值對目標值</text>
<!-- 箭頭 -->
<path d="M185 96 V174 H286" fill="none" stroke="#1f4e79" stroke-width="1.6" marker-end="url(#oc-main)"/>
<line x1="440" y1="174" x2="466" y2="174" stroke="#1f4e79" stroke-width="1.6" marker-end="url(#oc-main)"/>
<line x1="620" y1="174" x2="646" y2="174" stroke="#1f4e79" stroke-width="1.6" marker-end="url(#oc-main)"/>
<line x1="725" y1="202" x2="725" y2="248" stroke="#1f4e79" stroke-width="1.6" marker-end="url(#oc-main)"/>
<path d="M800 280 H905 V100" fill="none" stroke="#1f4e79" stroke-width="1.6" marker-end="url(#oc-main)"/>
<path d="M650 280 H545 V206" fill="none" stroke="#c62828" stroke-width="1.6" stroke-dasharray="5 4" marker-end="url(#oc-back)"/>
<text x="597" y="272" text-anchor="middle" font-size="11.5" font-weight="700" fill="#c62828">沒通過</text>
<text x="193" y="150" font-size="11" fill="#1f4e79">指派執行者</text>
</svg></div>
<p class="fig-note">虛線框是條件式 Sub-task。方案評估、使用統計也是條件式，條件見第 3 節。</p>
"""


OCEAN_NAV_LABEL = {"14.": "不計入情況"}   # 太長的章節名改短名，不截斷


def ocean_nav(b: str):
    """替每個 h2 加 id，回傳 (加好 id 的內文, 導覽列 HTML)。"""
    links = []
    def add_id(m):
        num, title = m.group(1), m.group(2)
        sid = "sec-" + num.rstrip(".")
        label = OCEAN_NAV_LABEL.get(num) or re.sub(r"（.*?）", "", title.split("：")[0]).strip()
        links.append(f'<a href="#{sid}"><b>{num.rstrip(".")}</b>{label}</a>')
        return f'<h2 id="{sid}">{num} {title}</h2>'
    b = re.sub(r"<h2>(\S+?) (.*?)</h2>", add_id, b)
    return b, '<nav class="mnav"><div class="mw">' + "".join(links) + "</div></nav>"


def build_ocean(body: str) -> str:
    b = body.replace("@@FLOW@@", FLOW_INTRO + OCEAN_SVG)
    # 只有 Markdown 原稿算程式碼，維持深色；其餘 pre 是範例與公式，改淺色
    code_anchor = "的描述（Markdown 原稿，節錄）：</p>\n<pre>"
    if b.count(code_anchor) != 1:
        sys.exit("找不到 Markdown 原稿區塊；來源頁改版了，請更新 code_anchor")
    b = b.replace(code_anchor, code_anchor[:-5] + '<pre class="code">')
    # 章節之間加分隔線（第一節除外）
    b = b.replace("<h2>", '<hr class="sec"><h2>').replace('<hr class="sec"><h2>', "<h2>", 1)
    b = b.replace('<table class="g">', '<div class="tblw"><table class="g">').replace("</table>", "</table></div>")
    b, nav = ocean_nav(b)
    head, sep, rest = b.partition("</h1>")   # 大標題在導覽列上面，和 Momo 的封面 → 導覽列同順序
    if not sep:
        sys.exit("找不到 </h1>；來源頁改版了")
    return page("jira 使用說明（Ocean 示範）", OCEAN_CSS,
                '<div class="page" style="padding-bottom:0">' + switcher("ocean") + head + sep + "</div>" + nav + '<div class="page">' + rest + "</div>",
                "<script>" + MOMO_NAV_JS.read_text(encoding="utf-8") + "</script>")

# ---------- C. Momo 計畫版 + CSS 流程框 ----------

MOMO_EXTRA = r"""
.demo-switch{max-width:1120px;margin:0 auto;padding:10px 24px 0;font-size:13px;color:var(--fg2)}
.demo-switch a,.demo-switch b{margin-left:4px}
.blk h2{display:flex;align-items:baseline;gap:8px}
.blk .card{font-size:14.5px}
.tree{font-family:Consolas,Menlo,monospace;font-size:13px;background:var(--surface2);border-radius:10px;padding:14px 18px;white-space:pre;overflow-x:auto;line-height:1.6}
.tblw{overflow-x:auto}
tr.lv-epic td{background:var(--surface2);font-weight:700}tr.lv-base td{background:var(--warn-bg)}tr.lv-story td{background:var(--bg)}
code{font-size:13px;background:var(--surface2);padding:1px 5px;border-radius:4px}
.steps li{margin:8px 0}
footer{max-width:1120px;margin:0 auto;padding:0 24px 40px;color:var(--mut);font-size:12.5px}
.flow-note{font-size:13px;color:var(--fg2);margin:4px 0 0}
.flow.seven .bx{min-height:84px}
@media(max-width:800px){.blk{padding:20px 18px}}
"""

MOMO_FLOW = FLOW_INTRO + """
<div class="flow seven">
  <div class="bx dark"><b>開案</b><span>八項必填</span></div><div class="arr">→</div>
  <div class="bx opt"><b>基準量測</b><span>現值待量才建</span></div><div class="arr">→</div>
  <div class="bx opt"><b>方案評估</b><span>多個做法才建</span></div><div class="arr">→</div>
  <div class="bx"><b>任務</b><span>一件事一張</span></div><div class="arr">→</div>
  <div class="bx"><b>文件</b><span>交接給接手者</span></div><div class="arr">→</div>
  <div class="bx"><b>簽收</b><span>對方服務台關單</span></div><div class="arr">→</div>
  <div class="bx good"><b>關單</b><span>SC 結果對目標</span></div>
</div>
<p class="flow-note">虛線框是條件式 Sub-task。reach-wide 的 Story 另建使用統計，上線後 30 天撈。</p>
"""

# 章節分組：chip 名稱、標題、包含的 h2 編號前綴
MOMO_GROUPS = [
    ("為什麼", "讓工單本身就是 PACE 紀錄", ["1."]),
    ("結構", "一張 Story 長什麼樣、要建哪些 Sub-task", ["2.", "3.", "4."]),
    ("怎麼寫", "成功指標、優先度、開單、描述、留言", ["5.", "5a.", "6.", "7.", "8.", "13."]),
    ("收尾", "送簽收、使用統計、關單", ["9.", "10.", "11."]),
    ("參考", "其他例子、扣分情況、常見問題", ["12.", "14.", "15."]),
]


def build_momo(body: str) -> str:
    css = MOMO_CSS.read_text(encoding="utf-8") + MOMO_SOFT.read_text(encoding="utf-8") + MOMO_EXTRA
    b = body.replace("@@FLOW@@", MOMO_FLOW)
    # 元件對應
    b = b.replace('<table class="g">', '<div class="tblw"><table class="t">').replace("</table>", "</table></div>")
    b = re.sub(r'<div class="box">', '<div class="card">', b)
    b = re.sub(r'<div class="rule">', '<div class="card ok">', b)
    b = re.sub(r'<div class="warn">', '<div class="card warn">', b)
    b = re.sub(r'<div class="no">', '<div class="card no">', b)
    for old, new in [("b1", "o1"), ("b2", "o3"), ("b3", "o4"), ("b4", "o2"), ("b5", "st-todo")]:
        b = b.replace(f'<span class="tag {old}">', f'<span class="pill {new}">')

    footer = ""
    fm = re.search(r"<footer>.*?</footer>", b, re.S)
    if fm:
        footer, b = fm.group(0), b.replace(fm.group(0), "")

    h1m = re.search(r"<h1>(.*?)</h1>", b, re.S)
    title = h1m.group(1)
    main_t, _, sub_t = title.partition("｜")
    b = b.replace(h1m.group(0), "")
    intro_end = b.find("<h2>")
    intro, rest = b[:intro_end], b[intro_end:]

    # 依 h2 切段
    parts = re.split(r"(?=<h2>)", rest)
    sections = {}
    for p in parts:
        m = re.match(r"<h2>(\S+?)\s", p)
        if m:
            sections[m.group(1)] = p
    used = set()
    out = [f'<div class="cover"><h1>{main_t}</h1><p>{sub_t}</p></div>']
    colors = ["var(--fg2)", "#1b4f9c", "#c2410c", "#0a6a0a", "#5b3a9c", "#0e7490"]
    items = [("g-intro", "總覽")] + [(f"g{i}", chip) for i, (chip, _, _) in enumerate(MOMO_GROUPS)]
    nav = "".join(f'<a href="#{k}" style="--c:{colors[n % len(colors)]}"><i></i>{t}</a>' for n, (k, t) in enumerate(items))
    out.append(f'<nav class="mnav"><div class="mw">{nav}</div></nav>')
    out.append('<main>')
    out.append(f'<section id="g-intro"><div class="divider"><span>總覽</span>它做什麼、不做什麼</div><div class="blk">{intro}</div></section>')
    for i, (chip, head, keys) in enumerate(MOMO_GROUPS):
        out.append(f'<section id="g{i}"><div class="divider"><span>{chip}</span>{head}</div>')
        for k in keys:
            if k not in sections:
                sys.exit(f"找不到第 {k} 節；來源頁改版了，請更新 MOMO_GROUPS")
            out.append(f'<div class="blk">{sections[k]}</div>')
            used.add(k)
        out.append("</section>")
    missing = set(sections) - used
    if missing:
        sys.exit(f"有章節沒分到組：{sorted(missing)}")
    out.append("</main>")
    out.append(footer)
    html = "".join(out)
    return page("jira 使用說明（Momo 示範）", css, switcher("momo") + html,
                "<script>" + MOMO_NAV_JS.read_text(encoding="utf-8") + "</script>")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1])
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE
    body = load_body(src)
    for name, fn in [("radix", build_radix), ("ocean", build_ocean), ("momo", build_momo)]:
        p = out / f"jira-{name}.html"
        p.write_text(fn(body), encoding="utf-8")
        print(f"wrote {p} ({p.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
