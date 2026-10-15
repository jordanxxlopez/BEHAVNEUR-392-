#!/usr/bin/env python3
"""Build a NEUR 411 lecture deck in the Lecture 8-10 format.

    python tools/build_lecture.py lectures/L11/lecture.json

The spec file (see lectures/_template/lecture.json) holds the content. Title,
date and course line are read from course/schedule.json so the lecture title
can never drift from the schedule. Output: 1 title slide + N content slides
(default 44) + 1 key-takeaways slide, 16:9, Arial, full references in notes.
After writing the deck the script runs tools/check_lecture.py on it.
"""
import json
import math
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parent.parent
FONT = "Arial"
W, H = 13.333, 7.5
M = 0.62                      # side margin (matches Lecture 10)
TITLE_Y, TITLE_H = 0.36, 0.62
BODY_Y = 1.35
FOOT_Y = 6.98                 # hairline above the citation footer
BODY_BOTTOM = 6.80
BODY_MAX_PT, BODY_MIN_PT = 18, 13
CAPTION_PT = 10
DEFAULT_CONTENT_SLIDES = 73


class SpecError(Exception):
    pass


sys.path.insert(0, str(Path(__file__).resolve().parent))
from style_rules import (ARTICLE_CAPTION, MADE_IMAGE_WORDS, MAX_WEB_IMAGES, MIN_ARTICLE_FIGURE_SLIDES,  # noqa: E402
                         MIN_IMAGE_SLIDES, WEB_CAPTION,
                         framing_problems, stats_problems)
from style_rules import EM_DASH, MAX_LIMITATION_SHARE, ends_with_limitation  # noqa: E402
from theme_colors import aligned_palette  # noqa: E402


def check_image(fig, where):
    """Images are never created. kind 'article' (default): a panel cropped from a published article,
    captioned 'Author (year), Fig. N…'. kind 'web': a real photograph from a credited web source
    (e.g. the animal on the title slide), captioned 'Photo: …' with a license. Both need source_url."""
    cap = fig.get("caption", "")
    kind = fig.get("kind", "article")
    if MADE_IMAGE_WORDS.search(cap):
        raise SpecError(f"{where}: image looks self-made ({MADE_IMAGE_WORDS.search(cap).group(0)!r}). Never create figures, "
                        "schematics, charts or illustrations; use an article figure, a credited web photo, or a text slide.")
    if not fig.get("source_url"):
        raise SpecError(f"{where}: image needs 'source_url' (article DOI, or the web page the photo came from)")
    if kind == "article":
        if not ARTICLE_CAPTION.search(cap):
            raise SpecError(f"{where}: article figure caption must start 'Author (year), Fig. N…': {cap[:70]!r}")
    elif kind == "textbook":
        if not all(fig.get(k) for k in ("isbn", "pdf_page", "figure_id")):
            raise SpecError(f"{where}: textbook crop needs isbn, pdf_page, and figure_id")
        if not cap.startswith("Carlson and Birkett (2022),"):
            raise SpecError(f"{where}: textbook caption must name Carlson and Birkett (2022), figure, and page")
    elif kind == "web":
        if not WEB_CAPTION.search(cap):
            raise SpecError(f"{where}: web image caption must start 'Photo: …' (or Image:/Specimen:/Micrograph:): {cap[:70]!r}")
        if not fig.get("credit") or not fig.get("license"):
            raise SpecError(f"{where}: web image needs 'credit' (photographer/owner) and 'license' (e.g. CC BY-SA 4.0)")
    else:
        raise SpecError(f"{where}: image kind must be 'article' or 'web', not {kind!r}")


def check_writing(texts, where):
    for t in texts:
        for why, hit in framing_problems(t):
            raise SpecError(f"{where}: {why}: {hit!r} in {t[:60]!r}")
        for hit in stats_problems(t):
            raise SpecError(f"{where}: statistics clutter ({hit!r}). Teach the finding; keep numbers only when they "
                            "carry the concept (latencies in ms, frequencies, rates), not test statistics or error terms.")


def flatten_transcript(items, depth=0):
    """transcript = list of strings or [text, [sub-bullets]] pairs → (lines, plain texts)."""
    lines, texts = [], []
    for it in items:
        if isinstance(it, (list, tuple)):
            head, subs = it[0], it[1]
            lines.append("  " * depth + "• " + head)
            texts.append(head)
            sl, st = flatten_transcript(subs, depth + 1)
            lines += sl
            texts += st
        else:
            lines.append("  " * depth + ("• " if depth == 0 else "– ") + it)
            texts.append(it)
    return lines, texts


# ---------------------------------------------------------------- helpers
def rgb(hex_):
    return RGBColor.from_string(hex_)


def inline_runs(text):
    """Split '**bold** and _italic_ text' into (chunk, bold, italic) runs."""
    out = []
    for part in re.split(r"(\*\*.+?\*\*|(?<![A-Za-z0-9])_[^_]+?_(?![A-Za-z0-9]))", text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            out.append((part[2:-2], True, False))
        elif part.startswith("_") and part.endswith("_") and len(part) > 2:
            out.append((part[1:-1], False, True))
        else:
            out.append((part, False, False))
    return out


def plain(text):
    return "".join(c for c, _, _ in inline_runs(text))


_TITLE_FONT = None


def title_width_in(text, pt):
    """Width of a bold Arial title in inches, measured with Arial or the metric-compatible
    Liberation Sans Bold when either is installed; None if neither is available."""
    global _TITLE_FONT
    if _TITLE_FONT is None:
        from PIL import ImageFont
        _TITLE_FONT = False
        for name in ("Arial Bold.ttf", "arialbd.ttf", "Arial_Bold.ttf", "LiberationSans-Bold.ttf"):
            for base in ("/usr/share/fonts", "/Library/Fonts", "/System/Library/Fonts", "C:/Windows/Fonts"):
                hits = list(Path(base).rglob(name)) if Path(base).exists() else []
                if hits:
                    _TITLE_FONT = ImageFont.truetype(str(hits[0]), 300)
                    break
            if _TITLE_FONT:
                break
    if not _TITLE_FONT:
        return None
    return _TITLE_FONT.getlength(plain(text)) / 300 * pt / 72


_BODY_METRIC_FONTS = {}

def lines_needed(paras, width_in, pt):
    """Estimate actual Arial wraps using metric-compatible fonts, not average glyphs."""
    from PIL import ImageFont
    if not _BODY_METRIC_FONTS:
        regular = list(Path('/usr/share/fonts').rglob('LiberationSans-Regular.ttf'))
        bold = list(Path('/usr/share/fonts').rglob('LiberationSans-Bold.ttf'))
        if regular and bold:
            _BODY_METRIC_FONTS.update({False:ImageFont.truetype(str(regular[0]),300),True:ImageFont.truetype(str(bold[0]),300)})
    limit=width_in*72;total=0
    for paragraph in paras:
        words=[];segments=[]
        for chunk,is_bold,_ in inline_runs(paragraph):
            for part in re.split(r'(\s+)',chunk):
                if not part:continue
                if part.isspace():
                    if segments:words.append(segments);segments=[]
                else:segments.append((part,is_bold))
        if segments:words.append(segments)
        line=0;n=1
        space=_BODY_METRIC_FONTS[False].getlength(' ')/300*pt if _BODY_METRIC_FONTS else pt*.28
        for word in words:
            w=sum(_BODY_METRIC_FONTS[bold].getlength(t)/300*pt for t,bold in word) if _BODY_METRIC_FONTS else sum(len(t)*pt*.5 for t,_ in word)
            add=w+(space if line else 0)
            if line+add>limit:n+=1;line=w
            else:line+=add
        total+=n
    return total


def fit_size(paras, width_in, height_in, max_pt=BODY_MAX_PT, min_pt=BODY_MIN_PT, where=""):
    for pt in range(max_pt, min_pt - 1, -1):
        n_lines = lines_needed(paras, width_in, pt)
        need = n_lines * pt * 1.30 / 72 + (len(paras) - 1) * pt * 0.6 / 72
        if need <= height_in * 0.97:
            return pt, need
    raise SpecError(
        f"{where}: text does not fit at {min_pt} pt in a {width_in:.1f}x{height_in:.1f} in box. "
        "Cut words, move a paragraph to another slide, or use the 'text' layout."
    )


def textbox(slide, x, y, w, h, name=None):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if name:
        tb.name = name
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    return tb, tf


def write_paras(tf, paras, pt, color, bold_color=None, space_after=None, align=PP_ALIGN.LEFT):
    first = True
    for text in paras:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = align
        p.space_after = Pt(space_after if space_after is not None else pt * 0.6)
        p.line_spacing = 1.08
        for chunk, b, i in inline_runs(text):
            r = p.add_run()
            r.text = chunk
            f = r.font
            f.name, f.size, f.bold, f.italic = FONT, Pt(pt), b, i
            f.color.rgb = rgb(bold_color if (b and bold_color) else color)


def rect(slide, x, y, w, h, fill, line=None):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid()
    s.fill.fore_color.rgb = rgb(fill)
    if line:
        s.line.color.rgb = rgb(line)
        s.line.width = Pt(0.75)
    else:
        s.line.fill.background()
    s.shadow.inherit = False
    style = s._element.find("{http://schemas.openxmlformats.org/presentationml/2006/main}style")
    if style is not None:  # drop theme effect/line refs so no renderer adds a shadow
        s._element.remove(style)
    return s


def picture_contain(slide, path, x, y, w, h):
    """Place an image inside the box, preserving aspect ratio, top-centered."""
    with Image.open(path) as im:
        iw, ih = im.size
    scale = min(w / iw, h / ih)
    pw, ph = iw * scale, ih * scale
    px = x + (w - pw) / 2
    slide.shapes.add_picture(str(path), Inches(px), Inches(y), Inches(pw), Inches(ph))
    return ph


def set_bg(slide, color):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = rgb(color)


# ------------------------------------------------------------ slide parts
class Deck:
    def __init__(self, spec, spec_dir):
        self.spec = spec
        self.dir = spec_dir
        sched = json.loads((ROOT / "course/schedule.json").read_text())
        self.course = sched
        n = spec["lecture"]
        match = [l for l in sched["lectures"] + sched.get("special_topics", []) if l["n"] == n]
        if not match:
            raise SpecError(f"Lecture {n} not in course/schedule.json")
        self.meta = match[0]
        themes = json.loads((ROOT / "course/themes.json").read_text())
        key = spec.get("theme")
        if key not in themes["palettes"]:
            raise SpecError(f"theme '{key}' not in course/themes.json palettes: {list(themes['palettes'])}")
        # a lecture may keep its own recorded theme when it is rebuilt
        used_labels = {str(v) for k, v in themes["used"].items() if k != str(n)}
        if themes["palettes"][key]["label"] in used_labels and not spec.get("allow_reused_theme"):
            raise SpecError(f"theme '{key}' was already used by another lecture; pick a new one")
        # titles/bold = darker shade of the title-slide color; all other text black
        self.t = aligned_palette(themes["palettes"][key])
        self.prs = Presentation()
        self.prs.slide_width, self.prs.slide_height = Inches(W), Inches(H)
        self.blank = self.prs.slide_layouts[6]
        self.num = 0
        self.web_images = 0
        self.image_slides = 0
        self.article_slides = 0
        self.caveat_endings = []

    def path(self, p):
        q = (self.dir / p).resolve()
        if not q.exists():
            raise SpecError(f"figure not found: {q}")
        return q

    def new_slide(self):
        self.num += 1
        s = self.prs.slides.add_slide(self.blank)
        set_bg(s, self.t["bg"])
        return s

    def title(self, s, text):
        _, tf = textbox(s, M, TITLE_Y, W - 2 * M, TITLE_H, "Title")
        tf.vertical_anchor = MSO_ANCHOR.TOP
        write_paras(tf, [text], 30, self.t["heading"])
        for r in tf.paragraphs[0].runs:
            r.font.bold = True
        if len(text) > 62:
            raise SpecError(f"slide {self.num}: title over 62 characters will wrap: {text!r}")
        width = title_width_in(text, 30)
        if width is not None and width > W - 2 * M - 0.05:
            raise SpecError(f"slide {self.num}: title is {width:.1f} in wide at 30 pt bold and will wrap onto the body; shorten it: {text!r}")

    def footer(self, s, cite):
        rect(s, M, FOOT_Y, W - 2 * M, 0.01, self.t["rule"])  # hairline above the footer
        _, tf = textbox(s, M, FOOT_Y + 0.08, W - 2 * M - 0.6, 0.25, "Citation")
        write_paras(tf, [cite], 9, self.t["muted"], space_after=0)
        _, tf = textbox(s, W - M - 0.5, FOOT_Y + 0.08, 0.5, 0.25, "Slide number")
        write_paras(tf, [f"{self.num:02d}"], 9, self.t["muted"], space_after=0, align=PP_ALIGN.RIGHT)

    def notes(self, s, sd):
        parts = []
        if sd.get("transcript"):
            lines, _ = flatten_transcript(sd["transcript"])
            parts.append("\n".join(lines))
        refs = sd.get("refs", [])
        if refs:
            parts.append("References:\n" + "\n".join(refs))
        figs = [sd["figure"]] if "figure" in sd else sd.get("figures", [])
        for f in figs:
            if f.get("kind", "article") == "web":
                parts.append(f"Image: {f['caption']} Credit: {f['credit']}. License: {f['license']}. Source: {f['source_url']}")
            else:
                parts.append(("Textbook figure: " if f.get("kind") == "textbook" else "Figure: ") + f["caption"] + "\nFigure source: " + f["source_url"])
        s.notes_slide.notes_text_frame.text = "\n\n".join(parts)

    def caption(self, s, x, y, w, text):
        _, tf = textbox(s, x, y, w, 0.55, "Figure caption")
        write_paras(tf, [text], CAPTION_PT, self.t["muted"], space_after=0)

    def body(self, s, paras, x, y, w, h, where, max_pt=BODY_MAX_PT):
        """Write paragraphs at the largest size that fits; return the estimated height used."""
        pt, need = fit_size(paras, w, h, max_pt=max_pt, where=where)
        _, tf = textbox(s, x, y, w, h, "Body")
        write_paras(tf, paras, pt, self.t["text"], bold_color=self.t["heading"])
        return need

    # ---------------------------------------------------------- layouts
    def title_slide(self):
        s = self.new_slide()
        t = self.t
        img = self.spec.get("title_image")
        if not img:
            raise SpecError("title slide: provide a credited source image relevant to the chapter")
        check_image(img, "title slide")
        rect(s, 0, 0, W, H, "FFFFFF")
        picture_contain(s, self.path(img["path"]), 0.65, 0.85, W / 2 - 1.2, 5.35)
        self.caption(s, 0.65, 6.4, W / 2 - 1.2, img["caption"])
        x, w = W / 2 + 0.55, W / 2 - 1.1
        _, tf = textbox(s, x, 0.9, w, 0.45)
        write_paras(tf, [self.course["course"]], 12, "000000", space_after=0)
        _, tf = textbox(s, x, 1.75, w, 0.45)
        write_paras(tf, ["Foundations and Frontiers"], 18, "000000", space_after=0)
        title = self.meta["title"]
        _, tf = textbox(s, x, 2.4, w, 2.4, "Lecture title")
        pt, need = fit_size([title], w, 2.4, max_pt=30, min_pt=22, where="title slide")
        write_paras(tf, [title], pt, t["title_text"], space_after=0)
        for p in tf.paragraphs:
            for r in p.runs:
                r.font.bold = True
        _, tf = textbox(s, x, 5.15, w, 0.4)
        write_paras(tf, [self.meta["date"]], 16, "000000", space_after=0)
        _, tf = textbox(s, x, 5.9, w, 0.85)
        write_paras(tf, [self.course["instructor"], self.course["instructor_title"]], 12, "000000", space_after=2)
        s.notes_slide.notes_text_frame.text = (
            f"{title}\nChapter {self.meta['n']}. {self.course['course']}. {self.meta['date']}."
            + f"\n\nFigure: {img['caption']}\nFigure source: {img['source_url']}"
            + "\n\nReferences:\n" + "\n".join(self.spec.get("title_refs", []))
        )

    def content_slide(self, sd):
        s = self.new_slide()
        where = f"slide {self.num} ({sd.get('title','')!r})"
        for k in ("title", "body", "cite", "refs"):
            if not sd.get(k):
                raise SpecError(f"{where}: missing '{k}'")
        if not sd.get("transcript"):
            raise SpecError(f"{where}: missing 'transcript' (speaker notes written as a natural teaching transcript)")
        _, ttexts = flatten_transcript(sd["transcript"])
        check_writing(sd["body"] + ttexts + [sd["title"]], where)
        for t in sd["body"] + [sd["title"]]:
            if EM_DASH in t:
                raise SpecError(f"{where}: em dash in slide text: {t[:60]!r}. Use a comma, semicolon, colon or new sentence.")
        if ends_with_limitation(sd["body"]):
            self.caveat_endings.append(self.num)
        imgs = [sd["figure"]] if "figure" in sd else sd.get("figures", [])
        for f in imgs:
            check_image(f, where)
            if f.get("kind", "article") == "web":
                self.web_images += 1
        if imgs:
            self.image_slides += 1
        if any(f.get("kind", "article") == "article" for f in imgs):
            self.article_slides += 1
        self.title(s, sd["title"])
        lay = sd.get("layout", "text")
        avail = BODY_BOTTOM - BODY_Y
        if lay == "text":
            self.body(s, sd["body"], M, BODY_Y, W - 2 * M, avail, where)
        elif lay in ("figure-right", "figure-left"):
            fig_w = sd.get("figure_width", 5.6)
            text_w = W - 2 * M - fig_w - 0.4
            fx = W - M - fig_w if lay == "figure-right" else M
            tx = M if lay == "figure-right" else M + fig_w + 0.4
            self.body(s, sd["body"], tx, BODY_Y, text_w, avail, where)
            ph = picture_contain(s, self.path(sd["figure"]["path"]), fx, BODY_Y + 0.05, fig_w, avail - 0.75)
            self.caption(s, fx, BODY_Y + 0.15 + ph, fig_w, sd["figure"]["caption"])
        elif lay in ("figures-right", "figures-left"):
            fig_w = sd.get("figure_width", 6.0)
            text_w = W - 2 * M - fig_w - 0.4
            fx = W - M - fig_w if lay == "figures-right" else M
            tx = M if lay == "figures-right" else M + fig_w + 0.4
            self.body(s, sd["body"], tx, BODY_Y, text_w, avail, where)
            figs = sd["figures"]
            if len(figs) != 2:
                raise SpecError(f"{where}: {lay} needs exactly 2 figures")
            if sd.get("figure_arrangement") == "side-by-side":
                # Tall article recordings use the full body height; a smaller
                # source anatomy panel stays beside them, without altering pixels.
                primary_w = sd.get("primary_figure_width", 4.0)
                gap = 0.2
                secondary_w = fig_w - primary_w - gap
                if primary_w <= 0 or secondary_w < 1.2:
                    raise SpecError(f"{where}: invalid side-by-side figure widths")
                ph = picture_contain(s, self.path(figs[0]["path"]), fx, BODY_Y + 0.05,
                                     primary_w, avail - 0.75)
                self.caption(s, fx, BODY_Y + 0.15 + ph, primary_w, figs[0]["caption"])
                sx, sy = fx + primary_w + gap, BODY_Y + 1.0
                ph = picture_contain(s, self.path(figs[1]["path"]), sx, sy, secondary_w,
                                     BODY_BOTTOM - sy - 0.75)
                self.caption(s, sx, sy + ph + 0.08, secondary_w, figs[1]["caption"])
            else:
                primary_h = sd.get("primary_figure_height", 2.7)
                ph = picture_contain(s, self.path(figs[0]["path"]), fx, BODY_Y + 0.05, fig_w, primary_h)
                self.caption(s, fx, BODY_Y + 0.15 + ph, fig_w, figs[0]["caption"])
                fy = BODY_Y + primary_h + 0.65
                ph = picture_contain(s, self.path(figs[1]["path"]), fx, fy, fig_w, BODY_BOTTOM - fy - 0.5)
                self.caption(s, fx, fy + ph + 0.08, fig_w, figs[1]["caption"])
        elif lay == "figure-below":
            top_h = sd.get("text_height", 1.9)
            used = self.body(s, sd["body"], M, BODY_Y, W - 2 * M, top_h, where, max_pt=16)
            fy = BODY_Y + used + 0.2
            ph = picture_contain(s, self.path(sd["figure"]["path"]), M, fy, W - 2 * M, BODY_BOTTOM - fy - 0.5)
            self.caption(s, M, fy + ph + 0.08, W - 2 * M, sd["figure"]["caption"])
        elif lay == "two-figures":
            top_h = sd.get("text_height", 1.8)
            used = self.body(s, sd["body"], M, BODY_Y, W - 2 * M, top_h, where, max_pt=16)
            figs = sd["figures"]
            if len(figs) != 2:
                raise SpecError(f"{where}: two-figures needs exactly 2 figures")
            fy = BODY_Y + used + 0.2
            gap, fw = 0.4, (W - 2 * M - 0.4) / 2
            for i, f in enumerate(figs):
                fx = M + i * (fw + gap)
                ph = picture_contain(s, self.path(f["path"]), fx, fy, fw, BODY_BOTTOM - fy - 0.55)
                self.caption(s, fx, fy + ph + 0.08, fw, f["caption"])
        elif lay == "table":
            tbl = sd["table"]
            rows = len(tbl["rows"]) + 1
            top_h = sd.get("text_height", 2.0)
            used = self.body(s, sd["body"], M, BODY_Y, W - 2 * M, top_h, where, max_pt=16)
            ty = BODY_Y + used + 0.25
            row_h = min(0.6, (BODY_BOTTOM - ty) / rows)
            shape = s.shapes.add_table(rows, len(tbl["header"]), Inches(M), Inches(ty),
                                       Inches(W - 2 * M), Inches(row_h * rows))
            table = shape.table
            for r_i, row in enumerate([tbl["header"]] + tbl["rows"]):
                for c_i, val in enumerate(row):
                    cell = table.cell(r_i, c_i)
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = rgb(self.t["tint"] if r_i == 0 else self.t["bg"])
                    cell.margin_left = cell.margin_right = Inches(0.08)
                    tf = cell.text_frame
                    tf.word_wrap = True
                    tf.paragraphs[0].text = ""
                    write_paras(tf, [f"**{val}**" if r_i == 0 else val], 13, self.t["text"],
                                bold_color=self.t["heading"], space_after=0)
        else:
            raise SpecError(f"{where}: unknown layout {lay!r}")
        self.footer(s, sd["cite"])
        self.notes(s, sd)

    def takeaways_slide(self, tk):
        s = self.new_slide()
        self.title(s, "Key takeaways")
        items = tk["items"]
        if not 5 <= len(items) <= 6:
            raise SpecError("key takeaways: give 5 or 6 items")
        cols, gap = 2, 0.3
        rows = math.ceil(len(items) / cols)
        cw = (W - 2 * M - gap) / cols
        ch = (BODY_BOTTOM - BODY_Y - gap * (rows - 1)) / rows
        for i, it in enumerate(items):
            cx = M + (i % cols) * (cw + gap)
            cy = BODY_Y + (i // cols) * (ch + gap)
            rect(s, cx, cy, cw, ch, self.t["tint"])
            paras = [f"**{it['lead']}** {it['text']}"]
            pt, _ = fit_size(paras, cw - 0.4, ch - 0.3, max_pt=16, min_pt=12, where=f"takeaway {i+1}")
            _, tf = textbox(s, cx + 0.2, cy + 0.15, cw - 0.4, ch - 0.3)
            write_paras(tf, paras, pt, self.t["text"], bold_color=self.t["heading"])
        self.footer(s, tk["cite"])
        s.notes_slide.notes_text_frame.text = "\n\n".join(tk.get("refs", []))

    def build(self, out):
        want = self.spec.get("content_slides", DEFAULT_CONTENT_SLIDES)
        got = len(self.spec["slides"])
        if got != want:
            raise SpecError(f"spec has {got} content slides; this lecture needs exactly {want}")
        self.title_slide()
        for sd in self.spec["slides"]:
            self.content_slide(sd)
        tk = self.spec["takeaways"]
        check_writing([f"{i['lead']} {i['text']}" for i in tk["items"]], "key takeaways")
        for i in tk["items"]:
            if EM_DASH in f"{i['lead']} {i['text']}":
                raise SpecError(f"key takeaways: em dash in {i['lead']!r}. Use a comma, semicolon, colon or new sentence.")
        self.takeaways_slide(tk)
        n = len(self.spec["slides"])
        need_img = n
        policy = json.loads((ROOT / "course/policy.json").read_text())
        need_art = math.ceil(policy["primary_article_figure_minimum_fraction"] * n)
        if self.image_slides < need_img:
            raise SpecError(f"only {self.image_slides} of {n} content slides have an image; nearly all must (>= {need_img}). "
                            "Add article figures, or request the PDFs you need.")
        if self.article_slides < need_art:
            raise SpecError(f"only {self.article_slides} content slides have an article figure; need >= {need_art}. "
                            "Primary-article figures come first; request the PDFs you need.")
        if self.web_images > MAX_WEB_IMAGES:
            raise SpecError(f"{self.web_images} web photos; at most {MAX_WEB_IMAGES}. Decorative/general images only where needed — "
                            "give priority to primary-article figures.")
        if len(self.caveat_endings) > MAX_LIMITATION_SHARE * n:
            raise SpecError(f"{len(self.caveat_endings)} of {n} slides end on a caveat paragraph (slides "
                            f"{self.caveat_endings[:12]}); at most {int(MAX_LIMITATION_SHARE * n)}. Make the last paragraph "
                            "teaching content (mechanism, follow-up result, behavior); keep a limitation only when it "
                            "changes what students should conclude.")
        self.prs.core_properties.title = self.meta["title"]
        self.prs.core_properties.author = self.course["instructor"]
        self.prs.save(out)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    spec_path = Path(sys.argv[1]).resolve()
    spec = json.loads(spec_path.read_text())
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else spec_path.parent / spec.get("output_filename", f"BehavioralNeuroscience392_Lecture{spec['lecture']}_FA2026.pptx")
    try:
        Deck(spec, spec_path.parent).build(out)
    except SpecError as e:
        sys.exit(f"BUILD FAILED: {e}")
    print(f"wrote {out}")
    rc = subprocess.call([sys.executable, str(ROOT / "tools/check_lecture.py"), str(out),
                          "--lecture", str(spec["lecture"]),
                          "--content-slides", str(spec.get("content_slides", DEFAULT_CONTENT_SLIDES))])
    sys.exit(rc)


if __name__ == "__main__":
    main()
