"""Generate 21-page PDF matching Daksh's exact Word-like format"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Preformatted)
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Register Times New Roman (Windows has it)
for name, fname in [
    ("TimesNewRoman", "times.ttf"),
    ("TimesNewRoman-Bold", "timesbd.ttf"),
    ("TimesNewRoman-Italic", "timesi.ttf"),
    ("Calibri", "calibri.ttf"),
    ("CourierNew", "cour.ttf"),
]:
    try:
        pdfmetrics.registerFont(TTFont(name, fname))
    except:
        pass

W, H = A4

def header_footer(canvas, doc):
    canvas.saveState()
    # Match Daksh: bold TNR left, Calibri center+right
    canvas.setFont("TimesNewRoman-Bold", 10)
    canvas.drawString(1.8*cm, H - 1.2*cm, "DVA Assignment 2")
    try:
        canvas.setFont("Calibri", 11)
    except:
        canvas.setFont("Helvetica", 11)
    canvas.drawCentredString(W/2, H - 1.2*cm, "Akshat Tripathi")
    canvas.drawRightString(W - 1.8*cm, H - 1.2*cm, "04914202023")
    canvas.restoreState()

def build_pdf():
    doc = SimpleDocTemplate("DVA_Assignment_2_Akshat_Tripathi.pdf", pagesize=A4,
        topMargin=2.0*cm, bottomMargin=1.5*cm, leftMargin=1.8*cm, rightMargin=1.8*cm)

    # Styles matching Daksh's Word doc
    title_s = ParagraphStyle("Title", fontName="TimesNewRoman-Bold", fontSize=24,
        alignment=TA_CENTER, spaceAfter=12, spaceBefore=30)
    subtitle_s = ParagraphStyle("SubTitle", fontName="TimesNewRoman-Bold", fontSize=14,
        alignment=TA_CENTER, spaceAfter=10, spaceBefore=8, leading=20)
    h1_s = ParagraphStyle("H1", fontName="TimesNewRoman-Bold", fontSize=12,
        spaceAfter=8, spaceBefore=16)
    body_s = ParagraphStyle("Body", fontName="TimesNewRoman", fontSize=12,
        spaceAfter=4, leading=16)
    link_s = ParagraphStyle("Link", fontName="TimesNewRoman", fontSize=12,
        spaceAfter=6, leading=16)
    bullet_s = ParagraphStyle("Bullet", fontName="TimesNewRoman", fontSize=12,
        spaceAfter=3, leading=15, leftIndent=20, bulletIndent=8)
    sub_bullet_s = ParagraphStyle("SubBullet", fontName="TimesNewRoman", fontSize=12,
        spaceAfter=3, leading=15, leftIndent=40, bulletIndent=28)
    code_s = ParagraphStyle("Code", fontName="CourierNew", fontSize=8, leading=10,
        leftIndent=6, rightIndent=6, spaceBefore=2, spaceAfter=2,
        backColor=HexColor("#F8F8F8"), borderPadding=4)
    caption_s = ParagraphStyle("Caption", fontName="TimesNewRoman-Bold", fontSize=12,
        spaceAfter=6, spaceBefore=8)

    story = []

    # ═══════ PAGE 1 — Cover + Overview + Dataset ═══════
    story.append(Spacer(1, 1.5*cm))
    story.append(Paragraph("Assignment-2", title_s))
    story.append(Spacer(1, 0.6*cm))
    story.append(Paragraph(
        "Data Visualization and Analytics Project: Social Media Trends Analytics Dashboard", subtitle_s))
    story.append(Spacer(1, 0.6*cm))
    story.append(Paragraph(
        'Project Link: https://github.com/akshattripathi1/Social-Media-Trends-Dashboard', link_s))
    story.append(Paragraph(
        'Dataset: Custom Social Media Trends Dataset (2000 records, 12 columns)', link_s))
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("Project Overview", h1_s))
    story.append(Paragraph(
        'This project presents a <b>multi-page interactive dashboard</b> developed using Python, Tkinter, Pandas, and '
        'Matplotlib to analyze <b>social media trends and engagement metrics</b> across different platforms.', body_s))
    story.append(Paragraph(
        'The system transforms raw social media data into a <b>visual analytics platform</b> that helps users understand '
        'platform performance, content engagement patterns, and trending hashtags.', body_s))
    story.append(Paragraph('The dashboard is designed to provide insights into:', body_s))

    for b in [
        "Social media engagement trends across Twitter, Instagram, YouTube, Facebook, and TikTok",
        "Hashtag performance and trending analysis across 10 content categories",
        "Platform-wise reach comparison (Views, Likes, Comments, Shares)",
        "Content category engagement patterns (Entertainment, Sports, Technology, etc.)",
        "Metric correlation analysis (Posts vs Likes vs Views vs Engagement Rate)",
        "Platform × Category engagement heatmap for identifying content sweet spots",
    ]:
        story.append(Paragraph(f"• {b}", bullet_s))

    story.append(Paragraph(
        'The interface follows a <b>clean modern UI design</b> with a midnight purple theme and color-coded '
        'platform indicators for better visual understanding.', body_s))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("Dataset Overview", h1_s))
    story.append(Paragraph(
        'The dataset contains <b>2000 records of social media trend data</b> simulating realistic engagement '
        'patterns across multiple platforms and content categories.', body_s))
    story.append(Paragraph('It includes:', body_s))
    for b in [
        "Platform (Twitter, Instagram, YouTube, Facebook, TikTok)",
        "Hashtag name (60 unique hashtags)",
        "Content Category (Entertainment, Sports, Politics, Technology, Fashion, Gaming, Food, Travel, Education, Health)",
        "Country of origin (11 countries, India-biased)",
        "Date and Month",
        "Metrics:",
    ]:
        story.append(Paragraph(f"• {b}", bullet_s))
    for sb in ["Posts count", "Likes", "Views", "Comments", "Shares", "Engagement Rate (%)"]:
        story.append(Paragraph(f"o {sb}", sub_bullet_s))

    # ═══════ PAGE 2 — Tech Stack ═══════
    story.append(Paragraph(
        'This dataset is used to analyze social media trends and visualize engagement patterns effectively.', body_s))
    story.append(Paragraph("Tech Stack", h1_s))
    for tech, desc in [
        ("Python", "Programming language"),
        ("Tkinter", "GUI framework for dashboard"),
        ("Pandas", "Data cleaning and analysis"),
        ("Matplotlib", "Data visualization (charts &amp; graphs)"),
        ("NumPy", "Numerical computation and data processing"),
    ]:
        story.append(Paragraph(f"<b>{tech}</b> → {desc}", body_s))

    story.append(PageBreak())

    # ═══════ PAGES 3-18 — Code ═══════
    story.append(Paragraph("Program Code", h1_s))
    story.append(Spacer(1, 0.2*cm))

    with open("dashboard.py", "r", encoding="utf-8") as f:
        code_text = f.read()

    lines = code_text.split("\n")
    chunk_size = 16
    for i in range(0, len(lines), chunk_size):
        chunk = "\n".join(lines[i:i+chunk_size])
        chunk = chunk.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        chunk = chunk.replace("\t", "    ")
        story.append(Preformatted(chunk, code_s))
        if i + chunk_size < len(lines):
            story.append(PageBreak())

    story.append(PageBreak())

    # ═══════ PAGES 19-21 — Output Screenshots ═══════
    story.append(Paragraph("Output", ParagraphStyle("Out", fontName="TimesNewRoman-Bold",
        fontSize=16, spaceAfter=10, spaceBefore=6)))
    story.append(Spacer(1, 0.3*cm))

    ss_pages = [
        [("page1_overview.png", "Page 1- Overview"),
         ("page2_platform.png", "Page 2- Platform Analysis")],
        [("page3_category.png", "Page 3- Category Trends"),
         ("page4_hashtag.png", "Page 4- Hashtag Rankings")],
        [("page5_heatmap.png", "Page 5- Heatmap &amp; Correlations")],
    ]
    for page_group in ss_pages:
        for fname, caption in page_group:
            fpath = os.path.join("screenshots", fname)
            if os.path.exists(fpath):
                story.append(Paragraph(caption, caption_s))
                story.append(Spacer(1, 0.2*cm))
                img = Image(fpath, width=17*cm, height=9.5*cm)
                story.append(img)
                story.append(Spacer(1, 0.5*cm))
        story.append(PageBreak())

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print("PDF generated!")

if __name__ == "__main__":
    build_pdf()
