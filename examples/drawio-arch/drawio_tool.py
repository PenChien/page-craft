#!/usr/bin/env python3
"""drawio 轉檔前兩步的工具。
  python3 drawio_tool.py list   <檔.drawio>            列出每頁的設備（框）與連線（含座標、顏色、虛實、箭頭）
  python3 drawio_tool.py render <檔.drawio> <輸出目錄>  每頁畫成一張 PNG，用來和重繪結果逐條比對
render 需要：能連 https://viewer.diagrams.net（下載 viewer-static.min.js），以及無頭 Chrome。
Chrome 路徑依序找：環境變數 CHROME、playwright 快取、PATH 上的 chromium / google-chrome。"""
import glob, html, json, os, re, shutil, subprocess, sys, urllib.request
import xml.etree.ElementTree as ET

KEYS = ('fillColor', 'strokeColor', 'dashed', 'shape', 'prIcon', 'strokeWidth', 'startArrow', 'endArrow')


def label(c):
    v = re.sub(r'<br\s*/?>', ' / ', c.get('value') or '')
    return html.unescape(re.sub(r'<[^>]+>', '', v)).strip()


def style(c):
    kv = dict(x.split('=', 1) for x in (c.get('style') or '').split(';') if '=' in x)
    return ';'.join(f'{k}={kv[k]}' for k in KEYS if k in kv)


def cmd_list(path):
    for i, d in enumerate(ET.parse(path).getroot().iter('diagram')):
        print(f'#### 第 {i + 1} 頁：{d.get("name")}')
        for c in d.iter('mxCell'):
            g = c.find('mxGeometry')
            if c.get('vertex'):
                print(f"V {c.get('id')} parent={c.get('parent')} ({g.get('x')},{g.get('y')} {g.get('width')}x{g.get('height')}) "
                      f"'{label(c)}' [{style(c)}]")
            elif c.get('edge'):
                ends = [(p.get('as'), p.get('x'), p.get('y')) for p in g.iter('mxPoint') if p.get('as')]
                way = [(p.get('x'), p.get('y')) for p in g.iter('mxPoint') if not p.get('as')]
                print(f"E {c.get('id')}: {c.get('source')} -> {c.get('target')} '{label(c)}' [{style(c)}] ends={ends} via={way}")
    print('提示：source/target 是 None 的線只有座標，要對照 render 的圖判斷接到哪個框；子框座標是相對於 parent。')


def find_chrome():
    cands = [os.environ.get('CHROME')]
    cands += sorted(glob.glob(os.path.expanduser('~/.cache/ms-playwright/chromium-*/chrome-linux*/chrome')))[-1:]
    cands += [shutil.which(n) for n in ('chromium', 'chromium-browser', 'google-chrome')]
    for c in cands:
        if c and os.path.exists(c):
            return c
    sys.exit('找不到 Chrome：請設環境變數 CHROME=<chrome 執行檔>')


def cmd_render(path, out):
    os.makedirs(out, exist_ok=True)
    js = os.path.join(out, 'viewer-static.min.js')
    if not os.path.exists(js):
        # 預設的 Python User-Agent 會被擋 (403)，改用 curl 的格式
        req = urllib.request.Request('https://viewer.diagrams.net/js/viewer-static.min.js', headers={'User-Agent': 'curl/8'})
        open(js, 'wb').write(urllib.request.urlopen(req, timeout=60).read())
    xml = open(path, encoding='utf-8').read()
    chrome = find_chrome()
    pages = list(ET.fromstring(xml).iter('diagram'))
    for i, d in enumerate(pages):
        xs = [float(g.get('x') or 0) + float(g.get('width') or 0) for g in d.iter('mxGeometry')]
        ys = [float(g.get('y') or 0) + float(g.get('height') or 0) for g in d.iter('mxGeometry')]
        w, h = int(max(xs + [800])) + 120, int(max(ys + [500])) + 120
        cfg = {'xml': xml, 'page': i, 'nav': False, 'toolbar': '', 'lightbox': False, 'resize': True}
        page = os.path.join(out, f'page{i + 1}.html')
        open(page, 'w', encoding='utf-8').write(
            '<!doctype html><meta charset="utf-8"><body style="margin:0;background:#fff">'
            f'<div class="mxgraph" data-mxgraph="{html.escape(json.dumps(cfg))}"></div>'
            '<script src="viewer-static.min.js"></script>')
        png = os.path.join(out, f'page{i + 1}.png')
        subprocess.run([chrome, '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
                        '--virtual-time-budget=8000', f'--window-size={w},{h}', f'--screenshot={png}',
                        'file://' + os.path.abspath(page)], check=True, stderr=subprocess.DEVNULL)
        if not os.path.exists(png) or os.path.getsize(png) < 2000:
            sys.exit(f'第 {i + 1} 頁沒有畫出來：{png}')
        print(f'第 {i + 1} 頁「{d.get("name")}」→ {png}')


if __name__ == '__main__':
    if len(sys.argv) >= 3 and sys.argv[1] == 'list':
        cmd_list(sys.argv[2])
    elif len(sys.argv) >= 4 and sys.argv[1] == 'render':
        cmd_render(sys.argv[2], sys.argv[3])
    else:
        sys.exit(__doc__)
