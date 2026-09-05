# Animated 301-redirect terminal. SMIL animation, same technique as the
# snake/pacman graphs, so GitHub's camo proxy serves it animated.
S = 1.30                                  # type scale — GitHub shrinks the SVG to column width
W, H = 1000, int(392*S)
BG,WIN,BORDER = "#08070c","#0d0b14","#2a2436"
ACC,GREEN,WHITE,GREY,DIM = "#c2a4ff","#4ade80","#e6e1ee","#8a8199","#5a5368"
CYCLE = 11
def fs(n): return round(n*S,1)
def y(n):  return round(n*S,1)
CH = 9.63*fs(16)/16                       # mono advance at the scaled command size

import json,subprocess
def gh(args):
    return subprocess.run(["gh"]+args,capture_output=True,text=True,timeout=60).stdout.strip()

USER="saksham10arora-dotcom"
def stats():
    """Live counts. Falls back to the previous values if the API is unreachable,
       so a transient failure never publishes a card reading 0."""
    try:
        repos=int(gh(["api",f"users/{USER}","--jq",".public_repos"]))
        stars=sum(r["stargazerCount"] for r in json.loads(
            gh(["repo","list",USER,"--limit","300","--json","stargazerCount,isPrivate"]))
            if not r["isPrivate"])
        q='{user(login:"%s"){contributionsCollection{contributionCalendar{totalContributions}}}}'%USER
        contrib=int(gh(["api","graphql","-f",f"query={q}","--jq",
            ".data.user.contributionsCollection.contributionCalendar.totalContributions"]))
        assert repos>0 and contrib>0
        return repos,contrib,stars
    except Exception as e:
        print("stat fetch failed, keeping last known:",e)
        return 50,6233,11
REPOS,CONTRIB,STARS=stats()
print(f"stats: repos={REPOS} contributions={CONTRIB} stars={STARS}")

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def line(x,yy,parts,size,delay,bold=False):
    t="".join(f'<tspan fill="{c}">{esc(s)}</tspan>' for s,c in parts)
    return (f'<text x="{x}" y="{yy}" font-size="{size}" font-weight="{400 if bold else 700}"'
            f' opacity="0" xml:space="preserve">{t}'
            f'<animate attributeName="opacity" values="0;1;1;1" keyTimes="0;0.04;0.93;1"'
            f' dur="{CYCLE}s" begin="{delay}s" repeatCount="indefinite" fill="freeze"/></text>')

CMD="curl -sI https://github.com/nerfsaksham"; cmd_px=len(CMD)*CH
X=round(60*S); CX=round(86*S)

svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"
 font-family="'JetBrains Mono','SFMono-Regular',Menlo,Consolas,monospace">
<defs>
  <filter id="g" x="-60%" y="-60%" width="220%" height="220%">
    <feGaussianBlur stdDeviation="8" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <clipPath id="type"><rect x="{CX}" y="{y(96)}" height="{fs(28)}" width="0">
    <animate attributeName="width" values="0;0;{cmd_px};{cmd_px};{cmd_px}"
      keyTimes="0;0.03;0.25;0.93;1" dur="{CYCLE}s" repeatCount="indefinite"/>
  </rect></clipPath>
  <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{ACC}" stop-opacity="0.55"/>
    <stop offset="1" stop-color="{ACC}" stop-opacity="0.08"/>
  </linearGradient>
</defs>
<rect width="{W}" height="{H}" fill="{BG}"/>
<rect x="18" y="18" width="{W-36}" height="{H-36}" rx="16" fill="{WIN}" stroke="url(#edge)" stroke-width="2"/>
<line x1="19" y1="{y(66)}" x2="{W-19}" y2="{y(66)}" stroke="{BORDER}" stroke-width="2"/>
<circle cx="46" cy="{y(42)}" r="7" fill="#ff5f57"/><circle cx="70" cy="{y(42)}" r="7" fill="#febc2e"/><circle cx="94" cy="{y(42)}" r="7" fill="#28c840"/>
<text x="124" y="{y(48)}" font-size="{fs(13)}" font-weight="700" letter-spacing="2.4" fill="{ACC}">RESOLVING  ·  NERFSAKSHAM</text>

<text x="{X}" y="{y(115)}" font-size="{fs(16)}" font-weight="700" fill="{GREEN}">$</text>
<g clip-path="url(#type)"><text x="{CX}" y="{y(115)}" font-size="{fs(16)}" fill="{WHITE}">{esc(CMD)}</text></g>
<rect x="{CX}" y="{y(99)}" width="{fs(9)}" height="{fs(21)}" fill="{ACC}" opacity="0.9">
  <animate attributeName="x" values="{CX};{CX};{CX+cmd_px};{CX+cmd_px}" keyTimes="0;0.03;0.25;1" dur="{CYCLE}s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="0.9;0.9;0;0.9;0" keyTimes="0;0.62;0.66;0.70;1" dur="1.05s" repeatCount="indefinite"/>
</rect>

{line(X,y(165),[("HTTP/2",GREY)],fs(16),2.9)}
<text x="{round(150*S)}" y="{y(170)}" font-size="{fs(46)}" font-weight="700" fill="{ACC}" filter="url(#g)" opacity="0">301
  <animate attributeName="opacity" values="0;1;1;1" keyTimes="0;0.05;0.93;1" dur="{CYCLE}s" begin="2.9s" repeatCount="indefinite" fill="freeze"/></text>
<text x="{round(262*S)}" y="{y(170)}" font-size="{fs(17)}" fill="{GREY}" opacity="0">moved permanently
  <animate attributeName="opacity" values="0;1;1;1" keyTimes="0;0.05;0.93;1" dur="{CYCLE}s" begin="3.35s" repeatCount="indefinite" fill="freeze"/></text>

{line(X,y(216),[("location: ",DIM),("https://github.com/",GREY),("saksham10arora-dotcom",ACC)],fs(17),3.9)}
{line(X,y(251),[("x-repos: ",DIM),(str(REPOS),WHITE),("     x-contributions: ",DIM),(f"{CONTRIB:,}",WHITE),("     x-stars: ",DIM),(str(STARS),WHITE)],fs(15),4.6)}
<line x1="{X}" y1="{y(281)}" x2="{W-X}" y2="{y(281)}" stroke="{BORDER}" stroke-width="1.5" opacity="0">
  <animate attributeName="opacity" values="0;1;1;1" keyTimes="0;0.05;0.93;1" dur="{CYCLE}s" begin="5.2s" repeatCount="indefinite" fill="freeze"/></line>
{line(X,y(311),[("same person  ·  the handle moved, the work did not",GREY)],fs(16),5.5)}
{line(X,y(347),[("saksham.digital",ACC),("   ·   ",DIM),("blog.saksham.digital",ACC),("   ·   ",DIM),("x.com/nerfsaksham",ACC)],fs(15),6.2)}
</svg>'''
open("assets/redirect.svg","w").write(svg)
print("canvas",W,"x",H,"| cmd width px:",round(cmd_px))
