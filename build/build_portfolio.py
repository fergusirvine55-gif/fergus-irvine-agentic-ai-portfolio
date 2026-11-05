#!/usr/bin/env python3
"""Build README.md and index.html from portfolio.json. Stdlib only.
Run from the repo root: python3 build/build_portfolio.py"""
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
P = json.loads((ROOT / "portfolio.json").read_text())
GH_BLOB = P["repo"] + "/blob/main/"
GH_TREE = P["repo"] + "/tree/main/"
STATUS_CLASS = {"live": "st-live", "demo": "st-demo", "in prep": "st-prep"}


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


# ---------- README ----------
def md_link(l):
    return f"[{l['label']}]({l['href']})"


def md_links(links):
    return " · ".join(md_link(l) for l in links)


def md_start():
    rows = ["| If you run | Start with |", "|---|---|"]
    for s in P["start"]:
        rows.append(f"| {s['who']} | {md_links(s['go'])} |")
    return "\n".join(rows)


def md_projects():
    out = []
    for d in P["domains"]:
        rows = ["| Project | What | Stack | Proof | Links |", "|---|---|---|---|---|"]
        for pr in d["projects"]:
            name = f"{pr['name']} `{pr['status']}`"
            stack = " · ".join(pr["stack"])
            links = md_links(pr["links"]) if pr.get("links") else ""
            rows.append(f"| {name} | {pr['what']} | {stack} | {pr['proof']} | {links} |")
        out.append(f"### {d['title']}\n\n{d['blurb']}\n\n" + "\n".join(rows))
    return "\n\n".join(out)


def md_prep():
    ip = P["in_preparation"]
    return f"### {ip['title']}\n\n{ip['blurb']}\n\n" + "\n".join(f"- {i}" for i in ip["items"])


def build_readme():
    per = P["person"]
    rep = {
        "NAME": per["name"],
        "TAGLINE": per["tagline"],
        "META": " · ".join(per["meta"]),
        "CONTACTS": f"{per['email']} · [LinkedIn]({per['linkedin']}) · [Site]({P['site']})",
        "INTRO": per["intro"],
        "START": md_start(),
        "PROJECTS": md_projects(),
        "PREP": md_prep(),
        "BUILD_TITLE": P["build"]["title"],
        "BUILD": "\n".join(f"- {s}" for s in P["build"]["summary"]),
        "BUILD_HREF": P["build"]["href"],
        "TREE": P["tree"],
        "RUN": P["run"],
        "RUN_NOTE": P["run_note"],
        "PROVES": "\n".join(f"- {s}" for s in P["proves"]),
        "VERSION": P["version"],
        "UPDATED": P["updated"],
    }
    t = (ROOT / "build" / "README.template.md").read_text()
    for k, v in rep.items():
        t = t.replace("{{" + k + "}}", v)
    (ROOT / "README.md").write_text(t)


# ---------- index.html ----------
def site_href(href):
    """HTML apps are served by Pages next to this file; Markdown and folders open on GitHub."""
    if href.startswith(("http", "#")) or href.endswith(".html") or href == "demo/":
        return href
    return (GH_TREE if href.endswith("/") else GH_BLOB) + href


def e(s):
    return html.escape(s, quote=True)


def h_links(links):
    return "".join(f'<a class="pill" href="{e(site_href(l["href"]))}">{e(l["label"])}</a>' for l in links)


def h_start():
    cards = []
    for s in P["start"]:
        cards.append(f'<div class="start"><div class="who">{e(s["who"])}</div><p class="links">{h_links(s["go"])}</p></div>')
    return '<div class="grid3">' + "".join(cards) + "</div>"


def h_card(pr):
    st = pr["status"]
    stack = "".join(f"<code>{e(s)}</code>" for s in pr["stack"])
    links = f'<p class="links">{h_links(pr["links"])}</p>' if pr.get("links") else ""
    return (
        f'<article class="card"><header><h3>{e(pr["name"])}</h3>'
        f'<span class="st {STATUS_CLASS.get(st, "st-prep")}">{e(st)}</span></header>'
        f'<p>{e(pr["what"])}</p><p class="stack">{stack}</p>'
        f'<p class="proof"><span class="lab">proof</span>{e(pr["proof"])}</p>{links}</article>'
    )


def h_projects():
    out = []
    for d in P["domains"]:
        out.append(
            f'<section id="{slug(d["title"])}"><h2>{e(d["title"])}</h2><p class="blurb">{e(d["blurb"])}</p>'
            f'<div class="grid">{"".join(h_card(pr) for pr in d["projects"])}</div></section>'
        )
    ip = P["in_preparation"]
    out.append(
        f'<section id="{slug(ip["title"])}"><h2>{e(ip["title"])}</h2><p class="blurb">{e(ip["blurb"])}</p>'
        "<ul>" + "".join(f"<li>{e(i)}</li>" for i in ip["items"]) + "</ul></section>"
    )
    return "".join(out)


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%%NAME%%: portfolio</title>
<meta name="description" content="%%TAGLINE%%">
<style>
:root{--bg:#ffffff;--fg:#1f2328;--mute:#59636e;--line:#d0d7de;--card:#f6f8fa;--accent:#0969da;--chip:#eaeef2;--chip-fg:#1f2328;--ok:#1a7f37;--ok-bg:#dafbe1;--info:#0969da;--info-bg:#ddf4ff;--prep:#59636e;--prep-bg:#eaeef2;--pre:#f6f8fa}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0d1117;--fg:#e6edf3;--mute:#8d96a0;--line:#30363d;--card:#161b22;--accent:#4493f8;--chip:#21262d;--chip-fg:#e6edf3;--ok:#3fb950;--ok-bg:#12261e;--info:#4493f8;--info-bg:#121d2f;--prep:#8d96a0;--prep-bg:#21262d;--pre:#161b22}}
:root[data-theme="dark"]{--bg:#0d1117;--fg:#e6edf3;--mute:#8d96a0;--line:#30363d;--card:#161b22;--accent:#4493f8;--chip:#21262d;--chip-fg:#e6edf3;--ok:#3fb950;--ok-bg:#12261e;--info:#4493f8;--info-bg:#121d2f;--prep:#8d96a0;--prep-bg:#21262d;--pre:#161b22}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;overflow-x:hidden}
code,pre,.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace}
main{max-width:1040px;margin:0 auto;padding:36px 16px 56px}
h1{font-size:1.9rem;line-height:1.2;margin:0 0 4px;letter-spacing:-.01em}
.tag{font-size:1.05rem;color:var(--mute);margin:0 0 10px;max-width:64ch}
.meta{margin:0 0 14px;display:flex;flex-wrap:wrap;gap:6px}
.meta code,.stack code{display:inline-block;padding:2px 8px;border-radius:6px;background:var(--chip);color:var(--chip-fg);font-size:.8rem}
.intro{max-width:72ch;margin:0 0 16px}
.cta{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 22px}
.cta a{padding:7px 12px;border-radius:6px;border:1px solid var(--line);color:var(--fg);text-decoration:none;font-weight:600;font-size:.92rem}
.cta a.primary{background:var(--accent);color:#fff;border-color:var(--accent)}
.cta a:hover{border-color:var(--accent)}
hr{border:0;border-top:1px solid var(--line);margin:0 0 20px}
h2{font-size:1.25rem;margin:28px 0 6px}
h3{font-size:1rem;margin:0}
.blurb{color:var(--mute);margin:0 0 12px;max-width:76ch}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px}
.grid3{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}
.card,.start{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:14px 14px 8px}
.card header{display:flex;justify-content:space-between;align-items:flex-start;gap:8px;margin-bottom:6px}
.card p{margin:0 0 8px}
.stack{display:flex;flex-wrap:wrap;gap:4px}
.proof{color:var(--mute);font-size:.9rem}
.lab{display:inline-block;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.72rem;color:var(--accent);margin-right:6px}
.st{flex:none;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.72rem;padding:2px 8px;border-radius:999px;border:1px solid transparent}
.st-live{color:var(--ok);background:var(--ok-bg)}
.st-demo{color:var(--info);background:var(--info-bg)}
.st-prep{color:var(--prep);background:var(--prep-bg)}
.who{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.78rem;color:var(--mute);margin-bottom:8px}
.links{display:flex;flex-wrap:wrap;gap:6px}
.pill{display:inline-block;padding:3px 10px;border-radius:999px;background:var(--chip);color:var(--chip-fg);text-decoration:none;font-size:.84rem;font-weight:600}
.pill:hover{outline:1px solid var(--accent)}
ul{padding-left:20px;margin:0 0 8px;max-width:80ch}
li{margin:3px 0}
pre{background:var(--pre);border:1px solid var(--line);border-radius:8px;padding:12px 14px;overflow-x:auto;font-size:.84rem;line-height:1.45;margin:0 0 10px}
a{color:inherit}
a.more{font-weight:600;color:var(--accent)}
footer{margin-top:36px;padding-top:14px;border-top:1px solid var(--line);color:var(--mute);font-size:.86rem}
@media (max-width:480px){h1{font-size:1.6rem}main{padding:24px 16px 40px}}
</style>
</head>
<body>
<main>
<header>
<h1>%%NAME%%</h1>
<p class="tag">%%TAGLINE%%</p>
<p class="meta">%%META%%</p>
<p class="intro">%%INTRO%%</p>
<p class="cta"><a class="primary" href="demo/">Live demo</a><a href="projects/client-book-dashboards/dashboards-hub.html">All four dashboards</a><a href="%%BUILD_HREF%%">How I build with Claude</a><a href="%%REPO%%">GitHub</a><a href="%%LINKEDIN%%">LinkedIn</a></p>
</header>
<hr>
<section id="start-here"><h2>Start here</h2>%%START%%</section>
<h2 id="projects">Projects</h2>
%%PROJECTS%%
<section id="how-i-build"><h2>%%BUILD_TITLE%%</h2><ul>%%BUILD%%</ul><a class="more" href="%%BUILD_HREF%%">Full page</a></section>
<section id="repo-map"><h2>Repo map</h2><pre>%%TREE%%</pre></section>
<section id="run-locally"><h2>Run locally</h2><pre>%%RUN%%</pre><p class="blurb">%%RUN_NOTE%%</p></section>
<section id="what-this-proves"><h2>What this proves</h2><ul>%%PROVES%%</ul></section>
<footer>v%%VERSION%% · %%UPDATED%% · %%EMAIL%% · generated from <a href="%%JSON%%">portfolio.json</a></footer>
</main>
</body>
</html>
"""


def build_index():
    per = P["person"]
    rep = {
        "NAME": e(per["name"]),
        "TAGLINE": e(per["tagline"]),
        "META": "".join(f"<code>{e(m)}</code>" for m in per["meta"]),
        "INTRO": e(per["intro"]),
        "BUILD_HREF": e(site_href(P["build"]["href"])),
        "REPO": e(P["repo"]),
        "LINKEDIN": e(per["linkedin"]),
        "START": h_start(),
        "PROJECTS": h_projects(),
        "BUILD_TITLE": e(P["build"]["title"]),
        "BUILD": "".join(f"<li>{e(s)}</li>" for s in P["build"]["summary"]),
        "TREE": e(P["tree"]),
        "RUN": e(P["run"]),
        "RUN_NOTE": e(P["run_note"]),
        "PROVES": "".join(f"<li>{e(s)}</li>" for s in P["proves"]),
        "VERSION": e(P["version"]),
        "UPDATED": e(P["updated"]),
        "EMAIL": e(per["email"]),
        "JSON": e(GH_BLOB + "portfolio.json"),
    }
    page = TEMPLATE
    for k, v in rep.items():
        page = page.replace("%%" + k + "%%", v)
    (ROOT / "index.html").write_text(page)


if __name__ == "__main__":
    build_readme()
    build_index()
    print("wrote README.md and index.html")
