"""Generate PDF assignment matching Daksh's format"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import os

W, H = A4
MARGIN = 1.2*cm

def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(HexColor("#555555"))
    canvas.drawString(MARGIN, H - 0.8*cm, "DVA Assignment 2")
    canvas.drawCentredString(W/2, H - 0.8*cm, "Akshat Tripathi")
    canvas.drawRightString(W - MARGIN, H - 0.8*cm, "04914202023")
    canvas.restoreState()

def build_pdf():
    doc = SimpleDocTemplate("DVA_Assignment_2_Akshat_Tripathi.pdf", pagesize=A4,
        topMargin=1.5*cm, bottomMargin=1.2*cm, leftMargin=MARGIN, rightMargin=MARGIN)
    styles = getSampleStyleSheet()
    title_s = ParagraphStyle("Title2", parent=styles["Title"], fontSize=22, spaceAfter=6, alignment=TA_CENTER)
    h1 = ParagraphStyle("H1", parent=styles["Heading1"], fontSize=16, spaceAfter=10, spaceBefore=16)
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=13, spaceAfter=8, spaceBefore=12)
    body = ParagraphStyle("Body2", parent=styles["BodyText"], fontSize=11, spaceAfter=6, leading=15)
    bullet = ParagraphStyle("Bullet2", parent=body, leftIndent=20, bulletIndent=10)
    code_s = ParagraphStyle("Code2", parent=styles["Code"], fontSize=8, leading=10, leftIndent=10,
        backColor=HexColor("#F5F5F5"), borderWidth=1, borderColor=HexColor("#DDDDDD"), borderPadding=6)
    small = ParagraphStyle("Small2", parent=body, fontSize=10, textColor=HexColor("#555555"))

    story = []

    # COVER
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("Assignment-2", title_s))
    story.append(Spacer(1, 0.8*cm))
    story.append(Paragraph("Data Visualization and Analytics Project:<br/>Social Media Trends Analytics Dashboard", h1))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph('<b>Project Link:</b> <a href="https://github.com/akshattripathi1/Social-Media-Trends-Dashboard">https://github.com/akshattripathi1/Social-Media-Trends-Dashboard</a>', body))
    story.append(Paragraph('<b>Dataset:</b> Custom generated Social Media Trends dataset (2000 records)', body))
    story.append(Spacer(1, 0.8*cm))

    # Project Overview
    story.append(Paragraph("Project Overview", h1))
    story.append(Paragraph(
        "This project presents a multi-page interactive dashboard developed using Python, Tkinter, Pandas, and "
        "Matplotlib to analyze social media trends and engagement metrics across different platforms.", body))
    story.append(Paragraph(
        "The system transforms raw social media data into a visual analytics platform that helps users understand "
        "platform performance, hashtag popularity, and content engagement patterns.", body))
    story.append(Paragraph("The dashboard is designed to provide insights into:", body))
    for item in [
        "Platform-wise reach and engagement comparison (Twitter, Instagram, YouTube, Facebook, TikTok)",
        "Hashtag performance and trending analysis",
        "Content category engagement patterns (Entertainment, Sports, Technology, etc.)",
        "Metric correlations (Posts, Likes, Views, Comments, Shares)",
        "Platform vs Category engagement heatmap",
        "Top performing and underperforming content identification",
    ]:
        story.append(Paragraph(f"• {item}", bullet))
    story.append(Paragraph(
        "The interface follows a clean modern UI design with a midnight purple theme and color-coded "
        "platform indicators for better visual understanding.", body))

    # Dataset Overview
    story.append(Paragraph("Dataset Overview", h1))
    story.append(Paragraph(
        "The dataset contains 2000 records of social media trend data generated to simulate realistic "
        "engagement patterns across multiple platforms and content categories.", body))
    story.append(Paragraph("It includes:", body))
    for item in ["Platform (Twitter, Instagram, YouTube, Facebook, TikTok)", "Hashtag name",
                  "Content Category", "Country of origin", "Date and Month",
                  "Posts count", "Likes, Views, Comments, Shares", "Engagement Rate (%)"]:
        story.append(Paragraph(f"• {item}", bullet))

    # Tech Stack
    story.append(Paragraph("Tech Stack", h1))
    for tech, desc in [
        ("Python", "Programming language"),
        ("Tkinter", "GUI framework for dashboard"),
        ("Pandas", "Data cleaning and analysis"),
        ("Matplotlib", "Data visualization (charts & graphs)"),
        ("NumPy", "Numerical computations"),
    ]:
        story.append(Paragraph(f"<b>{tech}</b> → {desc}", body))

    story.append(PageBreak())

    # CODE
    story.append(Paragraph("Program Code", h1))

    # Read dashboard.py
    with open("dashboard.py", "r", encoding="utf-8") as f:
        code = f.read()

    # Split code into chunks to fit pages
    lines = code.split("\n")
    chunk_size = 55
    for i in range(0, len(lines), chunk_size):
        chunk = "\n".join(lines[i:i+chunk_size])
        chunk = chunk.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        chunk = chunk.replace(" ", "&nbsp;").replace("\n", "<br/>")
        story.append(Paragraph(chunk, code_s))
        if i + chunk_size < len(lines):
            story.append(PageBreak())

    story.append(PageBreak())

    # OUTPUT SCREENSHOTS
    story.append(Paragraph("Output", h1))
    ss_dir = "screenshots"
    pages_info = [
        ("page1_overview.png", "Page 1 - Overview"),
        ("page2_platform.png", "Page 2 - Platform Analysis"),
        ("page3_category.png", "Page 3 - Category Trends"),
        ("page4_hashtag.png", "Page 4 - Hashtag Rankings"),
        ("page5_heatmap.png", "Page 5 - Heatmap & Correlation"),
    ]
    for fname, caption in pages_info:
        fpath = os.path.join(ss_dir, fname)
        if os.path.exists(fpath):
            story.append(Spacer(1, 0.3*cm))
            story.append(Paragraph(caption, h2))
            img = Image(fpath, width=16*cm, height=9*cm)
            story.append(img)
            story.append(Spacer(1, 0.5*cm))

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print("PDF generated: DVA_Assignment_2_Akshat_Tripathi.pdf")

if __name__ == "__main__":
    build_pdf()
