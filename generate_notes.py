from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

def add_header(doc, text, level=1):
    p = doc.add_paragraph()
    run = p.add_run(text)
    if level == 1:
        run.font.size = Pt(18)
        run.bold = True
        run.font.color.rgb = RGBColor(75, 0, 130) # Dark Purple
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif level == 2:
        run.font.size = Pt(14)
        run.bold = True
        run.font.color.rgb = RGBColor(0, 51, 102)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.space_before = Pt(12)

def add_para(doc, text, bold_words=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    
    if bold_words:
        # Simple splitting for bold words if needed, but for simplicity we'll just format manually below
        pass
    
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(11)

def add_bullet(doc, text, bold_prefix=""):
    p = doc.add_paragraph(style='List Bullet')
    if bold_prefix:
        r1 = p.add_run(bold_prefix)
        r1.bold = True
        r2 = p.add_run(" " + text)
    else:
        p.add_run(text)
    p.paragraph_format.space_after = Pt(4)

def build_notes():
    doc = Document()
    
    # Set margins
    for section in doc.sections:
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(2.0)
        section.right_margin = Cm(2.0)
        
    add_header(doc, "Presentation & Viva Notes", 1)
    add_header(doc, "Social Media Trends Analytics Dashboard", 1)
    
    add_para(doc, "Use these notes to explain your project in simple English during your presentation. It covers what you built, how it works, and the most common questions your teacher might ask.")
    
    add_header(doc, "1. Project Introduction (How to Start)", 2)
    add_para(doc, "Start your presentation by saying:")
    add_para(doc, "\"Good morning/afternoon. My project is a Desktop Dashboard for analyzing Social Media Trends. Today, businesses need to know where to post their content (like Twitter or Instagram) and what topics are trending. I built a Python application that reads 2000 records of social media data and turns it into beautiful, easy-to-understand charts.\"")
    
    add_header(doc, "2. Explaining the Technologies Used", 2)
    add_bullet(doc, "Used to load, clean, and group the data very quickly.", "Pandas:")
    add_bullet(doc, "Used to draw the actual graphs (bar charts, pie charts, heatmaps).", "Matplotlib:")
    add_bullet(doc, "Used to build the Desktop Window (GUI) so the user can click tabs and see the data without looking at code.", "Tkinter:")
    
    add_header(doc, "3. Explaining the Visualizations (Page by Page)", 2)
    
    add_bullet(doc, "Shows the 'Big Picture'. We have Key Performance Indicators (KPIs) showing total views and likes. The Donut Chart shows which categories have the most posts. The charts prove which platform gets the most traffic overall.", "Page 1 - Overview:")
    
    add_bullet(doc, "Here, I compare platforms side-by-side. You can easily see if Instagram gets more likes than TikTok. It helps businesses decide where to spend their marketing budget.", "Page 2 - Platform Analysis:")
    
    add_bullet(doc, "This tells us WHAT people want to see. Are they watching Sports or Tech? The bar charts rank the categories by engagement.", "Page 3 - Category Trends:")
    
    add_bullet(doc, "I made a scrollable table and two charts showing the absolute best and worst hashtags. This tells us what words to use in a post to go viral.", "Page 4 - Hashtag Rankings:")
    
    add_bullet(doc, "This is the most advanced chart. It compares two things at once (Platform vs Category). Dark colors mean 'Hot/High Engagement', light colors mean 'Cold/Low'. For example, if Gaming on YouTube is dark colored, it means that's a perfect match.", "Page 5 - Heatmap:")
    
    doc.add_page_break()
    
    add_header(doc, "4. Frequently Asked Questions (Viva Q&A)", 2)
    
    p = doc.add_paragraph()
    p.add_run("Q: Why did you use Tkinter and not a website framework like HTML/Django?").bold = True
    add_para(doc, "Answer: I wanted to build a standalone desktop application. Tkinter is built right into Python and connects very smoothly with Matplotlib to embed graphs directly into the window without needing a browser.")
    
    p = doc.add_paragraph()
    p.add_run("Q: How did you handle the large amount of data?").bold = True
    add_para(doc, "Answer: I used Pandas DataFrames. Instead of using slow 'for' loops, I used Pandas built-in functions like '.groupby()' and '.sum()' which are optimized in C and calculate the totals instantly.")
    
    p = doc.add_paragraph()
    p.add_run("Q: What is 'Engagement Rate' and how did you calculate it?").bold = True
    add_para(doc, "Answer: Engagement Rate is the percentage of people who actually liked, commented, or shared after seeing the post, not just scrolling past it. It shows the true quality of the content.")
    
    p = doc.add_paragraph()
    p.add_run("Q: Why did you choose the dark 'Midnight Purple' theme?").bold = True
    add_para(doc, "Answer: Dark mode is an industry standard for professional analytics dashboards (like Bloomberg or Grafana). It reduces eye strain, makes the bright colors of the charts pop out, and looks highly premium.")
    
    p = doc.add_paragraph()
    p.add_run("Q: What is the Heatmap showing exactly?").bold = True
    add_para(doc, "Answer: The Heatmap is a 2D matrix. It answers complex questions like 'Does Fashion content perform better on Instagram or Twitter?'. The color intensity gives the answer instantly without looking at raw numbers.")
    
    add_header(doc, "5. Conclusion (How to End)", 2)
    add_para(doc, "End your presentation by saying:")
    add_para(doc, "\"To conclude, this dashboard successfully transforms raw, boring CSV data into actionable business intelligence. It proves my skills in data wrangling, statistical grouping, and advanced GUI development in Python. Thank you.\"")

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
