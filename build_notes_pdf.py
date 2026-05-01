
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable)
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def create_notes():
    doc = SimpleDocTemplate("viva_notes.pdf", pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    S = []

    # Styles
    title_sty = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=24, textColor=colors.HexColor("#1D4ED8"), alignment=TA_CENTER, spaceAfter=0.5*cm)
    sub_title = ParagraphStyle("sub", fontName="Helvetica", fontSize=14, textColor=colors.HexColor("#64748B"), alignment=TA_CENTER, spaceAfter=1.5*cm)
    h1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=16, textColor=colors.HexColor("#0F2A54"), spaceBefore=0.8*cm, spaceAfter=0.3*cm)
    h2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=12, textColor=colors.HexColor("#1D4ED8"), spaceBefore=0.5*cm, spaceAfter=0.2*cm)
    body = ParagraphStyle("body", fontName="Helvetica", fontSize=10, leading=15, spaceAfter=0.3*cm)
    bullet = ParagraphStyle("bullet", fontName="Helvetica", fontSize=10, leading=15, leftIndent=15, spaceAfter=0.1*cm)

    def hr(): return HRFlowable(width="100%", thickness=1, color=colors.HexColor("#DBEAFE"), spaceBefore=10, spaceAfter=10)

    S.append(Paragraph("DVA Assignment 1: Viva & Concept Notes", title_sty))
    S.append(Paragraph("A quick overview of concepts for teacher questions", sub_title))
    S.append(hr())

    # Topic 1: Data Wrangling
    S.append(Paragraph("Topic 1: Data Wrangling (Canada Dataset)", h1))
    S.append(Paragraph("<b>Q: What is Data Wrangling?</b>", h2))
    S.append(Paragraph("Data wrangling is the process of cleaning, structuring, and enriching raw data into a desired format for better decision making. In this assignment, we manipulated rows/columns to extract meaningful insights.", body))
    S.append(Paragraph("<b>Key Actions Taken:</b>", h2))
    S.append(Paragraph("• Added a 'Total' column by summing immigrants from 1980 to 2013.", bullet))
    S.append(Paragraph("• Checked for Null Values (found 0 missing values).", bullet))
    S.append(Paragraph("• Sorted data to find the Top 5 countries (India, China, UK, Philippines, Pakistan).", bullet))
    
    # Topic 2: Data Preprocessing
    S.append(Paragraph("Topic 2: Data Preprocessing (Laptop Dataset)", h1))
    S.append(Paragraph("<b>Q: How did you handle missing data?</b>", h2))
    S.append(Paragraph("We had missing values in RAM, Weight, and GPU. For RAM and Weight (numerical), we used the <b>Median</b> instead of Mean because Median is robust and not affected by extreme outliers. For GPU (categorical), we filled missing data with the placeholder 'Unknown'.", body))
    
    S.append(Paragraph("<b>Q: What is the difference between Standardization and Normalization?</b>", h2))
    S.append(Paragraph("• <b>Standardization (Z-score):</b> Transforms data to have a mean of 0 and standard deviation of 1. Good for algorithms that assume Gaussian (normal) distribution.", bullet))
    S.append(Paragraph("• <b>Normalization (Min-Max Scaling):</b> Compresses data into a fixed range, usually between 0 and 1. Good when the data doesn't follow a normal distribution.", bullet))
    
    S.append(Paragraph("<b>Q: What is Label Encoding?</b>", h2))
    S.append(Paragraph("Machine learning models cannot read text. Label Encoding converts categorical text data (like Company names 'Dell', 'HP') into numerical values (like 0, 1).", body))

    S.append(PageBreak())

    # Topic 3: Hypothesis Testing
    S.append(Paragraph("Topic 3: Hypothesis Testing (Insurance Dataset)", h1))
    S.append(Paragraph("<b>Q: What does a p-value mean?</b>", h2))
    S.append(Paragraph("The p-value tells us if our result is statistically significant. If <b>p-value < 0.05</b>, we Reject the Null Hypothesis (H₀). If <b>p-value > 0.05</b>, we Accept the Null Hypothesis.", body))
    
    S.append(Paragraph("<b>Q: Explain the different Statistical Tests used.</b>", h2))
    S.append(Paragraph("<b>1. T-Test:</b> Used to compare the means of exactly TWO groups.", bullet))
    S.append(Paragraph("- Example: Comparing BMI of Males vs Females. (Result: No difference, p > 0.05)", bullet))
    S.append(Paragraph("- Example: Comparing Medical Charges of Smokers vs Non-smokers. (Result: Smokers pay more, p < 0.05)", bullet))
    
    S.append(Paragraph("<b>2. Pearson Correlation:</b> Used to check the linear relationship between two continuous variables.", bullet))
    S.append(Paragraph("- Example: Age vs Charges. As age increases, do charges increase? (Result: Yes, positive correlation, p < 0.05)", bullet))
    
    S.append(Paragraph("<b>3. Chi-Square Test:</b> Used to check relationship between two CATEGORICAL variables.", bullet))
    S.append(Paragraph("- Example: Region vs Smoking Habit. Are some regions more likely to smoke? (Result: No, independent, p > 0.05)", bullet))
    
    S.append(Paragraph("<b>4. ANOVA (Analysis of Variance):</b> Used to compare the means of THREE OR MORE groups.", bullet))
    S.append(Paragraph("- Example: Comparing BMI among women with 0, 1, or 2 children. (Result: No significant difference, p > 0.05)", bullet))

    S.append(hr())

    # Topic 4: Data Visualization
    S.append(Paragraph("Topic 4: Data Visualization Concepts", h1))
    S.append(Paragraph("<b>Q: When do you use different types of plots?</b>", h2))
    S.append(Paragraph("• <b>Line Plot:</b> Best for showing trends over time (e.g., immigration from 1980-2013).", bullet))
    S.append(Paragraph("• <b>Box Plot:</b> Best for showing data distribution, quartiles, and identifying outliers.", bullet))
    S.append(Paragraph("• <b>Scatter Plot:</b> Best for showing the relationship or correlation between two numerical variables.", bullet))
    S.append(Paragraph("• <b>Histogram:</b> Best for showing frequency distributions (e.g., how many countries sent X number of immigrants).", bullet))
    S.append(Paragraph("• <b>Grouped Bar Chart:</b> Best for comparing sub-categories across main categories (Segmentation).", bullet))

    S.append(Spacer(1, 1*cm))
    S.append(Paragraph("<i>End of Notes - Best of luck for the submission and viva!</i>", ParagraphStyle("end", fontName="Helvetica-Oblique", fontSize=11, textColor=colors.HexColor("#64748B"), alignment=TA_CENTER)))

    doc.build(S)
    print("viva_notes.pdf created successfully.")

if __name__ == "__main__":
    create_notes()
