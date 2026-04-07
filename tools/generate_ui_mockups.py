from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "mockups"
OUT.mkdir(parents=True, exist_ok=True)

BG = "#0D1117"
CARD = "#161B22"
CARD_2 = "#0F141B"
TEXT = "#F0F6FC"
MUTED = "#8B949E"
BLUE = "#58A6FF"
BLUE_2 = "#1F6FEB"
GREEN = "#39D353"
GREEN_2 = "#26A641"
YELLOW = "#D29922"
RED = "#F85149"


def load_font(size: int, bold: bool = False, condensed: bool = False):
    candidates = []
    if condensed:
        candidates.extend(
            [
                "C:/Windows/Fonts/impact.ttf",
                "C:/Windows/Fonts/arialbd.ttf",
            ]
        )
    if bold:
        candidates.extend(
            [
                "C:/Windows/Fonts/arialbd.ttf",
                "C:/Windows/Fonts/segoeuib.ttf",
                "C:/Windows/Fonts/bahnschrift.ttf",
            ]
        )
    candidates.extend(
        [
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/calibri.ttf",
        ]
    )
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size=size)
            except OSError:
                continue
    return ImageFont.load_default()


def rounded(draw, xy, fill, radius=24, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def text(draw, xy, value, size=24, fill=TEXT, bold=False, condensed=False, anchor=None):
    font = load_font(size, bold=bold, condensed=condensed)
    draw.text(xy, value, fill=fill, font=font, anchor=anchor)


def pill(draw, x, y, w, h, label, fill, fg="#0D1117", size=14):
    rounded(draw, (x, y, x + w, y + h), fill, radius=h // 2)
    text(draw, (x + w / 2, y + h / 2), label, size=size, fill=fg, bold=True, anchor="mm")


def wrapped(draw, x, y, value, width, size=16, fill=MUTED, line_gap=6, bold=False):
    font = load_font(size, bold=bold)
    words = value.split()
    lines = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    yy = y
    for line in lines:
        draw.text((x, yy), line, fill=fill, font=font)
        bbox = draw.textbbox((0, 0), line, font=font)
        yy += (bbox[3] - bbox[1]) + line_gap
    return yy


def draw_mobile_programs():
    img = Image.new("RGB", (430, 1220), BG)
    d = ImageDraw.Draw(img)
    text(d, (24, 24), "PROGRAMS", size=56, condensed=True)
    text(d, (24, 88), "MANAGE YOUR WORKOUT STRUCTURE", size=14, fill=MUTED, bold=True)
    pill(d, 320, 34, 86, 36, "+ New", BLUE, fg=BG, size=14)

    rounded(d, (20, 140, 410, 420), CARD, outline="#223244")
    text(d, (40, 165), "ACTIVE PROGRAM", size=14, fill=BLUE, bold=True)
    text(d, (40, 190), "PUSH PULL LEGS", size=52, condensed=True)
    wrapped(d, 40, 252, "3 splits, 18 planned exercises, used 4x this week.", 280, size=16, fill="#C9D1D9")
    pill(d, 318, 168, 70, 28, "Active", "#173726", fg=GREEN, size=13)

    stats = [("Splits", "3", TEXT), ("Exercises", "18", BLUE), ("Next", "PULL", GREEN)]
    for i, (label, value, color) in enumerate(stats):
        x = 40 + i * 118
        rounded(d, (x, 318, x + 104, 392), CARD_2)
        text(d, (x + 16, 332), label.upper(), size=11, fill=MUTED, bold=True)
        text(d, (x + 16, 350), value, size=30, fill=color, condensed=True)

    rounded(d, (40, 406, 218, 456), CARD_2)
    text(d, (129, 431), "Edit Program", size=16, bold=True, anchor="mm")
    rounded(d, (232, 406, 390, 456), BLUE)
    text(d, (311, 431), "Start Split", size=16, fill=BG, bold=True, anchor="mm")

    text(d, (24, 486), "MY PROGRAMS", size=24, bold=True)
    text(d, (350, 492), "3 total", size=14, fill=MUTED)

    items = [
        ("Push Pull Legs", "PUSH • PULL • LEG", "18 exercises", "Updated today", GREEN, "Active"),
        ("Upper Lower", "UPPER • LOWER", "12 exercises", "Used last month", MUTED, "Inactive"),
        ("Full Body A/B", "DAY A • DAY B", "9 exercises", "Needs review", YELLOW, "Draft"),
    ]
    y = 530
    for name, subtitle, tag1, tag2, color, status in items:
        rounded(d, (20, y, 410, y + 140), CARD, outline="#1F2733")
        text(d, (38, y + 22), name, size=22, bold=True)
        text(d, (340, y + 24), status, size=14, fill=color)
        text(d, (38, y + 56), subtitle, size=15, fill=MUTED)
        pill(d, 38, y + 90, 110, 28, tag1, CARD_2, fg=MUTED, size=12)
        pill(d, 158, y + 90, 118, 28, tag2, CARD_2, fg=MUTED, size=12)
        y += 156

    rounded(d, (20, 1070, 410, 1142), BLUE)
    text(d, (215, 1106), "CREATE PROGRAM", size=34, fill=BG, condensed=True, anchor="mm")
    text(d, (215, 1168), "Duplicate   Archive   Reorder soon", size=13, fill=MUTED, anchor="mm")
    return img


def draw_mobile_builder():
    img = Image.new("RGB", (430, 1500), BG)
    d = ImageDraw.Draw(img)
    pill(d, 22, 24, 42, 42, "<", CARD, fg=TEXT, size=18)
    text(d, (78, 26), "PROGRAM BUILDER", size=48, condensed=True)
    text(d, (78, 82), "CREATE OR UPDATE PROGRAM", size=14, fill=MUTED, bold=True)
    pill(d, 282, 34, 126, 34, "Autosave draft", "#173726", fg=GREEN, size=13)

    rounded(d, (20, 128, 410, 390), CARD, outline="#1F2733")
    text(d, (40, 154), "PROGRAM DETAILS", size=22, bold=True)
    text(d, (40, 198), "PROGRAM NAME", size=12, fill=MUTED, bold=True)
    rounded(d, (40, 220, 390, 270), CARD_2)
    text(d, (58, 236), "Push Pull Legs", size=18)
    text(d, (40, 294), "DESCRIPTION", size=12, fill=MUTED, bold=True)
    rounded(d, (40, 316, 390, 376), CARD_2)
    wrapped(d, 58, 332, "Classic 3-day rotation focused on strength and hypertrophy with room for ad-hoc accessories.", 300, size=14)

    text(d, (24, 426), "SPLITS & EXERCISES", size=24, bold=True)
    text(d, (315, 432), "+ Add split", size=15, fill=BLUE)

    y = 468
    split_cards = [
        ("PUSH", True, [("Bench Press", "4 sets • 6-8 reps"), ("Incline DB Press", "3 sets • 8-10 reps"), ("Shoulder Press", "3 sets • 8-10 reps")]),
        ("PULL", False, []),
        ("LEG", False, []),
    ]
    for name, expanded, exercises in split_cards:
        h = 270 if expanded else 120
        fill = "#1A2430" if expanded else CARD
        outline = "#2B4A68" if expanded else "#1F2733"
        rounded(d, (20, y, 410, y + h), fill, outline=outline)
        text(d, (40, y + 24), name, size=26, bold=True)
        text(d, (330, y + 28), f"{5 if name=='PUSH' else 6 if name=='PULL' else 7} exercises", size=13, fill=BLUE if expanded else MUTED)
        if expanded:
            yy = y + 66
            for ex_name, meta in exercises:
                rounded(d, (40, yy, 390, yy + 54), CARD_2)
                text(d, (56, yy + 10), ex_name, size=16, bold=True)
                text(d, (56, yy + 30), meta, size=12, fill=MUTED)
                text(d, (346, yy + 18), "Edit", size=13, fill=MUTED)
                yy += 64
            rounded(d, (40, y + 224, 206, y + 258), CARD_2)
            text(d, (123, y + 241), "+ Add exercise", size=14, bold=True, anchor="mm")
            rounded(d, (224, y + 224, 390, y + 258), CARD_2)
            text(d, (307, y + 241), "Rename split", size=14, fill=MUTED, anchor="mm")
        else:
            rounded(d, (40, y + 62, 390, y + 102), CARD_2)
            text(d, (215, y + 82), "Open split details", size=14, fill=BLUE, bold=True, anchor="mm")
        y += h + 14

    rounded(d, (20, 1390, 410, 1462), GREEN_2)
    text(d, (215, 1426), "SAVE PROGRAM", size=34, fill=BG, condensed=True, anchor="mm")
    return img


def draw_mobile_split_selector():
    img = Image.new("RGB", (430, 980), BG)
    d = ImageDraw.Draw(img)
    pill(d, 22, 24, 42, 42, "<", CARD, fg=TEXT, size=18)
    text(d, (78, 26), "SPLIT SELECTOR", size=48, condensed=True)
    text(d, (78, 82), "CHOOSE FROM YOUR ACTIVE PROGRAM", size=14, fill=MUTED, bold=True)
    rounded(d, (20, 128, 410, 330), CARD, outline="#223244")
    text(d, (40, 154), "PROGRAM IN ROTATION", size=14, fill=BLUE, bold=True)
    text(d, (40, 178), "PUSH PULL LEGS", size=46, condensed=True)
    wrapped(d, 40, 232, "Completed splits are dimmed. The next recommended split is highlighted.", 330, size=15, fill="#C9D1D9")
    rounded(d, (40, 280, 192, 316), CARD_2)
    rounded(d, (212, 280, 370, 316), CARD_2)
    text(d, (58, 292), "Cycle done 1/3", size=13)
    text(d, (230, 292), "Last split PUSH", size=13)

    cards = [
        ("PULL", "6 exercises • lats, rows, rear delts, biceps", BLUE, "Next", True),
        ("PUSH", "5 exercises • chest, shoulders, triceps", "#2C3643", "Done", False),
        ("LEG", "7 exercises • quads, hamstrings, glutes, calves", CARD, "Pending", False),
    ]
    y = 360
    for name, desc, fill, status, next_flag in cards:
        rounded(d, (20, y, 410, y + 156), fill, outline="#2B4A68" if next_flag else "#1F2733")
        text(d, (40, y + 24), name, size=28, bold=True)
        pill(d, 320, y + 22, 62 if status != "Pending" else 82, 28, status, BLUE if next_flag else "#173726" if status == "Done" else CARD_2, fg=BG if next_flag else GREEN if status == "Done" else MUTED, size=12)
        wrapped(d, 40, y + 62, desc, 320, size=15, fill="#C9D1D9")
        rounded(d, (40, y + 106, 390, y + 142), CARD_2)
        text(d, (215, y + 124), "Start this split" if next_flag else "Completed yesterday" if status == "Done" else "Preview exercises", size=14, fill=TEXT if next_flag else MUTED if status == "Done" else TEXT, bold=True, anchor="mm")
        y += 170

    rounded(d, (20, 894, 410, 946), CARD)
    text(d, (215, 920), "Quick Start instead", size=15, bold=True, anchor="mm")
    return img


def draw_mobile_history():
    img = Image.new("RGB", (430, 1320), BG)
    d = ImageDraw.Draw(img)
    text(d, (24, 24), "HISTORY", size=56, condensed=True)
    text(d, (24, 88), "WORKOUTS, EXERCISES, AND PROGRESSION", size=14, fill=MUTED, bold=True)
    rounded(d, (20, 132, 410, 190), CARD)
    text(d, (40, 150), "Search exercise or date...", size=16, fill=MUTED)

    rounded(d, (20, 214, 410, 306), CARD, outline="#223244")
    text(d, (40, 236), "APRIL OVERVIEW", size=14, fill=BLUE, bold=True)
    stats = [("Sessions", "8"), ("Streak", "12"), ("Best lift", "65x8")]
    for i, (label, value) in enumerate(stats):
        x = 40 + i * 118
        text(d, (x, 262), label.upper(), size=11, fill=MUTED, bold=True)
        text(d, (x, 278), value, size=28, condensed=True, fill=GREEN if label == "Streak" else BLUE if label == "Best lift" else TEXT)

    text(d, (24, 338), "RECENT WORKOUTS", size=24, bold=True)
    y = 378
    workouts = [
        ("Apr 4 • PUSH", "18 sets • 8,420 kg volume", "Fresh", GREEN),
        ("Apr 3 • PULL", "16 sets • upper back focus", "Fresh", GREEN),
        ("Apr 1 • LEG", "14 sets • lower energy", "Tired", YELLOW),
    ]
    for title, meta, tag, color in workouts:
        rounded(d, (20, y, 410, y + 104), CARD)
        text(d, (40, y + 20), title, size=20, bold=True)
        text(d, (40, y + 50), meta, size=14, fill=MUTED)
        pill(d, 320, y + 24, 62 if tag == "Fresh" else 66, 28, tag, "#173726" if tag == "Fresh" else "#3A2D15", fg=color, size=12)
        y += 118

    text(d, (24, 756), "EXERCISE PROGRESS", size=24, bold=True)
    rounded(d, (20, 796, 410, 1048), CARD, outline="#1F2733")
    text(d, (40, 820), "BENCH PRESS", size=18, bold=True)
    text(d, (40, 846), "Top set trend over time", size=14, fill=MUTED)
    points = [(54, 972), (112, 950), (170, 938), (228, 900), (286, 880), (344, 850)]
    d.line(points, fill=BLUE, width=4)
    for px, py in points:
        d.ellipse((px - 5, py - 5, px + 5, py + 5), fill=GREEN)
    text(d, (40, 1008), "55x8   57.5x10   60x10   65x8", size=13, fill=MUTED)

    rounded(d, (20, 1074, 410, 1256), CARD)
    text(d, (40, 1098), "HEATMAP INSPECT", size=18, bold=True)
    text(d, (40, 1126), "Tap a date to open workout detail and daily flag.", size=14, fill=MUTED)
    # simple heatmap rows
    for row in range(3):
        for col in range(12):
            color = [CARD_2, "#0E4429", "#006D32", "#26A641", GREEN][(row + col) % 5]
            rounded(d, (40 + col * 28, 1172 + row * 28, 60 + col * 28, 1192 + row * 28), color, radius=5)
    return img


def draw_mobile_pt():
    img = Image.new("RGB", (430, 1280), BG)
    d = ImageDraw.Draw(img)
    text(d, (24, 24), "PT ZONE", size=56, condensed=True)
    text(d, (24, 88), "MEMBER ACCESS AND COACH MONITORING", size=14, fill=MUTED, bold=True)

    rounded(d, (20, 132, 410, 344), CARD, outline="#223244")
    text(d, (40, 156), "INVITE A PT", size=22, bold=True)
    wrapped(d, 40, 190, "Generate a 48-hour invite code so your trainer can view your workout history, heatmap, and progress.", 320, size=15, fill="#C9D1D9")
    rounded(d, (40, 250, 256, 306), BLUE)
    text(d, (148, 278), "CREATE INVITE CODE", size=24, fill=BG, condensed=True, anchor="mm")
    rounded(d, (274, 250, 390, 306), CARD_2)
    text(d, (332, 278), "Share link", size=14, anchor="mm")

    text(d, (24, 380), "ACTIVE ACCESS", size=24, bold=True)
    rounded(d, (20, 420, 410, 610), CARD)
    text(d, (40, 444), "COACH ANDI", size=22, bold=True)
    text(d, (40, 474), "Read-only access • 31 workouts viewed", size=14, fill=MUTED)
    rounded(d, (40, 514, 390, 560), CARD_2)
    text(d, (56, 528), "Last note", size=12, fill=MUTED, bold=True)
    text(d, (56, 544), "Bench tempo looked more stable this week.", size=14)
    rounded(d, (40, 574, 206, 598), "#173726")
    rounded(d, (224, 574, 390, 598), "#33191A")
    text(d, (123, 586), "View profile", size=13, fill=GREEN, anchor="mm")
    text(d, (307, 586), "Revoke access", size=13, fill=RED, anchor="mm")

    rounded(d, (20, 638, 410, 860), CARD, outline="#1F2733")
    text(d, (40, 662), "PT VIEW PREVIEW", size=22, bold=True)
    wrapped(d, 40, 696, "When you log in as a trainer, you see member list, consistency heatmap, workout history, and comments only.", 320, size=15, fill="#C9D1D9")
    rounded(d, (40, 758, 390, 824), CARD_2)
    text(d, (56, 774), "Members", size=12, fill=MUTED, bold=True)
    text(d, (56, 794), "Bro Jimbo   •   12-day streak   •   Fresh yesterday", size=15)

    text(d, (24, 896), "COMMENTS", size=24, bold=True)
    y = 936
    comments = [
        ("Apr 4", "Coach Andi", "Bench lockout looked cleaner. Keep this pace."),
        ("Apr 1", "Coach Andi", "Leg day still completed even with low energy. Good consistency."),
    ]
    for date, author, body in comments:
        rounded(d, (20, y, 410, y + 116), CARD)
        text(d, (40, y + 18), f"{date} • {author}", size=16, bold=True)
        wrapped(d, 40, y + 48, body, 330, size=15, fill=MUTED)
        y += 130
    return img


def draw_desktop_programs():
    img = Image.new("RGB", (1440, 900), BG)
    d = ImageDraw.Draw(img)
    rounded(d, (24, 24, 286, 876), CARD, outline="#1F2733")
    text(d, (48, 48), "JIMBOR", size=72, condensed=True)
    text(d, (48, 116), "PROGRAMS DESKTOP", size=14, fill=MUTED, bold=True)
    nav = ["Home", "Programs", "Builder", "History", "PT Zone"]
    y = 164
    for item in nav:
        fill = "#203450" if item == "Programs" else CARD_2
        rounded(d, (48, y, 238, y + 48), fill)
        text(d, (72, y + 14), item, size=18, bold=item == "Programs")
        y += 60

    text(d, (324, 36), "PROGRAMS MANAGEMENT", size=68, condensed=True)
    text(d, (324, 102), "Create, edit, activate, and review all workout programs from one place.", size=18, fill=MUTED)
    pill(d, 1240, 48, 150, 40, "+ Create Program", BLUE, fg=BG, size=16)

    rounded(d, (324, 152, 902, 408), CARD, outline="#223244")
    text(d, (356, 182), "ACTIVE PROGRAM", size=16, fill=BLUE, bold=True)
    text(d, (356, 208), "PUSH PULL LEGS", size=86, condensed=True)
    wrapped(d, 356, 308, "3 splits, 18 exercises, rotation currently points to PULL. Last updated today.", 430, size=18, fill="#C9D1D9")
    for i, (label, value, color) in enumerate([("Splits", "3", TEXT), ("Exercises", "18", BLUE), ("Next", "PULL", GREEN)]):
        x = 356 + i * 164
        rounded(d, (x, 348, x + 140, 394), CARD_2)
        text(d, (x + 18, 360), label.upper(), size=12, fill=MUTED, bold=True)
        text(d, (x + 18, 372), value, size=34, fill=color, condensed=True)

    rounded(d, (934, 152, 1416, 408), CARD)
    text(d, (966, 182), "QUICK ACTIONS", size=18, bold=True)
    for idx, label in enumerate(["Start Split", "Edit Program", "Duplicate Program", "Archive Drafts"]):
        rounded(d, (966, 222 + idx * 46, 1384, 260 + idx * 46), BLUE if idx == 0 else CARD_2)
        text(d, (990, 232 + idx * 46), label, size=18, fill=BG if idx == 0 else TEXT, bold=True)

    text(d, (324, 446), "PROGRAM LIBRARY", size=30, bold=True)
    card_y = 492
    for idx, (title, meta, status, color) in enumerate([
        ("Push Pull Legs", "PUSH • PULL • LEG • 18 exercises", "Active", GREEN),
        ("Upper Lower", "UPPER • LOWER • 12 exercises", "Inactive", MUTED),
        ("Full Body A/B", "DAY A • DAY B • 9 exercises", "Draft", YELLOW),
    ]):
        x = 324 + idx * 368
        rounded(d, (x, card_y, x + 340, card_y + 216), CARD, outline="#1F2733")
        text(d, (x + 24, card_y + 24), title, size=28, bold=True)
        text(d, (x + 24, card_y + 62), meta, size=15, fill=MUTED)
        pill(d, x + 24, card_y + 98, 84 if status != "Inactive" else 92, 28, status, CARD_2, fg=color, size=13)
        rounded(d, (x + 24, card_y + 154, x + 316, card_y + 194), CARD_2)
        text(d, (x + 170, card_y + 174), "Open details", size=16, anchor="mm")
    return img


def draw_desktop_builder():
    img = Image.new("RGB", (1440, 900), BG)
    d = ImageDraw.Draw(img)
    text(d, (36, 32), "PROGRAM BUILDER", size=70, condensed=True)
    text(d, (36, 102), "Create and update program metadata, split names, and exercise templates.", size=18, fill=MUTED)
    pill(d, 1212, 42, 180, 40, "Save Program", GREEN, fg=BG, size=18)

    rounded(d, (36, 152, 438, 418), CARD)
    text(d, (64, 182), "PROGRAM DETAILS", size=20, bold=True)
    text(d, (64, 226), "Program Name", size=13, fill=MUTED, bold=True)
    rounded(d, (64, 248, 410, 294), CARD_2)
    text(d, (84, 260), "Push Pull Legs", size=20)
    text(d, (64, 324), "Description", size=13, fill=MUTED, bold=True)
    rounded(d, (64, 346, 410, 394), CARD_2)
    text(d, (84, 360), "Classic rotation for strength + hypertrophy", size=16, fill=MUTED)

    rounded(d, (468, 152, 940, 760), CARD, outline="#223244")
    text(d, (500, 182), "SPLITS", size=20, bold=True)
    pill(d, 814, 176, 94, 30, "+ Add split", BLUE, fg=BG, size=14)
    split_y = 228
    for idx, name in enumerate(["PUSH", "PULL", "LEG"]):
        rounded(d, (500, split_y, 908, split_y + 144), "#1A2430" if idx == 0 else CARD_2, outline="#2B4A68" if idx == 0 else None)
        text(d, (524, split_y + 22), name, size=28, bold=True)
        text(d, (812, split_y + 26), f"{5 + idx} exercises", size=14, fill=BLUE if idx == 0 else MUTED)
        if idx == 0:
            for e_idx, ex_name in enumerate(["Bench Press", "Incline DB Press", "Shoulder Press"]):
                rounded(d, (524, split_y + 58 + e_idx * 24, 860, split_y + 80 + e_idx * 24), CARD)
                text(d, (540, split_y + 62 + e_idx * 24), ex_name, size=14)
        else:
            text(d, (524, split_y + 70), "Open split details", size=16, fill=BLUE)
        split_y += 160

    rounded(d, (970, 152, 1404, 760), CARD)
    text(d, (1000, 182), "EXERCISE EDITOR", size=20, bold=True)
    text(d, (1000, 220), "Bench Press", size=34, bold=True)
    for idx, line in enumerate(["Target sets: 4", "Target reps: 6-8", "Notes: Main strength lift for push day"]):
        rounded(d, (1000, 272 + idx * 68, 1372, 324 + idx * 68), CARD_2)
        text(d, (1020, 288 + idx * 68), line, size=18)
    rounded(d, (1000, 504, 1180, 550), BLUE)
    text(d, (1090, 527), "+ Add exercise", size=18, fill=BG, bold=True, anchor="mm")
    rounded(d, (1192, 504, 1372, 550), CARD_2)
    text(d, (1282, 527), "Delete selected", size=17, fill=RED, anchor="mm")
    return img


def draw_desktop_split_selector():
    img = Image.new("RGB", (1440, 900), BG)
    d = ImageDraw.Draw(img)
    text(d, (36, 32), "SPLIT SELECTOR", size=70, condensed=True)
    text(d, (36, 102), "Visual rotation status for program-driven workout starts.", size=18, fill=MUTED)

    rounded(d, (36, 152, 1404, 300), CARD, outline="#223244")
    text(d, (72, 182), "PROGRAM IN ROTATION", size=16, fill=BLUE, bold=True)
    text(d, (72, 206), "PUSH PULL LEGS", size=84, condensed=True)
    wrapped(d, 560, 196, "Completed splits are muted. The next recommended split is highlighted. Rotation resets after all splits are completed.", 720, size=18, fill="#C9D1D9")

    cards = [
        ("PULL", BLUE, "Next", "6 exercises • lats, rows, rear delts, biceps"),
        ("PUSH", "#202B36", "Done", "5 exercises • chest, shoulders, triceps"),
        ("LEG", CARD, "Pending", "7 exercises • quads, hamstrings, glutes, calves"),
    ]
    for idx, (name, fill, status, desc) in enumerate(cards):
        x = 36 + idx * 460
        rounded(d, (x, 344, x + 412, 650), fill, outline="#2B4A68" if idx == 0 else "#1F2733")
        text(d, (x + 28, 374), name, size=54, condensed=True)
        pill(d, x + 292, 374, 88 if status == "Pending" else 68, 30, status, BLUE if status == "Next" else "#173726" if status == "Done" else CARD_2, fg=BG if status == "Next" else GREEN if status == "Done" else MUTED, size=13)
        wrapped(d, x + 28, 452, desc, 340, size=18, fill="#C9D1D9")
        rounded(d, (x + 28, 566, x + 384, 614), CARD_2)
        text(d, (x + 206, 590), "Start this split" if status == "Next" else "Completed yesterday" if status == "Done" else "Preview exercises", size=18, anchor="mm")

    rounded(d, (36, 704, 300, 760), CARD)
    text(d, (168, 732), "Quick Start instead", size=18, bold=True, anchor="mm")
    return img


def draw_desktop_history():
    img = Image.new("RGB", (1440, 900), BG)
    d = ImageDraw.Draw(img)
    text(d, (36, 32), "HISTORY", size=72, condensed=True)
    text(d, (36, 102), "Workout timeline, exercise lookup, heatmap, and progression.", size=18, fill=MUTED)

    rounded(d, (36, 152, 404, 836), CARD)
    text(d, (64, 182), "WORKOUTS", size=22, bold=True)
    for idx, (title, meta, tag, color) in enumerate([
        ("Apr 4 • PUSH", "18 sets • 8,420 kg", "Fresh", GREEN),
        ("Apr 3 • PULL", "16 sets • upper back focus", "Fresh", GREEN),
        ("Apr 1 • LEG", "14 sets • lower energy", "Tired", YELLOW),
        ("Mar 29 • PUSH", "17 sets • incline emphasis", "Fresh", GREEN),
    ]):
        y = 230 + idx * 124
        rounded(d, (64, y, 376, y + 98), CARD_2)
        text(d, (86, y + 18), title, size=22, bold=True)
        text(d, (86, y + 52), meta, size=15, fill=MUTED)
        pill(d, 294, y + 20, 62 if tag == "Fresh" else 66, 28, tag, "#173726" if tag == "Fresh" else "#3A2D15", fg=color, size=12)

    rounded(d, (434, 152, 968, 420), CARD, outline="#223244")
    text(d, (462, 182), "EXERCISE SEARCH", size=22, bold=True)
    rounded(d, (462, 224, 940, 276), CARD_2)
    text(d, (484, 240), "Search: Bench Press", size=18, fill=MUTED)
    text(d, (462, 312), "BENCH PRESS TREND", size=18, fill=BLUE, bold=True)
    pts = [(490, 372), (560, 354), (630, 340), (700, 310), (770, 286), (840, 256), (910, 236)]
    d.line(pts, fill=BLUE, width=5)
    for px, py in pts:
        d.ellipse((px - 6, py - 6, px + 6, py + 6), fill=GREEN)
    text(d, (484, 388), "55x8   57.5x10   60x10   65x8", size=15, fill=MUTED)

    rounded(d, (434, 448, 968, 836), CARD)
    text(d, (462, 478), "ACTIVITY HEATMAP", size=22, bold=True)
    for row in range(5):
        for col in range(16):
            color = [CARD_2, "#0E4429", "#006D32", "#26A641", GREEN][(row * 2 + col) % 5]
            rounded(d, (484 + col * 28, 536 + row * 28, 504 + col * 28, 556 + row * 28), color, radius=5)

    rounded(d, (998, 152, 1404, 836), CARD)
    text(d, (1026, 182), "DETAIL PANEL", size=22, bold=True)
    text(d, (1026, 224), "Apr 4 • PUSH", size=28, bold=True)
    for idx, line in enumerate(["Flag: Fresh", "Duration: 1h 12m", "PRs: Bench Press 65x8", "Notes: Strong top set pacing"]):
        rounded(d, (1026, 270 + idx * 70, 1374, 322 + idx * 70), CARD_2)
        text(d, (1046, 286 + idx * 70), line, size=18)
    return img


def draw_desktop_pt():
    img = Image.new("RGB", (1440, 900), BG)
    d = ImageDraw.Draw(img)
    text(d, (36, 32), "PT ZONE", size=72, condensed=True)
    text(d, (36, 102), "Invite trainers, manage access, and preview trainer read-only mode.", size=18, fill=MUTED)

    rounded(d, (36, 152, 452, 390), CARD, outline="#223244")
    text(d, (68, 182), "INVITE A PT", size=22, bold=True)
    wrapped(d, 68, 220, "Generate a 48-hour invite code for a trainer to access view-only member data.", 320, size=18, fill="#C9D1D9")
    rounded(d, (68, 300, 272, 352), BLUE)
    text(d, (170, 326), "CREATE INVITE CODE", size=26, fill=BG, condensed=True, anchor="mm")
    rounded(d, (286, 300, 420, 352), CARD_2)
    text(d, (353, 326), "Share link", size=17, anchor="mm")

    rounded(d, (36, 422, 452, 836), CARD)
    text(d, (68, 452), "ACTIVE ACCESS", size=22, bold=True)
    rounded(d, (68, 494, 420, 624), CARD_2)
    text(d, (92, 518), "Coach Andi", size=26, bold=True)
    text(d, (92, 554), "Read-only access • 31 workouts viewed", size=16, fill=MUTED)
    text(d, (92, 586), "Last comment: Bench tempo looked more stable.", size=16)
    rounded(d, (92, 642, 248, 684), "#173726")
    rounded(d, (264, 642, 420, 684), "#33191A")
    text(d, (170, 664), "View profile", size=16, fill=GREEN, anchor="mm")
    text(d, (342, 664), "Revoke access", size=16, fill=RED, anchor="mm")

    rounded(d, (484, 152, 1404, 460), CARD, outline="#223244")
    text(d, (516, 182), "PT VIEW PREVIEW", size=22, bold=True)
    text(d, (516, 224), "Coach dashboard shows members, consistency, history, and comments only.", size=18, fill=MUTED)
    rounded(d, (516, 274, 786, 420), CARD_2)
    text(d, (540, 300), "MEMBER LIST", size=16, fill=BLUE, bold=True)
    text(d, (540, 332), "Bro Jimbo • 12-day streak", size=22, bold=True)
    text(d, (540, 366), "Fresh yesterday • last comment 1 day ago", size=16, fill=MUTED)

    rounded(d, (812, 274, 1372, 420), CARD_2)
    text(d, (836, 300), "MEMBER SNAPSHOT", size=16, fill=BLUE, bold=True)
    text(d, (836, 332), "Heatmap + latest workout summary", size=22, bold=True)
    for row in range(3):
        for col in range(10):
            color = [CARD, "#0E4429", "#006D32", "#26A641", GREEN][(row + col) % 5]
            rounded(d, (836 + col * 22, 368 + row * 22, 852 + col * 22, 384 + row * 22), color, radius=4)

    rounded(d, (484, 494, 1404, 836), CARD)
    text(d, (516, 524), "COMMENT THREAD", size=22, bold=True)
    comments = [
        ("Apr 4 • Coach Andi", "Bench lockout looked cleaner. Keep this pacing next week."),
        ("Apr 1 • Coach Andi", "Great consistency finishing leg day even on a low-energy day."),
        ("Mar 29 • Coach Andi", "Pull volume is trending well. Watch elbow fatigue."),
    ]
    y = 572
    for title, body in comments:
        rounded(d, (516, y, 1372, y + 78), CARD_2)
        text(d, (540, y + 14), title, size=17, bold=True)
        text(d, (540, y + 40), body, size=16, fill=MUTED)
        y += 92
    return img


def contact_sheet(images, cols, bg=BG, padding=28, gap=24):
    widths = [img.width for img in images]
    heights = [img.height for img in images]
    thumb_w = max(widths)
    thumb_h = max(heights)
    rows = (len(images) + cols - 1) // cols
    canvas = Image.new(
        "RGB",
        (padding * 2 + cols * thumb_w + (cols - 1) * gap, padding * 2 + rows * thumb_h + (rows - 1) * gap),
        bg,
    )
    for idx, img in enumerate(images):
        x = padding + (idx % cols) * (thumb_w + gap)
        y = padding + (idx // cols) * (thumb_h + gap)
        canvas.paste(img, (x, y))
    return canvas


def main():
    mobile = [
        ("programs-mobile.png", draw_mobile_programs()),
        ("program-builder-mobile.png", draw_mobile_builder()),
        ("split-selector-mobile.png", draw_mobile_split_selector()),
        ("history-mobile.png", draw_mobile_history()),
        ("pt-zone-mobile.png", draw_mobile_pt()),
    ]
    desktop = [
        ("programs-desktop.png", draw_desktop_programs()),
        ("program-builder-desktop.png", draw_desktop_builder()),
        ("split-selector-desktop.png", draw_desktop_split_selector()),
        ("history-desktop.png", draw_desktop_history()),
        ("pt-zone-desktop.png", draw_desktop_pt()),
    ]

    mobile_saved = []
    for name, img in mobile:
        path = OUT / name
        img.save(path)
        mobile_saved.append(img)

    desktop_saved = []
    for name, img in desktop:
        path = OUT / name
        img.save(path)
        desktop_saved.append(img)

    mobile_sheet = contact_sheet(mobile_saved, cols=3)
    mobile_sheet.save(OUT / "mobile-next-screens-board.png")

    scaled_desktop = [img.resize((720, 450)) for img in desktop_saved]
    desktop_sheet = contact_sheet(scaled_desktop, cols=2)
    desktop_sheet.save(OUT / "desktop-next-screens-board.png")

    print(str(OUT))


if __name__ == "__main__":
    main()
