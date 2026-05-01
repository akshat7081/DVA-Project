
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                 Table, TableStyle, PageBreak, HRFlowable)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os

W, H = A4
PLOT_DIR = "assignment1_plots"

doc = SimpleDocTemplate(
    "akshat.pdf",
    pagesize=A4,
    leftMargin=1.8*cm, rightMargin=1.8*cm,
    topMargin=2*cm, bottomMargin=2*cm
)

styles = getSampleStyleSheet()

# ── Custom styles ─────────────────────────────────────────────
NAVY   = colors.HexColor("#1E3A5F")
BLUE   = colors.HexColor("#2563EB")
PURPLE = colors.HexColor("#7C3AED")
LIGHT  = colors.HexColor("#EFF6FF")
GREY   = colors.HexColor("#6B7280")
WHITE  = colors.white

def S(name, **kw):
    return ParagraphStyle(name, **kw)

sTitle   = S("sTitle",   fontName="Helvetica-Bold",  fontSize=18, textColor=WHITE,   alignment=TA_CENTER, spaceAfter=4)
sSubtit  = S("sSubtit",  fontName="Helvetica",        fontSize=10, textColor=WHITE,   alignment=TA_CENTER)
sQHead   = S("sQHead",   fontName="Helvetica-Bold",  fontSize=13, textColor=NAVY,    spaceBefore=14, spaceAfter=6)
sSub     = S("sSub",     fontName="Helvetica-Bold",  fontSize=10, textColor=BLUE,    spaceBefore=8, spaceAfter=4)
sBody    = S("sBody",    fontName="Helvetica",        fontSize=9,  textColor=colors.black, leading=14, spaceAfter=4)
sResult  = S("sResult",  fontName="Helvetica-Oblique",fontSize=9, textColor=PURPLE,  leading=13, spaceAfter=3)
sCode    = S("sCode",    fontName="Courier",          fontSize=8,  textColor=colors.HexColor("#1F2937"),
             backColor=colors.HexColor("#F3F4F6"), leading=12, spaceAfter=6,
             leftIndent=10, rightIndent=10, borderPadding=(4,6,4,6))
sCap     = S("sCap",     fontName="Helvetica-Oblique",fontSize=8, textColor=GREY, alignment=TA_CENTER, spaceAfter=8)

def img(path, w=14*cm):
    if os.path.exists(path):
        im = Image(path, width=w, height=w*0.52)
        im.hAlign = 'CENTER'
        return im
    return Paragraph(f"[Image not found: {path}]", sBody)

def divider():
    return HRFlowable(width="100%", thickness=1, color=colors.HexColor("#DBEAFE"), spaceAfter=6, spaceBefore=6)

def header_block(title, subtitle):
    data = [[Paragraph(title, sTitle)], [Paragraph(subtitle, sSubtit)]]
    t = Table(data, colWidths=[doc.width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), NAVY),
        ('ROWBACKGROUNDS',(0,0),(-1,-1),[NAVY, NAVY]),
        ('TOPPADDING',(0,0),(-1,-1),10),
        ('BOTTOMPADDING',(0,0),(-1,-1),10),
        ('LEFTPADDING',(0,0),(-1,-1),16),
        ('RIGHTPADDING',(0,0),(-1,-1),16),
    ]))
    return t

def info_table():
    data = [
        ["Student Name", "Akshat Tripathi", "Course", "Data Visualization & Analytics"],
        ["Roll Number",  "12314934",        "Subject Code", "BCAT 312"],
        ["Session",      "2024-25",          "Institute", "JIMS, Vasant Kunj"],
    ]
    t = Table(data, colWidths=[3.5*cm, 5.5*cm, 3.5*cm, 5.5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(0,-1), LIGHT),
        ('BACKGROUND',(2,0),(2,-1), LIGHT),
        ('FONTNAME',(0,0),(0,-1),'Helvetica-Bold'),
        ('FONTNAME',(2,0),(2,-1),'Helvetica-Bold'),
        ('FONTSIZE',(0,0),(-1,-1),8.5),
        ('TEXTCOLOR',(0,0),(-1,-1),NAVY),
        ('GRID',(0,0),(-1,-1),0.5,colors.HexColor("#BFDBFE")),
        ('TOPPADDING',(0,0),(-1,-1),5),
        ('BOTTOMPADDING',(0,0),(-1,-1),5),
    ]))
    return t

# ═══════════════════════════════════════════════════════════════
story = []

# ── COVER PAGE ─────────────────────────────────────────────────
story.append(Spacer(1, 1.5*cm))
story.append(header_block(
    "DVA Assignment 1 — Data Visualization & Analytics",
    "Jagannath International Management School | BCAT 312 | 2024-25"
))
story.append(Spacer(1, 0.5*cm))
story.append(info_table())
story.append(Spacer(1, 0.4*cm))
story.append(divider())

toc_data = [
    ["Q.No", "Topic", "Dataset"],
    ["Q1", "Data Wrangling — Cleaning, Filtering & Sorting", "Canada.xlsx"],
    ["Q2", "Data Preprocessing — Missing Values, Scaling & Encoding", "Laptop.csv"],
    ["Q3", "Statistical Hypothesis Testing (t-test, ANOVA, Chi-square)", "Insurance.csv"],
    ["Q4", "Data Visualization — Line, Box, Scatter, Pie & Subplots", "Canada.xlsx"],
]
toc = Table(toc_data, colWidths=[1.5*cm, 10.5*cm, 4*cm])
toc.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0), NAVY),
    ('TEXTCOLOR',(0,0),(-1,0), WHITE),
    ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
    ('FONTNAME',(0,1),(-1,-1),'Helvetica'),
    ('FONTSIZE',(0,0),(-1,-1),9),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE, LIGHT]),
    ('GRID',(0,0),(-1,-1),0.5,colors.HexColor("#DBEAFE")),
    ('ALIGN',(0,0),(-1,-1),'LEFT'),
    ('TOPPADDING',(0,0),(-1,-1),5),
    ('BOTTOMPADDING',(0,0),(-1,-1),5),
]))
story.append(toc)
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# Q1 — Canada Data Wrangling
# ═══════════════════════════════════════════════════════════════
story.append(Paragraph("Question 1 — Data Wrangling (Canada.xlsx)", sQHead))
story.append(divider())

tasks = [
    ("1. Perform Data Wrangling",
     "Loaded the Canada immigration dataset using pandas read_excel(). Set 'Country' as index. "
     "Verified shape: (195, 43) — 195 countries, year columns from 1980–2013."),
    ("2. Add 'Total' Column",
     "Summed all year columns (1980–2013) row-wise to compute total immigrants per country."),
    ("3. Check Null Values",
     "Used df.isnull().sum() — Result: 0 null values across all columns."),
    ("4. Highest & Lowest Immigration",
     "Highest: India → 691,904 immigrants | Lowest: Palau → 1 immigrant"),
    ("5. Filter by Country & Years 1980–1985",
     "Selected columns: ['Continent','Region', 1980–1985, 'Total'] to create filtered view."),
    ("6. Top 5 Countries by Total (Descending)",
     "Sorted on 'Total' descending. Top 5: India (691,904), China (659,962), "
     "United Kingdom (551,500), Philippines (511,391), Pakistan (241,600)."),
]
for title, body in tasks:
    story.append(Paragraph(title, sSub))
    story.append(Paragraph(body, sBody))

story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("Code Snippet:", sSub))
story.append(Paragraph(
    "df_can = pd.read_excel('Canada.xlsx', sheet_name='Canada by Citizenship', skiprows=20, skipfooter=2)<br/>"
    "df_can.set_index('OdName', inplace=True)<br/>"
    "years = list(range(1980, 2014))<br/>"
    "df_can['Total'] = df_can[years].sum(axis=1)<br/>"
    "print(df_can.isnull().sum())<br/>"
    "print(df_can['Total'].idxmax(), df_can['Total'].max())<br/>"
    "top5 = df_can.sort_values('Total', ascending=False).head(5)",
    sCode))

story.append(Paragraph("Output Visualization — Top 5 Contributing Countries", sSub))
story.append(img(f"{PLOT_DIR}/q1_top5_countries.png", w=14*cm))
story.append(Paragraph("Figure 1: Horizontal bar chart showing top 5 countries by total immigration to Canada (1980–2013).", sCap))

# Results table
res_data = [
    ["Country", "Total Immigrants"],
    ["India", "691,904"],
    ["China", "659,962"],
    ["United Kingdom", "551,500"],
    ["Philippines", "511,391"],
    ["Pakistan", "241,600"],
]
rt = Table(res_data, colWidths=[8*cm, 5*cm])
rt.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0), BLUE),
    ('TEXTCOLOR',(0,0),(-1,0), WHITE),
    ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
    ('FONTNAME',(0,1),(-1,-1),'Helvetica'),
    ('FONTSIZE',(0,0),(-1,-1),9),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE, LIGHT]),
    ('GRID',(0,0),(-1,-1),0.5,colors.HexColor("#DBEAFE")),
    ('ALIGN',(1,0),(-1,-1),'CENTER'),
    ('TOPPADDING',(0,0),(-1,-1),5), ('BOTTOMPADDING',(0,0),(-1,-1),5),
]))
story.append(rt)
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# Q2 — Laptop Data Preprocessing
# ═══════════════════════════════════════════════════════════════
story.append(Paragraph("Question 2 — Data Preprocessing (Laptop.csv)", sQHead))
story.append(divider())

q2tasks = [
    ("1. Handle Missing Data",
     "Detected 30 missing values each in Ram, Weight, and Gpu columns. "
     "Filled Ram and Weight with median values; Gpu filled with 'Unknown'. After filling: 0 nulls."),
    ("2. Correct Data Types",
     "Inches column was object type; converted to float64 using pd.to_numeric(). "
     "Ram converted to int after filling. All columns now have appropriate types."),
    ("3. Standardize & Normalize",
     "Applied StandardScaler (Z-score) and MinMaxScaler (0–1 range) on the Price column. "
     "Standardized mean ≈ 0, std ≈ 1. Normalized range: [0, 1]."),
    ("4. Grouped Bar Chart — Segmentation by Company & Type",
     "Plotted average price grouped by Company and TypeName for top 6 companies using a grouped bar chart."),
    ("5. Categorical Encoding",
     "Applied LabelEncoder on Company, TypeName, Cpu, Memory, Gpu, OpSys to convert to numerical indicator variables."),
]
for title, body in q2tasks:
    story.append(Paragraph(title, sSub))
    story.append(Paragraph(body, sBody))

story.append(Paragraph("Code Snippet:", sSub))
story.append(Paragraph(
    "df_lap['Ram'].fillna(df_lap['Ram'].median(), inplace=True)<br/>"
    "df_lap['Inches'] = pd.to_numeric(df_lap['Inches'], errors='coerce')<br/>"
    "from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder<br/>"
    "df_lap['Price_std'] = StandardScaler().fit_transform(df_lap[['Price']])<br/>"
    "df_lap['Price_norm'] = MinMaxScaler().fit_transform(df_lap[['Price']])<br/>"
    "le = LabelEncoder()<br/>"
    "for col in ['Company','TypeName','Cpu','Gpu','OpSys']:<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;df_lap[col+'_enc'] = le.fit_transform(df_lap[col])",
    sCode))

story.append(Paragraph("Grouped Bar Chart — Average Price by Company & Type", sSub))
story.append(img(f"{PLOT_DIR}/q2_grouped_bar.png", w=15*cm))
story.append(Paragraph("Figure 2: Segmented grouped bar chart showing average laptop price by company and type.", sCap))

story.append(Paragraph("Key Results:", sSub))
story.append(Paragraph("• Missing values: 30 each in Ram, Weight, Gpu — all filled successfully.", sBody))
story.append(Paragraph("• Inches dtype: object → float64 | Ram: float → int", sBody))
story.append(Paragraph("• Price standardized mean ≈ 0.0 | Price normalized range: [0.0, 1.0]", sBody))
story.append(Paragraph("• 6 categorical columns encoded to numerical indicator variables.", sBody))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# Q3 — Insurance Hypothesis Testing
# ═══════════════════════════════════════════════════════════════
story.append(Paragraph("Question 3 — Hypothesis Testing (Insurance.csv)", sQHead))
story.append(divider())

hyp_tasks = [
    ("1. BMI: Male vs Female — Independent t-test",
     "H0: No difference in BMI between males and females.\n"
     "Result: t = 1.6968, p = 0.0900 > 0.05 → Fail to reject H0. "
     "No statistically significant difference in BMI between genders."),
    ("2. Charges: Smokers <= Non-smokers — t-test",
     "H0: Smokers' charges are less than or equal to non-smokers'.\n"
     "Result: t = 46.665, p ≈ 0.000 → Reject H0. "
     "Smokers pay significantly MORE in medical charges than non-smokers."),
    ("3. Charges Increase with Age — Pearson Correlation",
     "H0: No correlation between age and charges.\n"
     "Result: r = 0.2990, p ≈ 0.000 → Reject H0. "
     "Positive correlation confirmed — charges increase with age."),
    ("4. Smoker Proportion Across Regions — Chi-square Test",
     "H0: Proportion of smokers is the same across all regions.\n"
     "Result: chi2 = 7.3435, p = 0.0617 > 0.05 → Fail to reject H0. "
     "No significant difference in smoker proportion across regions."),
    ("5. BMI by Children Count (0, 1, 2) — One-way ANOVA",
     "H0: No difference in BMI among women with 0, 1, or 2 children.\n"
     "Result: F = 0.4170, p = 0.6591 > 0.05 → Fail to reject H0. "
     "No significant difference in BMI by number of children."),
]
for title, body in hyp_tasks:
    story.append(Paragraph(title, sSub))
    story.append(Paragraph(body.replace('\n','<br/>'), sBody))

story.append(Paragraph("Code Snippet:", sSub))
story.append(Paragraph(
    "from scipy.stats import ttest_ind, f_oneway, pearsonr<br/>"
    "from scipy.stats import chi2_contingency<br/>"
    "# 1. BMI t-test<br/>"
    "t1,p1 = ttest_ind(df[df.sex=='male']['bmi'], df[df.sex=='female']['bmi'])<br/>"
    "# 2. Charges t-test<br/>"
    "t2,p2 = ttest_ind(df[df.smoker=='yes']['charges'], df[df.smoker=='no']['charges'])<br/>"
    "# 3. Pearson r<br/>"
    "r,p3 = pearsonr(df['age'], df['charges'])<br/>"
    "# 4. Chi-square<br/>"
    "ct = pd.crosstab(df['region'], df['smoker'])<br/>"
    "chi2,p4,_,_ = chi2_contingency(ct)<br/>"
    "# 5. ANOVA<br/>"
    "f5,p5 = f_oneway(df[df.children==0]['bmi'], df[df.children==1]['bmi'], df[df.children==2]['bmi'])",
    sCode))

story.append(img(f"{PLOT_DIR}/q3_hypothesis.png", w=15*cm))
story.append(Paragraph("Figure 3: (Left) BMI boxplot by gender; (Center) Charges vs Age scatter; (Right) BMI by children ANOVA.", sCap))

# Summary table
sum_data = [
    ["Test", "Statistic", "p-value", "Decision"],
    ["BMI Male vs Female (t-test)", "t = 1.697", "0.090", "H0 Accepted"],
    ["Smoker vs Non-smoker Charges (t-test)", "t = 46.665", "≈ 0.000", "H0 Rejected"],
    ["Age–Charges Correlation (Pearson)", "r = 0.299", "≈ 0.000", "H0 Rejected"],
    ["Smoker Proportion by Region (Chi2)", "chi2 = 7.344", "0.062", "H0 Accepted"],
    ["BMI by Children (ANOVA)", "F = 0.417", "0.659", "H0 Accepted"],
]
st = Table(sum_data, colWidths=[6*cm, 3.5*cm, 2.5*cm, 3*cm])
st.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0), PURPLE),
    ('TEXTCOLOR',(0,0),(-1,0), WHITE),
    ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
    ('FONTNAME',(0,1),(-1,-1),'Helvetica'),
    ('FONTSIZE',(0,0),(-1,-1),8.5),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE, colors.HexColor("#F5F3FF")]),
    ('GRID',(0,0),(-1,-1),0.5,colors.HexColor("#DDD6FE")),
    ('ALIGN',(1,0),(-1,-1),'CENTER'),
    ('TOPPADDING',(0,0),(-1,-1),5), ('BOTTOMPADDING',(0,0),(-1,-1),5),
]))
story.append(st)
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# Q4 — Canada Visualization
# ═══════════════════════════════════════════════════════════════
story.append(Paragraph("Question 4 — Data Visualization (Canada.xlsx)", sQHead))
story.append(divider())

story.append(Paragraph("1. Line Plot, Box Plot & Scatter Plot — Immigration Trend 1980–2013", sSub))
story.append(Paragraph(
    "Created three types of plots to visualize Canadian immigration trends from 1980 to 2013. "
    "The line plot shows the annual trend; the box plot shows year-wise distribution across countries; "
    "the scatter plot uses a color gradient to represent time progression.", sBody))

story.append(img(f"{PLOT_DIR}/q4_line.png", w=14*cm))
story.append(Paragraph("Figure 4a: Line plot — total annual immigrants to Canada (1980–2013).", sCap))

story.append(img(f"{PLOT_DIR}/q4_box.png", w=14*cm))
story.append(Paragraph("Figure 4b: Box plot — distribution of immigrants per country for selected years.", sCap))

story.append(img(f"{PLOT_DIR}/q4_scatter.png", w=14*cm))
story.append(Paragraph("Figure 4c: Scatter plot — immigration trend with color-coded year index.", sCap))

story.append(Paragraph("2 & 3. Marker Size, Color, Line Style & Grid/Legend/Axis Limits", sSub))
story.append(Paragraph(
    "Customized plots: marker style (circle 'o'), size=5, FBBF24 gold fill; line color #2563EB; "
    "dashed gridlines (alpha=0.5); legend shown; x-axis limited to [1980, 2013].", sBody))

story.append(Paragraph("4. Frequency Distribution — Immigrants from Various Countries to Canada in 2013", sSub))
story.append(img(f"{PLOT_DIR}/q4_freq_2013.png", w=14*cm))
story.append(Paragraph("Figure 5: Histogram of immigrant counts per country for year 2013.", sCap))

story.append(Paragraph("5. Denmark, Norway & Sweden Immigration Distribution (1980–2013)", sSub))
story.append(img(f"{PLOT_DIR}/q4_scand.png", w=14*cm))
story.append(Paragraph("Figure 6: Line chart comparing immigration from Denmark, Norway, and Sweden.", sCap))

story.append(Paragraph("6. Pie Chart — Total Immigrants by Continent", sSub))
story.append(img(f"{PLOT_DIR}/q4_pie.png", w=12*cm))
story.append(Paragraph("Figure 7: Pie chart showing proportion of total immigrants by continent (1980–2013).", sCap))

story.append(Paragraph("7. Line & Scatter Subplot in One Row", sSub))
story.append(img(f"{PLOT_DIR}/q4_subplot.png", w=15*cm))
story.append(Paragraph("Figure 8: Side-by-side subplots — line chart and scatter plot in one row using matplotlib subplots.", sCap))

story.append(Paragraph("Code Snippet:", sSub))
story.append(Paragraph(
    "# Line + Scatter subplot<br/>"
    "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14,5))<br/>"
    "ax1.plot(years, total_year, 'o-', color='#2563EB', linewidth=2.5)<br/>"
    "ax1.grid(True, linestyle='--', alpha=0.5)<br/>"
    "ax2.scatter(years, total_year, c=range(len(years)), cmap='plasma', s=80)<br/>"
    "plt.tight_layout(); plt.savefig('q4_subplot.png', dpi=150)",
    sCode))

# Final page
story.append(PageBreak())
story.append(Spacer(1, 3*cm))
story.append(header_block("Assignment 1 — Completed", "All Questions Answered | DVA BCAT 312"))
story.append(Spacer(1, 1*cm))

final_data = [
    ["Question", "Topic", "Status"],
    ["Q1", "Data Wrangling — Canada Immigration Dataset", "Complete"],
    ["Q2", "Data Preprocessing — Laptop Dataset", "Complete"],
    ["Q3", "Hypothesis Testing — Insurance Dataset", "Complete"],
    ["Q4", "Data Visualization — Canada Immigration", "Complete"],
]
ft = Table(final_data, colWidths=[2*cm, 10*cm, 4*cm])
ft.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0), NAVY),
    ('TEXTCOLOR',(0,0),(-1,0), WHITE),
    ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
    ('FONTNAME',(0,1),(-1,-1),'Helvetica'),
    ('FONTSIZE',(0,0),(-1,-1),10),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE, LIGHT]),
    ('GRID',(0,0),(-1,-1),0.5,colors.HexColor("#BFDBFE")),
    ('ALIGN',(2,0),(-1,-1),'CENTER'),
    ('TEXTCOLOR',(2,1),(-1,-1), colors.HexColor("#059669")),
    ('FONTNAME',(2,1),(-1,-1),'Helvetica-Bold'),
    ('TOPPADDING',(0,0),(-1,-1),7), ('BOTTOMPADDING',(0,0),(-1,-1),7),
]))
story.append(ft)
story.append(Spacer(1, 1*cm))
story.append(Paragraph("Student: Akshat Tripathi | Roll: 12314934 | JIMS Vasant Kunj | 2024-25", 
                        S("sc", fontName="Helvetica", fontSize=9, textColor=GREY, alignment=TA_CENTER)))

doc.build(story)
print("PDF saved as akshat.pdf")
