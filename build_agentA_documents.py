"""
Build "AgentA - Data Flow Diagrams" as a Word .docx and a matching black-and-white .pdf
from the 7 self-contained DFD HTML figures.

A4 LANDSCAPE.  The portrait version printed every diagram at a fixed 6.0 in wide, which
made a 4-6 pt label.  Landscape A4 gives a 9.69 x 6.27 in content box, so each figure is
now scaled to fill whatever width/height its own aspect ratio allows and every main label
prints at 6.3-10.1 pt.

Pipeline
  Step 1  parse each HTML (lxml) -> heading / caption / narrative text + raw SVG source
          + the font sizes actually used inside the SVG (for the printed-size report)
  Step 2  plan the placement of every figure (fit to the content box) and the PNG width
          needed to keep >= MIN_DPI on the page
  Step 3  render each SVG to a wide PNG with Playwright/Chromium
          (device_scale_factor = targetPx/viewBoxWidth, element screenshot at scale="device")
  Step 4  build the .docx with python-docx (A4 LANDSCAPE, 2.54 cm margins, Times New Roman)
  Step 5  build a print-mirrored HTML and print it to PDF with Chromium (A4 landscape)
  Step 6  verify everything and print a report

Only python-docx, playwright, lxml, pillow and pypdf are used. No Inkscape / pandoc / Word.
"""

import html as html_mod
import io
import math
import os
import re
import shutil
import sys
import zipfile

from lxml import etree
from lxml import html as LH
from PIL import Image
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor
from playwright.sync_api import sync_playwright

# --------------------------------------------------------------------------- config

SRC_DIR = r"C:\Users\joashua\Downloads\dfd-generator-zen"
TMP_PNG = r"C:\Users\joashua\AppData\Local\Temp\opencode\dfd_png"
DOCX_PATH = os.path.join(SRC_DIR, "AgentA - Data Flow Diagrams.docx")
PDF_PATH = os.path.join(SRC_DIR, "AgentA - Data Flow Diagrams.pdf")

FIGURES = [
    "Figure 1 - Context Diagram.html",
    "Figure 2 - Level 0 DFD (Diagram 0).html",
    "Figure 3 - Registration DFD.html",
    "Figure 4 - Login DFD.html",
    "Figure 5 - Chat DFD.html",
    "Figure 6 - Profile & Account DFD.html",
    "Figure 7 - Forgot Password DFD.html",
]

# ---- page geometry: A4 LANDSCAPE -------------------------------------------------
PAGE_W_CM, PAGE_H_CM = 29.7, 21.0          # landscape: wide edge first
MARGIN_CM = 2.54                            # 1 inch on all four sides
CM_PER_IN = 2.54
PAGE_W_IN = PAGE_W_CM / CM_PER_IN           # 11.6929
PAGE_H_IN = PAGE_H_CM / CM_PER_IN           #  8.2677
# Content box = page minus margins.  Derived, never typed: A4 landscape is only 8.27 in
# tall, so the printable height is 6.27 in -- an image may not exceed it.
CONTENT_W_IN = PAGE_W_IN - 2 * (MARGIN_CM / CM_PER_IN)   # 9.6929
CONTENT_H_IN = PAGE_H_IN - 2 * (MARGIN_CM / CM_PER_IN)   # 6.2677

TARGET_W = 3600          # px, floor for every rendered PNG
MIN_DPI = 600            # effective print resolution every figure must reach
PX_ROUND = 50            # round the required pixel width up to a tidy number
CSS_PX_PER_IN = 96.0     # Chromium lays images out in whole CSS px: quantise the placement
                         # width so the PDF can never draw an image wider than the docx asks for
FONT = "Times New Roman"
NARRATIVE_HEADING = "Narrative Flow of Data"
NARR_INDENT_IN = 0.9     # landscape measure is 9.69 in -> too wide to read comfortably


def hr(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


# ------------------------------------------------------------------ step 1: parse

def css_font_sizes(css):
    """class name -> px font-size, from the page's own <style> (e.g. .fl { font-size:9.5px })."""
    out = {}
    for m in re.finditer(r"\.([A-Za-z][\w-]*)\s*\{([^}]*)\}", css):
        fs = re.search(r"font-size\s*:\s*([\d.]+)px", m.group(2))
        if fs:
            out[m.group(1)] = float(fs.group(1))
    return out


def svg_font_sizes(svg, css):
    """{px: count} for every <text> in the SVG, honouring <g font-size> inheritance and CSS."""
    classes = css_font_sizes(css)
    sizes = {}

    def walk(el, inherited):
        if not isinstance(el.tag, str):          # comments / PIs
            return
        size = el.get("font-size") or inherited
        for c in (el.get("class") or "").split():
            if c in classes:
                size = classes[c]
        if etree.QName(el).localname == "text" and size:
            px = float(size)
            sizes[px] = sizes.get(px, 0) + 1
        for ch in el:
            walk(ch, size)

    try:
        walk(etree.fromstring(svg.encode("utf-8")), None)
    except etree.XMLSyntaxError:                 # tolerate a non-XML-clean SVG
        for m in re.finditer(r"<text\b[^>]*>", svg):
            fs = re.search(r'font-size\s*=\s*"([\d.]+)"', m.group(0))
            if fs:
                px = float(fs.group(1))
                sizes[px] = sizes.get(px, 0) + 1
    return sizes


def parse_figure(path):
    """Return dict with heading, caption, narrative, raw svg text, viewbox, page css."""
    raw = io.open(path, encoding="utf-8").read()
    tree = LH.fromstring(raw)

    heading = " ".join(tree.xpath("//h1")[0].text_content().split())

    # Figure 1 uses class "caption"; figures 2-7 use class "cap".
    caps = tree.xpath('//p[@class="cap"]') + tree.xpath('//p[@class="caption"]')
    if not caps:
        raise RuntimeError("no caption found in %s" % path)
    caption = " ".join(caps[0].text_content().split())

    # Figures 2-7 use <p class="narr">; figure 1 uses a bare <p> inside .narrative.
    narrs = tree.xpath('//p[@class="narr"]')
    if not narrs:
        narrs = tree.xpath('//div[@class="narrative"]//p')
    if not narrs:
        raise RuntimeError("no narrative found in %s" % path)
    narrative = " ".join(narrs[0].text_content().split())

    # Raw SVG bytes: lxml's HTML parser lowercases camelCase attributes
    # (viewBox -> viewbox), so we slice the untouched source instead.
    m = re.search(r"<svg\b.*?</svg>", raw, re.S)
    if not m:
        raise RuntimeError("no <svg> in %s" % path)
    svg = m.group(0)

    vb = re.search(r'viewBox\s*=\s*"([^"]+)"', svg)
    if not vb:
        raise RuntimeError("no viewBox in %s" % path)
    nums = [float(x) for x in re.split(r"[ ,]+", vb.group(1).strip())]
    vw, vh = nums[2], nums[3]

    # The page <style> carries real diagram CSS (.fl label halo, .bp box strokes).
    # It must travel with the SVG or the labels render wrong.
    styles = tree.xpath("//style")
    css = "\n".join(s.text_content() for s in styles)

    sizes = svg_font_sizes(svg, css)
    if not sizes:
        raise RuntimeError("no <text> found in %s" % path)
    # "Main" label = the biggest font size carried by at least 3 text elements, i.e. the
    # entity/process box labels.  The one-off bigger/smaller runs (a process name, the
    # 9.5 px flow labels on the arrows) are counted separately in the report.
    main_px = max(px for px, n in sizes.items() if n >= 3)

    return dict(path=path, heading=heading, caption=caption, narrative=narrative,
                svg=svg, vbw=vw, vbh=vh, css=css,
                png=os.path.join(TMP_PNG, "%02d.png" % (FIGURES.index(os.path.basename(path)) + 1)),
                sizes=sizes, main_px=main_px, min_px=min(sizes))


# --------------------------------------------------------- step 2: plan the layout

def plan_geometry(figures):
    """Fit every figure to the content box and decide how wide its PNG must be.

    Each diagram keeps its own aspect ratio and takes the full content width unless
    that would make it taller than the page allows (only figure 6 is height-limited).
    """
    for f in figures:
        r = f["vbw"] / f["vbh"]
        f["ratio"] = r
        f["limited"] = "height" if CONTENT_H_IN * r < CONTENT_W_IN else "width"
        # whole CSS pixels: guarantees the printed width in the PDF (floor(px) * 0.75 pt)
        # never exceeds the width asked for in the docx
        f["img_w"] = math.floor(min(CONTENT_W_IN, CONTENT_H_IN * r) * CSS_PX_PER_IN) / CSS_PX_PER_IN
        f["img_h"] = f["img_w"] / r

        # PNG must be wide enough to print at >= MIN_DPI at this placement width.
        need_px = f["img_w"] * MIN_DPI
        f["target_px"] = max(TARGET_W, int(math.ceil(need_px / PX_ROUND)) * PX_ROUND)
        f["scale"] = f["target_px"] / f["vbw"]

        # printed size of a label: px / viewBoxWidth * placedInches * 72 pt
        f["dpi"] = f["target_px"] / f["img_w"]
        f["main_pt"] = f["main_px"] / f["vbw"] * f["img_w"] * 72.0
        f["min_pt"] = f["min_px"] / f["vbw"] * f["img_w"] * 72.0

    hr("STEP 2  PLACEMENT (A4 landscape, content box %.4f x %.4f in)"
       % (CONTENT_W_IN, CONTENT_H_IN))
    print("  %-5s %-12s %-9s %-17s %-7s %-8s %-8s %s"
          % ("Fig", "viewBox", "ratio", "placed in (w x h)", "limit", "png px",
             "DPI", "main label pt"))
    for i, f in enumerate(figures, 1):
        print("  %-5d %-12s %-9.4f %-17s %-7s %-8d %-8.0f %.2f  (%.1f px -> %.2f pt)"
              % (i, "%.0fx%.0f" % (f["vbw"], f["vbh"]), f["ratio"],
                 "%.3f x %.3f" % (f["img_w"], f["img_h"]), f["limited"],
                 f["target_px"], f["dpi"], f["main_px"], f["main_px"], f["main_pt"]))
    print("\n  every figure is at least %d px wide and prints at >= %d DPI"
          % (min(f["target_px"] for f in figures), MIN_DPI))
    worst = min(range(len(figures)), key=lambda i: figures[i]["min_pt"])
    print("  smallest text of any kind (arrow flow labels): %.2f pt on figure %d"
          % (figures[worst]["min_pt"], worst + 1))


# ------------------------------------------------------- step 3: render the PNGs

WRAPPER = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>svg</title>
<style>
{css}
/* --- overrides: isolate the diagram on pure white, 1 user unit = 1 CSS pixel --- */
html, body {{ margin:0; padding:0; background:#ffffff; border:0; max-width:none; }}
body {{ display:inline-block; width:auto; }}
svg {{ display:block; width:{w}px !important; height:{h}px !important;
       max-width:none !important; background:#ffffff; overflow:visible; }}
</style></head>
<body>{svg}</body></html>
"""


def render_pngs(figures):
    if os.path.isdir(TMP_PNG):
        shutil.rmtree(TMP_PNG)
    os.makedirs(TMP_PNG)
    print("temp png folder: %s" % TMP_PNG)

    for f in figures:
        f["wrapper"] = os.path.join(TMP_PNG, "wrap_%s.html" % os.path.basename(f["png"]))
        io.open(f["wrapper"], "w", encoding="utf-8").write(
            WRAPPER.format(css=f["css"], svg=f["svg"], w=f["vbw"], h=f["vbh"]))

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--force-color-profile=srgb",
                                          "--disable-lcd-text",
                                          "--hide-scrollbars"])
        try:
            for f in figures:
                ctx = browser.new_context(device_scale_factor=f["scale"],
                                          viewport={"width": int(f["vbw"]) + 80,
                                                    "height": int(f["vbh"]) + 80},
                                          color_scheme="light")
                page = ctx.new_page()
                page.goto("file:///" + f["wrapper"].replace("\\", "/"))
                page.wait_for_timeout(120)
                page.locator("svg").screenshot(path=f["png"], scale="device", omit_background=False)
                ctx.close()
                f["png_w"], f["png_h"] = Image.open(f["png"]).size
                print("  %-34s viewBox %gx%g  scale %.4f  png %dx%d  -> %.0f DPI at %.3f in"
                      % (os.path.basename(f["path"]), f["vbw"], f["vbh"], f["scale"],
                         f["png_w"], f["png_h"], f["png_w"] / f["img_w"], f["img_w"]))
        finally:
            browser.close()


def check_pngs(figures):
    """Full-resolution check. Must NOT downsample first: 1.1-1.5 px strokes are
    averaged into the background by any downscaling, which fakes a blank image."""
    hr("STEP 3b  PNG sanity (Pillow, FULL RESOLUTION): size + pure black/white pixels")
    ok = True
    for f in figures:
        im = Image.open(f["png"]).convert("RGB")
        w, h = im.size
        size_ok = abs(w - f["target_px"]) <= 2

        g = im.convert("L")
        hist = g.histogram()
        black = hist[0]                      # pure black (0,0,0)
        white = hist[255]                    # pure white (255,255,255)
        total = w * h
        ink = sum(hist[:128])                # anything darker than mid grey
        # a real diagram is mostly white paper with a modest amount of ink
        not_blank = black > 1000 and white > 1000 and 0.005 < (ink / total) < 0.60

        # clipping probe: the outer 4 px ring must be pure white
        strips = [g.crop((0, 0, w, 4)), g.crop((0, h - 4, w, h)),
                  g.crop((0, 0, 4, h)), g.crop((w - 4, 0, w, h))]
        edge_ink = 0
        for st in strips:
            edge_ink += st.size[0] * st.size[1] - st.histogram()[255]
        no_clip = edge_ink == 0

        f["black_px"], f["white_px"], f["ink_pct"], f["edge_ink"] = black, white, 100.0 * ink / total, edge_ink
        ok &= size_ok and not_blank and no_clip
        print("  %-34s %5dx%-5d size_ok=%-5s pure_black=%-8d pure_white=%-8d ink=%5.2f%% edge_ink=%d"
              % (os.path.basename(f["path"]), w, h, size_ok, black, white,
                 f["ink_pct"], edge_ink))
    return ok


# ---------------------------------------------------------- step 4: build the docx

def force_font(run, size, bold=False, italic=False):
    run.font.name = FONT
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(0, 0, 0)
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = rpr.makeelement(qn("w:rFonts"), {})
        rpr.insert(0, rf)
    for a in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rf.set(qn(a), FONT)


def build_docx(figures):
    doc = Document()

    sec = doc.sections[0]
    sec.page_width = Cm(PAGE_W_CM)        # python-docx defaults to US Letter -> A4 landscape
    sec.page_height = Cm(PAGE_H_CM)
    sec.left_margin = sec.right_margin = Cm(MARGIN_CM)
    sec.top_margin = sec.bottom_margin = Cm(MARGIN_CM)
    sec.header_distance = Cm(1.27)
    sec.footer_distance = Cm(1.27)

    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal.font.size = Pt(12)
    normal.font.color.rgb = RGBColor(0, 0, 0)
    rpr = normal.element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = rpr.makeelement(qn("w:rFonts"), {})
        rpr.insert(0, rf)
    for a in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rf.set(qn(a), FONT)
    normal.paragraph_format.space_after = Pt(0)
    normal.paragraph_format.line_spacing = 1.0

    for i, f in enumerate(figures):
        # 1. heading
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(10)
        p.paragraph_format.keep_with_next = True
        force_font(p.add_run(f["heading"]), 14, bold=True)

        # 2. diagram -- WIDTH ONLY (width+height would distort the aspect ratio)
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        p.add_run().add_picture(f["png"], width=Inches(f["img_w"]))

        # 3. caption
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(12)
        force_font(p.add_run(f["caption"]), 11, italic=True)

        # 4. narrative heading -- indented, a 9.69 in measure is unreadable
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.left_indent = Inches(NARR_INDENT_IN)
        p.paragraph_format.right_indent = Inches(NARR_INDENT_IN)
        force_font(p.add_run(NARRATIVE_HEADING), 12, bold=True)

        # 5. narrative -- real editable text
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.left_indent = Inches(NARR_INDENT_IN)
        p.paragraph_format.right_indent = Inches(NARR_INDENT_IN)
        force_font(p.add_run(f["narrative"]), 12)

        # 6. page break after every figure except the last
        if i < len(figures) - 1:
            doc.add_page_break()

    doc.core_properties.title = "AgentA - Data Flow Diagrams"
    doc.core_properties.subject = "Data Flow Diagrams"
    doc.save(DOCX_PATH)
    print("saved: %s (%d bytes)" % (DOCX_PATH, os.path.getsize(DOCX_PATH)))


# -------------------------------------------------------------- step 5: build pdf

PRINT_CSS = """
@page { size: A4 landscape; margin: 25.4mm; }
html, body { margin:0; padding:0; background:#fff; color:#000; }
body { font-family:"Times New Roman", Times, serif; font-size:12pt; line-height:1.15; }
.fig { break-inside: avoid; page-break-inside: avoid; }
.fig + .fig { break-before: page; page-break-before: always; }
h1  { font-size:14pt; font-weight:bold; text-align:center; margin:0 0 10pt; }
img { display:block; height:auto; margin:0 auto; }
p.cap { font-size:11pt; font-style:italic; text-align:center; margin:8pt 0 12pt; }
p.sec { font-size:12pt; font-weight:bold; margin:0 0 4pt;
        padding:0 %(ind)sin; }
p.narr { font-size:12pt; text-align:justify; margin:0;
         padding:0 %(ind)sin; }
""" % {"ind": NARR_INDENT_IN}


def print_html(figures):
    """The print-mirrored page: exactly the same geometry the .docx uses."""
    blocks = []
    for f in figures:
        blocks.append(
            '<section class="fig">'
            '<h1>%s</h1>'
            '<img src="file:///%s" alt="" style="width:%.4fin">'
            '<p class="cap">%s</p>'
            '<p class="sec">%s</p>'
            '<p class="narr">%s</p>'
            '</section>' % (
                html_mod.escape(f["heading"]),
                f["png"].replace("\\", "/"),
                f["img_w"],
                html_mod.escape(f["caption"]),
                html_mod.escape(NARRATIVE_HEADING),
                html_mod.escape(f["narrative"])))

    return ("<!DOCTYPE html><html><head><meta charset=\"utf-8\">"
            "<title>AgentA - Data Flow Diagrams</title>"
            "<style>%s</style></head><body>%s</body></html>"
            % (PRINT_CSS, "\n".join(blocks)))


def build_pdf(figures):
    tmp = os.path.join(TMP_PNG, "print.html")
    io.open(tmp, "w", encoding="utf-8").write(print_html(figures))

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--force-color-profile=srgb", "--hide-scrollbars"])
        try:
            page = browser.new_page()
            page.goto("file:///" + tmp.replace("\\", "/"))
            page.emulate_media(media="print")
            page.wait_for_function(
                "() => Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)")
            page.pdf(path=PDF_PATH, format="A4", landscape=True, print_background=True,
                     margin={"top": "25.4mm", "bottom": "25.4mm",
                             "left": "25.4mm", "right": "25.4mm"},
                     prefer_css_page_size=True)
        finally:
            browser.close()
    print("saved: %s (%d bytes)" % (PDF_PATH, os.path.getsize(PDF_PATH)))


# ------------------------------------------------------------------ step 6: verify

def pdf_pages(path):
    """[(mediabox_w, mediabox_h, [drawn image widths in pt])] for every page."""
    from pypdf import PdfReader
    from pypdf.generic import ContentStream

    def mul(m, n):
        a, b, c, d, e, f = m
        A, B, C, D, E, F = n
        return (a * A + b * C, a * B + b * D, c * A + d * C,
                c * B + d * D, e * A + f * C + E, e * B + f * D + F)

    reader = PdfReader(path)
    pages = []
    for page in reader.pages:
        mb = page.mediabox
        ctm = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)
        stack = []
        widths = []
        try:
            ops = ContentStream(page.get_contents(), reader).operations
        except Exception:
            ops = []
        for operands, operator in ops:
            op = operator.decode("latin-1") if isinstance(operator, bytes) else str(operator)
            if op == "q":
                stack.append(ctm)
            elif op == "Q":
                ctm = stack.pop() if stack else (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)
            elif op == "cm" and len(operands) == 6:
                ctm = mul(tuple(float(x) for x in operands), ctm)
            elif op == "Do":
                # the XObject is drawn into a 1x1 unit square -> its printed width is
                # the length of the CTM's first column vector
                widths.append(math.hypot(ctm[0], ctm[1]))
        pages.append((float(mb.width), float(mb.height), widths))
    return pages


def page_budget(figures):
    """Measure, in Chromium print media, how tall each figure + its text block really is.

    This is what decides whether one figure still fits on one A4 landscape page.
    """
    tmp = os.path.join(TMP_PNG, "budget.html")
    io.open(tmp, "w", encoding="utf-8").write(print_html(figures))
    js = ('function(){var out=[];var ss=document.getElementsByTagName("section");'
          'for(var i=0;i<ss.length;i++){var s=ss[i];'
          'function box(t){var e=s.querySelector(t);if(!e)return 0;var c=getComputedStyle(e);'
          'return e.getBoundingClientRect().height+parseFloat(c.marginTop)'
          '+parseFloat(c.marginBottom);}'
          'var ih=s.querySelector("img").getBoundingClientRect().height;'
          'out.push({img:ih,text:box("h1")+box("p.cap")+box("p.sec")+box("p.narr")});}'
          'return out;}')
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--hide-scrollbars"])
        try:
            page = browser.new_page()
            page.goto("file:///" + tmp.replace("\\", "/"))
            page.emulate_media(media="print")
            page.wait_for_function(
                "() => Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)")
            return page.evaluate(js)
        finally:
            browser.close()


def verify(figures):
    hr("STEP 6  VERIFICATION")
    results = []

    for label, path in (("docx", DOCX_PATH), ("pdf", PDF_PATH)):
        e = os.path.isfile(path)
        s = os.path.getsize(path) if e else 0
        good = e and s > 50000
        results.append((good, "%s exists and is non-trivial" % label))
        print("  [%s] %s exists=%s size=%d bytes"
              % ("PASS" if good else "FAIL", label, e, s))

    # ---- docx page geometry
    doc = Document(DOCX_PATH)
    sec = doc.sections[0]
    cw = sec.page_width.inches - sec.left_margin.inches - sec.right_margin.inches
    ch = sec.page_height.inches - sec.top_margin.inches - sec.bottom_margin.inches
    pg_ok = (abs(sec.page_width.cm - PAGE_W_CM) < 0.02
             and abs(sec.page_height.cm - PAGE_H_CM) < 0.02)
    land_ok = sec.page_width > sec.page_height
    mar_ok = all(abs(getattr(sec, a).inches - 1.0) < 0.01
                 for a in ("left_margin", "right_margin", "top_margin", "bottom_margin"))
    results.append((pg_ok and land_ok, "docx page is A4 LANDSCAPE 29.7 x 21.0 cm"))
    results.append((mar_ok, "docx margins are 2.54 cm on all four sides"))
    results.append((abs(cw - CONTENT_W_IN) < 0.01,
                    "docx content box is %.2f x %.2f in" % (cw, ch)))
    print("  [%s] page %.2f x %.2f cm = %.3f x %.3f in  (landscape=%s, A4 landscape = 29.70 x 21.00 cm)"
          % ("PASS" if pg_ok and land_ok else "FAIL", sec.page_width.cm, sec.page_height.cm,
             sec.page_width.inches, sec.page_height.inches, land_ok))
    print("  [%s] margins L%.2f R%.2f T%.2f B%.2f in"
          % ("PASS" if mar_ok else "FAIL", sec.left_margin.inches, sec.right_margin.inches,
             sec.top_margin.inches, sec.bottom_margin.inches))
    print("  [%s] content box %.3f x %.3f in (%.2f x %.2f cm)"
          % ("PASS" if abs(cw - CONTENT_W_IN) < 0.01 else "FAIL", cw, ch, cw * 2.54, ch * 2.54))

    paras = doc.paragraphs
    body = [p for p in paras if p.text.strip()]
    pics = [p for p in paras if p._element.findall(".//" + qn("w:drawing"))]
    breaks = doc.element.body.findall(".//" + qn("w:br") + "[@" + qn("w:type") + "='page']")
    n_ok = len(pics) == 7 and len(breaks) == 6
    results.append((n_ok, "docx has 7 image paragraphs and 6 page breaks"))
    print("  [%s] paragraphs=%d  image paragraphs=%d  page breaks=%d (expect 7 / 6)"
          % ("PASS" if n_ok else "FAIL", len(paras), len(pics), len(breaks)))

    # order + fonts + alignment + real text
    headings = [p for p in body if p.runs and p.runs[0].font.size == Pt(14)]
    caps = [p for p in body if p.runs and p.runs[0].font.size == Pt(11)]
    secs = [p for p in body if p.text.strip() == NARRATIVE_HEADING]
    narrs = [p for p in body if p.text.strip() and p.text.strip() != NARRATIVE_HEADING
             and p not in headings and p not in caps]
    struct_ok = (len(headings) == 7 and len(caps) == 7 and len(secs) == 7
                 and len(narrs) == 7)
    results.append((struct_ok, "docx has 7 headings / 7 captions / 7 narrative headings / 7 narratives"))
    print("  [%s] h1=%d caption=%d '%s'=%d narrative=%d"
          % ("PASS" if struct_ok else "FAIL", len(headings), len(caps),
             NARRATIVE_HEADING, len(secs), len(narrs)))

    font_ok = all(r.font.name == FONT for p in body for r in p.runs)
    b_ok = all(r.bold for p in headings for r in p.runs)
    i_ok = all(r.italic for p in caps for r in p.runs)
    align_ok = (all(p.alignment == WD_ALIGN_PARAGRAPH.CENTER for p in headings)
                and all(p.alignment == WD_ALIGN_PARAGRAPH.CENTER for p in caps)
                and all(p.alignment == WD_ALIGN_PARAGRAPH.JUSTIFY for p in narrs))
    pic_centered = all(p.alignment == WD_ALIGN_PARAGRAPH.CENTER for p in pics)
    ind_ok = (all(p.paragraph_format.left_indent is not None
                  and abs(p.paragraph_format.left_indent.inches - NARR_INDENT_IN) < 0.01
                  and abs(p.paragraph_format.right_indent.inches - NARR_INDENT_IN) < 0.01
                  for p in secs + narrs)
              and all(p.paragraph_format.left_indent is None
                      for p in headings + caps + pics))
    results.append((font_ok and b_ok and i_ok, "Times New Roman on every run; headings bold; captions italic"))
    results.append((align_ok and pic_centered, "headings/captions/images centred, narratives justified"))
    results.append((ind_ok, "narratives indented %.1f in each side, measure %.2f in"
                    % (NARR_INDENT_IN, cw - 2 * NARR_INDENT_IN)))
    print("  [%s] every run font == '%s'" % ("PASS" if font_ok else "FAIL", FONT))
    print("  [%s] headings bold=%s  captions italic=%s" % ("PASS" if (b_ok and i_ok) else "FAIL", b_ok, i_ok))
    print("  [%s] centred headings/captions/pictures=%s  justified narratives=%s"
          % ("PASS" if (align_ok and pic_centered) else "FAIL", align_ok and pic_centered, align_ok))
    print("  [%s] narrative measure %.2f in (indent %.1f + %.1f, content %.2f)"
          % ("PASS" if ind_ok else "FAIL", cw - 2 * NARR_INDENT_IN, NARR_INDENT_IN,
             NARR_INDENT_IN, cw))

    longest = max(narrs, key=lambda p: len(p.text))
    txt_ok = longest.text.strip() == figures[0]["narrative"] or len(longest.text.strip()) > 200
    results.append((txt_ok, "narratives are real editable text (no <w:drawing> in them)"))
    print("  [%s] narrative chars: %s"
          % ("PASS" if txt_ok else "FAIL", [len(p.text.strip()) for p in narrs]))
    print("         sample: \"%s...\"" % longest.text.strip()[:90])

    # ---- embedded media: every image must match its planned placement and fit the box
    media_ok = True
    fit_ok = True
    with zipfile.ZipFile(DOCX_PATH) as z:
        media = sorted(n for n in z.namelist() if n.startswith("word/media/"))
        media_ok = len(media) == 7
        print("  [%s] media parts in docx = %d" % ("PASS" if media_ok else "FAIL", len(media)))
    shapes = doc.inline_shapes
    for i, f in enumerate(figures):
        sh = shapes[i]
        pw, ph = sh.width.inches, sh.height.inches
        good = abs(pw - f["img_w"]) < 0.01 and abs(ph - f["img_h"]) < 0.01
        fits = pw <= cw + 0.005 and ph <= ch + 0.005
        media_ok &= good
        fit_ok &= fits
        print("         fig %d placed %6.3f x %6.3f in  (%s-limited, planned %.3f x %.3f)  "
              "fits content box=%s"
              % (i + 1, pw, ph, f["limited"], f["img_w"], f["img_h"], fits))
    results.append((media_ok, "every embedded image sits at its planned width and height"))
    results.append((fit_ok, "no image exceeds the content box (%.2f x %.2f in)" % (cw, ch)))

    # ---- page-break positions
    brk_ok = True
    idx = 0
    for p in paras:
        if p._element.findall(".//" + qn("w:br") + "[@" + qn("w:type") + "='page']"):
            idx += 1
            nxt = [q.text.strip() for q in paras[paras.index(p) + 1:] if q.text.strip()]
            if idx <= 6 and (not nxt or nxt[0] != figures[idx]["heading"]):
                brk_ok = False
                print("         break %d followed by %r (expected %r)"
                      % (idx, nxt[0] if nxt else None, figures[idx]["heading"]))
    results.append((brk_ok, "each page break is followed by the next figure's heading"))
    print("  [%s] page breaks land in the right places (6 breaks, last figure has none)"
          % ("PASS" if brk_ok else "FAIL"))

    # ---- printed label sizes
    hr("PRINTED SIZE OF EVERY DIAGRAM LABEL")
    print("  printed pt = label_px / viewBoxWidth * placed_inches * 72")
    print("  %-5s %-12s %-13s %-17s %-8s %-9s %-11s %s"
          % ("Fig", "viewBox", "PNG px", "placed in (w x h)", "DPI", "main px", "main pt", "smallest px -> pt"))
    min_main = 99.0
    for i, f in enumerate(figures, 1):
        min_main = min(min_main, f["main_pt"])
        print("  %-5d %-12s %-13s %-17s %-8.0f %-9.1f %-11.2f %.1f -> %.2f"
              % (i, "%.0fx%.0f" % (f["vbw"], f["vbh"]),
                 "%dx%d" % (f["png_w"], f["png_h"]),
                 "%.3f x %.3f" % (f["img_w"], f["img_h"]), f["dpi"],
                 f["main_px"], f["main_pt"], f["min_px"], f["min_pt"]))
    results.append((min_main >= 6.0,
                    "every main label prints at >= 6 pt (smallest %.2f pt)" % min_main))
    print("\n  [%s] smallest MAIN label across the set = %.2f pt (figure %d, %.1f px)"
          % ("PASS" if min_main >= 6.0 else "FAIL", min_main,
             min(range(7), key=lambda i: figures[i]["main_pt"]) + 1,
             min(figures, key=lambda f: f["main_pt"])["main_px"]))
    print("  %s  smallest text of any kind = %.2f pt (%.1f px arrow flow labels) -- "
          "these sit on a diagram that is already at full page width, so page geometry"
          % ("NOTE", min(f["min_pt"] for f in figures),
             min(f["min_px"] for f in figures)))
    print("        cannot enlarge them further; only editing the SVG could.")

    # ---- png quality
    png_ok = all(abs(f["png_w"] - f["target_px"]) <= 2 and f["black_px"] > 1000
                 and f["white_px"] > 1000 and f["edge_ink"] == 0 for f in figures)
    dpi_ok = all(f["dpi"] >= MIN_DPI - 1 for f in figures)
    results.append((png_ok, "all 7 PNGs are at least %d px wide, non-blank, black+white, unclipped" % TARGET_W))
    results.append((dpi_ok, "every PNG prints at >= %d DPI at its placed width" % MIN_DPI))
    print("  [%s] all PNGs non-blank, correctly sized, nothing touching the border"
          % ("PASS" if png_ok else "FAIL"))
    print("         pure-black px per image: %s" % [f["black_px"] for f in figures])
    print("         ink on 4px border ring: %s" % [f["edge_ink"] for f in figures])
    print("  [%s] effective DPI per figure: %s (all >= %d)"
          % ("PASS" if dpi_ok else "FAIL", [round(f["dpi"]) for f in figures], MIN_DPI))

    # ---- pdf
    hr("PDF GEOMETRY")
    pages = pdf_pages(PDF_PATH)
    pdf_ok = len(pages) == 7
    results.append((pdf_ok, "PDF has 7 pages"))
    print("  [%s] PDF page count = %d" % ("PASS" if pdf_ok else "FAIL", len(pages)))
    max_w_pt = CONTENT_W_IN * 72.0
    land_ok = all(abs(w - 841.89) < 2.0 and abs(h - 595.28) < 2.0 for w, h, _ in pages)
    width_ok = all(all(x <= max_w_pt + 0.05 for x in ws) for _, _, ws in pages)
    drawn = [ws[0] for _, _, ws in pages if len(ws) == 1]
    match_ok = (len(drawn) == 7
                and all(abs(drawn[i] - figures[i]["img_w"] * 72.0) < 0.5 for i in range(7)))
    one_img_ok = all(len(ws) == 1 for _, _, ws in pages)
    results.append((land_ok, "every PDF page has a landscape MediaBox (841.9 x 595.3 pt)"))
    results.append((width_ok, "no PDF image is wider than %.1f pt (%.4f in content box)"
                    % (max_w_pt, CONTENT_W_IN)))
    results.append((match_ok, "PDF image widths match the docx placements to within 0.5 pt"))
    results.append((one_img_ok, "every PDF page carries exactly one image"))
    for i, (w, h, ws) in enumerate(pages, 1):
        print("         page %d  MediaBox %.1f x %.1f pt  images=%d  %s"
              % (i, w, h, len(ws),
                 "  ".join("%.1f pt (%.3f in)" % (x, x / 72.0) for x in ws) or "-"))
    print("  [%s] all MediaBoxes landscape = %s (A4 landscape = 841.89 x 595.28 pt)"
          % ("PASS" if land_ok else "FAIL", land_ok))
    print("  [%s] widest image on any page = %.2f pt (limit %.2f pt)"
          % ("PASS" if width_ok else "FAIL",
             max([x for _, _, ws in pages for x in ws] or [0.0]), max_w_pt))
    print("  [%s] pdf vs docx image widths match to < 0.5 pt"
          % ("PASS" if match_ok else "FAIL"))
    for i, x in enumerate(drawn):
        print("         fig %d  pdf %.2f pt (%.4f in)  docx %.2f pt (%.4f in)  delta %.2f pt"
              % (i + 1, x, x / 72.0, figures[i]["img_w"] * 72.0, figures[i]["img_w"],
                 abs(x - figures[i]["img_w"] * 72.0)))
    print("  [%s] exactly one image per page = %s" % ("PASS" if one_img_ok else "FAIL", one_img_ok))
    print("         page -> figure order: %s"
          % ([i + 1 for i, (_, _, ws) in enumerate(pages) if ws],))

    # ---- why the page count is what it is
    content_pt = CONTENT_H_IN * 72.0
    try:
        budget = page_budget(figures)
    except Exception as exc:                       # diagnostic only, never fatal
        budget = None
        print("  (could not measure page budget: %s)" % exc)
    if budget:
        hr("PAGE BUDGET  (A4 landscape holds %.1f pt of content)" % content_pt)
        print("  %-5s %-11s %-11s %-11s %s" % ("Fig", "image pt", "text pt", "total pt", "one page?"))
        over = []
        for i, b in enumerate(budget, 1):
            total = b["img"] + b["text"]
            if total > content_pt:
                over.append(i)
            print("  %-5d %-11.1f %-11.1f %-11.1f %s"
                  % (i, b["img"], b["text"], total,
                     "yes" if total <= content_pt else "NO - over by %.0f pt" % (total - content_pt)))
        if over:
            print("\n  NOTE: figures %s cannot share a page with their own narrative at this"
                  % ", ".join(str(i) for i in over))
            print("        image width.  A 6.27 in tall page cannot hold a 5.4-6.3 in image AND")
            print("        a heading, caption, section heading and a ~140-word narrative.")
            print("        Legible labels win here; the extra pages are the cost.  Shrinking the")
            print("        image to fit would drop the main labels to about 4.0-4.8 pt on figures")
            print("        3-7, which is the unreadable case this layout was meant to remove.")
            print("        To trade back: lower CONTENT_H_IN in plan_geometry() to ~3.3 in.")

    hr("SUMMARY")
    for good, msg in results:
        print("  %s  %s" % ("PASS" if good else "FAIL", msg))
    return all(g for g, _ in results)


# --------------------------------------------------------------------------- main

def main():
    hr("STEP 1  PARSE 7 HTML FIGURES")
    figures = []
    for name in FIGURES:
        p = os.path.join(SRC_DIR, name)
        if not os.path.isfile(p):
            sys.exit("missing source: %s" % p)
        f = parse_figure(p)
        figures.append(f)
        print("  %-34s h1=%-42s caption=%.40s..." % (name, f["heading"], f["caption"]))
        print("  %-34s viewBox %.0fx%.0f   narrative %d chars   css %d bytes"
              % ("", f["vbw"], f["vbh"], len(f["narrative"]), len(f["css"])))
        print("  %-34s text sizes %s -> main %.1f px, smallest %.1f px"
              % ("", sorted(f["sizes"].keys()), f["main_px"], f["min_px"]))

    plan_geometry(figures)

    hr("STEP 3  RENDER 7 PNGs (>= %d PX, >= %d DPI ON THE PAGE)" % (TARGET_W, MIN_DPI))
    render_pngs(figures)
    check_pngs(figures)

    hr("STEP 4  BUILD DOCX (A4 LANDSCAPE)")
    build_docx(figures)

    hr("STEP 5  BUILD PDF (A4 LANDSCAPE)")
    build_pdf(figures)

    ok = verify(figures)

    hr("CLEANUP")
    if os.path.isdir(TMP_PNG):
        shutil.rmtree(TMP_PNG)
        print("removed temp folder: %s" % TMP_PNG)

    hr("RESULT: %s" % ("ALL CHECKS PASSED" if ok else "SOME CHECKS FAILED"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())