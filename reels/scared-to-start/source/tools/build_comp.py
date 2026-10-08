"""Generate the HyperFrames composition index.html for the 9:16 reel."""
import json, html, math

ASR = "/tmp/claude-0/-home-user-Halal-Brows-Workshop-Booking/3b93af53-cdc7-5211-b07a-7219c4d1a2f9/scratchpad/asr/"
PROJ = "/tmp/claude-0/-home-user-Halal-Brows-Workshop-Booking/3b93af53-cdc7-5211-b07a-7219c4d1a2f9/scratchpad/hf/reel-scared-business/"
WORDS = json.load(open(ASR + "words_out.json"))
CUTS = [c["out"] for c in json.load(open(ASR + "cuts.json"))["cuts"]][1:]
FACE = json.load(open(ASR + "face_out.json"))
DUR = 93.733

INK = "#16120E"
CREAM = "#FFF6E6"
ACCENT = "#FFD23F"

def wt(word, after=0.0, nth=1):
    """Start time of the nth occurrence of word (case/punct-insensitive) at/after `after`."""
    k = 0
    for w in WORDS:
        if w["start"] + 1e-6 >= after and norm(w["text"]) == word:
            k += 1
            if k == nth:
                return w["start"]
    raise KeyError(word)

def norm(s):
    return "".join(ch for ch in s.lower() if ch.isalpha() or ch == "'")

def face_at(t0, t1):
    pts = [f for f in FACE if t0 - 0.05 <= f[0] <= t1 + 0.05] or [min(FACE, key=lambda f: abs(f[0] - t0))]
    xs = sorted(p[1] for p in pts); ys = sorted(p[2] for p in pts)
    return xs[len(xs) // 2], ys[len(ys) // 2]

# --------------------------------------------------------------------------------------
# Beats in "card" mode (C): camera shrinks into a card, keyword title / insert on top.
# Each line: (text, reveal word, after, accent, style)
# --------------------------------------------------------------------------------------
B = []
def beat(id, t0, t1, lines, icon=None, ghost=None, layout="stack", tilt=0.0, slam=None, per=2):
    B.append(dict(id=id, t0=round(t0, 3), t1=round(t1, 3), lines=lines, icon=icon, ghost=ghost,
                  layout=layout, tilt=tilt, slam=slam, per=per))

beat("independence", 2.55, 3.85, [("INDEPENDENCE", 2.67, True, "slam")], icon=None, ghost="FREE", tilt=-1.5, slam=2.67)
beat("money", 4.45, 8.95, [("YOUR OWN", 4.56, False, "left"), ("MONEY", 5.09, True, "slam"),
                            ("BUY WHAT YOU WANT", 6.77, False, "rise"), ("TRAVEL", 8.05, True, "pop")],
     icon="money", ghost="$$$", layout="swap", tilt=1.2, slam=5.09)
beat("business", 14.25, 15.95, [("START", 14.44, False, "left"), ("YOUR OWN", 14.91, False, "right"),
                                 ("BUSINESS", 15.31, True, "slam")], ghost="BOSS", tilt=-1.0, slam=15.31)
beat("terrified", 16.45, 17.72, [("TERRIFIED", 16.60, True, "shake")], icon=None, ghost="FEAR", tilt=1.5, slam=16.60)
beat("blocking", 19.55, 21.9, [("BLOCKING", 19.72, False, "left"), ("STOPPING", 20.63, True, "right")],
     icon="barrier", ghost="STOP", layout="icon-left", tilt=-1.2, slam=20.63)
beat("jump", 25.7, 27.62, [("NEED HELP", 25.01, False, "rise"), ("TO JUMP", 25.96, True, "slam")],
     icon="jump", ghost="JUMP", layout="icon-right", tilt=1.0, slam=25.96)
beat("stuck", 28.95, 32.0, [("STUCK", 29.81, False, "slam"), ("FREEZING", 31.16, True, "rise")],
     icon="snow", ghost="COLD", layout="icon-left", tilt=-1.4, slam=29.81)
beat("scaredbad", 36.3, 40.85, [("NOT ALWAYS", 36.62, False, "left"), ("TRUE", 37.29, True, "pop"),
                                 ("SCARED", 37.93, False, "slam"), ("≠", 39.36, True, "pop"), ("BAD", 40.11, False, "slam")],
     ghost="TRUTH", layout="equation", tilt=1.2, slam=40.11)
beat("nervous", 42.45, 46.05, [("NERVOUS", 42.61, False, "left"), ("SYSTEM", 43.05, True, "right"),
                               ("PANICKING", 43.67, True, "shake")], icon="ecg", ghost="PULSE", layout="ecg", tilt=-1.0, slam=43.67)
beat("willitwork", 48.0, 50.6, [("WILL IT", 48.54, False, "rise"), ("WORK?", 49.81, True, "slam")],
     icon="question", ghost="???", layout="icon-right", tilt=1.3, slam=49.81)
beat("platform", 51.4, 54.6, [("NOBODY", 50.67, True, "slam"), ("CAN TELL YOU", 52.45, False, "rise")],
     icon="phone", ghost="NO ONE", layout="icon-right", tilt=-1.1, slam=None)
beat("promise", 55.4, 57.15, [("THE ONLY", 55.13, False, "left"), ("PROMISE", 55.96, True, "slam")],
     ghost="TRUST", tilt=1.0, slam=55.96)
beat("whenhow", 60.7, 63.62, [("WHEN?", 60.93, True, "slam"), ("HOW MUCH?", 62.95, True, "slam")],
     icon="clock", ghost="?", layout="swap", tilt=-1.3, slam=60.93, per=1)
beat("above", 64.5, 67.4, [("NOT ME", 64.97, False, "left"), ("ABOVE", 65.83, True, "rise"), ("HE KNOWS", 66.66, True, "pop")],
     icon="rays", ghost="FAITH", layout="rays", tilt=0.0, slam=None)
beat("keepgoing", 69.2, 76.3, [("START", 69.48, True, "slam"), ("KEEP GOING", 70.44, False, "right")],
     icon=None, ghost="KEEP", layout="checklist", tilt=1.0, slam=69.48)
beat("ready", 81.0, 83.8, [("WAKE UP", 81.79, False, "rise"), ("READY?", 83.20, True, "strike")],
     icon="alarm", ghost="NEVER", layout="icon-left", tilt=-1.2, slam=None)
beat("fear", 89.1, 90.7, [("I STARTED", 89.43, False, "left"), ("WITH FEAR", 90.10, True, "slam")],
     ghost="FEAR", tilt=1.2, slam=90.10)
beat("game", 92.15, DUR, [("PART OF", 92.58, False, "rise"), ("THE GAME", 93.05, True, "slam")],
     icon=None, ghost="GAME", tilt=0.0, slam=93.05)

CHECK = [("KEEP POSTING", 71.22), ("KEEP LEARNING", 72.17), ("FIND CLIENTS", 73.14), ("WORK ON YOUR DREAM", 74.61)]

COVER_END = 2.5

# --------------------------------------------------------------------------------------
# Camera plan
# --------------------------------------------------------------------------------------
CARD = dict(top=740, left=60, right=60, bottom=480)  # window 960x700 at y 740..1440
CARD_CY = 740 + 350

def cam_A(t0, t1, s, fx=540):
    faceX, faceY = face_at(t0, t1)
    y = 1440 - (faceY + 340) * s
    y = min(0, max(1920 - 1080 * s, y))
    x = fx - faceX * s
    x = min(0, max(1080 - 1920 * s, x))
    return dict(x=round(x, 1), y=round(y, 1), s=round(s, 4), fX=faceX, fY=faceY)

def cam_C(t0, t1, s=1.05, dx=0):
    faceX, faceY = face_at(t0, t1)
    x = 540 + dx - faceX * s
    y = CARD_CY - faceY * s
    return dict(x=round(x, 1), y=round(y, 1), s=round(s, 4), fX=faceX, fY=faceY)

def pushed(st, k):
    """Zoom by factor k around the face point (keeps face anchored)."""
    s2 = st["s"] * k
    fxs = st["x"] + st["fX"] * st["s"]; fys = st["y"] + st["fY"] * st["s"]
    return dict(x=round(fxs - st["fX"] * s2, 1), y=round(fys - st["fY"] * s2, 1), s=round(s2, 4), fX=st["fX"], fY=st["fY"])

# timeline of modes
periods = []  # (t0, t1, mode, beat)
t = 0.0
periods.append((0.0, COVER_END, "COVER", None))
t = COVER_END
for b in B:
    if b["t0"] > t + 0.01:
        periods.append((t, b["t0"], "A", None))
    periods.append((b["t0"], b["t1"], "C", b))
    t = b["t1"]
if t < DUR - 0.01:
    periods.append((t, DUR, "A", None))
# cover ends straight into first beat? fix any period overlap: cover end must be <= first beat start
assert all(p[0] < p[1] for p in periods), periods

EMPH = {wt("cannot"): 2.75, wt("terrifying"): 2.8, wt("big"): 2.7, wt("me"): 2.65, wt("never", 84.0): 2.6,
        wt("dream"): 2.55, wt("happen", 83.0): 2.4, wt("new"): 2.5, wt("scared", 78.5): 2.6, wt("idea"): 2.6,
        wt("help"): 2.5, wt("loved"): 2.55, wt("something"): 2.45}
SCALES = [2.0, 2.25, 1.92, 2.38, 2.1, 2.42, 1.98, 2.3]
FXS = [540, 515, 565, 540, 525, 555]

shots = []  # dict(t0,t1,mode,start_state,trans)
si = 0
for (p0, p1, mode, b) in periods:
    if mode in ("A", "COVER"):
        bounds = [p0] + [c for c in CUTS if p0 + 0.4 < c < p1 - 0.4] + [p1]
        for e in sorted(EMPH):
            if p0 + 0.4 < e - 0.04 < p1 - 0.4:
                bounds.append(round(e - 0.04, 3))
        bounds = sorted(set(round(x, 3) for x in bounds))
        # split long holds (>2.4s) at word starts
        changed = True
        while changed:
            changed = False
            for i in range(len(bounds) - 1):
                a, z = bounds[i], bounds[i + 1]
                if z - a > 2.4:
                    mid = (a + z) / 2
                    cand = [w["start"] for w in WORDS if a + 0.8 < w["start"] < z - 0.8]
                    m = min(cand, key=lambda c: abs(c - mid)) if cand else mid
                    bounds.insert(i + 1, round(m - 0.03, 3)); changed = True
                    break
        for i in range(len(bounds) - 1):
            a, z = bounds[i], bounds[i + 1]
            emph = [EMPH[e] for e in EMPH if abs((e - 0.04) - a) < 0.02]
            if mode == "COVER":
                s = 1.95
            elif emph:
                s = emph[0]
            else:
                s = SCALES[si % len(SCALES)]; si += 1
            s = min(s, 2.45)
            st = cam_A(a, z, s, FXS[si % len(FXS)])
            is_cut = any(abs(a - c) < 0.02 for c in CUTS)
            trans = "cut" if (is_cut or emph or i == 0) else "smooth"
            shots.append(dict(t0=a, t1=z, mode=mode, st=st, trans=trans, push=1.05 if not emph else 1.025))
    else:
        # card mode: inner reframe every <=2.4s
        n = max(1, math.ceil((p1 - p0) / 2.4))
        for i in range(n):
            a = p0 + (p1 - p0) * i / n; z = p0 + (p1 - p0) * (i + 1) / n
            s = [1.06, 1.22, 1.12, 1.3][i % 4]
            st = cam_C(a, z, s, [0, -20, 20, 0][i % 4])
            shots.append(dict(t0=round(a, 3), t1=round(z, 3), mode="C", st=st, trans="cut" if i == 0 else "smooth", push=1.06, beat=b["id"]))

# camera segments (fromTo list) for #camInner
cam_segs = []
for k, sh in enumerate(shots):
    st = sh["st"]; end = pushed(st, sh["push"])
    a, z = sh["t0"], sh["t1"]
    if sh["trans"] == "smooth" and k > 0:
        prev_end = cam_segs[-1]["to"]
        td = min(0.32, (z - a) * 0.4)
        td = round(td, 3)
        cam_segs.append(dict(t=a, d=td, frm=prev_end, to=st, ease="power3.inOut"))
        cam_segs.append(dict(t=round(a + td, 3) + 0.001, d=round(z - a - td, 3) - 0.002, frm=st, to=end, ease="sine.inOut"))
    else:
        cam_segs.append(dict(t=a, d=round(z - a, 3) - 0.001, frm=st, to=end, ease="sine.inOut"))
# the mode transitions (A<->C) are handled by the box tween; at mode change the inner jumps
# under a fast clip morph, which is masked by a 0.28s morph. Make inner transitions into/out of C smooth:
for i in range(1, len(cam_segs)):
    pass

def clip_str(mode):
    if mode == "C":
        return f"inset({CARD['top']}px {CARD['right']}px {CARD['bottom']}px {CARD['left']}px round 44px)"
    return "inset(0px 0px 0px 0px round 0px)"

box_segs = []  # transitions of #camBox clip-path + rotation, and #cardFrame
prev_mode = "COVER"
for (p0, p1, mode, b) in periods[1:]:
    m = "C" if mode == "C" else "A"
    pm = "C" if prev_mode == "C" else "A"
    if m != pm:
        box_segs.append(dict(t=p0, frm=pm, to=m, tilt=(b["tilt"] if b else 0.0)))
    elif m == "C":
        box_segs.append(dict(t=p0, frm="C", to="C", tilt=b["tilt"]))
    prev_mode = mode

# --------------------------------------------------------------------------------------
# Captions
# --------------------------------------------------------------------------------------
KEY = {"want", "independence", "money", "buy", "traveling", "loved", "business", "own", "terrified", "situation",
       "blocking", "stopping", "help", "jump", "cannot", "stuck", "freezing", "scared", "true", "bad", "nervous",
       "system", "panicking", "terrifying", "never", "work", "nobody", "platform", "promise", "when", "much",
       "above", "knows", "start", "going", "posting", "learning", "clients", "dream", "big", "new", "ready",
       "anyone", "included", "fear", "game", "started", "keep", "idea", "happen", "morning"}

groups = []
cur = []
for i, w in enumerate(WORDS):
    txt = w["text"]
    if cur:
        prev = cur[-1]
        chars = sum(len(x["text"]) + 1 for x in cur) + len(txt)
        gap = w["start"] - prev["end"]
        if prev["text"][-1] in ".,?" or chars > 15 or len(cur) >= 3 or gap > 0.45:
            groups.append(cur); cur = []
    cur.append(w)
if cur:
    groups.append(cur)
caps = []
for gi, g in enumerate(groups):
    a = g[0]["start"] - 0.04
    nxt = groups[gi + 1][0]["start"] - 0.04 if gi + 1 < len(groups) else DUR
    z = min(nxt, g[-1]["end"] + 0.9)
    caps.append(dict(t0=round(max(0, a), 3), t1=round(min(z, DUR), 3), words=g))

# --------------------------------------------------------------------------------------
# SFX
# --------------------------------------------------------------------------------------
sfx = []
def add_sfx(kind, t, vol, dur):
    sfx.append(dict(kind=kind, t=round(max(0, t), 3), vol=vol, d=dur))
DURS = dict(whoosh=0.5, swish=0.3, impact=0.7, pop=0.12, ding=0.45, riser=1.2)
for bs in box_segs:
    if bs["frm"] == "A" and bs["to"] == "C":
        add_sfx("whoosh", bs["t"] - 0.12, 0.75, 0.5)
    elif bs["frm"] == "C" and bs["to"] == "A":
        add_sfx("swish", bs["t"] - 0.05, 0.6, 0.3)
    else:
        add_sfx("swish", bs["t"] - 0.05, 0.6, 0.3)
add_sfx("whoosh", COVER_END - 0.15, 0.75, 0.5)
for b in B:
    if b["slam"]:
        add_sfx("impact", b["slam"], 0.6, 0.7)
    for (txt, tw, acc, style) in b["lines"]:
        if style == "pop":
            add_sfx("pop", tw, 0.7, 0.12)
for (txt, tw) in CHECK:
    add_sfx("ding", tw + 0.05, 0.55, 0.45)
add_sfx("riser", 92.15 - 1.15, 0.6, 1.2)
# emphasis punch-ins in A mode get a soft impact
for e in EMPH:
    add_sfx("impact", e - 0.04, 0.35, 0.7)
sfx.sort(key=lambda s: s["t"])
# drop sfx overlapping too closely with same kind
clean = []
for s in sfx:
    if clean and s["kind"] == clean[-1]["kind"] and s["t"] - clean[-1]["t"] < 0.25:
        continue
    clean.append(s)
sfx = clean
for s in sfx:
    s["d"] = round(min(s["d"], DUR - s["t"]), 3)

# --------------------------------------------------------------------------------------
# HTML builders
# --------------------------------------------------------------------------------------
def esc(s):
    return html.escape(s, quote=True)

def fit(text, maxw=940, maxsize=240, factor=0.74):
    n = max(1, len(text))
    return int(min(maxsize, maxw / (n * factor)))

ICONS = {}
ICONS["money"] = """<svg viewBox="0 0 300 300" class="ico">
  <ellipse class="draw" pathLength="1" cx="150" cy="232" rx="110" ry="30"/>
  <path class="draw" pathLength="1" d="M40 232 V200 M260 232 V200"/>
  <ellipse class="draw" pathLength="1" cx="150" cy="200" rx="110" ry="30"/>
  <path class="draw" pathLength="1" d="M40 200 V168 M260 200 V168"/>
  <ellipse class="draw" pathLength="1" cx="150" cy="168" rx="110" ry="30"/>
  <circle class="draw acc coin" pathLength="1" cx="150" cy="86" r="62"/>
  <text x="150" y="112" class="glyph coin">$</text>
</svg>"""
ICONS["barrier"] = """<svg viewBox="0 0 300 300" class="ico">
  <rect class="draw" pathLength="1" x="20" y="90" width="260" height="70" rx="10"/>
  <path class="draw acc" pathLength="1" d="M60 90 L20 140 M120 90 L60 160 M180 90 L120 160 M240 90 L180 160 M280 110 L240 160"/>
  <path class="draw" pathLength="1" d="M60 160 V270 M240 160 V270 M30 270 H90 M210 270 H270"/>
  <circle class="draw acc" pathLength="1" cx="60" cy="60" r="20"/><circle class="draw acc" pathLength="1" cx="240" cy="60" r="20"/>
</svg>"""
ICONS["jump"] = """<svg viewBox="0 0 300 300" class="ico">
  <path class="draw" pathLength="1" d="M10 260 H110 M190 260 H290"/>
  <path class="draw acc dash" pathLength="1" d="M70 250 C 100 40, 200 40, 235 240"/>
  <path class="draw acc" pathLength="1" d="M205 215 L235 245 L260 205"/>
</svg>"""
ICONS["snow"] = """<svg viewBox="0 0 300 300" class="ico spin">
  <path class="draw" pathLength="1" d="M150 20 V280 M37 85 L263 215 M37 215 L263 85"/>
  <path class="draw acc" pathLength="1" d="M120 45 L150 75 L180 45 M120 255 L150 225 L180 255 M58 120 L100 108 L88 66 M242 180 L200 192 L212 234 M58 180 L100 192 L88 234 M242 120 L200 108 L212 66"/>
</svg>"""
ICONS["ecg"] = """<svg viewBox="0 0 960 200" class="ecg">
  <path class="draw acc" pathLength="1" d="M0 120 H220 L250 120 L270 70 L295 170 L325 20 L355 190 L380 100 L400 120 H520 L545 120 L565 60 L590 175 L615 30 L640 185 L662 110 L680 120 H960"/>
</svg>"""
ICONS["question"] = """<svg viewBox="0 0 300 300" class="ico">
  <circle class="draw" pathLength="1" cx="150" cy="150" r="128"/>
  <text x="150" y="222" class="glyph q">?</text>
</svg>"""
ICONS["phone"] = """<svg viewBox="0 0 300 380" class="ico phone">
  <rect class="draw" pathLength="1" x="40" y="10" width="220" height="360" rx="34"/>
  <path class="draw" pathLength="1" d="M120 34 H180"/>
  <rect class="bubble b1" x="62" y="78" width="176" height="64" rx="18"/>
  <text x="150" y="118" class="btxt">WILL IT WORK?</text>
  <rect class="bubble b2" x="62" y="164" width="110" height="56" rx="18"/>
  <circle class="dot d1" cx="92" cy="192" r="8"/><circle class="dot d2" cx="117" cy="192" r="8"/><circle class="dot d3" cx="142" cy="192" r="8"/>
</svg>"""
ICONS["clock"] = """<svg viewBox="0 0 300 300" class="ico">
  <circle class="draw" pathLength="1" cx="150" cy="150" r="120"/>
  <path class="draw" pathLength="1" d="M150 42 V62 M150 238 V258 M42 150 H62 M238 150 H258"/>
  <line class="hand hm" x1="150" y1="150" x2="150" y2="78"/>
  <line class="hand hh" x1="150" y1="150" x2="200" y2="150"/>
  <circle class="pin" cx="150" cy="150" r="10"/>
</svg>"""
ICONS["rays"] = """<svg viewBox="0 0 960 520" class="rays">
  <path class="draw acc" pathLength="1" d="M480 0 L480 150 M480 0 L330 140 M480 0 L630 140 M480 0 L190 110 M480 0 L770 110 M480 0 L70 60 M480 0 L890 60"/>
</svg>"""
ICONS["alarm"] = """<svg viewBox="0 0 300 300" class="ico alarm">
  <circle class="draw" pathLength="1" cx="150" cy="165" r="105"/>
  <path class="draw acc" pathLength="1" d="M48 88 A 46 46 0 0 1 112 42 M188 42 A 46 46 0 0 1 252 88"/>
  <path class="draw" pathLength="1" d="M85 262 L65 288 M215 262 L235 288"/>
  <path class="draw acc" pathLength="1" d="M150 165 V100 M150 165 L195 190"/>
</svg>"""

def line_html(b, i, text, acc, style, size):
    cls = "tl acc" if acc else "tl"
    if style == "strike":
        cls += " strike"
    inner = esc(text)
    extra = '<span class="strikebar"></span>' if style == "strike" else ""
    return f'<div class="{cls}" id="{b["id"]}-l{i}" style="font-size:{size}px">{inner}{extra}</div>'

def beat_html(b):
    lid = b["id"]
    lines = b["lines"]
    lay = b["layout"]
    out = []
    if lay in ("stack",):
        sizes = [fit(t, 940, 230) for (t, *_r) in lines]
        body = "".join(line_html(b, i, t, a, s, sizes[i]) for i, (t, tw, a, s) in enumerate(lines))
        out.append(f'<div class="zone stack">{body}</div>')
    elif lay == "swap":
        # pairs swap in place: lines grouped in twos (or one per slot)
        per = b['per']; slots = [lines[i:i + per] for i in range(0, len(lines), per)]
        parts = []
        for si_, pair in enumerate(slots):
            body = ""
            for j, (t, tw, a, s) in enumerate(pair):
                i = si_ * per + j
                body += line_html(b, i, t, a, s, fit(t, 560 if b["icon"] else 940, 200))
            parts.append(f'<div class="slot" id="{lid}-slot{si_}">{body}</div>')
        icon = f'<div class="iconbox" id="{lid}-icon">{ICONS[b["icon"]]}</div>' if b["icon"] else ""
        out.append(f'<div class="zone row">{icon}<div class="slots">{"".join(parts)}</div></div>')
    elif lay in ("icon-left", "icon-right"):
        sizes = [fit(t, 520, 160) for (t, *_r) in lines]
        body = "".join(line_html(b, i, t, a, s, sizes[i]) for i, (t, tw, a, s) in enumerate(lines))
        icon = f'<div class="iconbox" id="{lid}-icon">{ICONS[b["icon"]]}</div>'
        txt = f'<div class="txt">{body}</div>'
        out.append(f'<div class="zone row {lay}">{icon if lay=="icon-left" else txt}{txt if lay=="icon-left" else icon}</div>')
    elif lay == "equation":
        l = lines
        out.append(f'''<div class="zone stack eq">
          {line_html(b,0,l[0][0],l[0][2],l[0][3],110)}{line_html(b,1,l[1][0],l[1][2],l[1][3],110)}
          <div class="eqrow">{line_html(b,2,l[2][0],l[2][2],l[2][3],112)}{line_html(b,3,l[3][0],l[3][2],l[3][3],112)}{line_html(b,4,l[4][0],l[4][2],l[4][3],112)}</div>
        </div>''')
    elif lay == "ecg":
        body = (f'<div class="eqrow">{line_html(b,0,lines[0][0],lines[0][2],lines[0][3],86)}'
                f'{line_html(b,1,lines[1][0],lines[1][2],lines[1][3],86)}</div>'
                f'<div class="ecgbox" id="{lid}-icon">{ICONS["ecg"]}</div>'
                f'{line_html(b,2,lines[2][0],lines[2][2],lines[2][3],130)}')
        out.append(f'<div class="zone stack ecgzone">{body}</div>')
    elif lay == "rays":
        body = (f'<div class="raysbox" id="{lid}-icon">{ICONS["rays"]}</div>'
                f'{line_html(b,0,lines[0][0],lines[0][2],lines[0][3],100)}'
                f'{line_html(b,1,lines[1][0],lines[1][2],lines[1][3],190)}'
                f'{line_html(b,2,lines[2][0],lines[2][2],lines[2][3],110)}')
        out.append(f'<div class="zone stack raysz">{body}</div>')
    elif lay == "checklist":
        head = (f'<div class="slot" id="{lid}-slot0">{line_html(b,0,lines[0][0],lines[0][2],lines[0][3],200)}'
                f'{line_html(b,1,lines[1][0],lines[1][2],lines[1][3],150)}</div>')
        items = ""
        for k, (txt, tw) in enumerate(CHECK):
            items += (f'<div class="ck" id="{lid}-ck{k}"><svg viewBox="0 0 80 80" class="box"><rect x="6" y="6" width="68" height="68" rx="14"/>'
                      f'<path class="tick" pathLength="1" d="M20 42 L35 56 L62 24"/></svg><span>{esc(txt)}</span></div>')
        out.append(f'<div class="zone stack">{head}<div class="slot cklist" id="{lid}-slot1">{items}</div></div>')
    return "\n".join(out)

# ----------------------------- JS for beats ----------------------------------------
ENT = {
    "slam": ("{scale:1.9, opacity:0, filter:'blur(14px)'}", "{scale:1, opacity:1, filter:'blur(0px)', duration:0.32, ease:'power4.out'}"),
    "left": ("{x:-260, opacity:0}", "{x:0, opacity:1, duration:0.36, ease:'expo.out'}"),
    "right": ("{x:260, opacity:0}", "{x:0, opacity:1, duration:0.36, ease:'expo.out'}"),
    "rise": ("{y:110, rotation:5, opacity:0}", "{y:0, rotation:0, opacity:1, duration:0.42, ease:'circ.out'}"),
    "pop": ("{scale:0.2, opacity:0}", "{scale:1, opacity:1, duration:0.4, ease:'back.out(2.2)'}"),
    "shake": ("{scale:1.6, opacity:0}", "{scale:1, opacity:1, duration:0.28, ease:'power4.out'}"),
    "strike": ("{y:90, opacity:0}", "{y:0, opacity:1, duration:0.36, ease:'circ.out'}"),
}

js = []
def J(s):
    js.append(s)

for b in B:
    lid = b["id"]; t0, t1 = b["t0"], b["t1"]
    # ghost word drift
    if False: J(f"tl.fromTo('#{lid}-ghost .gw',{{xPercent:-8, opacity:0}},{{xPercent:4, opacity:1, duration:{t1-t0:.3f}, ease:'none'}},{t0:.3f});")
    for i, (txt, tw, acc, style) in enumerate(b["lines"]):
        tw = max(tw, t0 + 0.02)
        f, to = ENT[style]
        J(f"tl.fromTo('#{lid}-l{i}',{f},{to},{tw:.3f});")
        if style == "shake":
            J(f"tl.fromTo('#{lid}-l{i}',{{x:0}},{{keyframes:{{x:[0,-14,12,-10,8,-5,3,0]}}, duration:0.5, ease:'none', immediateRender:false}},{tw+0.28:.3f});")
        if style == "strike":
            J(f"tl.fromTo('#{lid}-l{i} .strikebar',{{scaleX:0}},{{scaleX:1, duration:0.3, ease:'power3.inOut'}},{tw+0.38:.3f});")
    if b["layout"] == "swap":
        nslots = math.ceil(len(b["lines"]) / b['per'])
        for k in range(1, nslots):
            tsw = b["lines"][k * b['per']][1] - 0.12
            J(f"tl.fromTo('#{lid}-slot{k-1}',{{y:0, opacity:1}},{{y:-80, opacity:0, duration:0.18, ease:'power2.in', immediateRender:false}},{tsw-0.06:.3f});")
    if b["layout"] == "checklist":
        tsw = CHECK[0][1] - 0.45
        J(f"tl.fromTo('#{lid}-slot0',{{y:0, opacity:1}},{{y:-60, opacity:0, duration:0.2, ease:'power2.in', immediateRender:false}},{tsw:.3f});")
        J(f"tl.fromTo('#{lid}-slot1',{{opacity:0}},{{opacity:1, duration:0.01}},{tsw+0.2:.3f});")
        for k, (txt, tw) in enumerate(CHECK):
            J(f"tl.fromTo('#{lid}-ck{k}',{{x:-120, opacity:0}},{{x:0, opacity:1, duration:0.3, ease:'expo.out'}},{tw-0.2:.3f});")
            J(f"tl.fromTo('#{lid}-ck{k} .tick',{{strokeDashoffset:1}},{{strokeDashoffset:0, duration:0.22, ease:'power2.out'}},{tw+0.05:.3f});")
            J(f"tl.fromTo('#{lid}-ck{k} rect',{{fill:'rgba(255,210,63,0)'}},{{fill:'rgba(255,210,63,1)', duration:0.15}},{tw+0.02:.3f});")
    if b["icon"]:
        sel = f"#{lid}-icon"
        J(f"tl.fromTo('{sel}',{{scale:0.6, opacity:0, rotation:-8}},{{scale:1, opacity:1, rotation:0, duration:0.45, ease:'back.out(1.8)'}},{t0+0.06:.3f});")
        if b['icon']!='ecg': J(f"tl.fromTo('{sel} .draw:not(.dash)',{{strokeDashoffset:1}},{{strokeDashoffset:0, duration:0.7, stagger:0.06, ease:'power2.out'}},{t0+0.1:.3f});")
        J(f"tl.fromTo('{sel}',{{y:0}},{{y:-14, duration:{(t1-t0)/2:.3f}, yoyo:true, repeat:1, ease:'sine.inOut', immediateRender:false}},{t0+0.55:.3f});")
        if b["icon"] == "snow":
            J(f"tl.fromTo('{sel} svg',{{rotation:0}},{{rotation:60, duration:{t1-t0:.3f}, ease:'none'}},{t0:.3f});")
        if b["icon"] == "money":
            J(f"tl.fromTo('{sel} .coin',{{y:-120, opacity:0}},{{y:0, opacity:1, duration:0.4, ease:'bounce.out'}},{wt('money'):.3f});")
            J(f"tl.fromTo('{sel}',{{rotationY:0}},{{rotationY:360, duration:0.6, ease:'power2.inOut', immediateRender:false}},{wt('buy'):.3f});")
        if b["icon"] == "clock":
            J(f"tl.fromTo('{sel} .hm',{{rotation:0, svgOrigin:'150 150'}},{{rotation:720, svgOrigin:'150 150', duration:{t1-t0:.3f}, ease:'power1.inOut'}},{t0:.3f});")
            J(f"tl.fromTo('{sel} .hh',{{rotation:0, svgOrigin:'150 150'}},{{rotation:120, svgOrigin:'150 150', duration:{t1-t0:.3f}, ease:'power1.inOut'}},{t0:.3f});")
        if b["icon"] == "phone":
            J(f"tl.fromTo('{sel} .b1',{{opacity:0, y:20}},{{opacity:1, y:0, duration:0.3, ease:'back.out(2)'}},{t0+0.5:.3f});")
            J(f"tl.fromTo('{sel} .btxt',{{opacity:0}},{{opacity:1, duration:0.2}},{t0+0.6:.3f});")
            J(f"tl.fromTo('{sel} .b2',{{opacity:0, y:20}},{{opacity:1, y:0, duration:0.3, ease:'back.out(2)'}},{t0+1.0:.3f});")
            for d in range(3):
                J(f"tl.fromTo('{sel} .d{d+1}',{{opacity:0.25}},{{opacity:1, duration:0.25, yoyo:true, repeat:{int((t1-t0-1.2)/0.5)*2-1 if (t1-t0)>1.8 else 1}, ease:'sine.inOut'}},{t0+1.1+d*0.12:.3f});")
        if b["icon"] == "alarm":
            J(f"tl.fromTo('{sel} svg',{{rotation:0}},{{keyframes:{{rotation:[0,-9,9,-9,9,-7,7,-4,4,0]}}, duration:0.9, ease:'none'}},{wt('wake'):.3f});")
        if b["icon"] == "jump":
            J(f"tl.fromTo('{sel} .dash',{{strokeDashoffset:1}},{{strokeDashoffset:0, duration:0.5, ease:'power2.inOut'}},{wt('jump'):.3f});")
        if b["icon"] == "ecg":
            if b['icon']!='ecg': J(f"tl.fromTo('{sel} .draw:not(.dash)',{{strokeDashoffset:1}},{{strokeDashoffset:0, duration:1.6, ease:'none'}},{wt('panicking')-0.7:.3f});")

# captions JS
cap_html = []
for ci, c in enumerate(caps):
    spans = []
    for wi, w in enumerate(c["words"]):
        t = w["text"].upper()
        clean = t.rstrip(".,")
        is_key = norm(clean) in KEY or norm(clean).rstrip("?") in KEY
        cls = "w key" if is_key else "w"
        spans.append(f'<span class="{cls}" id="c{ci}w{wi}">{esc(clean)}</span>')
        st = max(c["t0"], w["start"] - 0.03)
        J(f"tl.fromTo('#c{ci}w{wi}',{{opacity:0, scale:0.55, y:24}},{{opacity:1, scale:1, y:0, duration:0.16, ease:'back.out(2.4)'}},{st:.3f});")
        if is_key:
            J(f"tl.fromTo('#c{ci}w{wi}',{{scale:1}},{{scale:1.07, duration:0.1, yoyo:true, repeat:1, ease:'power2.out', immediateRender:false}},{st+0.17:.3f});")
    cap_html.append(f'<div class="clip cap" id="cap{ci}" data-start="{c["t0"]:.3f}" data-duration="{c["t1"]-c["t0"]:.3f}" data-track-index="20"><div class="capline">{"".join(spans)}</div></div>')

# camera JS
J("// camera")
J(f"tl.set('#camInner',{{x:{shots[0]['st']['x']}, y:{shots[0]['st']['y']}, scale:{shots[0]['st']['s']}}},0);")
for sg in cam_segs:
    f, to = sg["frm"], sg["to"]
    J(f"tl.fromTo('#camInner',{{x:{f['x']}, y:{f['y']}, scale:{f['s']}}},{{x:{to['x']}, y:{to['y']}, scale:{to['s']}, duration:{max(0.01, sg['d']):.3f}, ease:'{sg['ease']}', immediateRender:false}},{sg['t']:.3f});")

# box morph (A<->C)
J("// box")
J(f"tl.set('#camBox',{{clipPath:'{clip_str('A')}', rotation:0}},0);")
J("tl.set('#cardFrame',{opacity:0, rotation:0},0);")
prev_tilt = 0.0
for bs in box_segs:
    t = bs["t"]
    if bs["to"] == "C":
        J(f"tl.fromTo('#camBox',{{clipPath:'{clip_str(bs['frm'])}', rotation:{prev_tilt}}},{{clipPath:'{clip_str('C')}', rotation:{bs['tilt']}, duration:0.3, ease:'power3.inOut', immediateRender:false}},{t-0.02:.3f});")
        J(f"tl.fromTo('#cardFrame',{{opacity:{1 if bs['frm']=='C' else 0}, rotation:{prev_tilt}, scale:{1 if bs['frm']=='C' else 1.25}}},{{opacity:1, rotation:{bs['tilt']}, scale:1, duration:0.3, ease:'power3.inOut', immediateRender:false}},{t-0.02:.3f});")
        prev_tilt = bs["tilt"]
    else:
        J(f"tl.fromTo('#camBox',{{clipPath:'{clip_str('C')}', rotation:{prev_tilt}}},{{clipPath:'{clip_str('A')}', rotation:0, duration:0.28, ease:'power3.inOut', immediateRender:false}},{t-0.02:.3f});")
        J(f"tl.fromTo('#cardFrame',{{opacity:1, rotation:{prev_tilt}, scale:1}},{{opacity:0, rotation:0, scale:1.25, duration:0.2, ease:'power2.in', immediateRender:false}},{t-0.02:.3f});")
        prev_tilt = 0.0

# shake on emphasis words in A mode
for e in [wt("terrifying"), wt("cannot")]:
    J(f"tl.fromTo('#camShake',{{x:0, y:0}},{{keyframes:{{x:[0,-16,14,-12,9,-6,3,0], y:[0,8,-10,7,-5,3,-1,0]}}, duration:0.45, ease:'none', immediateRender:false}},{e:.3f});")

# cover
J("// cover")
J(f"tl.fromTo('#cover .ct',{{scale:1}},{{scale:1.04, duration:{COVER_END-0.2:.3f}, ease:'sine.inOut'}},0);")
J(f"tl.fromTo('#cover .row1, #cover .row3',{{x:0}},{{x:-1200, duration:0.35, ease:'power3.in'}},{COVER_END-0.3:.3f});")
J(f"tl.fromTo('#cover .row2, #cover .row4',{{x:0}},{{x:1200, duration:0.35, ease:'power3.in'}},{COVER_END-0.3:.3f});")
J(f"tl.fromTo('#scrim',{{opacity:1}},{{opacity:0, duration:0.3, ease:'power2.out'}},{COVER_END-0.25:.3f});")
J(f"tl.fromTo('#cover .tag',{{opacity:1}},{{opacity:0, duration:0.2}},{COVER_END-0.3:.3f});")

# stage ambient
J(f"tl.fromTo('#glow',{{scale:1, opacity:0.75}},{{scale:1.25, opacity:1, duration:6, yoyo:true, repeat:{int(DUR/12)*2-1}, ease:'sine.inOut'}},0);")
J(f"tl.fromTo('#grid',{{y:0}},{{y:-240, duration:{DUR:.3f}, ease:'none'}},0);")
J(f"tl.fromTo('#progress',{{scaleX:0}},{{scaleX:1, duration:{DUR:.3f}, ease:'none'}},0);")

# --------------------------------------------------------------------------------------
beats_html = []
for b in B:
    if False: beats_html.append(f'<section class="clip ghost" id="{b["id"]}-ghost" data-start="{b["t0"]:.3f}" data-duration="{b["t1"]-b["t0"]:.3f}" data-track-index="2"><svg class="gw" width="2400" height="460" aria-hidden="true"><text x="0" y="380">{esc(b["ghost"])}</text></svg></section>')
    beats_html.append(f'<section class="clip beat" id="{b["id"]}" data-start="{b["t0"]:.3f}" data-duration="{b["t1"]-b["t0"]:.3f}" data-track-index="10">{beat_html(b)}</section>')

sfx_html = []
for i, s in enumerate(sfx):
    sfx_html.append(f'<audio id="sfx{i}" src="assets/sfx/{s["kind"]}.wav" data-start="{s["t"]:.3f}" data-duration="{s["d"]:.3f}" data-track-index="{30 + (i % 3)}" data-volume="{s["vol"]}"></audio>')

CSS = f"""
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1920px; overflow:hidden; background:{INK}; }}
#root {{ position:relative; width:100%; height:100%; overflow:hidden; background:{INK}; font-family:'Montserrat', sans-serif; }}
#stage {{ position:absolute; inset:0; z-index:0; overflow:hidden; background:{INK}; }}
#glow {{ position:absolute; left:-260px; top:-200px; width:1600px; height:1300px; border-radius:50%;
  background:radial-gradient(closest-side, rgba(255,210,63,0.34), rgba(255,210,63,0.10) 55%, rgba(255,210,63,0) 75%); }}
#grid {{ position:absolute; left:0; top:0; width:1080px; height:2400px; opacity:0.22;
  background-image:radial-gradient(circle, rgba(255,246,230,0.55) 2.5px, transparent 3px); background-size:60px 60px; }}
#grain {{ position:absolute; inset:0; opacity:0.16; mix-blend-mode:overlay; }}
.ghost {{ z-index:1; overflow:hidden; }}
.ghost .gw {{ position:absolute; left:-40px; top:1380px; display:block; overflow:visible; }}
.ghost .gw text {{ font-family:'Archivo Black'; font-size:420px; fill:rgba(255,210,63,0.13); letter-spacing:-0.04em; }}
#camBox {{ position:absolute; inset:0; z-index:3; overflow:hidden; transform-origin:540px 1090px; }}
#camShake {{ position:absolute; inset:0; }}
#camInner {{ position:absolute; left:0; top:0; width:1920px; height:1080px; transform-origin:0 0; }}
#cam {{ position:absolute; left:0; top:0; width:1920px; height:1080px; object-fit:cover; }}
#cardFrame {{ position:absolute; left:{CARD['left']-10}px; top:{CARD['top']-10}px; width:{1080-CARD['left']-CARD['right']+20}px; height:{1920-CARD['top']-CARD['bottom']+20}px;
  border:7px solid {ACCENT}; border-radius:52px; z-index:4; transform-origin:50% 50%; box-shadow:0 30px 80px rgba(0,0,0,0.45); }}
#scrim {{ position:absolute; inset:0; z-index:5; background:radial-gradient(ellipse at 50% 50%, rgba(22,18,14,0.55), rgba(22,18,14,0.82)); }}
.beat {{ z-index:8; }}
.zone {{ position:absolute; left:60px; right:60px; top:210px; height:500px; display:flex; }}
.zone.stack {{ flex-direction:column; align-items:center; justify-content:center; gap:4px; }}
.zone.row {{ flex-direction:row; align-items:center; justify-content:space-between; gap:24px; }}
.zone.row .txt {{ flex:1; display:flex; flex-direction:column; justify-content:center; }}
.zone.icon-left .txt {{ align-items:flex-start; }}
.zone.icon-right .txt {{ align-items:flex-end; }}
.slots {{ position:relative; flex:1; height:100%; }}
.slot {{ position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; }}
.zone.stack > .slot {{ position:absolute; }}
.iconbox {{ width:320px; height:320px; flex:none; display:block; }}
.iconbox svg {{ width:100%; height:100%; display:block; overflow:visible; }}
.tl {{ display:block; font-family:'Archivo Black'; color:{CREAM}; line-height:0.98; letter-spacing:-0.035em; white-space:nowrap;
  text-shadow:0 8px 0 rgba(0,0,0,0.35); position:relative; }}
.tl.acc {{ color:{ACCENT}; }}
.strikebar {{ position:absolute; left:-4%; right:-4%; top:46%; height:22px; background:{CREAM}; display:block; transform-origin:0 50%; border-radius:6px; }}
.eqrow {{ display:flex; flex-direction:row; align-items:center; gap:34px; }}
.ecgbox {{ width:960px; height:170px; display:block; }}
.ecgbox svg {{ width:100%; height:100%; display:block; overflow:visible; }}
.raysbox {{ position:absolute; left:0; right:0; top:-40px; height:520px; display:block; }}
.raysbox svg {{ width:100%; height:100%; display:block; }}
.raysz {{ padding-top:60px; }}
svg .draw {{ fill:none; stroke:{CREAM}; stroke-width:12; stroke-linecap:round; stroke-linejoin:round; stroke-dasharray:1; stroke-dashoffset:0; }}
svg .draw.acc {{ stroke:{ACCENT}; }}
svg .glyph {{ font-family:'Archivo Black'; text-anchor:middle; fill:{ACCENT}; }}
svg .glyph.coin {{ font-size:78px; }}
svg .glyph.q {{ font-size:200px; }}
svg .bubble {{ fill:{CREAM}; }}
svg .btxt {{ font-family:'Montserrat'; font-weight:900; font-size:24px; text-anchor:middle; fill:{INK}; }}
svg .dot {{ fill:{INK}; }}
svg .hand {{ stroke:{ACCENT}; stroke-width:12; stroke-linecap:round; }}
svg .pin {{ fill:{CREAM}; }}
.ck {{ display:flex; flex-direction:row; align-items:center; gap:26px; width:900px; height:104px; }}
.ck .box {{ width:78px; height:78px; flex:none; display:block; }}
.ck rect {{ fill:rgba(255,210,63,0); stroke:{ACCENT}; stroke-width:7; }}
.ck .tick {{ fill:none; stroke:{INK}; stroke-width:10; stroke-linecap:round; stroke-linejoin:round; stroke-dasharray:1; stroke-dashoffset:1; }}
.ck span {{ font-family:'Archivo Black'; font-size:66px; color:{CREAM}; letter-spacing:-0.03em; white-space:nowrap; }}
.cklist {{ align-items:flex-start; padding-left:30px; gap:6px; }}
.cap {{ z-index:12; }}
.capline {{ position:absolute; left:50px; right:50px; top:1478px; height:180px; display:flex; flex-direction:row; flex-wrap:nowrap;
  align-items:center; justify-content:center; gap:46px; }}
.w {{ display:inline-block; font-family:'Montserrat'; font-weight:900; font-size:84px; line-height:1; color:{CREAM}; letter-spacing:-0.02em;
  -webkit-text-stroke:12px {INK}; paint-order:stroke fill; text-shadow:0 7px 0 {INK}, 0 10px 26px rgba(0,0,0,0.5); white-space:nowrap; }}
.w.key {{ color:{ACCENT}; }}
#cover {{ z-index:9; }}
#cover .ct {{ position:absolute; left:40px; right:40px; top:440px; height:1040px; display:flex; flex-direction:column; align-items:center; justify-content:center; }}
#cover .row {{ display:block; font-family:'League Gothic'; color:{CREAM}; line-height:0.88; letter-spacing:0.005em; white-space:nowrap; text-align:center;
  text-shadow:0 10px 0 rgba(0,0,0,0.45); }}
#cover .row2 {{ margin:6px 0 14px; }}
#cover .row2 .inner {{ display:block; color:{INK}; background:{ACCENT}; padding:4px 30px 0px; border-radius:18px; text-shadow:none; transform:rotate(-2deg); }}
#cover .tag {{ display:block; font-family:'Space Mono'; font-weight:700; font-size:40px; color:{ACCENT}; letter-spacing:0.18em; margin-bottom:18px; }}
#progress {{ position:absolute; left:0; bottom:0; width:1080px; height:10px; background:{ACCENT}; transform-origin:0 50%; z-index:14; }}
"""

def cover_html():
    r1 = "HOW TO STOP"; r2 = "BEING SCARED"; r3 = "TO START YOUR"; r4 = "OWN BUSINESS"
    return f'''<section class="clip" id="cover" data-start="0" data-duration="{COVER_END:.3f}" data-track-index="11">
  <div class="ct">
    <div class="tag">REAL TALK</div>
    <div class="row row1" style="font-size:250px">{r1}</div>
    <div class="row row2" style="font-size:236px"><span class="inner">{r2}</span></div>
    <div class="row row3" style="font-size:212px">{r3}</div>
    <div class="row row4" style="font-size:212px">{r4}</div>
  </div>
</section>'''

GRAIN = """<svg id="grain" width="1080" height="1920" xmlns="http://www.w3.org/2000/svg"><filter id="gn"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="4" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter><rect width="100%" height="100%" filter="url(#gn)"/></svg>"""

page = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>How to stop being scared to start your own business</title>
    <script src="assets/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
      <div id="stage"><div id="glow" data-layout-allow-overflow></div><div id="grid" data-layout-allow-overflow></div>{GRAIN}</div>
      <div id="camBox"><div id="camShake"><div id="camInner">
        <video id="cam" src="assets/edited.mp4" data-start="0" data-duration="{DUR}" data-track-index="0" playsinline data-has-audio="true"></video>
      </div></div></div>
      <div id="cardFrame"></div>
      <div id="scrim" class="clip" data-start="0" data-duration="{COVER_END:.3f}" data-track-index="5"></div>
      {cover_html()}
      {''.join(beats_html)}
      {''.join(cap_html)}
      <div id="progress"></div>
      {''.join(sfx_html)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {chr(10).join('      ' + x for x in js)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(PROJ + "index.html", "w").write(page)
print("beats", len(B), "shots", len(shots), "camsegs", len(cam_segs), "caps", len(caps), "sfx", len(sfx), "js lines", len(js))
# report shot lengths
mx = max(s["t1"] - s["t0"] for s in shots)
print("max shot", round(mx, 2))
json.dump(dict(periods=[(p[0], p[1], p[2]) for p in periods]), open(ASR + "periods.json", "w"))
