import json, html
clips = json.load(open("clips.json"))
SECS = {
 "A": ("Sambutan & arahan", "Welcome and instructions", "Warm and clear, like talking to a 4-year-old."),
 "B": ("Bismillah, siang & malam, nilai", "Bismillah, day cycle and values", "Calm and gentle. Say Bismillah slowly."),
 "C": ("Pujian", "Praise", "Big smile, proud and happy."),
 "D": ("Makanan tak selamat", "Unsafe foods", "Gentle and caring, never scary or scolding."),
 "E": ("Oyen (anak kucing)", "Oyen the kitten", "Say the name the same way every time."),
 "F": ("Bobo (anak anjing)", "Bobo the puppy", "Say the name the same way every time."),
 "G": ("Gebu (arnab)", "Gebu the rabbit", "Say the name the same way every time."),
 "H": ("Kiki (burung)", "Kiki the bird", "Say the name the same way every time."),
}
out = []
for s,(ms,en,tip) in SECS.items():
    items = [c for c in clips if c["id"][0]==s]
    rows = "".join(
      f'<li><span class="num">{c["id"]}</span><div class="line"><p class="ms">{html.escape(c["ms"])}</p>'
      f'<p class="en">{html.escape(c["en"])}</p>'
      + (f'<span class="tone">{html.escape(c["note"])}</span>' if c["note"] else "") + '</div></li>'
      for c in items)
    out.append(f'''<section class="sec" id="sec-{s}">
  <header class="sec-head">
    <div class="sec-title"><span class="badge">{s}</span><div><h2>{html.escape(ms)}</h2><p class="sub">{html.escape(en)} · {len(items)} lines · save as <code>{s}.m4a</code></p></div></div>
    <label class="done"><input type="checkbox" id="done-{s}" data-sec="{s}"> Recorded</label>
  </header>
  <p class="tip">{html.escape(tip)}</p>
  <ol class="lines">{rows}</ol>
</section>''')
tpl = open("script-src.html", encoding="utf8").read()
open("skrip-rakaman.html","w",encoding="utf8").write(tpl.replace("<!--SECTIONS-->", "\n".join(out)).replace("{{TOTAL}}", str(len(clips))))
print("ok")
