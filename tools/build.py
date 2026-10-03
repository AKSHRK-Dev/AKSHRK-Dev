#!/usr/bin/env python3
"""Writes README.md, README.ja.md, i18n/README.<code>.md, LANGUAGES.md and the animated SVGs
from tools/strings/<code>.json. Add a language: add its strings file, run python3 tools/build.py."""
import json
from html import escape
from pathlib import Path

from languages import LANGS, REGIONS

ROOT = Path(__file__).resolve().parent.parent
STRINGS = ROOT / "tools" / "strings"


def path_of(code):
    return {"en": "README.md", "ja": "README.ja.md"}.get(code, f"i18n/README.{code}.md")


def available():
    have = {p.stem for p in STRINGS.glob("*.json")}
    return [c for c in LANGS if c in have]


def load(code):
    return json.loads((STRINGS / f"{code}.json").read_text(encoding="utf-8"))


def lang_bar(code, n, s):
    up = "../" if "/" in path_of(code) else ""
    parts = []
    for c in ("en", "ja"):
        name = LANGS[c][0] if c != "en" else "English"
        parts.append(f"<b>{name}</b>" if c == code else f'<a href="{up}{path_of(c)}">{name}</a>')
    if code not in ("en", "ja"):
        parts.append(f"<b>{LANGS[code][0]}</b>")
    parts.append(f'<a href="{up}LANGUAGES.md">{escape(s["languages"].format(n=n))}</a>')
    return f'<p align="center">{" · ".join(parts)}</p>'


def readme(code, n):
    s = load(code)
    rtl = LANGS[code][3]
    bullets = lambda items: "\n".join(f"- {x}" for x in items)
    body = f"""<h1 align="center">{s['hi']}</h1>

<p align="center">
  {s['intro']}
</p>

<p align="center">
  <a href="https://ashikanw.com"><img src="https://img.shields.io/badge/ASHIKA%20Network-ashikanw.com-E63E3E?style=for-the-badge" alt="ASHIKA Network"></a>
  <a href="https://minecrafts.jp"><img src="https://img.shields.io/badge/SABALISU-minecrafts.jp-E63E3E?style=for-the-badge" alt="SABALISU"></a>
  <a href="https://storiamc.com"><img src="https://img.shields.io/badge/Storia-storiamc.com-1B60A6?style=for-the-badge" alt="Storia"></a>
</p>

---

## {s['about_t']}

{bullets(s['about'])}

### {s['can_write']}

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-5FA04E?style=flat-square&logo=nodedotjs&logoColor=white)
![C#](https://img.shields.io/badge/C%23-512BD4?style=flat-square&logo=dotnet&logoColor=white)

---

## {s['services_t']}

### {s['anw_t']}

{s['anw_p']}

| | |
|---|---|
| {s['website']} | https://www.ashikanw.com |
| Discord | https://link.ashikanw.com/discord |

<br>

### {s['sab_t']}

{s['sab_p']}

| | |
|---|---|
| {s['website']} | https://minecrafts.jp |
| Discord | https://discord.gg/KucQxEsJtr |

<br>

### {s['storia_t']}

{s['storia_p']}

{bullets(s['storia_points'])}

| | |
|---|---|
| {s['website']} | https://storiamc.com |
| {s['source']} | https://github.com/AKSHRK-Dev/Storia |

<p>
  <a href="https://github.com/AKSHRK-Dev/Storia/releases/latest"><img src="https://img.shields.io/github/v/release/AKSHRK-Dev/Storia?style=flat-square&label=Storia&color=1B60A6" alt="Storia release"></a>
  <a href="https://github.com/AKSHRK-Dev/Storia"><img src="https://img.shields.io/github/stars/AKSHRK-Dev/Storia?style=flat-square&color=1B60A6" alt="Stars"></a>
</p>

---

## {s['stats_t']}

<p align="left">
  <img height="150" src="https://github-readme-stats.vercel.app/api?username=AKSHRK-Dev&show_icons=true&hide_border=true&theme=default" alt="GitHub Stats">
  <img height="150" src="https://github-readme-stats.vercel.app/api/top-langs/?username=AKSHRK-Dev&layout=compact&hide_border=true&theme=default" alt="Top Languages">
</p>

---

## {s['contact_t']}

- {s['contact_afk']}: https://discord.gg/q8TbzdRfsV
- {s['contact_sab']}: https://discord.gg/KucQxEsJtr
- {s['mail']}: admin@minecrafts.jp

<p align="center">
  <sub>{s['welcome']}</sub>
</p>"""
    if rtl:
        body = f'<div dir="rtl">\n\n{body}\n\n</div>'
    return f"{lang_bar(code, n, s)}\n\n{body}\n"


def languages_page(codes):
    n = len(codes)
    have = set(codes)
    nav = " · ".join(f'<a href="#{cid}">{en} / {ja}</a>' for cid, en, ja, _ in REGIONS)
    out = [f"""<p align="center"><img src="assets/hello.svg" width="820" alt="Hello in many languages"></p>

<h1 align="center">Languages / 言語一覧</h1>

<p align="center">This profile is available in <b>{n}</b> languages. Pick yours below.<br>このプロフィールは <b>{n}</b> の言語で読めます。下から選んでください。</p>

<p align="center"><img src="assets/continents.svg" width="820" alt="Languages per continent"></p>

<p align="center">{nav}</p>
"""]
    for cid, en, ja, regions in REGIONS:
        count = len({c for _, _, cs in regions for c in cs if c in have})
        out.append(f'\n<h2 id="{cid}">{en} / {ja} <sub>({count})</sub></h2>\n')
        for ren, rja, cs in regions:
            rows = [f"| [{LANGS[c][0]}]({path_of(c)}) | {LANGS[c][1]} | {LANGS[c][2]} |" for c in cs if c in have]
            if not rows:
                continue
            out.append(f"\n### {ren} / {rja}\n\n| Language | English | 日本語 |\n|---|---|---|\n" + "\n".join(rows) + "\n")
    out.append("""
---

<sub>The English and Japanese versions are the originals. The other translations were written with care, but some may contain mistakes, especially in languages with few online resources. Corrections are welcome as issues or pull requests.<br>
原文は英語版と日本語版です。ほかの言語の翻訳には、特に資料の少ない言語で誤りがあるかもしれません。修正は Issue や Pull Request で歓迎します。</sub>
""")
    return "".join(out)


GREETINGS = [("Hello", "en"), ("こんにちは", "ja"), ("안녕하세요", "ko"), ("你好", "zh"), ("Bonjour", "fr"), ("Hola", "es"),
             ("Olá", "pt"), ("Привет", "ru"), ("مرحبا", "ar"), ("नमस्ते", "hi"), ("Hallo", "de"), ("Ciao", "it"),
             ("Merhaba", "tr"), ("Xin chào", "vi"), ("สวัสดี", "th"), ("Habari", "sw"), ("Kia ora", "mi"), ("Γεια σου", "el"),
             ("שלום", "he"), ("Salam", "az"), ("Talofa", "sm"), ("Halo", "id"), ("Hej", "sv"), ("Mingalaba", "my")]


def hello_svg(n):
    step = 2.2
    total = step * len(GREETINGS)
    vis = 100 / len(GREETINGS)
    texts = "".join(f'<text class="g" x="410" y="118" style="animation-delay:{i * step:.1f}s" lang="{l}">{escape(g)}</text>' for i, (g, l) in enumerate(GREETINGS))
    dots = "".join(f'<circle class="d" cx="{40 + (i * 97) % 760}" cy="{30 + (i * 53) % 150}" r="{1.5 + (i % 3)}" style="animation-delay:{(i * .37) % 4:.2f}s"/>' for i in range(26))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 200" width="820" height="200" role="img" aria-label="Hello in {n} languages">
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#14497e"/><stop offset="1" stop-color="#1b60a6"/></linearGradient></defs>
<style>
.g {{ font: 800 56px system-ui, -apple-system, "Segoe UI", "Noto Sans", "Noto Sans JP", sans-serif; fill: #fff; text-anchor: middle; opacity: 0; animation: show {total:.1f}s infinite; }}
@keyframes show {{ 0% {{ opacity: 0; transform: translateY(14px); }} {vis * .18:.2f}% {{ opacity: 1; transform: none; }} {vis * .82:.2f}% {{ opacity: 1; transform: none; }} {vis:.2f}% {{ opacity: 0; transform: translateY(-14px); }} 100% {{ opacity: 0; }} }}
.d {{ fill: #7fb2ea; opacity: .25; animation: tw 4s ease-in-out infinite; }}
@keyframes tw {{ 50% {{ opacity: .8; }} }}
.sub {{ font: 600 16px system-ui, -apple-system, "Segoe UI", sans-serif; fill: #cfe2f8; text-anchor: middle; letter-spacing: 2px; }}
.orbit {{ fill: none; stroke: #7fb2ea; stroke-opacity: .35; stroke-dasharray: 4 8; animation: spin 30s linear infinite; transform-origin: 410px 100px; }}
@keyframes spin {{ to {{ transform: rotate(360deg); }} }}
</style>
<rect width="820" height="200" rx="18" fill="url(#bg)"/>
{dots}
<ellipse class="orbit" cx="410" cy="100" rx="330" ry="78"/>
{texts}
<text class="sub" x="410" y="172">{n} LANGUAGES · {n} の言語</text>
</svg>
"""


def continents_svg(codes):
    have = set(codes)
    counts = [(en, ja, len({c for _, _, cs in regions for c in cs if c in have})) for _, en, ja, regions in REGIONS]
    top = max(1, max(c for _, _, c in counts))
    rows = []
    for i, (en, ja, c) in enumerate(counts):
        y = 34 + i * 34
        w = 520 * c / top
        rows.append(f"""<text class="l" x="20" y="{y + 15}">{en} / {ja}</text>
<rect class="track" x="270" y="{y}" width="520" height="20" rx="10"/>
<rect class="bar" x="270" y="{y}" width="{w:.1f}" height="20" rx="10" style="animation-delay:{i * .15:.2f}s"/>
<text class="n" x="{270 + w + 8 if w < 470 else 270 + w - 10:.1f}" y="{y + 15}" text-anchor="{'start' if w < 470 else 'end'}" style="fill:{'#14497e' if w < 470 else '#fff'}">{c}</text>""")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 {34 + len(counts) * 34 + 10}" width="820" role="img" aria-label="Languages per continent">
<style>
.l {{ font: 600 14px system-ui, -apple-system, "Segoe UI", "Noto Sans JP", sans-serif; fill: #3a4658; }}
.n {{ font: 700 13px system-ui, -apple-system, "Segoe UI", sans-serif; }}
.track {{ fill: #e8f0f9; }}
.bar {{ fill: #1b60a6; transform-box: fill-box; transform-origin: left; animation: grow 1.4s cubic-bezier(.2, .8, .2, 1) both; }}
@keyframes grow {{ from {{ transform: scaleX(0); }} }}
@media (prefers-color-scheme: dark) {{ .l {{ fill: #c3ccd8; }} .track {{ fill: #172a40; }} }}
@media (prefers-reduced-motion: reduce) {{ .bar {{ animation: none; }} }}
</style>
<text class="l" x="20" y="18" style="font-weight:800;fill:#1b60a6">Languages per continent / 州ごとの言語数</text>
{''.join(rows)}
</svg>
"""


def main():
    codes = available()
    n = len(codes)
    for c in codes:
        out = ROOT / path_of(c)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(readme(c, n), encoding="utf-8")
    (ROOT / "LANGUAGES.md").write_text(languages_page(codes), encoding="utf-8")
    (ROOT / "assets").mkdir(exist_ok=True)
    (ROOT / "assets" / "hello.svg").write_text(hello_svg(n), encoding="utf-8")
    (ROOT / "assets" / "continents.svg").write_text(continents_svg(codes), encoding="utf-8")
    print(f"{n} languages")


if __name__ == "__main__":
    main()
