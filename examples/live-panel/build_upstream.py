#!/usr/bin/env python3
"""把 live-panel/examples/*/config*.json 各產成一頁 up-<範例>.html，放在本目錄，給 live-panel-demo.html 的「上游範例」用。

用法：python3 build_upstream.py [字型目錄]
字型目錄放手繪範例要的字型（都是 OFL，太大所以不進 repo）：
  Xiaolai-Regular.ttf  https://github.com/lxgw/kose-font/releases （excalidraw 範例的中文手寫字）
  mali.ttf、mali-bold.ttf  https://github.com/google/fonts/tree/main/ofl/mali （hybrid-agent）
  wenkai.ttf  https://github.com/lxgw/LxgwWenKai/releases 的 LXGWWenKai-Regular.ttf （hybrid-agent）
沒給或缺字型時，頁面退回系統字型。裝了 fonttools 才會把大字型裁成頁面用到的字，否則整套內嵌（每頁 20 MB 以上）。
上游 config 是簡體，產頁前先轉成臺灣用語的繁體（OpenCC s2twp），再修 FIX 裡 s2twp 轉錯的詞。
需要：pip install opencc-python-reimplemented fonttools
同一範例有 3x4 與 4x5 兩版時只產 4x5。"""
import json, os, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
LP = HERE.parent.parent / "live-panel"
sys.path.insert(0, str(LP / "scripts"))
import livepanel as lp  # noqa: E402

try:
    from opencc import OpenCC
except ImportError:
    sys.exit("需要 OpenCC：pip install opencc-python-reimplemented")
S2TW = OpenCC("s2twp")
# s2twp 依詞轉換，下列在這些範例的語境裡轉錯，轉完再改回
FIX = [("測試透過", "測試通過"), ("評審透過", "評審通過"), ("引數", "參數"), ("覆盤", "復盤"),
       ("併發到", "並發到"), ("迴圈", "循環"), ("定製", "客製")]


def to_tw(text):
    text = S2TW.convert(text)
    for a, b in FIX:
        text = text.replace(a, b)
    return text


fonts = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else None
with tempfile.TemporaryDirectory() as tmp:
    for cfgp in sorted((LP / "examples").glob("*/config*.json")):
        if cfgp.stem == "config-3x4":
            continue
        name = cfgp.parent.name + ("" if cfgp.stem == "config" else "-" + cfgp.stem.replace("config-", ""))
        # 在暫存目錄放一份 config，旁邊連上字型：build_page 依 config 所在目錄找 theme.fonts 的 src
        d = Path(tmp) / name
        (d / "fonts").mkdir(parents=True)
        (d / "config.json").write_text(to_tw(cfgp.read_text(encoding="utf-8")), encoding="utf-8")
        if fonts:
            for f in fonts.iterdir():
                os.symlink(f, d / f.name)
                os.symlink(f, d / "fonts" / f.name)
        out = HERE / f"up-{name}.html"
        cfg = lp.build_page(str(d / "config.json"), str(out))
        print(json.dumps({"file": out.name, "title": cfg.get("meta", {}).get("title", ""), "kb": out.stat().st_size // 1024},
                         ensure_ascii=False))
