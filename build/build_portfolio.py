#!/usr/bin/env python3
"""Build README.md and index.html from portfolio.json, so the GitHub index and the
site never disagree. Stdlib only. Run from the repo root: python3 build/build_portfolio.py"""
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
P = json.loads((ROOT / "portfolio.json").read_text())
GH_BLOB = P["repo"] + "/blob/main/"
GH_TREE = P["repo"] + "/tree/main/"


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


# ---------- README ----------
def md_link(l):
    return f"[{l['label']}]({l['href']})"


def md_links(links):
    return " · ".join(md_link(l) for l in links)


def md_tracks():
    out = []
    for t in P["tracks"]:
        out.append(f"### {t['title']}\n\n{t['lead']}\n\n{md_links(t['links'])}")
    return "\n\n".join(out)


def md_projects():
    out = []
    for d in P["domains"]:
        rows = ["| Project | What it is | Proof | Links |", "|---|---|---|---|"]
        for pr in d["projects"]:
            links = md_links(pr["links"]) if pr.get("links") else pr.get("note", "")
            rows.append(f"| {pr['name']} | {pr['what']} | {pr['proof']} | {links} |")
        out.append(f"### {d['title']}\n\n{d['blurb']}\n\n" + "\n".join(rows))
    return "\n\n".join(out)


def md_prep():
    ip = P["in_preparation"]
    items = "\n".join(f"- {i}" for i in ip["items"])
    return f"### {ip['title']}\n\n{ip['blurb']}\n\n{items}"


def build_readme():
    per = P["person"]
    contacts = f"{per['email']} · [LinkedIn]({per['linkedin']}) · [Site]({P['site']})"
    t = (ROOT / "build" / "README.template.md").read_text()
    rep = {
        "NAME": per["name"],
        "TAGLINE": per["tagline"],
        "CONTACTS": contacts,
        "INTRO": per["intro"],
        "TRACKS": md_tracks(),
        "PROJECTS": md_projects(),
        "PREP": md_prep(),
        "BUILD_TITLE": P["build"]["title"],
        "BUILD": "\n".join(f"- {s}" for s in P["build"]["summary"]),
        "BUILD_HREF": P["build"]["href"],
        "PROVES": "\n".join(f"- {s}" for s in P["proves"]),
        "VERSION": P["version"],
        "UPDATED": P["updated"],
    }
    for k, v in rep.items():
        t = t.replace("{{" + k + "}}", v)
    (ROOT / "README.md").write_text(t)


# ---------- index.html ----------
def site_href(href):
    """Markdown pages render on GitHub; HTML apps are served by Pages next to this file."""
    if href.startswith("http") or href.startswith("#"):
        return href
    if href.endswith(".html") or href == "demo/":
        return href
    if href.endswith("/"):
        return GH_TREE + href
    return GH_BLOB + href


def e(s):
    return html.escape(s, quote=True)


def h_links(links):
    return " ".join(f'<a class="pill" href="{e(site_href(l["href"]))}">{e(l["label"])}</a>' for l in links)


def h_tracks():
    cards = []
    for t in P["tracks"]:
        cards.append(
            f'<article class="card"><h3>{e(t["title"])}</h3><p>{e(t["lead"])}</p>'
            f'<p class="links">{h_links(t["links"])}</p></article>'
        )
    return '<div class="grid">' + "".join(cards) + "</div>"


def h_projects():
    out = []
    for d in P["domains"]:
        cards = []
        for pr in d["projects"]:
            cards.append(
                f'<article class="card"><h3>{e(pr["name"])}</h3><p>{e(pr["what"])}</p>'
                f'<p class="proof"><span class="lab">Proof</span> {e(pr["proof"])}</p>'
                f'<p class="links">{h_links(pr["links"]) if pr.get("links") else e(pr.get("note", ""))}</p></article>'
            )
        out.append(
            f'<section id="{slug(d["title"])}"><h2>{e(d["title"])}</h2><p class="blurb">{e(d["blurb"])}</p>'
            f'<div class="grid">{"".join(cards)}</div></section>'
        )
    ip = P["in_preparation"]
    out.append(
        f'<section id="{slug(ip["title"])}"><h2>{e(ip["title"])}</h2><p class="blurb">{e(ip["blurb"])}</p><ul>'
        + "".join(f"<li>{e(i)}</li>" for i in ip["items"])
        + "</ul></section>"
    )
    return "".join(out)


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{name}: portfolio</title>
<meta name="description" content="{tagline}">
<style>
:root{{--bg:#fbfaf7;--fg:#1d2430;--mute:#5b6572;--line:#dcd8cf;--card:#ffffff;--accent:#9a6a2a;--accent-fg:#ffffff;--pill:#f1ece2;--pill-fg:#3a2e1a}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#171a1f;--fg:#e9e6df;--mute:#a7a39a;--line:#2d323a;--card:#1f242b;--accent:#d2a25c;--accent-fg:#1a1510;--pill:#2a2f37;--pill-fg:#e9e6df}}}}
:root[data-theme="dark"]{{--bg:#171a1f;--fg:#e9e6df;--mute:#a7a39a;--line:#2d323a;--card:#1f242b;--accent:#d2a25c;--accent-fg:#1a1510;--pill:#2a2f37;--pill-fg:#e9e6df}}
*{{box-sizing:border-box}}
html{{-webkit-text-size-adjust:100%}}
body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;overflow-x:hidden}}
main{{max-width:1040px;margin:0 auto;padding:40px 16px 56px}}
header.hero{{padding:8px 0 28px;border-bottom:1px solid var(--line);margin-bottom:28px}}
h1{{font-size:2.1rem;line-height:1.15;margin:0 0 6px;letter-spacing:-.01em}}
.tag{{font-size:1.15rem;color:var(--mute);margin:0 0 16px;max-width:60ch}}
.intro{{max-width:72ch;margin:0 0 18px}}
.cta a{{display:inline-block;margin:0 8px 8px 0;padding:9px 14px;border-radius:8px;border:1px solid var(--line);color:var(--fg);text-decoration:none;font-weight:600}}
.cta a.primary{{background:var(--accent);color:var(--accent-fg);border-color:var(--accent)}}
.cta a:hover{{border-color:var(--accent)}}
h2{{font-size:1.35rem;margin:34px 0 6px}}
h3{{font-size:1.05rem;margin:0 0 8px}}
.blurb{{color:var(--mute);margin:0 0 14px;max-width:72ch}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 16px 10px}}
.card p{{margin:0 0 10px}}
.proof{{color:var(--mute);font-size:.95rem}}
.lab{{display:inline-block;font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;color:var(--accent);font-weight:700;margin-right:4px}}
.links{{display:flex;flex-wrap:wrap;gap:6px}}
.pill{{display:inline-block;padding:4px 10px;border-radius:999px;background:var(--pill);color:var(--pill-fg);text-decoration:none;font-size:.86rem;font-weight:600}}
.pill:hover{{outline:1px solid var(--accent)}}
ul{{padding-left:20px;margin:0 0 10px;max-width:80ch}}
li{{margin:4px 0}}
a{{color:inherit}}
.build a.more{{display:inline-block;margin-top:6px;font-weight:600;color:var(--accent)}}
footer{{margin-top:40px;padding-top:16px;border-top:1px solid var(--line);color:var(--mute);font-size:.9rem}}
@media (max-width:480px){{h1{{font-size:1.7rem}}main{{padding:24px 16px 40px}}}}
</style>
</head>
<body>
<main>
<header class="hero">
<h1>{name}</h1>
<p class="tag">{tagline}</p>
<p class="intro">{intro}</p>
<p class="cta"><a class="primary" href="demo/">Open the live demo</a><a href="projects/client-book-dashboards/dashboards-hub.html">All four dashboards</a><a href="{build_href}">How I build with Claude</a><a href="{repo}">GitHub</a><a href="{linkedin}">LinkedIn</a></p>
</header>

<section id="start-here"><h2>Start here</h2>{tracks}</section>

<h2 id="projects">Projects</h2>
{projects}

<section id="how-i-build" class="build"><h2>{build_title}</h2><ul>{build_items}</ul><a class="more" href="{build_href}">Read the full page</a></section>

<section id="what-this-proves"><h2>What this proves</h2><ul>{proves}</ul></section>

<footer>Portfolio v{version}, updated {updated}. {email}. Built from <a href="{json_href}">portfolio.json</a>; the README on GitHub is built from the same file.</footer>
</main>
</body>
</html>
"""


def build_index():
    per = P["person"]
    page = TEMPLATE.format(
        name=e(per["name"]),
        tagline=e(per["tagline"]),
        intro=e(per["intro"]),
        build_href=e(site_href(P["build"]["href"])),
        repo=e(P["repo"]),
        linkedin=e(per["linkedin"]),
        tracks=h_tracks(),
        projects=h_projects(),
        build_title=e(P["build"]["title"]),
        build_items="".join(f"<li>{e(s)}</li>" for s in P["build"]["summary"]),
        proves="".join(f"<li>{e(s)}</li>" for s in P["proves"]),
        version=e(P["version"]),
        updated=e(P["updated"]),
        email=e(per["email"]),
        json_href=e(GH_BLOB + "portfolio.json"),
    )
    (ROOT / "index.html").write_text(page)


if __name__ == "__main__":
    build_readme()
    build_index()
    print("wrote README.md and index.html")
