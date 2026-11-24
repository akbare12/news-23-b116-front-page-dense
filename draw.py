#!/usr/bin/env python3
"""news-23 b116 front-page-dense: draw entry.png (1024x1024)."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = os.path.join(FD, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FD, "DejaVuSans.ttf")
SANS_B = os.path.join(FD, "DejaVuSans-Bold.ttf")


def f(path, size):
    return ImageFont.truetype(path, size)


def tw(draw, text, font):
    return draw.textlength(text, font=font)


def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(draw, t, font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, text, font, x, y, max_w, fill, lh=None):
    lines = wrap(draw, text, font, max_w)
    if lh is None:
        lh = font.size + 2
    for i, ln in enumerate(lines):
        draw.text((x, y + i * lh), ln, font=font, fill=fill)
    return lines


def chip(draw, x_right, y, text, bg, size=9):
    font = f(SANS_B, size)
    w = int(tw(draw, text, font)) + 8
    x0 = x_right - w
    draw.rounded_rectangle([x0, y, x_right, y + 11], radius=2, fill=bg)
    draw.text((x0 + 4, y + 1), text, font=font, fill="white")
    return x0


img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

BLACK = (0, 0, 0)
RED = (183, 28, 28)
GOLD = (212, 175, 55)
NAVY = (31, 58, 147)
DARK = (51, 51, 51)
GRAY = (110, 110, 110)

# ---- Masthead ----
d.rectangle([0, 0, W, 54], fill=BLACK)
d.text((12, 7), "THE WORLD TODAY", font=f(SERIF_B, 38), fill="white")
dt = "MONDAY 23 NOVEMBER 2026"
d.text((W - 12 - tw(d, dt, f(SANS_B, 14)), 19), dt, font=f(SANS_B, 14), fill=GOLD)

# ---- Kicker ----
d.rectangle([0, 54, W, 74], fill=RED)
kick = "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B"
d.text(((W - tw(d, kick, f(SANS_B, 13))) / 2, 58), kick, font=f(SANS_B, 13), fill="white")

# ---- Number strip: 5 cols x 2 rows ----
strip = [
    [("-3.3%", "KOSPI"), ("5.3", "US-CHINA POWER GAP"), ("11,762", "EBOLA CASES, DRC"),
     ("10T won", "SEOUL STABILISATION FUND"), ("2%", "BILLIONAIRE TAX IN PARIS")],
    [("$450M", "SKUBAL DEAL"), ("165", "RUSSIAN MISSILES/WEEK"), ("12,000", "CLEARED IN MANCHESTER"),
     ("264 kg", "EXPLOSIVES SEIZED"), ("$107.3B", "ANTHROPIC IPO")],
]
for r in range(2):
    yv = 76 + r * 32
    yl = yv + 21
    for c in range(5):
        x0 = int(c * 204.8) + 8
        val, lab = strip[r][c]
        d.text((x0, yv), val, font=f(SANS_B, 19), fill=BLACK)
        d.text((x0, yl), lab, font=f(SANS_B, 8), fill=DARK)
    if r == 0:
        d.line([0, 106, W, 106], fill=(230, 230, 230), width=1)
d.line([0, 138, W, 138], fill=(200, 200, 200), width=1)

# ---- Region bar ----
regions = [("ASIA-PACIFIC 7", (31, 58, 147)), ("AMERICAS 8", (192, 57, 43)),
           ("MIDDLE EAST 6", (14, 124, 123)), ("EUROPE 5", (108, 52, 131)),
           ("AFRICA 3", (30, 132, 73)), ("WORLD 2", (51, 51, 51))]
for i, (label, col) in enumerate(regions):
    x0 = int(i * 170.67)
    x1 = int((i + 1) * 170.67)
    d.rectangle([x0, 138, x1, 158], fill=col)
    d.text((x0 + (x1 - x0 - tw(d, label, f(SANS_B, 11))) / 2, 142), label,
           font=f(SANS_B, 11), fill="white")

# ---- THE DAY IN UTC strip ----
utc = "THE DAY IN UTC  \u00b7  ~00:00 Kospi dives  \u00b7  ~05:30 Guterres opens  \u00b7  ~09:00 Power Index  \u00b7  ~12:00 Paris 2% tax  \u00b7  ~15:00 Kyiv missiles"
d.text((8, 160), utc, font=f(SANS, 10), fill=GRAY)
d.text((W - 8 - tw(d, "~ APPROX", f(SANS, 10)), 160), "~ APPROX", font=f(SANS, 10), fill=GRAY)

# ---- Heroes ----
HERO_Y0 = 174
SCENE_H = 96
STRIP_H = 16
COLW = 341


def hero_scene_kospi(x0):
    d.rectangle([x0, HERO_Y0, x0 + COLW, HERO_Y0 + SCENE_H], fill=(11, 30, 58))
    # buildings with lit windows
    import random
    rnd = random.Random(7)
    bx = x0 + 8
    while bx < x0 + COLW - 30:
        bw = rnd.randint(26, 44)
        bh = rnd.randint(28, 62)
        by = HERO_Y0 + SCENE_H - bh
        d.rectangle([bx, by, bx + bw, HERO_Y0 + SCENE_H], fill=(20, 48, 88))
        for wy in range(by + 5, HERO_Y0 + SCENE_H - 5, 9):
            for wx in range(bx + 4, bx + bw - 4, 9):
                if rnd.random() < 0.55:
                    d.rectangle([wx, wy, wx + 4, wy + 4], fill=(255, 214, 90))
        bx += bw + 4
    # falling chart line (kept clear of the -3.3% label)
    pts = [(x0 + 20, HERO_Y0 + 55), (x0 + 90, HERO_Y0 + 62), (x0 + 150, HERO_Y0 + 58),
           (x0 + 210, HERO_Y0 + 72), (x0 + 270, HERO_Y0 + 78), (x0 + 325, HERO_Y0 + 88)]
    d.line(pts, fill=(255, 140, 40), width=3)
    for p in pts:
        d.ellipse([p[0] - 3, p[1] - 3, p[0] + 3, p[1] + 3], fill="white")
    d.text((x0 + 8, HERO_Y0 + 4), "-3.3%", font=f(SANS_B, 30), fill="white")


def hero_scene_guterres(x0):
    d.rectangle([x0, HERO_Y0, x0 + COLW, HERO_Y0 + SCENE_H], fill=(26, 107, 60))
    cx, cy, r = x0 + COLW - 62, HERO_Y0 + 48, 34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(165, 214, 167))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(26, 107, 60), width=2)
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(26, 107, 60), width=2)
    d.arc([cx - 14, cy - r, cx + 14, cy + r], 90, 270, fill=(26, 107, 60), width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(26, 107, 60), width=2)
    d.text((x0 + 10, HERO_Y0 + 4), "150", font=f(SANS_B, 40), fill=GOLD)
    for i, ln in enumerate(["DELEGATES", "BACK A RISK", "FRAMEWORK"]):
        d.text((x0 + 10, HERO_Y0 + 46 + i * 16), ln, font=f(SANS_B, 15), fill=GOLD)


def hero_scene_power(x0):
    d.rectangle([x0, HERO_Y0, x0 + COLW, HERO_Y0 + SCENE_H], fill=(245, 240, 225))
    d.text((x0 + 10, HERO_Y0 + 5), "NARROWEST SINCE 2018", font=f(SANS_B, 12), fill=BLACK)
    d.text((x0 + COLW - 10 - tw(d, "GAP 5.3", f(SANS_B, 13)), HERO_Y0 + 5),
           "GAP 5.3", font=f(SANS_B, 13), fill=RED)
    base = HERO_Y0 + SCENE_H - 20
    bars = [("78.9", "US", 36, NAVY), ("73.6", "CHINA", 33, (192, 57, 43)), ("40.5", "INDIA", 19, (176, 141, 26))]
    for i, (val, name, hgt, col) in enumerate(bars):
        cx = x0 + 70 + i * 101
        d.rectangle([cx - 28, base - hgt, cx + 28, base], fill=col)
        d.text((cx - tw(d, val, f(SANS_B, 13)) / 2, base - hgt - 16), val, font=f(SANS_B, 13), fill=BLACK)
        d.text((cx - tw(d, name, f(SANS_B, 11)) / 2, base + 3), name, font=f(SANS_B, 11), fill=BLACK)


heroes = [
    ("KOSPI 4,708.54 \u00b7 -161 PTS", "AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
     "KOREA EXCHANGE", "REPORTED", hero_scene_kospi),
    ("UN \u00b7 BRIDGETOWN", "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
     "UNITED NATIONS", "REPORTED", hero_scene_guterres),
    ("ASIA POWER INDEX 2026", "US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
     "LOWY INSTITUTE", "REPORTED", hero_scene_power),
]
for i, (strip_txt, headline, body, source, chip_txt, scene_fn) in enumerate(heroes):
    x0 = i * COLW
    scene_fn(x0)
    # source strip under scene
    d.rectangle([x0, HERO_Y0 + SCENE_H, x0 + COLW, HERO_Y0 + SCENE_H + STRIP_H], fill=BLACK)
    d.text((x0 + 8, HERO_Y0 + SCENE_H + 3), strip_txt, font=f(SANS_B, 10), fill="white")
    hy = HERO_Y0 + SCENE_H + STRIP_H + 2
    draw_wrapped(d, headline, f(SANS_B, 16), x0 + 8, hy, COLW - 16, BLACK, lh=18)
    by = hy + 36
    draw_wrapped(d, body, f(SANS, 11), x0 + 8, by, COLW - 16, DARK, lh=12)
    sy = hy + 36 + 24 + 2
    d.text((x0 + 8, sy), source, font=f(SANS, 9), fill=GRAY)
    chip(d, x0 + COLW - 8, sy - 1, chip_txt, NAVY)

# ---- MORE OF THE DAY strip ----
MORE_Y = 362
d.rectangle([0, MORE_Y, W, MORE_Y + 16], fill=BLACK)
d.text((8, MORE_Y + 2), "MORE OF THE DAY  \u2014  10 STORIES", font=f(SANS_B, 12), fill="white")

# ---- 10 cards ----
cards = [
    ("AMERICAS", (192, 57, 43), "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "WSJ", "REPORTED"),
    ("AMERICAS", (192, 57, 43), "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED"),
    ("WHITE HOUSE", (108, 52, 131), "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED"),
    ("MARKETS", (14, 124, 123), "US FUTURES JUMP 3%", "Holiday rally lifts 3%.", "Bloomberg", "REPORTED"),
    ("SPORT", (176, 141, 26), "SKUBAL'S $450M METS DEAL", "Nine-year, largest ever.", "AP", "REPORTED"),
    ("SPORT", (176, 141, 26), "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.", "ESPN", "REPORTED"),
    ("LEGAL", (30, 132, 73), "STATES SUE SPACEX", "Ten states sue over AI.", "AP", "REPORTED"),
    ("TECH", (31, 58, 147), "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.", "WSJ", "REPORTED"),
    ("EUROPE", (108, 52, 131), "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: 3 Kh-101s crossed.", "AP", "CLAIM"),
    ("SPACE", (51, 51, 51), "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM"),
]
CARD_Y0 = MORE_Y + 16
CARD_H = 62
for idx, (cat, ccol, head, body, source, chip_txt) in enumerate(cards):
    r, c = divmod(idx, 5)
    x0 = int(c * 204.8)
    y0 = CARD_Y0 + r * CARD_H
    d.text((x0 + 4, y0 + 3), cat, font=f(SANS_B, 8), fill=ccol)
    d.text((x0 + 200 - tw(d, str(idx + 1), f(SANS_B, 11)), y0 + 2), str(idx + 1),
           font=f(SANS_B, 11), fill=RED)
    draw_wrapped(d, head, f(SANS_B, 11), x0 + 4, y0 + 16, 196, BLACK, lh=13)
    d.text((x0 + 4, y0 + 44), body, font=f(SANS, 10), fill=DARK)
    d.text((x0 + 4, y0 + 53), source, font=f(SANS, 8), fill=GRAY)
    chip(d, x0 + 200, y0 + 50, chip_txt, NAVY if chip_txt == "REPORTED" else RED, size=8)
    if c < 4:
        d.line([x0 + 204, y0 + 2, x0 + 204, y0 + CARD_H - 2], fill=(225, 225, 225), width=1)
d.line([0, CARD_Y0 + 2 * CARD_H, W, CARD_Y0 + 2 * CARD_H], fill=(200, 200, 200), width=1)

# ---- WHERE IT HAPPENED strip ----
WHERE_Y = CARD_Y0 + 2 * CARD_H
d.rectangle([0, WHERE_Y, W, WHERE_Y + 16], fill=BLACK)
d.text((8, WHERE_Y + 2), "WHERE IT HAPPENED", font=f(SANS_B, 12), fill="white")

# ---- Map (left) ----
MAP_X0, MAP_Y0 = 8, WHERE_Y + 22
LAND = (198, 226, 190)
d.polygon([(30, 545), (110, 535), (140, 555), (130, 600), (95, 615), (70, 640), (45, 600), (25, 575)], fill=LAND)
d.polygon([(75, 650), (110, 650), (125, 690), (110, 740), (85, 765), (65, 720), (60, 680)], fill=LAND)
d.polygon([(172, 538), (235, 535), (245, 560), (225, 585), (195, 580), (170, 558)], fill=LAND)
d.polygon([(190, 600), (240, 595), (250, 640), (235, 700), (205, 715), (185, 660), (182, 625)], fill=LAND)
d.polygon([(240, 545), (330, 535), (335, 580), (320, 640), (290, 660), (258, 625), (240, 585)], fill=LAND)
d.polygon([(295, 725), (325, 720), (330, 745), (300, 755), (290, 740)], fill=LAND)
pins = [(315, 570), (88, 705), (295, 552), (70, 600), (95, 585), (218, 562),
        (206, 576), (194, 560), (236, 545), (178, 542), (255, 592), (248, 610), (212, 655)]
for i, (px, py) in enumerate(pins, 1):
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline="white", width=1)
    t = str(i)
    d.text((px - tw(d, t, f(SANS_B, 9)) / 2, py - 6), t, font=f(SANS_B, 9), fill="white")
leg = ["Pins 1\u201313:  1 Seoul  \u00b7  2 Bridgetown  \u00b7  3 Beijing  \u00b7  4 Washington",
       "5 New York  \u00b7  6 Kyiv  \u00b7  7 Paris  \u00b7  8 London  \u00b7  9 Warsaw  \u00b7  10 Manchester",
       "11 Beirut  \u00b7  12 Gaza  \u00b7  13 Khartoum"]
for i, ln in enumerate(leg):
    d.text((8, 768 + i * 11), ln, font=f(SANS, 9), fill=DARK)

# ---- ALSO list (right) ----
ALSO_X = 348
d.text((ALSO_X, WHERE_Y + 22), "ALSO ON MONDAY", font=f(SANS_B, 13), fill=BLACK)
also = [
    ("14. Paris: 100+ back 2% billionaire tax", None),
    ("15. Manchester: 12,000 cleared", None),
    ("16. Zelenskyy: 165 missiles in a week", None),
    ("17. COP31: the day after Antalya pact rejected", None),
    ("18. Israel unity talks resume", None),
    ("19. Gaza: two killed in Israeli strike", None),
    ("20. West Bank settler attacks", None),
    ("21. Iran war: no deal in sight", None),
    ("22. Lebanon seizes 264 kg explosives", None),
    ("23. Bahrain: strike hits plant, 2 hurt", None),
    ("24. Benghazi: UN demands probe", "[CLAIM]"),
    ("25. Sudan: defences down drones", "[CLAIM]"),
    ("26. DRC: fighting traps Ebola teams", None),
    ("27. Bangladesh: Hasina jailed if she returns", None),
    ("28. Seoul minister quits in exam row", None),
    ("29. SK Telecom -7.3% as hype cools", None),
    ("30. China eases margin rules", None),
    ("31. Seoul readies 10T-won fund", None),
]
for i, (txt, tag) in enumerate(also):
    col = 0 if i < 9 else 1
    row = i % 9
    x = ALSO_X + col * 336
    y = WHERE_Y + 44 + row * 28
    lines = wrap(d, txt, f(SANS, 11), 328)
    draw_wrapped(d, txt, f(SANS, 11), x, y, 328, BLACK, lh=13)
    if tag:
        d.text((x + tw(d, txt, f(SANS, 11)) + 4, y), tag, font=f(SANS_B, 10), fill=RED)

# ---- DATE CHECK box ----
DC_Y0 = 800
d.rectangle([8, DC_Y0, W - 8, 880], outline=RED, width=3)
d.text((16, DC_Y0 + 6), "DATE CHECK  \u2014  READ 23 NOV 2026, 23:59 UTC  \u00b7  STORIES DATED 23 NOV ONLY",
       font=f(SANS_B, 12), fill=RED)
d.text((16, DC_Y0 + 28),
       "LEFT OUT \u2014 NOT 23 NOV: Dems reach 258 (22 Nov) \u00b7 Sparta II fire (22 Nov) \u00b7 El Chapo Isidro captured (22 Nov) \u00b7 EU\u2013Indonesia pact (21 Nov) \u00b7 Nigeria boat (21 Nov) \u00b7 ICJ Myanmar ruling (19 Nov)",
       font=f(SANS, 9), fill=BLACK)
d.text((16, DC_Y0 + 50),
       "NOT YET \u2014  Dymer search continues (14 missing)  \u00b7  4 House races uncalled  \u00b7  COP32 venue not set  \u00b7  WHO evacuating trapped Ebola staff",
       font=f(SANS, 10), fill=BLACK)

# ---- Footer ----
d.text((8, 892), "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).",
       font=f(SANS, 10), fill=GRAY)
d.text((8, 910), "CHIPS: REPORTED = confirmed by wires \u00b7 CLAIM = one side's claim, not independently confirmed \u00b7 ONGOING = still developing.",
       font=f(SANS, 10), fill=GRAY)
d.text((8, 928), "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
       font=f(SANS, 10), fill=GRAY)
bot = "THE WORLD TODAY  \u00b7  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions"
d.text(((W - tw(d, bot, f(SANS_B, 13))) / 2, 994), bot, font=f(SANS_B, 13), fill=(150, 110, 20))

img.save(OUT, optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes")
