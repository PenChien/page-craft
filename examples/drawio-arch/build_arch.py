#!/usr/bin/env python3
"""drawio 轉檔範例：把一張網路架構 drawio 重繪成 Momo 風格的 inline SVG 線路圖。
格式來源：參考報告 報告的「線路架構」章（虛線分區框、設備框、介面框、彩色線、線速標籤）。
步驟見 ../../references/drawio.md。
用法：python3 build_arch.py <輸出.html>
可重用的部分：Fig 類別（zone / dev / port / line / text）、tbl()、sw()、own()。換圖時只改「圖 1–3」三段座標。"""
import sys, os

OUT = sys.argv[1] if len(sys.argv) > 1 else 'demo-arch.html'
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'assets')
css = '<style>\n' + open(os.path.join(ASSETS, 'momo.css'), encoding='utf-8').read() + '\n</style>'
navjs = '<script>\n' + open(os.path.join(ASSETS, 'momo-nav.js'), encoding='utf-8').read() + '\n</script>'
fonts = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&family=JetBrains+Mono:wght@400;600&display=swap">')

C = dict(g='#1baf7a', o='#eb6834', p='#6250d6', b='#1b4f9c', k='#52514e', u='#8a8985')
OWN = {'S': ('#fff6dc', '#c99a2e'), 'M': ('#eaf1fb', '#5b7fb5'), '': ('#fff', '#52514e')}


class Fig:
    def __init__(s, w, h, label):
        s.w, s.h, s.label, s.el = w, h, label, []

    def zone(s, x, y, w, h, title, blue=False):
        f, st = ('#f4f8fd', C['b']) if blue else ('#fafafa', C['u'])
        s.el.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{f}" stroke="{st}" stroke-dasharray="5 4"/>'
                    f'<text class="t3" x="{x + w / 2}" y="{y + 20}" text-anchor="middle" style="fill:{st}">{title}</text>')

    def dev(s, x, y, w, h, t1, t2='', own='', ty=None):
        f, st = OWN[own]
        cy = y + h / 2 if ty is None else ty
        s.el.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{f}" stroke="{st}" stroke-width="1.6"/>')
        if t2:
            s.el.append(f'<text class="t1" x="{x + w / 2}" y="{cy - 3}" text-anchor="middle">{t1}</text>'
                        f'<text class="t2" x="{x + w / 2}" y="{cy + 13}" text-anchor="middle">{t2}</text>')
        else:
            s.el.append(f'<text class="t1" x="{x + w / 2}" y="{cy + 4}" text-anchor="middle">{t1}</text>')
        if own:
            s.el.append(f'<text class="t6" x="{x + w - 5}" y="{y + 11}" text-anchor="end" style="fill:{st}">{own}</text>')

    def port(s, x, y, w, h, text, c):
        tint = {'g': '#f3faf5', 'o': '#fef5ef', 'p': '#f6f5fd', 'k': '#f5f5f4'}[c]
        dark = {'g': '#0f7d55', 'o': '#b4471a', 'p': '#4a3aa7', 'k': '#3a3936'}[c]
        s.el.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{tint}" stroke="{C[c]}" stroke-width="1.4"/>'
                    f'<text class="t3" x="{x + w / 2}" y="{y + h / 2 + 4.5}" text-anchor="middle" style="fill:{dark}">{text}</text>')

    def line(s, pts, c, lab=None, lab_at=None, start=False, end=True, dash=False):
        d = ' '.join(f'{x},{y}' for x, y in pts)
        mk = (f' marker-end="url(#am-{c})"' if end else '') + (f' marker-start="url(#am-{c})"' if start else '')
        da = ' stroke-dasharray="3 3"' if dash else ''
        op = ' opacity=".55"' if dash and c != 'u' else ''
        s.el.append(f'<polyline points="{d}" fill="none" stroke="{C[c]}" stroke-width="1.8"{da}{op}{mk}/>')
        if lab:
            if lab_at is None:
                (x1, y1), (x2, y2) = pts[0], pts[1]
                lab_at = ((x1 + x2) / 2, min(y1, y2) - 7)
            s.el.append(f'<text class="t4" x="{lab_at[0]}" y="{lab_at[1]}" text-anchor="middle">{lab}</text>')

    def text(s, x, y, t, cls='t2', c=None, anchor='start'):
        st = f' style="fill:{C[c]}"' if c else ''
        s.el.append(f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}"{st}>{t}</text>')

    def svg(s):
        mk = ''.join(f'<marker id="am-{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
                     f'orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{v}"/></marker>' for k, v in C.items())
        return (f'<div class="fig arch"><svg viewBox="0 0 {s.w} {s.h}" role="img" aria-label="{s.label}"><defs>{mk}</defs>'
                + ''.join(s.el) + '</svg></div>')


# ---------- 圖 1：正式環境（drawio 第 1 頁左半） ----------
f1 = Fig(1200, 460, '主站點的對外流量、API 與管理線路，以及與備援站點、辦公室的互連')
f1.zone(10, 14, 124, 432, '網際網路')
f1.zone(146, 14, 692, 432, '主站點')
f1.zone(860, 14, 330, 200, '備援站點', blue=True)
f1.zone(860, 226, 330, 220, '辦公室')
# 網際網路
f1.dev(22, 56, 100, 300, '使用者', 'Web · App', ty=206)
f1.text(160, 58, '對外 (綠)　使用者 → WAF → 負載平衡器 → Web', 't5', 'g')
f1.text(160, 78, 'API (橘)　負載平衡器 → API', 't5', 'o')
# 入口
f1.dev(180, 150, 96, 60, 'WAF', '', 'M')
f1.dev(306, 150, 96, 60, '負載平衡器', '', 'M')
# App 叢集 (主機框 + 服務)
f1.el.append(f'<rect x="450" y="90" width="140" height="230" rx="10" fill="{OWN["S"][0]}" stroke="{OWN["S"][1]}" stroke-width="1.6"/>')
f1.text(520, 104, 'App 叢集', 't1', anchor='middle')
f1.text(586, 100, 'S', 't6', anchor='end')
f1.el[-1] = f1.el[-1].replace('class="t6"', f'class="t6" style="fill:{OWN["S"][1]}"')
f1.port(460, 112, 120, 28, 'Web ①②', 'g')
f1.port(460, 170, 120, 28, 'API ③④', 'o')
f1.port(460, 228, 120, 28, '排程 ⑤', 'k')
f1.text(520, 300, 'SSH ⑥ · Agent ⑦', 't2', anchor='middle')
# 資料層
f1.dev(640, 106, 96, 44, '資料庫', 'PostgreSQL', 'S')
f1.dev(640, 176, 96, 44, '快取', 'Redis', 'S')
# 線：對外與 API
f1.line([(122, 180), (180, 180)], 'g', 'HTTPS')
f1.line([(276, 180), (306, 180)], 'g')
f1.line([(402, 160), (426, 160), (426, 126), (460, 126)], 'g', '1G', lab_at=(414, 120))
f1.line([(402, 184), (460, 184)], 'o', '1G', lab_at=(431, 200))
# 主機互連
f1.line([(590, 128), (640, 128)], 'k', '10G', lab_at=(615, 122), start=True)
f1.line([(590, 198), (640, 198)], 'k', '10G', lab_at=(615, 192), start=True)
# 管理 (紫) → 管理交換器
f1.text(160, 372, '管理 (紫)', 't5', 'p')
f1.dev(306, 340, 96, 60, '管理交換器', '', 'M')
f1.dev(640, 350, 96, 44, '跳板機', 'Bastion', 'S')
f1.line([(520, 320), (520, 358), (402, 358)], 'p', '1G', lab_at=(461, 352))
f1.line([(640, 382), (402, 382)], 'p', 'SSH', lab_at=(600, 376))
# 站點互連 (藍)
f1.line([(736, 128), (880, 128)], 'b', '串流複寫', lab_at=(808, 121))
f1.line([(354, 400), (354, 430), (846, 430), (846, 325), (880, 325)], 'b', 'VPN 通道', lab_at=(600, 424), start=True)
f1.text(160, 424, '站點互連 (藍)', 't5', 'b')
# 備援站點
f1.dev(880, 106, 96, 44, '資料庫 (備)', 'PostgreSQL', 'S')
f1.dev(1070, 106, 104, 44, 'App 叢集 (備)', '平時不接流量', 'S')
f1.dev(1070, 162, 104, 40, '備份儲存', '', 'M')
f1.line([(976, 128), (1070, 128)], 'k', '10G', lab_at=(1023, 122), start=True)
f1.line([(928, 150), (928, 182), (1070, 182)], 'u', '每日備份', lab_at=(1000, 176), dash=True)
# 辦公室
f1.dev(880, 300, 96, 50, '防火牆', '', 'M')
f1.dev(1070, 300, 104, 50, '遠端人員', 'VPN')
f1.dev(1070, 380, 104, 44, '監控主機', 'Grafana', 'S')
f1.line([(1070, 325), (976, 325)], 'p', 'VPN')
f1.line([(928, 350), (928, 402), (1070, 402)], 'p', '1G', lab_at=(1000, 396))

# ---------- 圖 2：測試環境（drawio 第 1 頁右半） ----------
f2 = Fig(1116, 392, '測試環境：測試流量與回報線路、管理網路經防火牆接 Internet')
f2.zone(10, 14, 124, 364, '開發端')
f2.zone(146, 14, 720, 364, '測試站點')
f2.zone(878, 14, 228, 364, '外部連線')
f2.dev(22, 56, 100, 220, 'CI', '自動 · 手動測試', ty=166)
f2.text(160, 58, '測試流量 (綠)　a、b 兩條', 't5', 'g')
f2.text(160, 188, '回報 (橘)　c', 't5', 'o')
f2.dev(160, 196, 96, 50, '防火牆', '', 'M')
f2.dev(306, 64, 96, 200, '測試閘道', '流量、回報共用', 'M', ty=150)
# 測試主機 主機框
f2.el.append(f'<rect x="462" y="56" width="124" height="236" rx="10" fill="{OWN["S"][0]}" stroke="{OWN["S"][1]}" stroke-width="1.6"/>')
f2.text(524, 74, '測試主機', 't1', anchor='middle')
f2.port(472, 82, 104, 28, 'a Web', 'g')
f2.port(472, 128, 104, 28, 'b API', 'g')
f2.port(472, 207, 104, 28, 'c 回報', 'o')
f2.text(524, 270, 'd mgmt · e Agent', 't2', anchor='middle')
f2.dev(632, 140, 96, 50, 'Mock 服務', 'f mgmt · g Agent', 'S')
# 測試流量 (穿過測試閘道)
for y, sp in ((96, '1G 電'), (142, '10G 光')):
    f2.line([(122, y), (306, y)], 'g')
    f2.line([(306, y), (402, y)], 'g', end=False, dash=True)
    f2.line([(402, y), (472, y)], 'g', sp, lab_at=(437, y - 7))
# 回報 c → 測試閘道 → 防火牆 → CI
f2.line([(472, 221), (402, 221)], 'o', '10G 光', lab_at=(437, 214))
f2.line([(306, 221), (256, 221)], 'o', '1G 電', lab_at=(281, 214))
f2.line([(160, 221), (122, 221)], 'o')
# 測試主機 – Mock 服務
f2.line([(586, 165), (632, 165)], 'k', end=False)
# 管理 (紫)
f2.text(160, 300, '管理 (紫)', 't5', 'p')
f2.dev(632, 300, 96, 50, '交換器', '管理', 'M')
f2.dev(756, 300, 96, 50, '防火牆', '', 'M')
f2.line([(524, 292), (524, 325), (632, 325)], 'p', start=True)
f2.line([(680, 190), (680, 300)], 'p', start=True)
f2.line([(728, 325), (756, 325)], 'p', start=True)
f2.dev(896, 300, 96, 50, 'Internet', '')
f2.line([(896, 325), (852, 325)], 'p')
f2.dev(994, 200, 104, 60, '協力廠商', '固定 IP', ty=232)
f2.line([(1046, 260), (1046, 280), (944, 280), (944, 300)], 'p')

# ---------- 圖 3：訂單系統（drawio 第 2 頁） ----------
f3 = Fig(1116, 300, '訂單系統：使用者經 API 閘道、訂單服務、訊息佇列、出口閘道到物流夥伴')
f3.zone(10, 14, 280, 272, '使用者端')
f3.zone(304, 14, 446, 272, '訂單平台')
f3.zone(970, 14, 136, 272, '物流夥伴')
f3.dev(30, 100, 96, 50, '使用者')
f3.dev(170, 100, 96, 50, 'API 閘道')
f3.dev(340, 100, 96, 50, '訂單服務')
f3.dev(620, 100, 96, 50, '訊息佇列')
f3.dev(468, 200, 124, 50, '排程器')
f3.dev(820, 100, 96, 50, '出口閘道')
f3.dev(990, 56, 96, 210, '物流夥伴', ty=161)
for a, b in ((126, 170), (266, 340), (436, 620), (716, 820), (916, 990)):
    f3.line([(a, 125), (b, 125)], 'k')
f3.line([(990, 76), (388, 76), (388, 100)], 'k')
f3.line([(388, 150), (388, 225), (468, 225)], 'k', start=True)
f3.line([(668, 150), (668, 225), (592, 225)], 'k', start=True)


def tbl(head, rows):
    h = ''.join(f'<th>{x}</th>' for x in head)
    r = ''.join('<tr>' + ''.join(f'<td>{x}</td>' for x in row) + '</tr>' for row in rows)
    return f'<div class="tbl"><table class="t"><tr>{h}</tr>{r}</table></div>'


def sw(c):
    return f'<span class="sw" style="background:{C[c]}"></span>'


def own(o, t):
    f, s = OWN[o]
    return f'<span class="sw" style="background:{f};outline:1.5px solid {s}"></span>{t}'


li = lambda x: f'<span class="li">{x}</span>'
legend = ('<p class="arch-legend">線色＝用途：' + ''.join(li(x) for x in (sw("g") + '對外流量', sw("o") + 'API / 回報', sw("p") + '管理',
          sw("b") + '站點互連', sw("k") + '主機互連', '虛線＝備份'))
          + '<br>框色＝設備歸屬：' + li(own("S", "S 自建")) + li(own("M", "M 代管")) + '</p>')

t1 = tbl(['線路', '經過的設備', '線速', '方向'], [
    [f'{sw("g")}對外', '使用者 → WAF → 負載平衡器 → App 叢集 Web ①②', '1G', '單向'],
    [f'{sw("o")}API', '負載平衡器 → App 叢集 API ③④', '1G', '單向'],
    [f'{sw("k")}主機互連', 'App 叢集 ↔ 資料庫、快取；資料庫 (備) ↔ App 叢集 (備)', '10G', '雙向'],
    [f'{sw("p")}管理', 'App 叢集 SSH ⑥、Agent ⑦ → 管理交換器；跳板機 → 管理交換器', '1G', '單向'],
    [f'{sw("b")}站點互連', '資料庫 → 資料庫 (備)，串流複寫', '10G', '單向'],
    [f'{sw("b")}主站點 → 辦公室', '管理交換器 ↔ 防火牆 (辦公室)，VPN 通道；遠端人員 → 防火牆；防火牆 → 監控主機', '1G', '雙向'],
    [f'{sw("u")}備份', '資料庫 (備) → 備份儲存', '每日一次', '單向'],
])
t2 = tbl(['線路', '經過的設備', '線速'], [
    [f'{sw("g")}測試流量 a', 'CI → 測試閘道 → 測試主機 a', '測試閘道到測試主機：1G 電'],
    [f'{sw("g")}測試流量 b', 'CI → 測試閘道 → 測試主機 b', '測試閘道到測試主機：10G 光'],
    [f'{sw("o")}回報 c', '測試主機 c → 測試閘道 → 防火牆 → CI', '測試主機到閘道：10G 光；閘道到防火牆：1G 電'],
    [f'{sw("p")}管理', '測試主機 d (mgmt)、e (Agent)；Mock 服務 f (mgmt)、g (Agent) → 交換器 (管理) ↔ 防火牆 ← Internet ← 協力廠商', '原圖未標'],
])

html = f'''<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>範例線路架構</title>
{fonts}
{css}
<style>
.fig.arch{{margin:10px 0 8px}}
.arch text{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang TC","Microsoft JhengHei","Noto Sans TC",sans-serif}}
.arch .t1{{fill:#0b0b0b;font-size:12.5px;font-weight:800}}
.arch .t2{{fill:#52514e;font-size:10.5px}}
.arch .t3{{font-size:12.5px;font-weight:700}}
.arch .t4{{fill:#1f2329;font-size:10.5px;font-weight:600;font-family:"JetBrains Mono",ui-monospace,monospace}}
.arch .t5{{font-size:12px;font-weight:800}}
.arch .t6{{font-size:9.5px;font-weight:800}}
.sw{{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:6px;vertical-align:-1px}}
.arch-legend{{font-size:12.5px;color:var(--fg2);margin:4px 0 0}}
.arch-legend .li{{white-space:nowrap;margin-right:14px}}
.tbl{{overflow-x:auto}}
.card.arch-note{{margin-top:14px}}
</style>
</head>
<body>
<div class="cover"><h1>範例線路架構</h1><p>依 demo-network.drawio 重繪｜2026-11-11</p></div>
<nav class="mnav"><div class="mw"><a href="#s-arch" style="--c:#0e8a8a"><i></i>正式環境</a><a href="#s-uat" style="--c:#1b4f9c"><i></i>測試環境</a><a href="#s-sys" style="--c:#5b3a9c"><i></i>訂單系統</a></div></nav>
<main>
<section id="s-arch">
<div class="divider"><span>線路架構</span>主站點與備援站點、辦公室<span class="pill o3">原圖第 1 頁</span></div>
<div class="blk">
<p class="sub">依原圖重繪，只換版面，不改連線。<b>由左到右：網際網路 → 主站點 (WAF、負載平衡器、App 叢集) → 備援站點、辦公室</b>；<b>管理交換器同時收 App 叢集與跳板機的管理線，並以 VPN 通道接辦公室</b>。</p>
{legend}
{f1.svg()}
{t1}
<div class="card warn arch-note"><b>注意</b><ul><li>原圖右下的區塊沒有標名，本圖暫稱「辦公室」。</li><li>線速照原圖線上的標註；原圖沒標的管理線 (SSH、Agent) 依同區交換器規格標 1G。</li><li>排程 ⑤ 在原圖沒有對外連線，只在叢集內部執行。</li></ul></div>
<p class="muted">資料來源：demo-network.drawio，第 1 頁「Phase 1」。框色沿用原圖：黃＝S 自建、藍＝M 代管。</p>
</div>
</section>

<section id="s-uat">
<div class="divider"><span>線路架構</span>測試環境<span class="pill o1">原圖第 1 頁右側</span></div>
<div class="blk">
<p class="sub">測試環境與正式環境沒有連線。<b>測試流量 a、b 從 CI 進測試主機；回報 c 經防火牆回 CI</b>；<b>管理網路經防火牆、Internet 給協力廠商</b>。</p>
{legend}
{f2.svg()}
{t2}
<div class="card warn arch-note"><b>注意</b><ul><li>原圖測試流量 a、b 兩條線穿過測試閘道框，沒有標示是否經過該設備；本圖照原圖畫成穿過 (框內虛線)。</li><li>測試主機與 Mock 服務之間的連線，原圖沒有標用途與線速。</li></ul></div>
<p class="muted">資料來源：demo-network.drawio，第 1 頁「測試站點」區。</p>
</div>
</section>

<section id="s-sys">
<div class="divider"><span>系統架構</span>訂單系統<span class="pill o4">原圖第 2 頁</span></div>
<div class="blk">
<p class="sub">使用者下單經 API 閘道、訂單服務、訊息佇列、出口閘道到物流夥伴；<b>物流夥伴另有一條線回訂單服務 (狀態回報)</b>；<b>排程器與訂單服務、訊息佇列各有雙向連線</b>。</p>
{f3.svg()}
<div class="card warn arch-note"><b>注意</b><ul><li>原圖第 2 頁沒有標線路用途與線速，本圖全部用灰線。</li><li>使用者後面與訊息佇列後面兩個設備在原圖只有圖示：依圖示分別是 API 閘道與出口閘道。</li></ul></div>
<p class="muted">資料來源：demo-network.drawio，第 2 頁。</p>
</div>
</section>
</main>
{navjs}
</body>
</html>
'''
open(OUT, 'w', encoding='utf-8').write(html)
print(OUT, len(html.encode()), 'bytes')
