
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                 Table, TableStyle, PageBreak, HRFlowable)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os

W, H = A4
D = "a1_plots"
NAVY   = colors.HexColor("#0F2A54")
BLUE   = colors.HexColor("#1D4ED8")
PURPLE = colors.HexColor("#6D28D9")
GREEN  = colors.HexColor("#065F46")
LIGHT  = colors.HexColor("#EFF6FF")
PLITE  = colors.HexColor("#F5F3FF")
WHITE  = colors.white
GREY   = colors.HexColor("#64748B")
RED    = colors.HexColor("#B91C1C")

def sty(name, **k):
    return ParagraphStyle(name, **k)

s_title  = sty("t",  fontName="Helvetica-Bold",   fontSize=20, textColor=WHITE,  alignment=TA_CENTER, spaceAfter=2)
s_sub    = sty("sb", fontName="Helvetica",         fontSize=9,  textColor=colors.HexColor("#CBD5E1"), alignment=TA_CENTER)
s_qh     = sty("qh", fontName="Helvetica-Bold",   fontSize=13, textColor=NAVY,   spaceBefore=10, spaceAfter=4)
s_sub2   = sty("s2", fontName="Helvetica-Bold",   fontSize=10, textColor=BLUE,   spaceBefore=6, spaceAfter=3)
s_body   = sty("bd", fontName="Helvetica",         fontSize=9,  leading=14,       spaceAfter=3)
s_result = sty("rs", fontName="Helvetica-Bold",   fontSize=9,  textColor=GREEN,  spaceAfter=4)
s_reject = sty("rj", fontName="Helvetica-Bold",   fontSize=9,  textColor=RED,    spaceAfter=4)
s_code   = sty("cd", fontName="Courier",           fontSize=7.5,leading=12,
               backColor=colors.HexColor("#1E293B"), textColor=colors.HexColor("#7DD3FC"),
               leftIndent=8, rightIndent=8, spaceBefore=3, spaceAfter=6,
               borderPadding=(5,8,5,8))
s_cap    = sty("cp", fontName="Helvetica-Oblique", fontSize=8, textColor=GREY, alignment=TA_CENTER, spaceAfter=8)
s_center = sty("cc", fontName="Helvetica",         fontSize=9, alignment=TA_CENTER, textColor=GREY)

doc = SimpleDocTemplate("akshat.pdf", pagesize=A4,
                        leftMargin=1.8*cm, rightMargin=1.8*cm,
                        topMargin=2*cm, bottomMargin=2*cm)
PW = doc.width

def HR():
    return HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#DBEAFE"),
                      spaceBefore=4, spaceAfter=6)

def img(fn, w=13.5*cm, ratio=0.52):
    p = f"{D}/{fn}"
    if os.path.exists(p):
        im = Image(p, width=w, height=w*ratio); im.hAlign='CENTER'; return im
    return Paragraph(f"[{fn}]", s_body)

def result_tbl(headers, rows, col_widths, head_color=BLUE):
    data=[headers]+rows
    t=Table(data, colWidths=col_widths)
    ts=[('BACKGROUND',(0,0),(-1,0),head_color),('TEXTCOLOR',(0,0),(-1,0),WHITE),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTNAME',(0,1),(-1,-1),'Helvetica'),
        ('FONTSIZE',(0,0),(-1,-1),8.5),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE,LIGHT]),
        ('GRID',(0,0),(-1,-1),0.5,colors.HexColor("#DBEAFE")),
        ('ALIGN',(0,0),(-1,-1),'LEFT'),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]
    t.setStyle(TableStyle(ts)); return t

def hdr(title, sub):
    t = Table([[Paragraph(title, s_title)],[Paragraph(sub, s_sub)]], colWidths=[PW])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),NAVY),
        ('TOPPADDING',(0,0),(-1,-1),12),('BOTTOMPADDING',(0,0),(-1,-1),10),
        ('LEFTPADDING',(0,0),(-1,-1),14),('RIGHTPADDING',(0,0),(-1,-1),14),
    ])); return t

def cover_page():
    inst_style = sty("inst", fontName="Helvetica-Bold", fontSize=26, textColor=NAVY, alignment=TA_CENTER, spaceAfter=0.5*cm, leading=32)
    sub_inst = sty("subinst", fontName="Helvetica", fontSize=14, textColor=GREY, alignment=TA_CENTER, spaceAfter=3.5*cm)
    
    title_style = sty("title", fontName="Helvetica-Bold", fontSize=32, textColor=BLUE, alignment=TA_CENTER, spaceAfter=1.5*cm)
    sub_title = sty("subtitle", fontName="Helvetica-Bold", fontSize=20, textColor=NAVY, alignment=TA_CENTER, spaceAfter=4*cm, leading=28)
    
    submit_head = sty("sch", fontName="Helvetica-Bold", fontSize=16, textColor=NAVY, alignment=TA_CENTER, spaceAfter=0.8*cm)
    submit_body = sty("scb", fontName="Helvetica", fontSize=16, textColor=colors.black, alignment=TA_CENTER, leading=24)

    flow = []
    flow.append(Spacer(1, 4*cm))
    flow.append(Paragraph("JAGANNATH INTERNATIONAL<br/>MANAGEMENT SCHOOL", inst_style))
    flow.append(Paragraph("Vasant Kunj, New Delhi", sub_inst))
    
    flow.append(Paragraph("Assignment 1", title_style))
    flow.append(Paragraph("Data Visualization & Analytics<br/>(BCAT 312)", sub_title))
    
    flow.append(Paragraph("Submitted By", submit_head))
    flow.append(Paragraph("<b>Akshat Tripathi</b><br/>Roll No: 04914202023", submit_body))
    
    flow.append(PageBreak())
    return flow

# ─── STORY ───────────────────────────────────────────────────
S = []

# Cover
S.extend(cover_page())

toc=[["Q.No","Topic","Dataset"],
     ["Q 1","Data Wrangling — Cleaning, Filtering, Sorting","Canada.xlsx"],
     ["Q 2","Data Preprocessing — Missing Values, Scaling, Encoding","Laptop.csv"],
     ["Q 3","Statistical Hypothesis Testing (t-test, ANOVA, Chi²)","Insurance.csv"],
     ["Q 4","Data Visualization — Line, Box, Scatter, Pie, Subplots","Canada.xlsx"]]
t=Table(toc,colWidths=[1.5*cm,10.5*cm,4*cm])
t.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0),NAVY),('TEXTCOLOR',(0,0),(-1,0),WHITE),
    ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),9),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE,LIGHT]),
    ('GRID',(0,0),(-1,-1),0.5,colors.HexColor("#DBEAFE")),
    ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
S += [Spacer(1, 1*cm), Paragraph("Table of Contents", sty("toc_title", fontName="Helvetica-Bold", fontSize=16, textColor=NAVY, spaceAfter=0.5*cm)), t, PageBreak()]

# ═══ Q1 ═══════════════════════════════════════════════════════
S += [Paragraph("Question 1 — Data Wrangling  (Canada.xlsx)", s_qh), HR()]
for h,b in [
    ("1.  Perform Data Wrangling",
     "Loaded <i>Canada.xlsx</i> (sheet: 'Canada by Citizenship', skiprows=20, skipfooter=2) using "
     "<b>pd.read_excel()</b>. Renamed key columns (OdName→Country, AreaName→Continent). "
     "Set 'Country' as DataFrame index. Final shape: <b>195 rows × 43 columns</b> "
     "(195 countries, year columns 1980–2013)."),
    ("2.  Add 'Total' Column",
     "Summed all 34 year columns (1980–2013) row-wise using <b>df[years].sum(axis=1)</b> "
     "and stored result in a new 'Total' column."),
    ("3.  Check Null Values",
     "Called <b>df.isnull().sum()</b> across all columns. "
     "<b>Result: 0 null values</b> — the dataset is completely clean with no missing entries."),
    ("4.  Highest and Lowest Immigration",
     "<b>Highest:</b> India → 691,904 total immigrants (1980–2013)<br/>"
     "<b>Lowest:</b> Palau → 1 total immigrant"),
    ("5.  Filter by 'Country' and Years 1980–1985",
     "Filtered the dataframe to include only columns: Continent, Region, years 1980–1985, and Total. "
     "Used <b>df_can[['Continent','Region',1980,1981,1982,1983,1984,1985,'Total']]</b>."),
    ("6.  Top 5 Countries by Total (Descending)",
     "Sorted the dataframe on 'Total' in descending order using <b>sort_values('Total', ascending=False).head(5)</b>.")]:
    S += [Paragraph(h, s_sub2), Paragraph(b, s_body)]

S.append(Paragraph("Python Code:", s_sub2))
S.append(Paragraph(
    "df_can = pd.read_excel('Canada.xlsx', sheet_name='Canada by Citizenship',<br/>"
    "&nbsp;&nbsp;skiprows=20, skipfooter=2)<br/>"
    "df_can.rename(columns={'OdName':'Country','AreaName':'Continent'}, inplace=True)<br/>"
    "df_can.set_index('Country', inplace=True)<br/>"
    "years = list(range(1980, 2014))<br/>"
    "df_can['Total'] = df_can[years].sum(axis=1)&nbsp;&nbsp;&nbsp;# Step 2<br/>"
    "print(df_can.isnull().sum())&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Step 3<br/>"
    "print(df_can['Total'].idxmax(), df_can['Total'].max())&nbsp;# Step 4<br/>"
    "df_filtered = df_can[['Continent','Region']+list(range(1980,1986))+['Total']]&nbsp;# Step 5<br/>"
    "top5 = df_can.sort_values('Total',ascending=False).head(5)&nbsp;# Step 6", s_code))

S += [Paragraph("Null Value Check", s_sub2), img("q1_nulls.png",w=10*cm,ratio=0.38),
      Paragraph("Figure 1: Visual confirmation — 0 null values in the Canada dataset.", s_cap)]
S += [Paragraph("Top 5 Countries by Total Immigration", s_sub2), img("q1_top5.png"),
      Paragraph("Figure 2: Top 5 countries contributing to immigration to Canada (1980–2013).", s_cap)]

S.append(result_tbl(
    ["Rank","Country","Total Immigrants"],
    [["1","India","691,904"],["2","China","659,962"],
     ["3","United Kingdom","551,500"],["4","Philippines","511,391"],["5","Pakistan","241,600"]],
    [1.5*cm,8*cm,5.5*cm]))

S += [Spacer(1,0.3*cm), Paragraph("Immigration 1980–1985 Filter — Stacked View", s_sub2),
      img("q1_filter.png"), Paragraph("Figure 3: Stacked bar showing immigration per year (1980–1985) for top 10 countries.", s_cap),
      PageBreak()]

# ═══ Q2 ═══════════════════════════════════════════════════════
S += [Paragraph("Question 2 — Data Preprocessing  (Laptop.csv)", s_qh), HR()]
for h,b in [
    ("1.  Handle Missing Data",
     "Detected <b>30 missing values each</b> in columns: Ram, Weight, Gpu.<br/>"
     "• Ram & Weight: filled with <b>median</b> (robust to outliers)<br/>"
     "• Gpu: filled with string <b>'Unknown'</b> (categorical placeholder)<br/>"
     "After imputation: <b>0 missing values</b> across all columns."),
    ("2.  Correct Data Types",
     "• <b>Inches</b>: was object → converted to <b>float64</b> using pd.to_numeric(errors='coerce')<br/>"
     "• <b>Ram</b>: was float (due to NaN) → converted to <b>int64</b> after filling<br/>"
     "• All other columns verified and already in correct types."),
    ("3.  Standardize and Normalize",
     "Applied two scaling techniques on the <b>Price</b> column:<br/>"
     "• <b>StandardScaler</b> (Z-score): transforms to mean=0, std=1<br/>"
     "• <b>MinMaxScaler</b> (Min-Max): scales to range [0, 1]<br/>"
     "Both scalers imported from <b>sklearn.preprocessing</b>."),
    ("4.  Grouped Bar Chart — Segmentation",
     "Grouped by <b>Company</b> and <b>TypeName</b>, computed mean price per segment. "
     "Plotted as a grouped bar chart showing price variation across laptop types within each brand."),
    ("5.  Encode Categorical → Numerical",
     "Used <b>LabelEncoder</b> from sklearn to convert 6 categorical columns "
     "(Company, TypeName, Cpu, Memory, Gpu, OpSys) to integer indicator variables.")]:
    S += [Paragraph(h, s_sub2), Paragraph(b, s_body)]

S.append(Paragraph("Python Code:", s_sub2))
S.append(Paragraph(
    "df['Ram'].fillna(df['Ram'].median(), inplace=True)<br/>"
    "df['Weight'].fillna(df['Weight'].median(), inplace=True)<br/>"
    "df['Gpu'].fillna('Unknown', inplace=True)<br/>"
    "df['Inches'] = pd.to_numeric(df['Inches'], errors='coerce')<br/>"
    "df['Ram'] = df['Ram'].astype(int)<br/>"
    "from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder<br/>"
    "df['Price_std']  = StandardScaler().fit_transform(df[['Price']])<br/>"
    "df['Price_norm'] = MinMaxScaler().fit_transform(df[['Price']])<br/>"
    "le = LabelEncoder()<br/>"
    "for col in ['Company','TypeName','Cpu','Memory','Gpu','OpSys']:<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;df[col+'_enc'] = le.fit_transform(df[col].astype(str))", s_code))

S += [Paragraph("Missing Values — Before vs After Imputation", s_sub2),
      img("q2_missing.png",ratio=0.38),
      Paragraph("Figure 4: Left — 30 missing in Ram/Weight/Gpu. Right — 0 missing after imputation.", s_cap)]
S += [Paragraph("Price Distribution — Original vs Standardized vs Normalized", s_sub2),
      img("q2_scaling.png",ratio=0.35),
      Paragraph("Figure 5: Price distributions after StandardScaler (Z-score) and MinMaxScaler (0–1).", s_cap)]
S += [Paragraph("Grouped Bar Chart — Price Segmentation by Company & Type", s_sub2),
      img("q2_grouped.png",ratio=0.42),
      Paragraph("Figure 6: Average laptop price grouped by Company and TypeName (Segmentation).", s_cap)]
S += [Paragraph("Label Encoding — Categorical to Numerical Indicator Variables", s_sub2),
      img("q2_encoding.png",ratio=0.42),
      Paragraph("Figure 7: Sample rows showing original categorical values mapped to integer codes.", s_cap),
      PageBreak()]

# ═══ Q3 ═══════════════════════════════════════════════════════
S += [Paragraph("Question 3 — Hypothesis Testing  (Insurance.csv)", s_qh), HR()]
S.append(Paragraph(
    "Dataset: 1,338 records with columns: age, sex, bmi, children, smoker, region, charges. "
    "All tests use significance level α = 0.05.", s_body))

tests = [
    ("1.  BMI: Male vs Female — Independent t-test",
     "H₀: No difference in BMI between males and females.<br/>"
     "Test: <b>scipy.stats.ttest_ind(male_bmi, female_bmi)</b>",
     "t = 1.697,  p = 0.0900  >  0.05",
     "FAIL TO REJECT H₀ — No significant difference in BMI between genders.", True),
    ("2.  Charges: Smokers ≤ Non-Smokers — t-test",
     "H₀: Smokers' average charges ≤ non-smokers' average charges.<br/>"
     "Test: <b>ttest_ind(smokers_charges, nonsmokers_charges)</b>",
     "t = 46.665,  p ≈ 0.000  <  0.05",
     "REJECT H₀ — Smokers pay SIGNIFICANTLY MORE ($32,050 vs $8,434 avg).", False),
    ("3.  Charges Increase with Age — Pearson Correlation",
     "H₀: No linear correlation between age and medical charges.<br/>"
     "Test: <b>scipy.stats.pearsonr(df['age'], df['charges'])</b>",
     "r = 0.299,  p ≈ 0.000  <  0.05",
     "REJECT H₀ — Significant positive correlation. Charges increase with age.", False),
    ("4.  Smoker Proportion Across Regions — Chi-square",
     "H₀: Proportion of smokers is the same across all 4 regions.<br/>"
     "Test: <b>chi2_contingency(pd.crosstab(df['region'], df['smoker']))</b>",
     "chi² = 7.344,  p = 0.0617  >  0.05",
     "FAIL TO REJECT H₀ — No significant difference in smoker proportion by region.", True),
    ("5.  BMI of Women by Children Count (0,1,2) — One-way ANOVA",
     "H₀: No difference in BMI of women with 0, 1, or 2 children.<br/>"
     "Test: <b>scipy.stats.f_oneway(bmi_0children, bmi_1child, bmi_2children)</b>",
     "F = 0.417,  p = 0.659  >  0.05",
     "FAIL TO REJECT H₀ — No significant difference in BMI by number of children.", True),
]
plot_fns = ["q3_bmi_gender.png","q3_charges_smoker.png","q3_age_charges.png","q3_region_smoker.png","q3_anova_bmi.png"]
fig_labels = [
    "Figure 8: BMI notch boxplot — Male vs Female. Overlapping notches confirm no significant difference.",
    "Figure 9: Charges boxplot — Smokers vs Non-Smokers. Smokers have dramatically higher charges.",
    "Figure 10: Scatter with regression line — positive slope confirms charges increase with age.",
    "Figure 11: Smoker % by region — proportions are similar, confirming H₀ acceptance.",
    "Figure 12: BMI by children count (ANOVA) — means nearly identical, H₀ accepted.",
]
for (h,setup,stat,conclusion,accepted), fn, cap in zip(tests, plot_fns, fig_labels):
    S += [Paragraph(h, s_sub2), Paragraph(setup, s_body),
          Paragraph(f"Result: {stat}", s_result if accepted else s_reject),
          Paragraph(f"Conclusion: {conclusion}", s_result if accepted else s_reject),
          img(fn, w=12*cm, ratio=0.55), Paragraph(cap, s_cap)]

S.append(Paragraph("Python Code — All 5 Tests:", s_sub2))
S.append(Paragraph(
    "from scipy.stats import ttest_ind, pearsonr, f_oneway, chi2_contingency<br/>"
    "# Q3.1<br/>"
    "t1,p1 = ttest_ind(df[df.sex=='male']['bmi'], df[df.sex=='female']['bmi'])<br/>"
    "# Q3.2<br/>"
    "t2,p2 = ttest_ind(df[df.smoker=='yes']['charges'], df[df.smoker=='no']['charges'])<br/>"
    "# Q3.3<br/>"
    "r,p3 = pearsonr(df['age'], df['charges'])<br/>"
    "# Q3.4<br/>"
    "chi2,p4,_,_ = chi2_contingency(pd.crosstab(df['region'],df['smoker']))<br/>"
    "# Q3.5<br/>"
    "w = df[df.sex=='female']<br/>"
    "f5,p5 = f_oneway(w[w.children==0]['bmi'], w[w.children==1]['bmi'], w[w.children==2]['bmi'])", s_code))

S.append(result_tbl(
    ["Test","Statistic","p-value","Decision"],
    [["BMI: Male vs Female (t-test)","t = 1.697","0.0900","H₀ Accepted ✓"],
     ["Smoker vs Non-Smoker Charges (t-test)","t = 46.665","≈ 0.000","H₀ Rejected ✗"],
     ["Age–Charges Correlation (Pearson r)","r = 0.299","≈ 0.000","H₀ Rejected ✗"],
     ["Smoker Proportion by Region (Chi²)","chi² = 7.344","0.0617","H₀ Accepted ✓"],
     ["BMI by Children — Women (ANOVA)","F = 0.417","0.6591","H₀ Accepted ✓"]],
    [5.5*cm,3.5*cm,2.5*cm,3.5*cm], head_color=PURPLE))
S.append(PageBreak())

# ═══ Q4 ═══════════════════════════════════════════════════════
S += [Paragraph("Question 4 — Data Visualization  (Canada.xlsx)", s_qh), HR()]

S += [Paragraph("1 & 2 & 3.  Line Plot — Customized with Markers, Grid, Legend & Axis Limits", s_sub2),
      Paragraph(
          "Plotted total annual immigrants (sum across all countries) from 1980–2013. "
          "Customized: marker style=Diamond ('D'), markersize=5, markerfacecolor='#FBBF24' (gold), "
          "line color='#2563EB', linestyle='-'. Added background grid (linestyle='--', alpha=0.5), "
          "legend, and axis limits: xlim=(1980,2013).", s_body),
      img("q4_line.png"),
      Paragraph("Figure 13: Customized line plot — immigration trend 1980–2013 with markers, grid, legend and axis limits.", s_cap)]

S += [Paragraph("1 & 2 & 3.  Box Plot — Distribution per Country per Year", s_sub2),
      Paragraph("Box plot of immigrants per country for each year. Shows median, IQR and outliers. "
                "Styled with blue fill, red median line.", s_body),
      img("q4_box.png",ratio=0.42),
      Paragraph("Figure 14: Box plot showing immigration distribution per country across years 1980–2013.", s_cap)]

S += [Paragraph("1 & 2 & 3.  Scatter Plot — Color-Coded by Volume", s_sub2),
      Paragraph("Scatter plot with colormap='plasma' to encode immigration volume. "
                "Dashed trendline added. Colorbar legend shown.", s_body),
      img("q4_scatter.png",ratio=0.48),
      Paragraph("Figure 15: Scatter plot — each point represents one year, colored by total immigration volume.", s_cap)]

S += [Paragraph("4.  Frequency Distribution — New Immigrants to Canada in 2013", s_sub2),
      Paragraph("Histogram showing how many countries sent a given number of immigrants in 2013. "
                "Most countries sent very few; a small number sent very large numbers (right-skewed). "
                "Red dashed line marks the mean.", s_body),
      img("q4_freq_2013.png",ratio=0.50),
      Paragraph("Figure 16: Frequency distribution of immigration counts per country for year 2013.", s_cap)]

S += [Paragraph("5.  Immigration: Denmark, Norway & Sweden (1980–2013)", s_sub2),
      Paragraph("Line chart comparing immigration from three Scandinavian countries. "
                "Each country uses distinct color, marker and linestyle for clear differentiation.", s_body),
      img("q4_scand.png",ratio=0.48),
      Paragraph("Figure 17: Immigration distribution for Denmark (red), Norway (amber), Sweden (green).", s_cap)]

S += [Paragraph("6.  Pie Chart — Total Immigrants by Continent", s_sub2),
      Paragraph("Aggregated 'Total' column by Continent. Asia and Europe dominate. "
                "Largest slice exploded for emphasis.", s_body),
      img("q4_pie.png",w=10*cm,ratio=0.85),
      Paragraph("Figure 18: Pie chart — proportion of total immigrants (1980–2013) by continent.", s_cap)]

S += [Paragraph("7.  Line & Scatter Subplot in One Row", s_sub2),
      Paragraph("Used <b>plt.subplots(1, 2)</b> to place line plot and scatter plot side-by-side "
                "in a single figure row. Shared y-axis. Scatter uses 'viridis' colormap.", s_body),
      img("q4_subplot.png",ratio=0.40),
      Paragraph("Figure 19: Subplots — line chart (left) and scatter plot (right) in one row.", s_cap)]

S.append(Paragraph("Python Code — Q4 Key Snippets:", s_sub2))
S.append(Paragraph(
    "total_yr = df_can[years].sum()&nbsp;&nbsp;# sum all countries per year<br/>"
    "# Line plot (Q4.1)<br/>"
    "ax.plot(years, total_yr, 'D-', color='#2563EB', markersize=5,<br/>"
    "&nbsp;&nbsp;markerfacecolor='#FBBF24', label='Total Immigrants')<br/>"
    "ax.grid(True, linestyle='--', alpha=0.5); ax.legend(); ax.set_xlim(1980,2013)<br/>"
    "# Freq distribution (Q4.4)<br/>"
    "ax.hist(df_can[2013], bins=25, cmap='plasma')<br/>"
    "# Pie chart (Q4.6)<br/>"
    "cont = df_can.groupby('Continent')['Total'].sum()<br/>"
    "ax.pie(cont, labels=cont.index, autopct='%1.1f%%', explode=[0.05,0.02,...])<br/>"
    "# Subplots (Q4.7)<br/>"
    "fig, (ax1,ax2) = plt.subplots(1,2,figsize=(14,5))<br/>"
    "ax1.plot(years, total_yr, 'D-', color='#2563EB')<br/>"
    "ax2.scatter(years, total_yr, c=total_yr, cmap='viridis', s=90)", s_code))

# Final page
S.append(PageBreak())
S += [Spacer(1,2*cm),
      hdr("Assignment 1 — Completed","All 4 Questions Answered with Code, Analysis & Visualizations"),
      Spacer(1,0.8*cm)]
S.append(result_tbl(
    ["Question","Topic","Dataset","Status"],
    [["Q 1","Data Wrangling — Cleaning, Filtering & Sorting","Canada.xlsx","Complete ✓"],
     ["Q 2","Data Preprocessing — Missing, Scaling & Encoding","Laptop.csv","Complete ✓"],
     ["Q 3","Hypothesis Testing — t-test, Chi², ANOVA","Insurance.csv","Complete ✓"],
     ["Q 4","Visualization — Line, Box, Scatter, Pie, Subplots","Canada.xlsx","Complete ✓"]],
    [1.5*cm,7.5*cm,3.5*cm,3*cm]))
S += [Spacer(1,0.8*cm),
      Paragraph("Student: Akshat Tripathi  |  Roll No: 04914202023  |  JIMS Vasant Kunj", s_center)]

doc.build(S)
print("Done — akshat.pdf")
