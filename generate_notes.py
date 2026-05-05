import os
from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_architecture_diagram():
    fig, ax = plt.subplots(figsize=(8, 4), dpi=150)
    ax.axis('off')
    boxes = [
        {"xy": (0.05, 0.4), "width": 0.2, "height": 0.3, "text": "Raw Data\n(Kaggle CSV)", "color": "#f39c12"},
        {"xy": (0.35, 0.4), "width": 0.2, "height": 0.3, "text": "Pandas\n(Data Engine)", "color": "#3498db"},
        {"xy": (0.65, 0.6), "width": 0.25, "height": 0.25, "text": "Matplotlib\n(Visualization)", "color": "#e74c3c"},
        {"xy": (0.65, 0.2), "width": 0.25, "height": 0.25, "text": "Tkinter\n(GUI Framework)", "color": "#9b59b6"}
    ]
    for b in boxes:
        rect = patches.Rectangle(b["xy"], b["width"], b["height"], linewidth=2, edgecolor='black', facecolor=b["color"], alpha=0.8)
        ax.add_patch(rect)
        ax.text(b["xy"][0] + b["width"]/2, b["xy"][1] + b["height"]/2, b["text"], 
                horizontalalignment='center', verticalalignment='center', 
                fontsize=11, fontweight='bold', color='white')
    ax.annotate('', xy=(0.35, 0.55), xytext=(0.25, 0.55), arrowprops=dict(facecolor='black', shrink=0.05, width=2))
    ax.annotate('', xy=(0.65, 0.72), xytext=(0.55, 0.65), arrowprops=dict(facecolor='black', shrink=0.05, width=2))
    ax.annotate('', xy=(0.65, 0.32), xytext=(0.55, 0.45), arrowprops=dict(facecolor='black', shrink=0.05, width=2))
    dash_rect = patches.Rectangle((0.6, 0.1), 0.35, 0.85, linewidth=2, edgecolor='#2c3e50', facecolor='none', linestyle='--')
    ax.add_patch(dash_rect)
    ax.text(0.775, 0.9, "Frontend Dashboard", horizontalalignment='center', fontweight='bold', color='#2c3e50')
    plt.tight_layout()
    plt.savefig('architecture_diagram.png', bbox_inches='tight', dpi=300)
    plt.close()

def add_header(doc, text, level=1):
    p = doc.add_paragraph()
    run = p.add_run(text)
    if level == 1:
        run.font.size = Pt(20)
        run.bold = True
        run.font.color.rgb = RGBColor(75, 0, 130)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif level == 2:
        run.font.size = Pt(16)
        run.bold = True
        run.font.color.rgb = RGBColor(0, 51, 102)
    elif level == 3:
        run.font.size = Pt(14)
        run.bold = True
        run.font.color.rgb = RGBColor(41, 128, 185)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.space_before = Pt(12)

def add_para(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    if "<b>" in text:
        parts = text.split("<b>")
        for part in parts:
            if "</b>" in part:
                bold_text, normal_text = part.split("</b>", 1)
                r = p.add_run(bold_text)
                r.bold = True
                r.font.name = "Calibri"
                r.font.size = Pt(12)
                if normal_text:
                    r2 = p.add_run(normal_text)
                    r2.font.name = "Calibri"
                    r2.font.size = Pt(12)
            else:
                r = p.add_run(part)
                r.font.name = "Calibri"
                r.font.size = Pt(12)
    else:
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(12)

def add_image(doc, img_path, width_inches=6.0):
    if os.path.exists(img_path):
        doc.add_picture(img_path, width=Inches(width_inches))
        last_paragraph = doc.paragraphs[-1]
        last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

def build_notes():
    create_architecture_diagram()
    doc = Document()
    
    for section in doc.sections:
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(2.0)
        section.right_margin = Cm(2.0)
        
    add_header(doc, "Complete Deep-Dive Viva & Analysis Report", 1)
    add_header(doc, "Social Media Trends Analytics Dashboard", 1)
    add_para(doc, "This is the <b>Ultimate Master Guide</b> for the Viva. It contains all the diagrams, deep data analysis, and perfectly phrased, bolded answers. <b>Read the bold parts</b> out loud to your professor.")
    
    add_header(doc, "1. Architecture Diagram & Workflow", 2)
    add_para(doc, "<b>How the project fundamentally works:</b>")
    add_image(doc, 'architecture_diagram.png', 6.0)
    add_para(doc, "1. <b>Kaggle CSV:</b> The raw data source.\n2. <b>Pandas Data Engine:</b> Cleans, calculates, and groups the data.\n3. <b>Matplotlib:</b> Draws the visual charts based on the Pandas calculations.\n4. <b>Tkinter Dashboard:</b> Wraps everything into a clickable desktop application.")
    
    doc.add_page_break()
    
    add_header(doc, "2. Deep Report Analysis (Page-by-Page)", 2)
    add_para(doc, "Here is the exact deep-level analysis of every screen. <b>Show these screens</b> during the presentation and read the bold explanations.")
    
    add_header(doc, "Tab 1: Executive Overview", 3)
    add_image(doc, os.path.join("screenshots", "page1_overview.png"), 6.5)
    add_para(doc, "<b>Deep Analysis:</b> This screen uses a 'Donut Pie Chart' to display the <b>Category Distribution</b>. We can clearly see that 'Entertainment' and 'Technology' dominate the space. The left side uses <b>KPI Cards (Key Performance Indicators)</b> to instantly show the total posts, views, and an <b>Average Engagement Rate</b> of all platforms combined. The horizontal bars handle the <b>Platform Reach</b> and <b>Top 5 Hashtags</b>.")
    
    doc.add_page_break()
    
    add_header(doc, "Tab 2: Platform Analysis", 3)
    add_image(doc, os.path.join("screenshots", "page2_platform.png"), 6.5)
    add_para(doc, "<b>Deep Analysis:</b> I built a custom <b>Scrollable Data Table</b> on the left using Tkinter Canvas logic. It proves the exact numbers behind the bar charts. I scaled the numbers (dividing by 1,000,000) so the Y-axis reads in 'Millions' (M). We can conclude that while <b>YouTube</b> might get the most Views, <b>Instagram</b> typically yields higher <b>Shares</b> and <b>Comments</b>.")
    
    doc.add_page_break()
    
    add_header(doc, "Tab 3: Category Trends", 3)
    add_image(doc, os.path.join("screenshots", "page3_category.png"), 6.5)
    add_para(doc, "<b>Deep Analysis:</b> This dashboard answers 'What are people watching?'. I used <b>GridSpec</b> to align four different charts. The bottom-left chart (Top 10 Hashtags by Eng Rate) proves that viral hashtags don't always get the most views, but they trigger the highest <b>user interaction percentage</b>.")
    
    doc.add_page_break()
    
    add_header(doc, "Tab 4 & 5: Heatmaps and Correlations", 3)
    add_image(doc, os.path.join("screenshots", "page5_heatmap.png"), 6.5)
    add_para(doc, "<b>Deep Analysis:</b> The <b>Correlation Matrix</b> proves mathematically how strongly 'Likes' are connected to 'Views' (usually a +0.9 correlation). The <b>Heatmap</b> is a 2D matrix (Platform vs Category). A bright yellow spot means 'High Engagement Sweet Spot' (e.g., Gaming on YouTube), whereas dark purple means 'Dead Zone' (e.g., Fashion on LinkedIn).")
    
    doc.add_page_break()
    
    add_header(doc, "3. Deep Technical Viva Questions & Bulletproof Answers", 2)
    
    qa_pairs = [
        (
            "Where did you get the dataset? Did you just download a pre-made CSV?",
            "<b>I sourced the raw data from Kaggle (Social Media Sentiment Dataset). However, my real work was Data Wrangling.</b> I had to clean missing values, normalize heavily skewed numbers, and engineer calculated fields like 'Engagement Rate'. I processed it into a clean 2,000-record format. It's not just a fake script; it's a rigorously processed dataset."
        ),
        (
            "How did you integrate Matplotlib graphs directly inside Tkinter without separate popups?",
            "<b>I used a bridge library called 'FigureCanvasTkAgg'.</b> Instead of `plt.show()` throwing a separate window, this converts the Matplotlib `Figure` into a Tkinter `Canvas` widget. This is how enterprise software embeds charts into unified dashboards."
        ),
        (
            "What is 'GridSpec' and why didn't you just use simple subplots?",
            "<b>`GridSpec` allows pixel-perfect custom layouts.</b> Simple subplots force equal sizing. GridSpec lets me span a chart across multiple rows or adjust exact horizontal/vertical spacing, which is critical for making the dashboard look professional."
        ),
        (
            "How do you prevent the UI from lagging or freezing with 2,000 rows?",
            "<b>I completely avoided Python 'for' loops.</b> Instead, I used Pandas vectorized C-based functions like `.groupby()` and `.sum()`. They calculate millions of records in milliseconds, so the Tkinter `mainloop()` never freezes."
        ),
        (
            "How did you build the Heatmap without using Seaborn?",
            "<b>I created a 2D matrix using Pandas `pivot_table()`, then rendered it using Matplotlib's `ax.imshow()`.</b> I even wrote a mathematical algorithm to dynamically change the text color to white or black based on the background luminance of the heatmap cell so it's always readable."
        ),
        (
            "Why did you build your own dashboard instead of using PowerBI?",
            "<b>Building this in Python proves deep algorithmic skills.</b> Drag-and-drop tools are easy. By programming this from scratch, I proved my mastery over Data Structures, Procedural UI Design, Data Aggregation, and Matplotlib canvas manipulation."
        )
    ]
    
    for q, a in qa_pairs:
        p = doc.add_paragraph()
        r1 = p.add_run("Q: " + q)
        r1.bold = True
        r1.font.color.rgb = RGBColor(192, 57, 43)
        r1.font.size = Pt(13)
        add_para(doc, "<b>Answer:</b> " + a)
        
    doc.save("Presentation_Notes_Akshat.docx")
    print("Word document created!")

    try:
        from docx2pdf import convert
        convert("Presentation_Notes_Akshat.docx", "Presentation_Notes_Akshat.pdf")
        print("PDF generated successfully!")
    except Exception as e:
        print(f"PDF auto-conversion failed: {e}")

if __name__ == '__main__':
    build_notes()
