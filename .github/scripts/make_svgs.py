"""Builds the hand-made animated SVGs in assets/ (banner, how-we-work, timeline,
languages, now, divider). Run: python3 .github/scripts/make_svgs.py assets
Animations rest on the final frame and animate *from* hidden, so static
renderers (GitHub mobile, link previews) never show a blank card."""
import base64, sys
out = sys.argv[1]
logo = base64.b64encode(open(f"{out}/cork-ai-mark.png","rb").read()).decode()
MONO = "ui-monospace, 'JetBrains Mono', Menlo, monospace"
SANS = "-apple-system, 'SF Pro Display', 'Segoe UI', Helvetica, Arial, sans-serif"

banner = f'''<?xml version="1.0" encoding="UTF-8"?>
<!-- Hero banner, Cork AI Consulting blue (#0066cc / #2997ff on black).
     Built by hand: CSS animation on transform/opacity only, SMIL-free, no JS,
     and the logo is inlined as a data URI because SVGs served as <img> cannot
     fetch anything external. -->
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1200 330" width="1200" height="330" role="img" aria-label="Murilo Reis — AI and Automation Engineer, Co-Founder of Cork AI Consulting, Cork, Ireland">
  <title>Murilo Reis — AI &amp; Automation Engineer · Co-Founder, Cork AI Consulting</title>
  <defs>
    <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#2997ff" stop-opacity="0.38"/>
      <stop offset="55%" stop-color="#0066cc" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#0066cc" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#000000"/>
      <stop offset="60%" stop-color="#050a14"/>
      <stop offset="100%" stop-color="#0a1a33"/>
    </linearGradient>
    <linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#0066cc" stop-opacity="0"/>
      <stop offset="20%" stop-color="#0066cc"/>
      <stop offset="80%" stop-color="#2997ff"/>
      <stop offset="100%" stop-color="#2997ff" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#2997ff" stop-opacity="0"/>
      <stop offset="50%" stop-color="#2997ff" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#2997ff" stop-opacity="0"/>
    </linearGradient>
    <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
      <path d="M32 0H0V32" fill="none" stroke="#2997ff" stroke-opacity="0.07"/>
    </pattern>
    <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="1" fill="#2997ff" opacity="0.045"/>
    </pattern>
    <clipPath id="frame"><rect width="1200" height="330" rx="14"/></clipPath>
    <clipPath id="tickclip"><rect x="56" y="284" width="560" height="24"/></clipPath>
    <clipPath id="typed"><rect class="type" x="56" y="168" width="560" height="40"/></clipPath>
    <style>
      .spin   {{ transform-box: view-box; transform-origin: 960px 160px; animation: spin 38s linear infinite; }}
      .spinr  {{ transform-box: view-box; transform-origin: 960px 160px; animation: spin 26s linear infinite reverse; }}
      .breath {{ transform-box: fill-box; transform-origin: center; animation: breath 5s ease-in-out infinite; }}
      .float  {{ animation: float 6s ease-in-out infinite; }}
      .sweep  {{ animation: sweep 8s cubic-bezier(.4,0,.6,1) infinite; }}
      .cursor {{ animation: blink 1s steps(1) infinite; }}
      .type   {{ transform-box: fill-box; transform-origin: left; animation: type 7s steps(26, end) infinite; }}
      .pulse  {{ animation: pulse 2.6s ease-in-out infinite; }}
      .tick   {{ animation: tick 30s linear infinite; }}
      .tw     {{ animation: pulse 3s ease-in-out infinite; }}
      .tw:nth-of-type(3n)   {{ animation-delay: -1s; }}
      .tw:nth-of-type(3n+1) {{ animation-delay: -2s; }}
      @keyframes spin   {{ to {{ transform: rotate(360deg); }} }}
      @keyframes breath {{ 0%,100% {{ transform: scale(1); opacity: .85; }} 50% {{ transform: scale(1.08); opacity: 1; }} }}
      @keyframes float  {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-6px); }} }}
      @keyframes sweep  {{ 0% {{ transform: translateX(-400px); }} 100% {{ transform: translateX(1250px); }} }}
      @keyframes blink  {{ 0%,49% {{ opacity: 1; }} 50%,100% {{ opacity: 0; }} }}
      @keyframes type   {{ 0%,40% {{ transform: scaleX(1); }} 50% {{ transform: scaleX(0); }} 85%,100% {{ transform: scaleX(1); }} }}
      @keyframes pulse  {{ 0%,100% {{ opacity: .35; }} 50% {{ opacity: 1; }} }}
      @keyframes tick   {{ to {{ transform: translateX(-1200px); }} }}
      @media (prefers-reduced-motion: reduce) {{
        .spin,.spinr,.breath,.float,.sweep,.cursor,.type,.pulse,.tick,.tw {{ animation: none; }}
      }}
    </style>
  </defs>
  <g clip-path="url(#frame)">
    <rect width="1200" height="330" fill="url(#bg)"/>
    <rect width="1200" height="330" fill="url(#grid)"/>
    <circle cx="960" cy="160" r="230" fill="url(#glow)"/>

    <g fill="#9cc9ff">
      <circle class="tw" cx="720" cy="40" r="1.3"/><circle class="tw" cx="760" cy="270" r="1.1"/>
      <circle class="tw" cx="1150" cy="50" r="1.5"/><circle class="tw" cx="1170" cy="250" r="1.2"/>
      <circle class="tw" cx="1100" cy="290" r="1"/><circle class="tw" cx="800" cy="120" r="1.2"/>
      <circle class="tw" cx="690" cy="200" r="1"/><circle class="tw" cx="1120" cy="140" r="1.1"/>
    </g>

    <!-- orbit rings around the mark -->
    <g class="spin" fill="none" stroke="#2997ff">
      <circle cx="960" cy="160" r="128" stroke-opacity="0.35" stroke-dasharray="2 9"/>
      <circle cx="1088" cy="160" r="5" fill="#2997ff" stroke="none"/>
      <circle cx="832" cy="160" r="3" fill="#9cc9ff" stroke="none"/>
    </g>
    <g class="spinr" fill="none" stroke="#0066cc">
      <circle cx="960" cy="160" r="104" stroke-opacity="0.55" stroke-dasharray="60 18 4 18"/>
      <circle cx="960" cy="56" r="4" fill="#2997ff" stroke="none"/>
    </g>
    <circle class="breath" cx="960" cy="160" r="84" fill="#ffffff" fill-opacity="0.97"/>
    <g class="float">
      <image x="896" y="96" width="128" height="128" xlink:href="data:image/png;base64,{logo}" href="data:image/png;base64,{logo}"/>
    </g>
    <text x="960" y="312" font-family="{MONO}" font-size="11" fill="#2997ff" text-anchor="middle" letter-spacing="3" class="pulse">● CORKAICONSULTING.IE</text>

    <g font-family="{MONO}">
      <rect x="0" y="0" width="1200" height="34" fill="#000" fill-opacity="0.6"/>
      <circle cx="22" cy="17" r="5" fill="#ff5f57"/><circle cx="40" cy="17" r="5" fill="#febc2e"/><circle cx="58" cy="17" r="5" fill="#28c840"/>
      <text x="82" y="22" font-size="12" fill="#6e7681" letter-spacing="1.2">murilo@cork: ~/cork-ai-consulting — zsh</text>
      <text x="56" y="84" font-size="14" fill="#2997ff" letter-spacing="2.4">$ whoami</text>
    </g>
    <text x="54" y="150" font-family="{SANS}" font-size="62" font-weight="700" fill="#f5f5f7" letter-spacing="-1.5">Murilo Reis</text>
    <g clip-path="url(#typed)">
      <text x="56" y="198" font-family="{MONO}" font-size="24" font-weight="700" fill="#2997ff">AI &amp; Automation Engineer_</text>
    </g>
    <g font-family="{MONO}">
      <rect x="56" y="222" width="372" height="32" rx="16" fill="#0066cc" fill-opacity="0.18" stroke="#2997ff" stroke-opacity="0.6"/>
      <circle class="pulse" cx="76" cy="238" r="5" fill="#2997ff"/>
      <text x="92" y="243" font-size="13" font-weight="700" fill="#cfe5ff" letter-spacing="1.6">CO-FOUNDER · CORK AI CONSULTING</text>
      <text x="444" y="243" font-size="13" fill="#8b949e">Cork, Ireland 🇮🇪</text>
    </g>
    <rect x="56" y="272" width="560" height="2" fill="url(#rule)"/>

    <!-- stack ticker -->
    <g clip-path="url(#tickclip)" font-family="{MONO}" font-size="12" fill="#6e7681" letter-spacing="2">
      <g class="tick">
        <text x="56" y="300">PYTHON · SQL · SNOWFLAKE · BIGQUERY · CLAUDE CODE · CLAUDE API · AGENTS · PLAYWRIGHT · RPA · NODE · VERCEL · TABLEAU ·</text>
        <text x="1256" y="300">PYTHON · SQL · SNOWFLAKE · BIGQUERY · CLAUDE CODE · CLAUDE API · AGENTS · PLAYWRIGHT · RPA · NODE · VERCEL · TABLEAU ·</text>
      </g>
    </g>

    <rect class="sweep" x="0" y="0" width="360" height="330" fill="url(#sweep)" opacity="0.5"/>
    <rect width="1200" height="330" fill="url(#scan)"/>
  </g>
  <rect x="0.5" y="0.5" width="1199" height="329" rx="14" fill="none" stroke="#2997ff" stroke-opacity="0.25"/>
</svg>
'''
open(f"{out}/banner.svg","w").write(banner)

# ---- how we work pipeline ----
steps = [("01","MEETUP","free · monthly"),("02","DISCOVERY CALL","free · 30 min"),
         ("03","AI ASSESSMENT","find the 5+ hours"),("04","IMPLEMENTATION","done for you"),
         ("05","AI CONCIERGE","ongoing support")]
xs = [130, 365, 600, 835, 1070]
nodes = ""
for i,(n,t,s) in enumerate(zip([a for a,_,_ in steps],[b for _,b,_ in steps],[c for _,_,c in steps])):
    x = xs[i]; d = i*1.2
    nodes += f'''
    <g>
      <circle cx="{x}" cy="150" r="34" fill="#050a14" stroke="#2997ff" stroke-opacity="0.35" stroke-width="1.5"/>
      <circle class="lit" style="animation-delay:{d}s" cx="{x}" cy="150" r="34" fill="#0066cc" fill-opacity="0.25" stroke="#2997ff" stroke-width="2"/>
      <text x="{x}" y="157" text-anchor="middle" font-family="{MONO}" font-size="19" font-weight="700" fill="#f5f5f7">{n}</text>
      <text x="{x}" y="212" text-anchor="middle" font-family="{MONO}" font-size="13" font-weight="700" fill="#cfe5ff" letter-spacing="1.4">{t}</text>
      <text x="{x}" y="232" text-anchor="middle" font-family="{MONO}" font-size="12" fill="#8b949e">{s}</text>
    </g>'''
pipeline = f'''<?xml version="1.0" encoding="UTF-8"?>
<!-- Cork AI Consulting offer ladder. No prices on purpose: offer.md is the
     only place prices live. A pulse travels the line and lights each step. -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 270" width="1200" height="270" role="img" aria-label="How Cork AI Consulting works: meetup, discovery call, AI assessment, implementation, AI concierge">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#000"/><stop offset="1" stop-color="#0a1a33"/></linearGradient>
    <linearGradient id="trail" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2997ff" stop-opacity="0"/><stop offset="1" stop-color="#2997ff"/></linearGradient>
    <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#2997ff" stroke-opacity="0.06"/></pattern>
    <style>
      .lit   {{ opacity: 0; animation: lit 6s ease-in-out infinite; }}
      .runner{{ animation: run 6s linear infinite; }}
      .dash  {{ animation: dash 1.2s linear infinite; }}
      @keyframes lit  {{ 0%,100% {{ opacity: 0; }} 8%,30% {{ opacity: 1; }} 45% {{ opacity: 0; }} }}
      @keyframes run  {{ 0% {{ transform: translateX(0); }} 100% {{ transform: translateX(940px); }} }}
      @keyframes dash {{ to {{ stroke-dashoffset: -16; }} }}
      @media (prefers-reduced-motion: reduce) {{ .lit,.runner,.dash {{ animation: none; }} .lit {{ opacity: .6; }} }}
    </style>
  </defs>
  <rect width="1200" height="270" rx="14" fill="url(#bg)"/>
  <rect width="1200" height="270" rx="14" fill="url(#grid)"/>
  <rect x="0.5" y="0.5" width="1199" height="269" rx="14" fill="none" stroke="#2997ff" stroke-opacity="0.25"/>
  <text x="40" y="48" font-family="{MONO}" font-size="13" fill="#2997ff" letter-spacing="2">$ cork-ai --how-we-work</text>
  <text x="1160" y="48" text-anchor="end" font-family="{MONO}" font-size="12" fill="#6e7681" letter-spacing="1.5">FOR CORK &amp; MUNSTER BUSINESSES</text>
  <line class="dash" x1="130" y1="150" x2="1070" y2="150" stroke="#2997ff" stroke-opacity="0.5" stroke-width="2" stroke-dasharray="8 8"/>
  <g class="runner"><rect x="70" y="148" width="60" height="4" rx="2" fill="url(#trail)"/><circle cx="130" cy="150" r="6" fill="#ffffff"/><circle cx="130" cy="150" r="12" fill="#2997ff" fill-opacity="0.35"/></g>
  {nodes}
</svg>
'''
open(f"{out}/how-we-work.svg","w").write(pipeline)

# ---- experience timeline ----
jobs = [("2021–22","IT Assistant","Marcelo Tostes Advogados"),("2022–24","Data Analyst","Porto · São Paulo"),
        ("2024–26","Freelance","Data &amp; Automation Engineer"),("2025–26","Data Analyst","Apple · EMEIA Sales BPR"),
        ("2026 →","Co-Founder","Cork AI Consulting")]
xs = [120, 360, 600, 840, 1080]
items=""
for i,(y,r,c) in enumerate(jobs):
    x=xs[i]; now = i==4; d=0.3+i*0.35
    items += f'''
  <g class="pop" style="animation-delay:{d}s">
    {'<circle class="ring" cx="%d" cy="120" r="10" fill="none" stroke="#2997ff" stroke-width="2"/>' % x if now else ''}
    <circle cx="{x}" cy="120" r="{9 if now else 7}" fill="{'#2997ff' if now else '#050a14'}" stroke="#2997ff" stroke-width="2"/>
    <text x="{x}" y="88" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{'#2997ff' if now else '#8b949e'}" letter-spacing="1">{y}</text>
    <text x="{x}" y="160" text-anchor="middle" font-family="{SANS}" font-size="17" font-weight="700" fill="#f5f5f7">{r}</text>
    <text x="{x}" y="182" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="#8b949e">{c}</text>
  </g>'''
timeline = f'''<?xml version="1.0" encoding="UTF-8"?>
<!-- Career timeline; facts from the vault's murilo-career-facts note. -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 220" width="1200" height="220" role="img" aria-label="Career: IT Assistant, Data Analyst at Porto, Freelance engineer, Data Analyst at Apple, Co-Founder of Cork AI Consulting">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#000"/><stop offset="1" stop-color="#0a1a33"/></linearGradient>
    <linearGradient id="line" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0066cc" stop-opacity="0.6"/><stop offset="1" stop-color="#2997ff"/></linearGradient>
    <style>
      .run {{ animation: run 4s ease-in-out infinite; }}
      .pop  {{ }}
      .ring {{ transform-box: fill-box; transform-origin: center; animation: ring 2s ease-out infinite; }}
      @keyframes run {{ 0% {{ transform: translateX(0); opacity: 0; }} 10% {{ opacity: 1; }} 90% {{ opacity: 1; }} 100% {{ transform: translateX(960px); opacity: 0; }} }}
      @keyframes pop  {{ from {{ opacity: 0; }} }}
      @keyframes ring {{ 0% {{ transform: scale(1); opacity: 1; }} 100% {{ transform: scale(2.6); opacity: 0; }} }}
      @media (prefers-reduced-motion: reduce) {{ .run,.ring {{ animation: none; }} .run {{ opacity: 0; }} }}
    </style>
  </defs>
  <rect width="1200" height="220" rx="14" fill="url(#bg)"/>
  <rect x="0.5" y="0.5" width="1199" height="219" rx="14" fill="none" stroke="#2997ff" stroke-opacity="0.25"/>
  <text x="40" y="40" font-family="{MONO}" font-size="13" fill="#2997ff" letter-spacing="2">$ git log --career --oneline</text>
  <line x1="120" y1="120" x2="1080" y2="120" stroke="url(#line)" stroke-width="3"/>
  <g class="run"><ellipse cx="120" cy="120" rx="34" ry="4" fill="#9cc9ff" opacity=".7"/></g>
  {items}
</svg>
'''
open(f"{out}/timeline.svg","w").write(timeline)

# ---- languages ----
langs=[("🇧🇷","Português","native",1.0),("🇬🇧","English","C2",0.95),("🇪🇸","Español","C1",0.8),
       ("🇫🇷","Français","B2",0.62),("🇮🇹","Italiano","B2",0.62)]
rows=""
for i,(f,n,l,p) in enumerate(langs):
    y=78+i*34; w=int(300*p)
    rows+=f'''
  <text x="32" y="{y+5}" font-size="17">{f}</text>
  <text x="64" y="{y+5}" font-family="{MONO}" font-size="13" fill="#f5f5f7">{n}</text>
  <rect x="180" y="{y-6}" width="300" height="10" rx="5" fill="#2997ff" fill-opacity="0.12"/>
  <rect x="180" y="{y-6}" width="{w}" height="10" rx="5" fill="url(#g)"/>
  <g clip-path="url(#c{i})"><rect class="shine" style="animation-delay:{i*0.3}s" x="140" y="{y-6}" width="40" height="10" fill="url(#sh)"/></g>
  <clipPath id="c{i}"><rect x="180" y="{y-6}" width="{w}" height="10" rx="5"/></clipPath>
  <text x="548" y="{y+4}" text-anchor="end" font-family="{MONO}" font-size="12" fill="#2997ff">{l}</text>'''
languages=f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 580 250" width="580" height="250" role="img" aria-label="Languages: Portuguese native, English C2, Spanish C1, French B2, Italian B2">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#000"/><stop offset="1" stop-color="#0a1a33"/></linearGradient>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0066cc"/><stop offset="1" stop-color="#2997ff"/></linearGradient>
    <linearGradient id="sh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
    <style>
      .shine {{ animation: shine 3.2s ease-in-out infinite; }}
      @keyframes shine {{ 0% {{ transform: translateX(0); }} 60%,100% {{ transform: translateX(360px); }} }}
      @media (prefers-reduced-motion: reduce) {{ .shine {{ animation: none; opacity: 0; }} }}
    </style>
  </defs>
  <rect width="580" height="250" rx="14" fill="url(#bg)"/>
  <rect x="0.5" y="0.5" width="579" height="249" rx="14" fill="none" stroke="#2997ff" stroke-opacity="0.25"/>
  <text x="32" y="40" font-family="{MONO}" font-size="13" fill="#2997ff" letter-spacing="2">$ locale -a</text>
  {rows}
</svg>
'''
open(f"{out}/languages.svg","w").write(languages)

# ---- now card ----
now=[("BUILDING","AI agents that do real back-office work"),("RUNNING","Cork AI Consulting with Douglas Woollam"),
     ("HOSTING","Cork AI Meetup — free, monthly"),("WRITING","the Cork AI blog, for local SMEs")]
rows=""
for i,(k,v) in enumerate(now):
    y=84+i*36
    rows+=f'''
  <g class="in" style="animation-delay:{0.2+i*0.45}s">
    <text x="32" y="{y}" font-family="{MONO}" font-size="12" font-weight="700" fill="#2997ff" letter-spacing="1.5">[{k}]</text>
    <text x="150" y="{y}" font-family="{MONO}" font-size="13" fill="#f5f5f7">{v}</text>
  </g>'''
nowsvg=f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 580 250" width="580" height="250" role="img" aria-label="Now: building AI agents, running Cork AI Consulting, hosting the Cork AI Meetup, writing the Cork AI blog">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#000"/><stop offset="1" stop-color="#0a1a33"/></linearGradient>
    <style>
      .in {{ }}
      .blink {{ animation: blink 1s steps(1) infinite; }}
      @keyframes in {{ from {{ opacity: 0; }} }}
      @keyframes blink {{ 50% {{ opacity: 0; }} }}
      @media (prefers-reduced-motion: reduce) {{ .in,.blink {{ animation: none; opacity: 1; }} }}
    </style>
  </defs>
  <rect width="580" height="250" rx="14" fill="url(#bg)"/>
  <rect x="0.5" y="0.5" width="579" height="249" rx="14" fill="none" stroke="#2997ff" stroke-opacity="0.25"/>
  <text x="32" y="40" font-family="{MONO}" font-size="13" fill="#2997ff" letter-spacing="2">$ tail -f now.log</text>
  {rows}
  <rect class="blink" x="32" y="218" width="10" height="16" fill="#2997ff"/>
</svg>
'''
open(f"{out}/now.svg","w").write(nowsvg)

divider=f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 14" width="1200" height="14" role="presentation">
  <defs>
    <linearGradient id="l" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0066cc" stop-opacity="0"/><stop offset=".5" stop-color="#0066cc" stop-opacity=".6"/><stop offset="1" stop-color="#0066cc" stop-opacity="0"/></linearGradient>
    <radialGradient id="p"><stop offset="0" stop-color="#9cc9ff"/><stop offset="1" stop-color="#2997ff" stop-opacity="0"/></radialGradient>
    <style>.p {{ animation: m 5s ease-in-out infinite alternate; }} @keyframes m {{ from {{ transform: translateX(0); }} to {{ transform: translateX(1080px); }} }} @media (prefers-reduced-motion: reduce) {{ .p {{ animation: none; }} }}</style>
  </defs>
  <rect y="6" width="1200" height="2" fill="url(#l)"/>
  <ellipse class="p" cx="60" cy="7" rx="60" ry="7" fill="url(#p)"/>
</svg>
'''
open(f"{out}/divider.svg","w").write(divider)
print("ok")
