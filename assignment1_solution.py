
# ============================================================
# DVA Assignment 1 - Complete Solution
# Student: Akshat Tripathi
# ============================================================
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from scipy import stats
from scipy.stats import f_oneway, chi2_contingency, ttest_ind
import warnings
import os
warnings.filterwarnings('ignore')

OUTPUT_DIR = "assignment1_plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── load Canada ────────────────────────────────────────────
df_can = pd.read_excel(
    'Canada.xlsx',
    sheet_name='Canada by Citizenship',
    skiprows=20, skipfooter=2
)
df_can.rename(columns={'OdName': 'Country', 'AreaName': 'Continent',
                        'RegName': 'Region', 'DevName': 'DevStatus'}, inplace=True)
df_can.set_index('Country', inplace=True)
years = list(range(1980, 2014))

# ─── load Insurance ─────────────────────────────────────────
df_ins = pd.read_csv('Insurance.csv')

# ─── load Laptop ────────────────────────────────────────────
df_lap = pd.read_csv('Laptop.csv')

plot_files = {}  # store paths keyed by label

# ============================================================
# QUESTION 1 — Canada.csv (Data Wrangling)
# ============================================================
print("\n===== Q1: Data Wrangling — Canada =====")

# 1. Data Wrangling overview
print(df_can.head(3))

# 2. Total column
df_can['Total'] = df_can[years].sum(axis=1)
print("\nTotal column added. Sample:\n", df_can[['Total']].head(5))

# 3. Null values
print("\nNull values per column:\n", df_can.isnull().sum())

# 4. Highest and Lowest immigration
print("\nHighest Total Immigration:", df_can['Total'].idxmax(), "->", df_can['Total'].max())
print("Lowest  Total Immigration:", df_can['Total'].idxmin(), "->", df_can['Total'].min())

# 5. Filter Country column & years 1980-1985
cols_1980_85 = ['Continent', 'Region'] + list(range(1980, 1986)) + ['Total']
df_filtered = df_can[cols_1980_85].copy()
print("\nFiltered (1980-1985):\n", df_filtered.head(5))

# 6. Top 5 countries by Total (descending)
top5 = df_can.sort_values('Total', ascending=False).head(5)[['Total']]
print("\nTop 5 countries contributing to Canada:\n", top5)

# Plot Q1 — Top 5 bar chart
fig, ax = plt.subplots(figsize=(9, 5))
colors = ['#2563EB', '#7C3AED', '#DB2777', '#D97706', '#059669']
ax.barh(top5.index, top5['Total'], color=colors, edgecolor='white')
ax.set_xlabel('Total Immigrants (1980-2013)', fontsize=11)
ax.set_title('Q1: Top 5 Countries by Total Immigration to Canada (1980–2013)', fontsize=12, fontweight='bold')
for i, (val, name) in enumerate(zip(top5['Total'], top5.index)):
    ax.text(val + 500, i, f'{val:,}', va='center', fontsize=9)
ax.invert_yaxis()
plt.tight_layout()
p = f"{OUTPUT_DIR}/q1_top5_countries.png"
plt.savefig(p, dpi=150, bbox_inches='tight')
plt.close()
plot_files['q1_top5'] = p
print("Saved:", p)

# ============================================================
# QUESTION 2 — Laptop.csv (Data Preprocessing)
# ============================================================
print("\n===== Q2: Laptop Data Preprocessing =====")

# 1. Handle missing data
print("Missing before:\n", df_lap.isnull().sum())
df_lap['Ram'].fillna(df_lap['Ram'].median(), inplace=True)
df_lap['Weight'].fillna(df_lap['Weight'].median(), inplace=True)
df_lap['Gpu'].fillna('Unknown', inplace=True)
print("Missing after:\n", df_lap.isnull().sum())

# 2. Correct data types
df_lap['Inches'] = pd.to_numeric(df_lap['Inches'], errors='coerce')
df_lap['Ram'] = df_lap['Ram'].astype(int)
print("\nDtypes after correction:\n", df_lap.dtypes)

# 3. Standardize & Normalize
from sklearn.preprocessing import StandardScaler, MinMaxScaler
scaler_std = StandardScaler()
scaler_mm  = MinMaxScaler()
df_lap['Price_standardized'] = scaler_std.fit_transform(df_lap[['Price']])
df_lap['Price_normalized']   = scaler_mm.fit_transform(df_lap[['Price']])
print("\nStandardized/Normalized Price sample:\n",
      df_lap[['Price','Price_standardized','Price_normalized']].head(5))

# 4. Grouped bar chart — Price by Company & TypeName (Segmentation)
seg = df_lap.groupby(['Company','TypeName'])['Price'].mean().unstack(fill_value=0)
# keep top 6 companies by count
top6 = df_lap['Company'].value_counts().head(6).index
seg = seg.loc[top6]

fig, ax = plt.subplots(figsize=(13, 6))
seg.plot(kind='bar', ax=ax, colormap='tab10', edgecolor='white', width=0.8)
ax.set_title('Q2: Avg Laptop Price by Company & Type (Segmentation)', fontsize=12, fontweight='bold')
ax.set_xlabel('Company', fontsize=11)
ax.set_ylabel('Avg Price (₹)', fontsize=11)
ax.legend(title='TypeName', bbox_to_anchor=(1.01, 1), loc='upper left', fontsize=8)
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
p = f"{OUTPUT_DIR}/q2_grouped_bar.png"
plt.savefig(p, dpi=150, bbox_inches='tight')
plt.close()
plot_files['q2_grouped'] = p
print("Saved:", p)

# 5. Encoding categorical to numerical
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
for col in ['Company','TypeName','Cpu','Memory','Gpu','OpSys']:
    df_lap[f'{col}_enc'] = le.fit_transform(df_lap[col].astype(str))
enc_cols = [c for c in df_lap.columns if c.endswith('_enc')]
print("\nEncoded columns:\n", df_lap[enc_cols].head(5))

# ============================================================
# QUESTION 3 — Insurance.csv (Hypothesis Testing)
# ============================================================
print("\n===== Q3: Insurance Hypothesis Testing =====")

# 1. BMI male vs female (t-test)
male   = df_ins[df_ins['sex']=='male']['bmi']
female = df_ins[df_ins['sex']=='female']['bmi']
t1, p1 = ttest_ind(male, female)
print(f"\nQ3.1 BMI Male vs Female: t={t1:.4f}, p={p1:.4f}")
print("  → No significant difference (H0 accepted)" if p1 > 0.05 else
      "  → Significant difference (H0 rejected)")

# 2. Charges smoker <= non-smoker (one-sided t-test)
smokers    = df_ins[df_ins['smoker']=='yes']['charges']
nonsmokers = df_ins[df_ins['smoker']=='no']['charges']
t2, p2 = ttest_ind(smokers, nonsmokers)
print(f"\nQ3.2 Charges smoker vs non-smoker: t={t2:.4f}, p={p2:.4f}")
print("  → Smokers pay LESS (H0 accepted)" if t2 < 0 and p2/2 < 0.05 else
      "  → Smokers pay MORE — H0 rejected; charges of smokers > non-smokers")

# 3. Charges increase with age (correlation + linear regression)
r, p3 = stats.pearsonr(df_ins['age'], df_ins['charges'])
print(f"\nQ3.3 Correlation age-charges: r={r:.4f}, p={p3:.4f}")
print("  → Charges increase with age" if r > 0 and p3 < 0.05 else
      "  → No significant increase")

# 4. Proportion of smokers across regions (Chi-square)
ct = pd.crosstab(df_ins['region'], df_ins['smoker'])
chi2, p4, dof, exp = chi2_contingency(ct)
print(f"\nQ3.4 Chi-square smoker proportion by region: chi2={chi2:.4f}, p={p4:.4f}")
print("  → Significantly different" if p4 < 0.05 else "  → Not significantly different")

# 5. ANOVA BMI by children groups (0,1,2)
g0 = df_ins[df_ins['children']==0]['bmi']
g1 = df_ins[df_ins['children']==1]['bmi']
g2 = df_ins[df_ins['children']==2]['bmi']
f5, p5 = f_oneway(g0, g1, g2)
print(f"\nQ3.5 ANOVA BMI (0,1,2 children): F={f5:.4f}, p={p5:.4f}")
print("  → Significant difference in BMI" if p5 < 0.05 else
      "  → No significant difference in BMI")

# Plots Q3
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle('Q3: Insurance — Hypothesis Testing Visualizations', fontsize=13, fontweight='bold')

# BMI by sex
axes[0].boxplot([male, female], labels=['Male','Female'], patch_artist=True,
                boxprops=dict(facecolor='#60A5FA', color='navy'),
                medianprops=dict(color='red', linewidth=2))
axes[0].set_title(f'BMI: Male vs Female\np={p1:.4f}', fontsize=10)
axes[0].set_ylabel('BMI')

# Charges scatter vs age
sc = axes[1].scatter(df_ins['age'], df_ins['charges'],
                     c=df_ins['smoker'].map({'yes':'#EF4444','no':'#3B82F6'}),
                     alpha=0.4, s=20)
m, b = np.polyfit(df_ins['age'], df_ins['charges'], 1)
x_line = np.linspace(df_ins['age'].min(), df_ins['age'].max(), 100)
axes[1].plot(x_line, m*x_line+b, 'k--', linewidth=2, label=f'r={r:.3f}')
axes[1].set_title(f'Charges vs Age\nr={r:.3f}, p={p3:.4f}', fontsize=10)
axes[1].set_xlabel('Age'); axes[1].set_ylabel('Charges')
axes[1].legend(fontsize=8)
red_p = mpatches.Patch(color='#EF4444', label='Smoker')
blue_p = mpatches.Patch(color='#3B82F6', label='Non-smoker')
axes[1].legend(handles=[red_p, blue_p], fontsize=8)

# BMI by children
axes[2].boxplot([g0, g1, g2], labels=['0 children','1 child','2 children'],
                patch_artist=True,
                boxprops=dict(facecolor='#A78BFA', color='purple'),
                medianprops=dict(color='red', linewidth=2))
axes[2].set_title(f'BMI by Children Count\nF={f5:.4f}, p={p5:.4f}', fontsize=10)
axes[2].set_ylabel('BMI')

plt.tight_layout()
p = f"{OUTPUT_DIR}/q3_hypothesis.png"
plt.savefig(p, dpi=150, bbox_inches='tight')
plt.close()
plot_files['q3_hyp'] = p
print("Saved:", p)

# ============================================================
# QUESTION 4 — Canada.csv (Visualization)
# ============================================================
print("\n===== Q4: Canada Visualization =====")

# Total immigrants per year
total_year = df_can[years].sum()

# 4.1 Line plot
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(years, total_year.values, color='#2563EB', linewidth=2.5,
        marker='o', markersize=5, markerfacecolor='#FBBF24', label='Total Immigrants')
ax.fill_between(years, total_year.values, alpha=0.15, color='#2563EB')
ax.set_title('Q4.1: Immigration to Canada (1980–2013) — Line Plot', fontsize=12, fontweight='bold')
ax.set_xlabel('Year'); ax.set_ylabel('Total Immigrants')
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(); ax.set_xlim(1980, 2013)
plt.tight_layout()
p = f"{OUTPUT_DIR}/q4_line.png"
plt.savefig(p, dpi=150, bbox_inches='tight'); plt.close()
plot_files['q4_line'] = p

# Box plot — yearly immigrants distribution
fig, ax = plt.subplots(figsize=(12, 5))
data_box = [df_can[y].values for y in years[::3]]
bp = ax.boxplot(data_box, patch_artist=True,
                boxprops=dict(facecolor='#93C5FD'), medianprops=dict(color='red', lw=2))
ax.set_xticklabels([str(y) for y in years[::3]], rotation=45)
ax.set_title('Q4: Box Plot — Yearly Immigration Distribution (every 3rd year)', fontsize=12, fontweight='bold')
ax.set_xlabel('Year'); ax.set_ylabel('Immigrants per Country')
ax.grid(True, linestyle='--', alpha=0.4)
plt.tight_layout()
p = f"{OUTPUT_DIR}/q4_box.png"
plt.savefig(p, dpi=150, bbox_inches='tight'); plt.close()
plot_files['q4_box'] = p

# Scatter plot — total vs year
fig, ax = plt.subplots(figsize=(10, 5))
ax.scatter(years, total_year.values, c=range(len(years)),
           cmap='viridis', s=80, edgecolors='white', linewidths=0.8, zorder=3)
ax.plot(years, total_year.values, '--', color='gray', alpha=0.5, zorder=2)
ax.set_title('Q4: Scatter Plot — Immigration Trend 1980–2013', fontsize=12, fontweight='bold')
ax.set_xlabel('Year'); ax.set_ylabel('Total Immigrants')
ax.grid(True, linestyle='--', alpha=0.4)
plt.tight_layout()
p = f"{OUTPUT_DIR}/q4_scatter.png"
plt.savefig(p, dpi=150, bbox_inches='tight'); plt.close()
plot_files['q4_scatter'] = p

# 4.4 Frequency distribution 2013
fig, ax = plt.subplots(figsize=(10, 5))
data_2013 = df_can[2013].dropna()
ax.hist(data_2013, bins=20, color='#7C3AED', edgecolor='white', alpha=0.85)
ax.set_title('Q4.4: Frequency Distribution — Immigrants to Canada in 2013', fontsize=12, fontweight='bold')
ax.set_xlabel('Number of Immigrants'); ax.set_ylabel('Frequency')
ax.grid(True, linestyle='--', alpha=0.4)
plt.tight_layout()
p = f"{OUTPUT_DIR}/q4_freq_2013.png"
plt.savefig(p, dpi=150, bbox_inches='tight'); plt.close()
plot_files['q4_freq'] = p

# 4.5 Denmark, Norway, Sweden 1980–2013
dns = df_can.loc[['Denmark','Norway','Sweden'], years].T
fig, ax = plt.subplots(figsize=(11, 5))
colors_dns = ['#EF4444','#F59E0B','#10B981']
for col, c in zip(dns.columns, colors_dns):
    ax.plot(dns.index, dns[col], marker='o', markersize=4, linewidth=2,
            color=c, label=col)
ax.set_title('Q4.5: Immigration — Denmark, Norway & Sweden (1980–2013)', fontsize=12, fontweight='bold')
ax.set_xlabel('Year'); ax.set_ylabel('Immigrants')
ax.legend(); ax.grid(True, linestyle='--', alpha=0.4)
plt.tight_layout()
p = f"{OUTPUT_DIR}/q4_scand.png"
plt.savefig(p, dpi=150, bbox_inches='tight'); plt.close()
plot_files['q4_scand'] = p

# 4.6 Pie chart — total by continent
cont_total = df_can.groupby('Continent')['Total'].sum().sort_values(ascending=False)
explode = [0.05] * len(cont_total)
fig, ax = plt.subplots(figsize=(9, 7))
wedges, texts, autotexts = ax.pie(
    cont_total, labels=cont_total.index, autopct='%1.1f%%',
    explode=explode, startangle=140,
    colors=plt.cm.Set3.colors[:len(cont_total)])
for at in autotexts: at.set_fontsize(9)
ax.set_title('Q4.6: Total Immigrants by Continent (1980–2013)', fontsize=12, fontweight='bold')
plt.tight_layout()
p = f"{OUTPUT_DIR}/q4_pie.png"
plt.savefig(p, dpi=150, bbox_inches='tight'); plt.close()
plot_files['q4_pie'] = p

# 4.7 Line + Scatter subplot in one row
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('Q4.7: Line & Scatter Subplots — Immigration 1980–2013', fontsize=12, fontweight='bold')
ax1.plot(years, total_year.values, color='#2563EB', linewidth=2.5, marker='o', markersize=5)
ax1.set_title('Line Plot'); ax1.set_xlabel('Year'); ax1.set_ylabel('Total Immigrants')
ax1.grid(True, linestyle='--', alpha=0.4)
sc2 = ax2.scatter(years, total_year.values, c=range(len(years)), cmap='plasma', s=80, edgecolors='white')
fig.colorbar(sc2, ax=ax2, label='Year Index')
ax2.set_title('Scatter Plot'); ax2.set_xlabel('Year'); ax2.set_ylabel('Total Immigrants')
ax2.grid(True, linestyle='--', alpha=0.4)
plt.tight_layout()
p = f"{OUTPUT_DIR}/q4_subplot.png"
plt.savefig(p, dpi=150, bbox_inches='tight'); plt.close()
plot_files['q4_subplot'] = p

print("All Q4 plots saved.")
print("\n=== All plots generated ===")
for k, v in plot_files.items():
    print(f"  {k}: {v}")
