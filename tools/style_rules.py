"""Writing and image rules shared by build_lecture.py and check_lecture.py.

Every pattern here comes from the instructor's rules (see AGENTS.md / SKILL.md).
"""
import re

# ------------------------------------------------------------------ writing
# (pattern, reason). Applied to slide text AND speaker-note transcripts.
FRAMING = [
    # structure / roadmap / presentation narration
    (r"\bup next\b|\bnext (time|lecture|class)\b|\bcoming up\b|\bpreview of\b", "no 'up next' / next-lecture lines"),
    (r"\bpart \d+ of \d+\b|\bpart [ivx]+\b", "no 'Part 1 of 4' style splitting"),
    (r"\bin this (lecture|section|slide|presentation)\b|\btoday we will\b|\bwe will (now )?(discuss|cover|explore|see|look)\b",
     "no lecture metacommentary"),
    (r"\blet'?s\b", "no 'let's …' narration"),
    (r"\bbefore getting to\b|\bthe next step is\b|\bnext we have\b|\bfrom here\b|\bthis sets up\b|"
     r"\bthis becomes important later\b|\bas we will see\b|\bwe(?:'ll| will) return\b", "no roadmap or transition framing"),
    (r"\b(attention|focus) (now )?(turns|shifts)\b|\bwe now (turn|consider)\b|\bturning (now )?to\b|\bmoving on\b|"
     r"\bour focus\b|\bnow (let'?s |we )?(look|turn)\b", "no attention-directing language"),
    (r"\bthis helps (us )?understand\b|\bthe key point is\b|\bthe (main |key )?takeaway is\b|\bit is (important|worth) (to note|noting|remembering)\b|"
     r"\bthis is important to understand\b|\bremember that\b|\bas you can see\b|\bkeep in mind\b|\bnote that\b|"
     r"\binterestingly\b|\bfascinating\b|\bremarkabl[ey]\b|\bstriking(ly)?\b|\bappreciate\b",
     "no takeaway framing, evaluative filler or reader-directed asides"),
    (r"\b(this|these|that|the|each)\s+(figure|graph|image|panel|plot|photo|picture|example|diagram|trace|recording)s?\s+"
     r"(illustrates?|demonstrates?|shows?|depicts?|reveals?)\b|\b(this|these|that)\s+(illustrates?|demonstrates?|shows?)\b",
     "no illustrative framing ('this shows …'): state the finding directly"),
    (r"\breading the (figure|graph|panel)\b|\b(in|on) the (left|right|top|bottom) (panel|of the (figure|slide))\b|"
     r"\bpanel [A-Z] shows\b|\bis shown (here|below|above|on the right|on the left)\b|\b(a|an) (graph|image|figure|example) (is|was) (shown|given)\b",
     "no figure-reading narration"),
    (r"\bwhy this matters\b|\bthis matters because\b|\bwhy (this|the) topic\b|\bto set the stage\b",
     "no explanation of why a topic is introduced"),
    (r"lorem|ipsum|\bTODO\b|(?<!Date )\bTBD\b|\[insert", "placeholder text left in"),
]
FRAMING_RE = [(re.compile(p, re.I), why) for p, why in FRAMING]

# statistics clutter: the lecture teaches findings, not test statistics
STATS = re.compile(
    r"\bP\s*[<=>≤]\s*0?\.\d|\bp\s*[<=>≤]\s*0?\.\d|±(?!\s*\d+(?:\.\d+)?\s*°)|\bs\.?e\.?m\.?\b|\bSEM\b|\bSD\b|\bstandard (deviation|error)\b|"
    r"χ|\bchi-?square\b|\bF\s*\(\s*\d|\bt\s*\(\s*\d|\bANOVA\b|\bMANOVA\b|\bBonferroni\b|\bWilcoxon\b|\bFisher'?s exact\b|"
    r"\bconfidence interval\b|\b95\s*%\s*CI\b|\bodds ratio\b", re.I)


def framing_problems(text):
    """Return a list of (reason, matched text) for banned framing in text."""
    out = []
    for rx, why in FRAMING_RE:
        m = rx.search(text)
        if m:
            out.append((why, m.group(0)))
    return out


def stats_problems(text):
    m = STATS.search(text)
    return [m.group(0)] if m else []


# ------------------------------------------------------------------ images
# Article figures: panels cropped from published articles, credited to the exact figure.
ARTICLE_CAPTION = re.compile(
    r"^[^()]{2,120}?\((?:19|20)\d{2}[a-z]?\),\s*(?:Fig\.|Figs\.?|Figure|Text-figs?\.?|Plate|Table|"
    r"Extended Data Fig\.|Supplementary Fig\.)", re.I)
# Web images (photo of the animal, habitat, specimen): real photographs from a credited source.
WEB_CAPTION = re.compile(r"^(Photo|Image|Specimen|Micrograph):\s+\S", re.I)
MADE_IMAGE_WORDS = re.compile(
    r"schematic|re-?plotted|redrawn|drawn from|diagram drawn|illustrat|our own|created for|generated|"
    r"\bAI\b|midjourney|dall-?e|stable diffusion|summary table|summary diagram|not original|template curves|"
    r"simulated|mock-?up|clip ?art|icon", re.I)
# Nearly every content slide carries an image; primary-article figures dominate.
MIN_IMAGE_SLIDES = 40           # of 44 content slides: article figure or credited photo
MIN_ARTICLE_FIGURE_SLIDES = 34  # content slides with at least one article figure
MIN_COLOR_SHARE = 0.5           # prefer colorful article figures: >= half of image slides in color (warning)
MAX_WEB_IMAGES = 10              # credited web photos (animal, habitat, specimen), only where needed


def is_color_image(blob):
    """True if a picture has real color: saturated pixels make up >= 3% of its non-white 'ink'.

    Measured against the ink rather than the whole image so that colored traces and labels
    on a white background count, while grayscale figures (0% saturated ink) do not.
    """
    import io
    from PIL import Image
    im = Image.open(io.BytesIO(blob)).convert("RGB")
    im.thumbnail((300, 300))
    hsv, rgb = im.convert("HSV").tobytes(), im.tobytes()
    colored = sum(1 for i in range(0, len(hsv), 3) if hsv[i + 1] > 80 and hsv[i + 2] > 35)
    ink = sum(1 for i in range(0, len(rgb), 3) if min(rgb[i:i + 3]) < 235)
    return colored >= 0.002 * (len(hsv) / 3) and colored >= 0.03 * max(ink, 1)


# ------------------------------------------------------------------ caveats and dashes
# A limitation earns a sentence only when it changes what students should conclude; a deck
# whose slides routinely close on "does not establish..." is disclaimer filler.
LIMITATION = re.compile(
    r"\b(?:does|do|did) not (?:establish|identify|show|prove|demonstrate|determine|reveal|isolate|specify|"
    r"mean|imply|address|exclude|rule out|explain|indicate)\b|"
    r"\bcannot (?:be )?(?:establish|exclude|excluded|determine|identify|distinguish|separate|rule out|explain)|"
    r"\b(?:has|have) not been (?:established|shown|tested|identified|demonstrated)\b|"
    r"\bremains? (?:unknown|unresolved|untested|unclear|unidentified|unproven|open)\b", re.I)
MAX_LIMITATION_SHARE = 0.2   # at most 1 in 5 content slides may end on a caveat paragraph
EM_DASH = "—"


def ends_with_limitation(paragraphs):
    """True when the slide's last paragraph is a caveat ("does not establish...", "remains unknown")."""
    paras = [p for p in paragraphs if p and p.strip()]
    return bool(paras) and bool(LIMITATION.search(paras[-1]))
