"""Build index.html (the game) and script.html (the recording script) from the sources in tools/.
Run from anywhere: python3 tools/build.py"""
import json, os, html as H
T = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(T)
HEAD = ('<!doctype html><html lang="ms"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
        'body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style></head><body>\n')
TAIL = '\n</body></html>\n'
clips = json.load(open(os.path.join(T, "clips.json"), encoding="utf8"))
rec = {}
for lang in ("ms", "en"):
    d = os.path.join(ROOT, "voice", lang)
    rec[lang] = sorted(f[:-4] for f in os.listdir(d) if f.endswith(".mp3")) if os.path.isdir(d) else []
src = open(os.path.join(T, "game-src.html"), encoding="utf8").read()
js = json.dumps([{"id": c["id"], "ms": c["ms"], "en": c["en"]} for c in clips], ensure_ascii=False)
game = src.replace("/*CLIPS*/[]", js).replace("/*RECORDED*/{ms:[], en:[]}", json.dumps(rec))
open(os.path.join(ROOT, "index.html"), "w", encoding="utf8").write(HEAD + game + TAIL)
# recording script page
cwd = os.getcwd(); os.chdir(T)
exec(open("script_build.py", encoding="utf8").read())
os.chdir(cwd)
page = open(os.path.join(T, "skrip-rakaman.html"), encoding="utf8").read()
os.remove(os.path.join(T, "skrip-rakaman.html"))
open(os.path.join(ROOT, "script.html"), "w", encoding="utf8").write(HEAD.replace('lang="ms"', 'lang="en"') + page + TAIL)
print(f"index.html: {len(clips)} lines, {len(rec['ms'])} recorded in BM")
