#!/usr/bin/env python3
"""Renders the profile's stats and language cards as self-hosted SVG.

WHY THIS EXISTS
---------------
The README used github-readme-stats, streak-stats and github-profile-trophy.
All three are free Vercel apps shared by hundreds of thousands of profiles, and
all three rendered as blank boxes — they rate-limit, and there is no fixing
someone else's quota. A blank box on a profile is worse than no box.

So the numbers are fetched from the GitHub API here, in a scheduled workflow,
and committed as plain SVG to this repo's `output` branch. Same place the
contribution snake lands. Nothing at display time depends on anyone else.

Only the standard library and GITHUB_TOKEN. No third-party packages, so the
workflow needs no install step and cannot break on a dependency release.
"""
from __future__ import annotations

import json
import os
import pathlib
import urllib.error
import urllib.request

USER = os.environ.get("GH_USER", "MuriloReisz")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = pathlib.Path(os.environ.get("OUT_DIR", "dist"))

# muriloreisz.com's palette, in both themes.
#
# These were module-level constants, which silently made every card dark-only —
# fine while the README was dark-only too, wrong once the cards are served
# through <picture> with a prefers-color-scheme source. Each card function now
# takes a theme dict and is rendered twice.
#
# The violet accents are shared: they carry the brand and read on both grounds.
# Only the ground, the ink and the muted tone flip, and the light rule is darker
# than a straight inversion would give because a 30%-alpha violet hairline
# disappears on white.
THEMES: dict[str, dict[str, str]] = {
    "dark": {
        "bg": "#0d0d10",
        "accent": "#a78bfa",
        "accent2": "#6d5ef0",
        "ink": "#f5f5f7",
        "muted": "#8a8a90",
        "line": "rgba(167,139,250,0.30)",
        "well": "rgba(167,139,250,0.10)",
    },
    "light": {
        "bg": "#ffffff",
        "accent": "#6d5ef0",
        "accent2": "#4c3fb5",
        "ink": "#0d0d10",
        "muted": "#5f5f68",
        "line": "rgba(76,63,181,0.28)",
        "well": "rgba(109,94,240,0.10)",
    },
}

MONO = "ui-monospace, 'JetBrains Mono', Menlo, monospace"

# Where the case-study card gets its data. Served by PWebsite's work.json.ts,
# which derives it from the same `projects` array the site renders, so the count
# and the illustrative flags cannot drift from the site the way a hand-typed
# badge did.
WORK_FEED = os.environ.get("WORK_FEED", "https://muriloreisz.com/work.json")

# Languages GitHub reports that say nothing about what someone can do.
SKIP_LANGS = {"HTML", "CSS", "SCSS", "Dockerfile", "Makefile", "Batchfile", "Shell"}

# Linguist labels a .ipynb by its container, not its contents, so every line of
# Python in a notebook is reported as "Jupyter Notebook". Left alone that read
# 66.7% Jupyter / 4.1% Python, which describes the file format rather than the
# skill. Merging is the accurate call, not the flattering one: the code in those
# notebooks is Python. Excluding Jupyter instead would have been worse on both
# counts — Python would have fallen to ~12%, behind TypeScript.
MERGE_LANGS = {"Jupyter Notebook": "Python"}


def api(path: str) -> object:
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": f"{USER}-profile-cards",
            **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def graphql(query: str, variables: dict) -> dict:
    body = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={
            "Content-Type": "application/json",
            "User-Agent": f"{USER}-profile-cards",
            "Authorization": f"Bearer {TOKEN}",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def esc(s: str) -> str:
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def clip(s: str, n: int) -> str:
    """Truncate to n characters on a word boundary where possible.

    SVG has no text overflow: a string wider than its box does not ellipsize, it
    simply paints over whatever is beside it. Every variable-length string on a
    card goes through here.
    """
    s = " ".join(str(s).split())
    if len(s) <= n:
        return s
    cut = s[: n - 1]
    if " " in cut[n // 2 :]:
        cut = cut[: cut.rfind(" ")]
    return cut.rstrip(" ,.;:-") + "…"


def fetch_work() -> list[dict]:
    """Case studies from muriloreisz.com/work.json.

    Returns [] rather than raising: the site being briefly unreachable must
    degrade to a placeholder card, not take down the snake and the stats.
    """
    try:
        req = urllib.request.Request(
            WORK_FEED, headers={"User-Agent": f"{USER}-profile-cards"}
        )
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.load(r)
        projects = data.get("projects", [])
        return projects if isinstance(projects, list) else []
    except (urllib.error.URLError, ValueError, TimeoutError) as e:
        print(f"!! work feed unavailable ({e}); case-study card will be a placeholder")
        return []


def frame(t: dict, w: int, h: int, cmd: str, title: str, label: str) -> list[str]:
    """The chrome every card shares: border, `$ command` eyebrow, title, rule.

    Factored out because there were two cards and there are now five; the
    alternative was five copies of the same four elements drifting apart.
    """
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">',
        f"<title>{esc(label)}</title>",
        f'<rect width="{w}" height="{h}" rx="4" fill="{t["bg"]}" stroke="{t["line"]}"/>',
        f'<text x="24" y="34" font-family="{MONO}" font-size="12" fill="{t["accent2"]}" letter-spacing="2">{esc(cmd)}</text>',
        f'<text x="24" y="62" font-family="{MONO}" font-size="16" font-weight="700" fill="{t["accent"]}" letter-spacing="1">{esc(title)}</text>',
        f'<rect x="24" y="74" width="{w - 48}" height="1" fill="{t["line"]}"/>',
    ]


def collect() -> dict:
    user = api(f"/users/{USER}")

    # Contribution totals are GraphQL-only; REST has no equivalent. Degrade to
    # None rather than to zero, so a transient failure cannot silently publish a
    # card claiming no contributions.
    contribs = None
    if TOKEN:
        try:
            q = """
            query($login:String!) {
              user(login:$login) {
                contributionsCollection {
                  totalCommitContributions
                  totalPullRequestContributions
                  totalIssueContributions
                  contributionCalendar { totalContributions }
                }
              }
            }"""
            cc = graphql(q, {"login": USER})["data"]["user"]["contributionsCollection"]
            contribs = {
                "year": cc["contributionCalendar"]["totalContributions"],
                "commits": cc["totalCommitContributions"],
                "prs": cc["totalPullRequestContributions"],
                "issues": cc["totalIssueContributions"],
            }
        except (urllib.error.URLError, KeyError, TypeError) as e:
            print(f"!! contributions unavailable ({e}); card will omit them")

    # Prefer /user/repos, which includes private repos, so the language mix
    # reflects actual work rather than only what is public. But GITHUB_TOKEN in
    # Actions is a repo-scoped installation token, NOT a user token, so that
    # endpoint 403s there — which is what broke the first run of this workflow.
    # Fall back to the public listing rather than failing the build; a slightly
    # narrower language mix is a much better outcome than no cards at all.
    def list_repos(path: str) -> list[dict]:
        out: list[dict] = []
        page = 1
        while page <= 10:
            batch = api(f"{path}{'&' if '?' in path else '?'}per_page=100&page={page}")
            if not isinstance(batch, list) or not batch:
                break
            out.extend(batch)
            if len(batch) < 100:
                break
            page += 1
        return out

    repos: list[dict] = []
    # Whether the token can actually see this user's account, as opposed to just
    # this one repo. It decides more than the repo list: `contributionsCollection`
    # silently returns only the contributions VISIBLE TO THE TOKEN, so a
    # repo-scoped token reports a small, wrong number rather than an error.
    # In Actions that read 66 contributions / 0 PRs against real totals of
    # 166 / 11 — published for weeks as fact. Understating is still inaccurate,
    # so the cards now omit those figures rather than print the wrong ones.
    user_scoped = False
    if TOKEN:
        try:
            repos = list_repos("/user/repos?affiliation=owner")
            user_scoped = bool(repos)
        except urllib.error.URLError as e:
            print(f"!! /user/repos unavailable ({e}); using the public listing")
    if not repos:
        repos = list_repos(f"/users/{USER}/repos")

    stars = sum(r.get("stargazers_count", 0) for r in repos)

    # Language mix, per repo, from /languages rather than the list response's
    # single `language` field. Two reasons that field is not good enough: it is
    # frequently null in list responses (six of these repos report null while
    # plainly containing Java), and it only ever names ONE language per repo.
    #
    # Each repo is then normalised to contribute 1.0 in total, so the mix
    # answers "what does he work in" rather than "which repo has the most
    # bytes". Weighting raw bytes let a single notebook repo take 69% of the
    # card, because .ipynb files carry their own base64 output images inline.
    langs: dict[str, float] = {}
    for r in repos:
        if r.get("fork"):
            continue
        try:
            per_repo = api(f"/repos/{r['full_name']}/languages")
        except urllib.error.URLError as e:
            print(f"!! languages for {r.get('full_name')} unavailable ({e})")
            continue
        if not isinstance(per_repo, dict):
            continue
        usable = {k: v for k, v in per_repo.items() if k not in SKIP_LANGS and v > 0}
        total_bytes = sum(usable.values())
        if not total_bytes:
            continue
        for name, byts in usable.items():
            name = MERGE_LANGS.get(name, name)
            langs[name] = langs.get(name, 0.0) + byts / total_bytes

    return {
        "user": user,
        "repos": repos,
        "stars": stars,
        "langs": langs,
        "contribs": contribs if user_scoped else None,
        "user_scoped": user_scoped,
    }


def stats_card(d: dict, t: dict) -> str:
    u, c = d["user"], d["contribs"]
    # Never let "total" read lower than "public": if the authenticated repo
    # listing under-returns (a scope change, a truncated page), the pair would
    # be visible nonsense on a card that is meant to inspire confidence.
    total_repos = max(len(d["repos"]), u["public_repos"])
    rows = [
        ("Public repos", f'{u["public_repos"]}'),
        ("Total repos", f'{total_repos}'),
        ("Stars earned", f'{d["stars"]}'),
        ("Followers", f'{u["followers"]}'),
    ]
    if c:
        rows = [
            ("Contributions (1y)", f'{c["year"]:,}'),
            ("Commits (1y)", f'{c["commits"]:,}'),
            ("Pull requests", f'{c["prs"]:,}'),
        ] + rows[:3]

    h = 92 + len(rows) * 34
    parts = frame(
        t, 480, h, f"$ gh api /users/{USER}", "STATISTICS",
        f"GitHub statistics for {USER}",
    )
    parts.insert(
        2,
        "<defs><style>"
        ".r{animation:in .5s ease-out backwards}"
        "@keyframes in{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:none}}"
        "@media (prefers-reduced-motion:reduce){.r{animation:none}}"
        "</style></defs>",
    )
    for i, (label, value) in enumerate(rows):
        y = 104 + i * 34
        parts += [
            f'<g class="r" style="animation-delay:{i * 90}ms">',
            f'<text x="24" y="{y}" font-family="{MONO}" font-size="13" fill="{t["muted"]}">{esc(label)}</text>',
            f'<text x="300" y="{y}" font-family="{MONO}" font-size="13" fill="{t["muted"]}" opacity="0.35">'
            + "." * 22 + "</text>",
            f'<text x="456" y="{y}" font-family="{MONO}" font-size="15" font-weight="700" fill="{t["ink"]}" text-anchor="end">{esc(value)}</text>',
            "</g>",
        ]
    parts.append("</svg>")
    return "\n".join(parts)


def langs_card(d: dict, t: dict) -> str:
    langs = d["langs"]
    # Drop anything that would round to 0.0%: a bar labelled "0.0%" reads as a
    # rendering fault rather than as a small number.
    ranked = sorted(langs.items(), key=lambda kv: -kv[1])
    grand = sum(v for _, v in ranked) or 1
    ranked = [(k, v) for k, v in ranked if v / grand >= 0.005]
    top = ranked[:6]
    total = sum(v for _, v in top) or 1
    ramp = ["#a78bfa", "#8b7cf5", "#6d5ef0", "#5b4fd6", "#4c3fb5", "#3b3191"]

    h = 92 + len(top) * 34
    parts = frame(
        t, 480, h, "$ cloc --by-language", "LANGUAGES", "Most used languages"
    )
    parts.insert(
        2,
        "<defs><style>"
        ".b{transform-origin:left center;animation:grow .8s cubic-bezier(.22,1,.36,1) backwards}"
        "@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
        "@media (prefers-reduced-motion:reduce){.b{animation:none}}"
        "</style></defs>",
    )
    for i, (name, size) in enumerate(top):
        pct = size / total * 100
        y = 96 + i * 34
        parts += [
            f'<text x="24" y="{y + 11}" font-family="{MONO}" font-size="12.5" fill="{t["muted"]}">{esc(name)}</text>',
            f'<text x="456" y="{y + 11}" font-family="{MONO}" font-size="12.5" font-weight="700" fill="{t["ink"]}" text-anchor="end">{pct:.1f}%</text>',
            f'<rect x="24" y="{y + 17}" width="432" height="6" rx="3" fill="{t["accent"]}" opacity="0.10"/>',
            f'<rect class="b" style="animation-delay:{i * 110}ms" x="24" y="{y + 17}" width="{max(4, 432 * pct / 100):.1f}" height="6" rx="3" fill="{ramp[i % len(ramp)]}"/>',
        ]
    parts.append("</svg>")
    return "\n".join(parts)


def showcase_card(d: dict, t: dict) -> str:
    """Top repositories, generated from the same data the stats card uses.

    Replaces a hand-maintained three-row HTML table in the README, which had
    already drifted: it still listed three repos long after there were more, and
    nothing kept it honest.

    Ranked by stars, then by recency. Forks and archived repos are excluded —
    an archived repo is deliberately-kept history, not a thing to lead with.
    """
    repos = [
        r for r in d["repos"]
        if not r.get("fork") and not r.get("archived") and not r.get("private")
        # The profile repo renders this very card; listing it is noise.
        and r.get("name") != USER
    ]
    # Most recently pushed first, THEN stable-sorted by stars, so the star
    # ranking wins and recency breaks its ties. Doing it in one key with
    # `pushed_at` ascending put the oldest repo on top the moment every repo
    # had zero stars — which is this account today, and it led the card with a
    # 2023 repo whose description is "TesteRepositorioLinkandoGit".
    repos.sort(key=lambda r: r.get("pushed_at") or "", reverse=True)
    repos.sort(key=lambda r: -r.get("stargazers_count", 0))
    top = repos[:5]

    row_h = 46
    h = 92 + len(top) * row_h + 8
    parts = frame(
        t, 980, h, "$ gh repo list --sort stars", "SELECTED REPOSITORIES",
        "Selected repositories",
    )
    parts.insert(
        2,
        "<defs><style>"
        ".sr{animation:fade .5s ease-out backwards}"
        "@keyframes fade{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}"
        "@media (prefers-reduced-motion:reduce){.sr{animation:none}}"
        "</style></defs>",
    )
    for i, r in enumerate(top):
        y = 104 + i * row_h
        lang = r.get("language") or "—"
        stars = r.get("stargazers_count", 0)
        desc = clip(r.get("description") or "no description", 74)
        parts += [
            f'<g class="sr" style="animation-delay:{i * 80}ms">',
            f'<text x="24" y="{y}" font-family="{MONO}" font-size="13.5" font-weight="700" fill="{t["accent"]}">{esc(clip(r["name"], 30))}</text>',
            f'<text x="24" y="{y + 18}" font-family="{MONO}" font-size="11.5" fill="{t["muted"]}">{esc(desc)}</text>',
            # Right-aligned metadata, so a long name never collides with it.
            f'<text x="956" y="{y}" font-family="{MONO}" font-size="11.5" fill="{t["muted"]}" text-anchor="end">{esc(lang)}  ★ {stars}</text>',
            f'<rect x="24" y="{y + 28}" width="932" height="1" fill="{t["line"]}" opacity="0.5"/>',
            "</g>",
        ]
    parts.append("</svg>")
    return "\n".join(parts)


def trophies_card(d: dict, t: dict) -> str:
    """An achievements strip computed from data already in `collect()`.

    The README used github-profile-trophy until it rate-limited into a blank
    box. This is the self-hosted replacement, and unlike that widget every tier
    here is derived from a real number rather than from an opaque ranking.
    """
    u, c = d["user"], d["contribs"]
    langs = len([k for k, v in d["langs"].items() if v >= 0.05])
    repos = max(len(d["repos"]), u["public_repos"])

    def tier(value: int, bronze: int, silver: int, gold: int) -> str:
        if value >= gold:
            return "GOLD"
        if value >= silver:
            return "SILVER"
        if value >= bronze:
            return "BRONZE"
        return ""

    # Only tiles whose number is both available and meaningful. Two rules,
    # both learned from publishing the opposite:
    #
    #   - contribution tiles appear only when the token can actually see the
    #     account (see `user_scoped` in collect()); otherwise they would show a
    #     figure roughly a third of the truth,
    #   - a tile whose value is 0 is dropped entirely. "STARS 0 —" reads as a
    #     broken widget rather than as a modest number, which is exactly the
    #     failure this card was built to replace.
    candidates = [
        ("POLYGLOT", langs, tier(langs, 3, 5, 7), "languages"),
        ("BUILDER", repos, tier(repos, 5, 15, 30), "repositories"),
        ("STARS", d["stars"], tier(d["stars"], 1, 10, 50), "earned"),
    ]
    if c:
        candidates = [
            ("COMMITS", c["commits"], tier(c["commits"], 100, 400, 1000), "1y"),
            ("ACTIVITY", c["year"], tier(c["year"], 150, 600, 1500), "contributions"),
            ("REVIEWS", c["prs"], tier(c["prs"], 5, 25, 100), "pull requests"),
        ] + candidates

    items = [
        (label, f"{value:,}", rank, unit)
        for label, value, rank, unit in candidates
        if value > 0
    ][:5]
    if not items:
        raise RuntimeError("no non-zero achievement available")
    tier_fill = {
        "GOLD": "#f2c811",
        "SILVER": "#c8c8d0",
        "BRONZE": "#c8874a",
        "": t["muted"],
    }

    w, h = 980, 168
    gap = 12
    tile_w = (w - 48 - gap * (len(items) - 1)) // len(items)
    parts = frame(t, w, h, "$ ./achievements --all", "ACHIEVEMENTS", "Achievements")
    parts.insert(
        2,
        "<defs><style>"
        ".tp{animation:pop .5s cubic-bezier(.22,1,.36,1) backwards}"
        "@keyframes pop{from{opacity:0;transform:scale(.94)}to{opacity:1;transform:none}}"
        "@media (prefers-reduced-motion:reduce){.tp{animation:none}}"
        "</style></defs>",
    )
    for i, (label, value, rank, unit) in enumerate(items):
        x = 24 + i * (tile_w + gap)
        parts += [
            f'<g class="tp" style="animation-delay:{i * 70}ms; transform-origin:{x + tile_w / 2}px 130px">',
            f'<rect x="{x}" y="{92}" width="{tile_w}" height="{60}" rx="4" fill="{t["well"]}" stroke="{t["line"]}"/>',
            f'<text x="{x + tile_w / 2}" y="{110}" font-family="{MONO}" font-size="10" fill="{t["muted"]}" text-anchor="middle" letter-spacing="1.5">{esc(label)}</text>',
            f'<text x="{x + tile_w / 2}" y="{132}" font-family="{MONO}" font-size="19" font-weight="700" fill="{t["ink"]}" text-anchor="middle">{esc(value)}</text>',
            f'<text x="{x + tile_w / 2}" y="{146}" font-family="{MONO}" font-size="9" fill="{t["muted"]}" text-anchor="middle">{esc(unit)}</text>',
            f'<text x="{x + tile_w / 2}" y="{166}" font-family="{MONO}" font-size="9.5" font-weight="700" fill="{tier_fill[rank]}" text-anchor="middle" letter-spacing="1.5">{esc(rank)}</text>',
            "</g>",
        ]
    parts.append("</svg>")
    return "\n".join(parts)


def casestudies_card(work: list[dict], t: dict) -> str:
    """Case studies, read from muriloreisz.com/work.json.

    The count used to be typed into a badge by hand and drifted to "9" while the
    site defined 11. It is derived here instead, so it cannot.

    `illustrative` is rendered, never dropped. The site marks those entries as
    anonymised composite scenarios rather than delivered client results, and a
    card that repeated their figures without that marker would be making a
    claim the site is careful not to make.
    """
    real = [p for p in work if not p.get("illustrative")]
    illus = [p for p in work if p.get("illustrative")]
    # Delivered work first, then composites, newest first within each group.
    ordered = (
        sorted(real, key=lambda p: -p.get("year", 0))
        + sorted(illus, key=lambda p: -p.get("year", 0))
    )[:6]

    row_h = 40
    h = 92 + len(ordered) * row_h + 34
    parts = frame(
        t, 980, h, "$ curl muriloreisz.com/work.json",
        f"CASE STUDIES · {len(work)}", "Case studies",
    )
    parts.insert(
        2,
        "<defs><style>"
        ".cs{animation:slide .5s ease-out backwards}"
        "@keyframes slide{from{opacity:0;transform:translateX(-6px)}to{opacity:1;transform:none}}"
        "@media (prefers-reduced-motion:reduce){.cs{animation:none}}"
        "</style></defs>",
    )
    for i, p in enumerate(ordered):
        y = 104 + i * row_h
        marker = "illustrative" if p.get("illustrative") else "delivered"
        marker_fill = t["muted"] if p.get("illustrative") else t["accent"]
        parts += [
            f'<g class="cs" style="animation-delay:{i * 70}ms">',
            f'<text x="24" y="{y}" font-family="{MONO}" font-size="10" fill="{t["accent2"]}" letter-spacing="1.5">{esc(clip(p.get("eyebrow", ""), 18))}</text>',
            f'<text x="150" y="{y}" font-family="{MONO}" font-size="13" fill="{t["ink"]}">{esc(clip(p.get("title", ""), 62))}</text>',
            f'<text x="956" y="{y}" font-family="{MONO}" font-size="10" fill="{marker_fill}" text-anchor="end" letter-spacing="1">{esc(marker)}</text>',
            f'<rect x="24" y="{y + 12}" width="932" height="1" fill="{t["line"]}" opacity="0.4"/>',
            "</g>",
        ]
    # The legend is the point of the card, not decoration: it is what keeps a
    # composite figure from reading as a client result.
    parts += [
        f'<text x="24" y="{h - 18}" font-family="{MONO}" font-size="10" fill="{t["muted"]}">'
        "illustrative = anonymised composite scenario, not a named client engagement"
        "</text>",
        "</svg>",
    ]
    return "\n".join(parts)


def placeholder(title: str, note: str, t: dict, w: int = 480) -> str:
    """A card that says so, for when the API could not be reached.

    Deliberately NOT a blank or a failed build: a blank box is exactly the
    failure mode this whole script exists to remove, and taking the build down
    would also drop the snake and the banner, which have nothing wrong with
    them.
    """
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="126" '
        f'viewBox="0 0 {w} 126" role="img" aria-label="{esc(title)} unavailable">'
        f"<title>{esc(title)} temporarily unavailable</title>"
        f'<rect width="{w}" height="126" rx="4" fill="{t["bg"]}" stroke="{t["line"]}"/>'
        f'<text x="24" y="40" font-family="{MONO}" font-size="12" fill="{t["accent2"]}" letter-spacing="2">$ {esc(title.lower())}</text>'
        f'<text x="24" y="72" font-family="{MONO}" font-size="14" font-weight="700" fill="{t["accent"]}">TEMPORARILY UNAVAILABLE</text>'
        f'<text x="24" y="98" font-family="{MONO}" font-size="11.5" fill="{t["muted"]}">{esc(note)}</text>'
        "</svg>"
    )


# name -> (builder, placeholder width). Both themes of every entry are written
# on every run, so the workflow's verify step can assert on a fixed file list
# and a silent no-write cannot pass as a green build again.
CARDS = {
    "stats": (lambda d, work, t: stats_card(d, t), 480),
    "langs": (lambda d, work, t: langs_card(d, t), 480),
    "showcase": (lambda d, work, t: showcase_card(d, t), 980),
    "trophies": (lambda d, work, t: trophies_card(d, t), 980),
    "casestudies": (lambda d, work, t: casestudies_card(work, t), 980),
}


def write_all(d: dict | None, work: list[dict], log: list[str]) -> None:
    """Render every card in both themes, degrading per card rather than wholesale.

    A card that raises takes only itself down to a placeholder. That matters
    most for the case-study card: it depends on a network hop to the website,
    and the website being briefly down must not blank the GitHub-sourced cards
    beside it — which is what a single try/except around everything did.
    """
    for name, (build, width) in CARDS.items():
        for theme_name, theme in THEMES.items():
            suffix = "" if theme_name == "dark" else "-light"
            path = OUT / f"{name}{suffix}.svg"
            try:
                if d is None:
                    raise RuntimeError("GitHub data unavailable")
                if name == "casestudies" and not work:
                    raise RuntimeError("work feed empty")
                path.write_text(build(d, work, theme))
            except Exception as e:
                note = (
                    "the website did not answer on the last build"
                    if name == "casestudies"
                    else "the GitHub API did not answer on the last build"
                )
                path.write_text(placeholder(name, note, theme, width))
                log.append(f"!!  {path.name} -> placeholder ({e})")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    log: list[str] = []

    d: dict | None = None
    try:
        d = collect()
        # Computed OUT of the f-string on purpose. A lambda inside an f-string
        # replacement field is a SyntaxError before Python 3.12 — the colon in
        # "key=lambda k: ..." is parsed as the format-spec separator — and the
        # runner is not guaranteed to be 3.12. That single line failed this
        # workflow at import time, silently, for four consecutive builds.
        top_langs = sorted(d["langs"], key=lambda k: -d["langs"][k])[:6]
        log.append(f"OK  repos={len(d['repos'])} stars={d['stars']}")
        log.append(f"OK  contribs={d['contribs']}")
        log.append(f"OK  langs={top_langs}")
    except Exception:
        import traceback

        log.append("FAILED to collect GitHub data — those cards become placeholders")
        log.append(traceback.format_exc())

    work = fetch_work()
    if work:
        n_illus = sum(1 for p in work if p.get("illustrative"))
        log.append(f"OK  work={len(work)} illustrative={n_illus}")
    else:
        log.append("!!  work feed empty or unreachable")

    write_all(d, work, log)
    log.append("wrote: " + ", ".join(sorted(p.name for p in OUT.glob("*.svg"))))

    text = "\n".join(log)
    (OUT / "build.log").write_text(text + "\n")
    print(text)
    # Never take the build down: the snake and the banner are fine, and a
    # placeholder card is a better outcome than no cards at all.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
