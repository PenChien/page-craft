#!/usr/bin/env python3
"""把 build_arch.py 產生的線路圖 (inline SVG) 反向轉成可編輯的 drawio。
用法: svg2drawio.py <報告.html> <輸出.drawio>
每個 <div class="fig arch"><svg> 轉成一頁；頁名取該章 .divider 的標題，圖前有 .arch-legend 就把圖例畫在頁頂。
  虛線 rect → 分區框 (標題併入框、靠上)；實線 rect → 設備框 / 介面框 (框內文字併入標籤)；
  其他 text → 文字格；polyline → 連線 (端點落在框邊上就接到該框，移動框時線會跟著走)。"""
import re, sys, html
import xml.etree.ElementTree as ET
from xml.sax.saxutils import quoteattr

SRC, OUT = sys.argv[1], sys.argv[2]
FONT = {'t1': (12.5, 1, '#0b0b0b'), 't2': (10.5, 0, '#52514e'), 't3': (12.5, 1, None),
        't4': (10.5, 1, '#1f2329'), 't5': (12, 1, None), 't6': (9.5, 1, None)}
LEGEND_H = 34  # 圖例高度；有圖例的頁，整張圖往下移


def textw(t, size):
    return sum(size * (1.0 if ord(ch) > 0x2E80 else 0.6) for ch in t) + 6


class Page:
    def __init__(s, name):
        s.name, s.cells, s.n = name, [], 1

    def nid(s):
        s.n += 1
        return f'c{s.n}'

    def vertex(s, val, style, x, y, w, h):
        i = s.nid()
        s.cells.append(f'<mxCell id="{i}" value={quoteattr(val)} style={quoteattr(style)} vertex="1" parent="1">'
                       f'<mxGeometry x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" as="geometry"/></mxCell>')
        return i

    def edge(s, style, src, tgt, pts):
        i = s.nid()
        st = f' source="{src}"' if src else ''
        tg = f' target="{tgt}"' if tgt else ''
        (x1, y1), (x2, y2) = pts[0], pts[-1]
        way = ''.join(f'<mxPoint x="{x}" y="{y}"/>' for x, y in pts[1:-1])
        s.cells.append(f'<mxCell id="{i}" style={quoteattr(style)} edge="1" parent="1"{st}{tg}>'
                       f'<mxGeometry relative="1" as="geometry"><mxPoint x="{x1}" y="{y1}" as="sourcePoint"/>'
                       f'<mxPoint x="{x2}" y="{y2}" as="targetPoint"/>' + (f'<Array as="points">{way}</Array>' if way else '')
                       + '</mxGeometry></mxCell>')

    def xml(s):
        return (f'<diagram name={quoteattr(s.name)} id="{abs(hash(s.name)) % 10**10}"><mxGraphModel grid="1" gridSize="10" '
                'guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="0" math="0" shadow="0"><root>'
                '<mxCell id="0"/><mxCell id="1" parent="0"/>' + ''.join(s.cells) + '</root></mxGraphModel></diagram>')


def fill_of(el):
    st = el.get('style') or ''
    m = re.search(r'fill:(#[0-9a-fA-F]+)', st)
    return m.group(1) if m else None


def convert(svg, name, legend):
    ns = {'s': 'http://www.w3.org/2000/svg'}
    root = ET.fromstring(svg.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ', 1))
    pg = Page(name)
    dy = LEGEND_H if legend else 0
    rects, texts, lines = [], [], []
    for el in root.iter():
        tag = el.tag.split('}')[1]
        if tag == 'rect':
            r = dict(x=float(el.get('x')), y=float(el.get('y')) + dy, w=float(el.get('width')), h=float(el.get('height')),
                     fill=el.get('fill'), stroke=el.get('stroke'), dash=el.get('stroke-dasharray'), rx=float(el.get('rx', 0)),
                     sw=el.get('stroke-width', '1'), texts=[])
            rects.append(r)
        elif tag == 'text':
            texts.append(dict(x=float(el.get('x')), y=float(el.get('y')) + dy, t=el.text or '', cls=el.get('class'),
                              anchor=el.get('text-anchor', 'start'), fill=fill_of(el)))
        elif tag == 'polyline':
            pts = [tuple(float(v) for v in p.split(',')) for p in el.get('points').split()]
            lines.append(dict(pts=[(x, y + dy) for x, y in pts], color=el.get('stroke'), dash=el.get('stroke-dasharray'),
                              op=el.get('opacity'), start='marker-start' in el.attrib, end='marker-end' in el.attrib))

    # 文字歸屬：分區標題 → 分區框；設備框 / 介面框內、置中的 t1/t2/t3 → 最小的實線框
    free = []
    for t in texts:
        owner = None
        if t['cls'] == 't3':
            for r in rects:
                if r['dash'] and abs(t['y'] - (r['y'] + 20)) < 1 and r['x'] < t['x'] < r['x'] + r['w']:
                    owner = r
        if owner is None and t['cls'] in ('t1', 't2', 't3') and t['anchor'] == 'middle':
            inside = [r for r in rects if not r['dash'] and r['x'] < t['x'] < r['x'] + r['w'] and r['y'] < t['y'] < r['y'] + r['h']
                      and abs(t['x'] - (r['x'] + r['w'] / 2)) < 1]
            inside.sort(key=lambda r: r['w'] * r['h'])
            # 主機大框 (rx=10) 只收框頂的主機名稱；框內其他說明留成文字格
            if inside and (inside[0]['rx'] != 10 or (t['cls'] == 't1' and t['y'] - inside[0]['y'] < 24)):
                owner = inside[0]
        (owner['texts'] if owner else free).append(t)

    ids = []
    for r in rects:
        base = f'rounded=1;arcSize={max(4, int(r["rx"] * 100 / min(r["w"], r["h"])))};absoluteArcSize=0;html=1;whiteSpace=wrap;' \
               f'fillColor={r["fill"]};strokeColor={r["stroke"]};strokeWidth={r["sw"]};'
        tx = r['texts']
        if r['dash']:  # 分區框
            t = tx[0] if tx else None
            style = base + f'dashed=1;dashPattern={r["dash"]};verticalAlign=top;spacingTop=4;fontSize=12.5;fontStyle=1;' \
                           f'fontColor={(t and t["fill"]) or r["stroke"]};container=0;'
            val = html.escape(t['t']) if t else ''
        else:
            tx.sort(key=lambda t: t['y'])
            parts = []
            for t in tx:
                size, bold, col = FONT[t['cls']]
                size = min(size, 12)  # drawio 的字比瀏覽器寬，框內標題縮 0.5 才不換行
                col = t['fill'] or col or '#0b0b0b'
                s = html.escape(t['t'])
                parts.append(f'<span style="font-size:{size}px;color:{col};{"font-weight:bold;" if bold else ""}">{s}</span>')
            top = r['rx'] == 10 and tx  # 主機大框：名稱靠上
            style = base + ('verticalAlign=top;spacing=0;spacingTop=3;' if top else 'verticalAlign=middle;spacing=1;') + 'fontSize=12;'
            val = '<br>'.join(parts)
        ids.append((r, pg.vertex(val, style, r['x'], r['y'], r['w'], r['h'])))

    for t in free:
        size, bold, col = FONT[t['cls']]
        col = t['fill'] or col or '#0b0b0b'
        w, h = textw(t['t'], size), size * 1.5
        x = {'start': t['x'], 'middle': t['x'] - w / 2, 'end': t['x'] - w}[t['anchor']]
        align = {'start': 'left', 'middle': 'center', 'end': 'right'}[t['anchor']]
        font = 'fontFamily=Courier New;' if t['cls'] == 't4' else ''
        pg.vertex(html.escape(t['t']), f'text;html=1;whiteSpace=nowrap;align={align};verticalAlign=middle;spacing=0;'
                  f'fontSize={size};fontStyle={bold};fontColor={col};{font}', x, t['y'] - size * 1.05, w, h)

    def snap(p):
        """端點落在哪個實線框的邊上 → (cell id, 相對位置)；優先最小的框。"""
        x, y = p
        best = None
        for r, i in ids:
            if r['dash']:
                continue
            on_v = abs(x - r['x']) <= 1.5 or abs(x - r['x'] - r['w']) <= 1.5
            on_h = abs(y - r['y']) <= 1.5 or abs(y - r['y'] - r['h']) <= 1.5
            inx = r['x'] - 1.5 <= x <= r['x'] + r['w'] + 1.5
            iny = r['y'] - 1.5 <= y <= r['y'] + r['h'] + 1.5
            if (on_v and iny) or (on_h and inx):
                if best is None or r['w'] * r['h'] < best[0]['w'] * best[0]['h']:
                    best = (r, i)
        if not best:
            return None, ''
        r, i = best
        fx, fy = min(max((x - r['x']) / r['w'], 0), 1), min(max((y - r['y']) / r['h'], 0), 1)
        return i, (fx, fy)

    linked = 0
    for ln in lines:
        p = ln['pts']
        s_id, s_c = snap(p[0])
        t_id, t_c = snap(p[-1])
        linked += bool(s_id) + bool(t_id)
        style = f'html=1;rounded=0;edgeStyle=orthogonalEdgeStyle;strokeColor={ln["color"]};strokeWidth=2;' \
                f'endArrow={"block" if ln["end"] else "none"};startArrow={"block" if ln["start"] else "none"};' \
                'endFill=1;startFill=1;endSize=5;startSize=5;'
        if ln['dash']:
            style += f'dashed=1;dashPattern={ln["dash"]};'
        if ln['op']:
            style += f'opacity={int(float(ln["op"]) * 100)};'
        if s_id:
            style += f'exitX={s_c[0]:.4f};exitY={s_c[1]:.4f};exitDx=0;exitDy=0;exitPerimeter=0;'
        if t_id:
            style += f'entryX={t_c[0]:.4f};entryY={t_c[1]:.4f};entryDx=0;entryDy=0;entryPerimeter=0;'
        pg.edge(style, s_id, t_id, p)

    if legend:  # 圖例：照 .arch-legend 的項目畫在頁頂（線色 → 線段、框色 → 小框、「虛線＝X」→ 灰虛線）
        T = 'text;html=1;whiteSpace=nowrap;align=left;fontSize=11;fontColor=#52514e;'
        x = 10
        for kind, a, b, lab in legend:
            if kind == 'head':
                pg.vertex(lab, T, x, 6, textw(lab, 11), 20)
                x += textw(lab, 11) + 2
                continue
            if kind == 'line':
                pg.edge(f'html=1;endArrow=none;strokeColor={a};strokeWidth=2;', None, None, [(x, 16), (x + 22, 16)])
            elif kind == 'dash':
                pg.edge('html=1;endArrow=none;strokeColor=#8a8985;strokeWidth=2;dashed=1;dashPattern=3 3;', None, None, [(x, 16), (x + 22, 16)])
            else:  # box
                pg.vertex('', f'rounded=1;html=1;fillColor={a};strokeColor={b};strokeWidth=1.5;', x + 4, 10, 14, 12)
            pg.vertex(lab, T, x + 26, 6, textw(lab, 11), 20)
            x += 34 + textw(lab, 11)
    return pg, linked, len(lines)


def parse_legend(p):
    """.arch-legend 的 HTML → [(kind, 色1, 色2, 文字)]；kind = head / line / box / dash。"""
    items = []
    for part in re.split(r'<br\s*/?>', p):
        head = re.match(r'\s*([^<]*?：)', part)
        if head:
            items.append(('head', None, None, head.group(1)))
        for li in re.findall(r'<span class="li">(.*?)</span>(?=<span class="li">|$)', part):
            m = re.match(r'<span class="sw" style="background:(#\w+)(?:;outline:[\d.]+px solid (#\w+))?"></span>(.*)', li)
            if m:
                items.append(('box' if m.group(2) else 'line', m.group(1), m.group(2), html.unescape(m.group(3))))
            else:
                d = re.match(r'虛線＝(.*)', li)
                items.append(('dash', None, None, d.group(1) if d else html.unescape(li)))
    return items


doc = open(SRC, encoding='utf-8').read()
figs = list(re.finditer(r'<div class="fig arch">(<svg.*?</svg>)</div>', doc, re.S))
if not figs:
    sys.exit('找不到 <div class="fig arch"><svg>…</svg></div>')
out, prev = [], 0
for k, m in enumerate(figs):
    before = doc[prev:m.start()]
    prev = m.end()
    titles = re.findall(r'<div class="divider"><span>[^<]*</span>([^<]+)', before)
    name = titles[-1].strip() if titles else f'圖 {k + 1}'
    lg = re.findall(r'<p class="arch-legend">(.*?)</p>', before, re.S)
    pg, linked, n = convert(m.group(1), name, legend=parse_legend(lg[-1]) if lg else None)
    print(f'{name}: {len(pg.cells)} 格，連線 {n} 條，接到框的端點 {linked}/{2 * n}')
    out.append(pg.xml())
open(OUT, 'w', encoding='utf-8').write(f'<mxfile host="app.diagrams.net" pages="{len(out)}">' + ''.join(out) + '</mxfile>')
ET.parse(OUT)  # XML 要能解析
print('寫出', OUT)
