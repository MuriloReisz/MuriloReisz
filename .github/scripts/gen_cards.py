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

# muriloreisz.com's palette.
BG = "#0d0d10"
ACCENT = "#a78bfa"
ACCENT2 = "#6d5ef0"
INK = "#f5f5f7"
MUTED = "#8a8a90"
LINE = "rgba(167,139,250,0.30)"

MONO = "ui-monospace, 'JetBrains Mono', Menlo, monospace"

# Languages GitHub reports that say nothing about what someone can do.
SKIP_LANGS = {"HTML", "CSS", "SCSS", "Dockerfile", "Makefile", "Batchfile", "Shell"}


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
    if TOKEN:
        try:
            repos = list_repos("/user/repos?affiliation=owner")
        except urllib.error.URLError as e:
            print(f"!! /user/repos unavailable ({e}); using the public listing")
    if not repos:
        repos = list_repos(f"/users/{USER}/repos")

    stars = sum(r.get("stargazers_count", 0) for r in repos)

    langs: dict[str, int] = {}
    for r in repos:
        if r.get("fork"):
            continue
        name = r.get("language")
        if not name or name in SKIP_LANGS:
            continue
        # Weight by repo size: one throwaway file should not outrank a project.
        langs[name] = langs.get(name, 0) + max(1, r.get("size", 1))

    return {
        "user": user,
        "repos": repos,
        "stars": stars,
        "langs": langs,
        "contribs": contribs,
    }


def stats_card(d: dict) -> str:
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
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="480" height="{h}" viewBox="0 0 480 {h}" role="img" aria-label="GitHub statistics for {esc(USER)}">',
        f"<title>GitHub statistics for {esc(USER)}</title>",
        "<defs><style>"
        ".r{animation:in .5s ease-out backwards}"
        "@keyframes in{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:none}}"
        "@media (prefers-reduced-motion:reduce){.r{animation:none}}"
        "</style></defs>",
        f'<rect width="480" height="{h}" rx="4" fill="{BG}" stroke="{LINE}"/>',
        f'<text x="24" y="34" font-family="{MONO}" font-size="12" fill="{ACCENT2}" letter-spacing="2">$ gh api /users/{esc(USER)}</text>',
        f'<text x="24" y="62" font-family="{MONO}" font-size="16" font-weight="700" fill="{ACCENT}" letter-spacing="1">STATISTICS</text>',
        f'<rect x="24" y="74" width="432" height="1" fill="{LINE}"/>',
    ]
    for i, (label, value) in enumerate(rows):
        y = 104 + i * 34
        parts += [
            f'<g class="r" style="animation-delay:{i * 90}ms">',
            f'<text x="24" y="{y}" font-family="{MONO}" font-size="13" fill="{MUTED}">{esc(label)}</text>',
            f'<text x="300" y="{y}" font-family="{MONO}" font-size="13" fill="{MUTED}" opacity="0.35">'
            + "." * 22 + "</text>",
            f'<text x="456" y="{y}" font-family="{MONO}" font-size="15" font-weight="700" fill="{INK}" text-anchor="end">{esc(value)}</text>',
            "</g>",
        ]
    parts.append("</svg>")
    return "\n".join(parts)


def langs_card(d: dict) -> str:
    langs = d["langs"]
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:6]
    total = sum(v for _, v in top) or 1
    ramp = ["#a78bfa", "#8b7cf5", "#6d5ef0", "#5b4fd6", "#4c3fb5", "#3b3191"]

    h = 92 + len(top) * 34
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="480" height="{h}" viewBox="0 0 480 {h}" role="img" aria-label="Most used languages">',
        "<title>Most used languages</title>",
        "<defs><style>"
        ".b{transform-origin:left center;animation:grow .8s cubic-bezier(.22,1,.36,1) backwards}"
        "@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
        "@media (prefers-reduced-motion:reduce){.b{animation:none}}"
        "</style></defs>",
        f'<rect width="480" height="{h}" rx="4" fill="{BG}" stroke="{LINE}"/>',
        f'<text x="24" y="34" font-family="{MONO}" font-size="12" fill="{ACCENT2}" letter-spacing="2">$ cloc --by-language</text>',
        f'<text x="24" y="62" font-family="{MONO}" font-size="16" font-weight="700" fill="{ACCENT}" letter-spacing="1">LANGUAGES</text>',
        f'<rect x="24" y="74" width="432" height="1" fill="{LINE}"/>',
    ]
    for i, (name, size) in enumerate(top):
        pct = size / total * 100
        y = 96 + i * 34
        parts += [
            f'<text x="24" y="{y + 11}" font-family="{MONO}" font-size="12.5" fill="{MUTED}">{esc(name)}</text>',
            f'<text x="456" y="{y + 11}" font-family="{MONO}" font-size="12.5" font-weight="700" fill="{INK}" text-anchor="end">{pct:.1f}%</text>',
            f'<rect x="24" y="{y + 17}" width="432" height="6" rx="3" fill="{ACCENT}" opacity="0.10"/>',
            f'<rect class="b" style="animation-delay:{i * 110}ms" x="24" y="{y + 17}" width="{max(4, 432 * pct / 100):.1f}" height="6" rx="3" fill="{ramp[i % len(ramp)]}"/>',
        ]
    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    d = collect()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "stats.svg").write_text(stats_card(d))
    (OUT / "langs.svg").write_text(langs_card(d))
    print(f"wrote {OUT}/stats.svg and {OUT}/langs.svg")
    print(f"  repos={len(d['repos'])} stars={d['stars']} contribs={d['contribs']}")
    print(f"  langs={sorted(d['langs'], key=lambda k: -d['langs'][k])[:6]}")


if __name__ == "__main__":
    main()
