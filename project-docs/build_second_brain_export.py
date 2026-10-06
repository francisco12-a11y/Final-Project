#!/usr/bin/env python3
"""Builds public/second-brain/index.html — a self-contained public export
of the Pareto Second Brain vault (L1). Re-run after editing vault notes."""
import os, re, html
import markdown

VAULT = "/home/fran/.zcode/workspace/default/Pareto-Second-Brain"
OUT = "/home/fran/.zcode/workspace/default/pareto-final/public/second-brain/index.html"

SECTIONS = [
    ("Home", "Overview"),
    ("00-CONTEXT", "Context"),
    ("01-COMPANIES", "Companies"),
    ("02-PEOPLE", "People"),
    ("03-MEDIA", "Media & Learning"),
    ("04-TOOLS", "Tools"),
    ("05-PROJECTS", "Projects"),
]

MD_EXT = ["extra", "sane_lists", "smarty"]

def strip_frontmatter(text):
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            return text[end + 3:].lstrip("\n")
    return text

def clean_wikilinks(text):
    # [[name]] or [[name|display]] -> display (or name) in bold
    def repl(m):
        inner = m.group(1)
        display = inner.split("|")[-1].strip()
        return f"<strong>{html.escape(display)}</strong>"
    return re.sub(r"\[\[([^\]]+)\]\]", repl, text)

def convert(md_text):
    text = strip_frontmatter(md_text)
    text = clean_wikilinks(text)
    # embed images as plain references (assets aren't shipped)
    text = re.sub(r"!\[\[([^\]]+)\]\]", r"*attachment: \1*", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "*attachment omitted in export*", text)
    return markdown.markdown(text, extensions=MD_EXT)

def note_title(path, md_text):
    base = os.path.splitext(os.path.basename(path))[0]
    m = re.search(r"^title:\s*(.+)$", md_text, re.M)
    return m.group(1).strip().strip('"') if m else base.replace("-", " ").title()

def collect():
    files = []
    for root, dirs, names in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d != ".obsidian"]
        for n in sorted(names):
            if n.endswith(".md") and n != "_template.md":
                files.append(os.path.join(root, n))
    # stable order: by section, then Home first inside root
    def key(p):
        rel = os.path.relpath(p, VAULT)
        sec = rel.split(os.sep)[0] if os.sep in rel else "!root"
        order = {s[0]: i for i, s in enumerate(SECTIONS)}
        return (order.get(sec, 99), rel)
    return sorted(files, key=key)

def section_of(path):
    rel = os.path.relpath(path, VAULT)
    top = rel.split(os.sep)[0]
    return top if os.sep in rel else "!root"

def build():
    files = collect()
    toc, body = [], []
    counts = {}
    for p in files:
        raw = open(p, encoding="utf-8").read()
        title = note_title(p, raw)
        sec = section_of(p)
        sec_label = dict(SECTIONS).get(sec, "Overview")
        counts[sec_label] = counts.get(sec_label, 0) + 1
        anchor = re.sub(r"[^a-z0-9]+", "-", (sec + "-" + title).lower()).strip("-")
        toc.append(f'<a class="toc-item" href="#{anchor}"><span class="toc-sec">{sec_label}</span>{html.escape(title)}</a>')
        body.append(f'<section id="{anchor}"><p class="crumb">{sec_label}</p>'
                    f'<h2>{html.escape(title)}</h2>'
                    f'<div class="note">{convert(raw)}</div></section>')
    nav = "\n".join(toc)
    content = "\n".join(body)
    sec_chips = " · ".join(f"<b>{s}</b> {counts.get(s,0)}" for _, s in SECTIONS)
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FP | Francisco Buiras | Second Brain</title>
<meta name="description" content="Public export of the Second Brain behind the Pareto Talent lead-magnet funnel: company intel, the Hire book and Bootcamp notes, competitor teardowns, ICP and founder personas.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:#050a0e; color:#f0f4f8; font-family:'DM Sans',sans-serif; }}
  .wrap {{ display:flex; min-height:100vh; }}
  nav {{ width:300px; flex:0 0 300px; position:sticky; top:0; height:100vh; overflow-y:auto;
        background:#0b1119; border-right:1px solid #ffffff14; padding:28px 18px 40px; }}
  nav h1 {{ font-family:'Plus Jakarta Sans',sans-serif; font-size:17px; line-height:1.3; margin-bottom:6px; }}
  nav .sub {{ color:#94a3b8; font-size:12px; margin-bottom:18px; }}
  .toc-item {{ display:block; color:#cbd5e1; text-decoration:none; font-size:12.5px; padding:5px 8px;
              border-radius:8px; margin-bottom:1px; }}
  .toc-item:hover {{ background:#ffffff0d; color:#f0f4f8; }}
  .toc-sec {{ display:block; color:#10b981; font-size:9.5px; font-weight:700; letter-spacing:.12em;
             text-transform:uppercase; }}
  main {{ flex:1; padding:48px clamp(24px,5vw,80px) 80px; max-width:980px; }}
  .hero {{ margin-bottom:40px; }}
  .hero .eyebrow {{ color:#10b981; font-size:11px; font-weight:800; letter-spacing:.18em;
                   text-transform:uppercase; }}
  .hero h1 {{ font-family:'Plus Jakarta Sans',sans-serif; font-size:clamp(26px,4vw,40px);
             line-height:1.15; margin:10px 0 12px; }}
  .hero p {{ color:#94a3b8; font-size:15.5px; max-width:640px; }}
  .chips {{ margin-top:16px; color:#94a3b8; font-size:12.5px; }}
  .chips b {{ color:#6ee7b7; }}
  section {{ margin-bottom:54px; }}
  .crumb {{ color:#10b981; font-size:10.5px; font-weight:800; letter-spacing:.16em;
           text-transform:uppercase; margin-bottom:6px; }}
  h2 {{ font-family:'Plus Jakarta Sans',sans-serif; font-size:23px; margin-bottom:14px;
       border-bottom:1px solid #ffffff14; padding-bottom:10px; }}
  .note {{ font-size:15px; line-height:1.7; color:#d7e0ea; overflow-wrap:break-word; }}
  .note h1, .note h2, .note h3, .note h4 {{ font-family:'Plus Jakarta Sans',sans-serif;
      color:#f0f4f8; margin:20px 0 8px; }}
  .note h1 {{ font-size:20px; }} .note h2 {{ font-size:18px; border:0; padding:0; }}
  .note h3 {{ font-size:16px; }} .note h4 {{ font-size:14.5px; }}
  .note p {{ margin-bottom:12px; }}
  .note ul, .note ol {{ margin:0 0 12px 22px; }}
  .note li {{ margin-bottom:5px; }}
  .note strong {{ color:#f0f4f8; }}
  .note code {{ background:#ffffff12; border-radius:5px; padding:1px 6px; font-size:13px; }}
  .note pre {{ background:#0b1119; border:1px solid #ffffff14; border-radius:10px; padding:14px;
              overflow-x:auto; margin-bottom:12px; }}
  .note pre code {{ background:none; }}
  .note blockquote {{ border-left:3px solid #10b981; padding:4px 16px; margin:0 0 12px;
                     color:#94a3b8; }}
  .note a {{ color:#6ee7b7; }}
  .note table {{ border-collapse:collapse; margin-bottom:12px; }}
  .note th, .note td {{ border:1px solid #ffffff1f; padding:6px 10px; font-size:13.5px; }}
  .note hr {{ border:0; border-top:1px solid #ffffff14; margin:18px 0; }}
  footer {{ color:#475569; font-size:12px; padding:24px clamp(24px,5vw,80px); }}
  @media (max-width: 860px) {{ .wrap {{ display:block; }} nav {{ position:static; width:100%;
      height:auto; border-right:0; border-bottom:1px solid #ffffff14; }} }}
</style>
</head>
<body>
<div class="wrap">
  <nav>
    <h1>FP | Francisco Buiras<br>Second Brain</h1>
    <div class="sub">Public export · {len(files)} notes · built for the Pareto Talent final project</div>
    {nav}
  </nav>
  <main>
    <div class="hero">
      <div class="eyebrow">L1 · Mini Second Brain</div>
      <h1>Everything the funnel was built from.</h1>
      <p>Company intel on Pareto Talent, the Hire book and Bootcamp notes, competitor
         lead-magnet teardowns, the ICP, and the founder personas — the notes behind every
         decision in this project, exported from Obsidian.</p>
      <div class="chips">{sec_chips}</div>
    </div>
    {content}
  </main>
</div>
<footer>FP | Francisco Buiras · Pareto Talent Final Project · L1 export</footer>
</body>
</html>"""
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(page)
    print(f"OK -> {OUT}  ({len(files)} notes, {os.path.getsize(OUT)//1024} KB)")

if __name__ == "__main__":
    build()
