"""Rewrite the README's ~/latest block from corkaiconsulting.ie/blog.

The site has no RSS feed, but every post is rendered into /blog as an
<article data-slug data-date> with its title, newest first. Parsing that is
less fragile than scraping the cards, and needs nothing beyond stdlib.
"""
import html
import http.client
import re
import sys
import urllib.request

BLOG = "https://www.corkaiconsulting.ie/blog"
README = "README.md"
START, END = "<!-- FEED:START -->", "<!-- FEED:END -->"
N = 5

ART = re.compile(
    r'<article class="post" data-slug="([^"]+)" data-tag="([^"]*)" data-date="([\d-]+)"'
    r'.*?<h2 class="post__title">(.*?)</h2>',
    re.S,
)


def main() -> int:
    req = urllib.request.Request(BLOG, headers={"User-Agent": "MuriloReisz-profile"})
    with urllib.request.urlopen(req, timeout=30) as r:
        try:
            raw = r.read()
        except http.client.IncompleteRead as e:
            # Posts come early in the page, newest first, so a truncated
            # body still carries them.
            raw = e.partial
    page = raw.decode("utf-8", "replace")
    posts = sorted(ART.findall(page), key=lambda p: p[2], reverse=True)[:N]
    if not posts:
        print("no posts parsed; leaving README untouched")
        return 0
    lines = ["```console", "murilo@cork:~$ ls -t ~/cork-ai/blog | head -5"]
    links = []
    for slug, tag, date, title in posts:
        title = html.unescape(re.sub(r"<[^>]+>", "", title)).strip()
        lines.append(f"{date}  [{tag.lower()}]  {title}")
        links.append(f"- [{title}]({BLOG}/{slug}) · `{date}`")
    lines.append("```")
    block = "\n".join([START, *lines, "", *links, END])
    with open(README, encoding="utf-8") as f:
        text = f.read()
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, text, flags=re.S)
    if new != text:
        with open(README, "w", encoding="utf-8") as f:
            f.write(new)
        print(f"updated with {len(posts)} posts")
    else:
        print("no change")
    return 0


if __name__ == "__main__":
    sys.exit(main())
