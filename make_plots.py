
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from scipy import stats
from scipy.stats import f_oneway, chi2_contingency, ttest_ind
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
import warnings, os
warnings.filterwarnings('ignore')

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.titlesize': 13,
    'axes.titleweight': 'bold',
    'axes.labelsize': 10,
    'figure.facecolor': 'white',
    'axes.facecolor': '#F8FAFF',
    'axes.edgecolor': '#CBD5E1',
    'grid.color': '#E2E8F0',
    'grid.linewidth': 0.8,
})

D = "a1_plots"
os.makedirs(D, exist_ok=True)

# ── Datasets ────────────────────────────────────────────────
df_can = pd.read_excel('Canada.xlsx', sheet_name='Canada by Citizenship', skiprows=20, skipfooter=2)
df_can.rename(columns={'OdName':'Country','AreaName':'Continent','RegName':'Region','DevName':'DevStatus'}, inplace=True)
df_can.set_index('Country', inplace=True)
years = list(range(1980, 2014))
df_can['Total'] = df_can[years].sum(axis=1)

df_ins = pd.read_csv('Insurance.csv')
df_lap = pd.read_csv('Laptop.csv')

PAL = ['#2563EB','#7C3AED','#DB2777','#D97706','#059669','#DC2626','#0891B2']

# ════════════════════════════════════════════════════════════
# Q1 PLOT — Top 5 countries
# ════════════════════════════════════════════════════════════
top5 = df_can.sort_values('Total', ascending=False).head(5)
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(top5.index, top5['Total'], color=PAL[:5], edgecolor='white', height=0.55)
for bar, val in zip(bars, top5['Total']):
    ax.text(bar.get_width()+3000, bar.get_y()+bar.get_height()/2,
            f'{val:,}', va='center', fontsize=9, fontweight='bold', color='#1E293B')
ax.set_xlabel('Total Immigrants (1980–2013)', fontsize=10)
ax.set_title('Q1 · Top 5 Countries by Total Immigration to Canada (1980–2013)')
ax.invert_yaxis(); ax.set_xlim(0, top5['Total'].max()*1.18)
ax.grid(True, axis='x', linestyle='--', alpha=0.5)
plt.tight_layout(); plt.savefig(f'{D}/q1_top5.png', dpi=150, bbox_inches='tight'); plt.close()

# Q1 — Null check bar (visual)
null_counts = df_can.isnull().sum()
non_null_numeric = null_counts[null_counts > 0]
fig, ax = plt.subplots(figsize=(8, 3))
if len(non_null_numeric) == 0:
    ax.text(0.5, 0.5, 'No Null Values Found in Dataset\n(All 195 countries × 43 columns clean)',
            ha='center', va='center', fontsize=13, color='#059669',
            fontweight='bold', transform=ax.transAxes)
    ax.set_facecolor('#F0FDF4'); ax.set_xticks([]); ax.set_yticks([])
ax.set_title('Q1 · Null Value Check — Canada Dataset')
plt.tight_layout(); plt.savefig(f'{D}/q1_nulls.png', dpi=150, bbox_inches='tight'); plt.close()

# Q1 — Filter 1980-1985
fig, ax = plt.subplots(figsize=(10, 5))
top10 = df_can.sort_values('Total', ascending=False).head(10)
yr_cols = list(range(1980, 1986))
bottom = np.zeros(len(top10))
colors_yr = plt.cm.Blues(np.linspace(0.35, 0.85, 6))
for i, yr in enumerate(yr_cols):
    ax.bar(range(len(top10)), top10[yr], bottom=bottom, color=colors_yr[i],
           label=str(yr), edgecolor='white', linewidth=0.5)
    bottom += top10[yr].values
ax.set_xticks(range(len(top10)))
ax.set_xticklabels([c[:12] for c in top10.index], rotation=35, ha='right', fontsize=8)
ax.set_title('Q1 · Immigration 1980–1985 — Top 10 Countries (Stacked)')
ax.set_ylabel('Immigrants'); ax.legend(title='Year', bbox_to_anchor=(1,1), fontsize=8)
plt.tight_layout(); plt.savefig(f'{D}/q1_filter.png', dpi=150, bbox_inches='tight'); plt.close()

print("Q1 plots done")

# ════════════════════════════════════════════════════════════
# Q2 PLOTS
# ════════════════════════════════════════════════════════════
df_lap2 = df_lap.copy()

# Missing values before/after
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
miss_before = df_lap2.isnull().sum()
miss_before[miss_before > 0].plot(kind='bar', ax=axes[0], color='#EF4444', edgecolor='white')
axes[0].set_title('Q2 · Missing Values — Before Imputation')
axes[0].set_ylabel('Count'); axes[0].tick_params(rotation=30)

df_lap2['Ram'].fillna(df_lap2['Ram'].median(), inplace=True)
df_lap2['Weight'].fillna(df_lap2['Weight'].median(), inplace=True)
df_lap2['Gpu'].fillna('Unknown', inplace=True)
miss_after = df_lap2.isnull().sum()
miss_after_nonzero = miss_after[miss_after > 0]
if len(miss_after_nonzero) == 0:
    axes[1].text(0.5, 0.5, 'No Missing Values\nAfter Imputation', ha='center', va='center',
                 fontsize=14, color='#059669', fontweight='bold', transform=axes[1].transAxes)
    axes[1].set_facecolor('#F0FDF4'); axes[1].set_xticks([]); axes[1].set_yticks([])
axes[1].set_title('Q2 · Missing Values — After Imputation')
plt.tight_layout(); plt.savefig(f'{D}/q2_missing.png', dpi=150, bbox_inches='tight'); plt.close()

# Standardize & Normalize distribution
df_lap2['Inches'] = pd.to_numeric(df_lap2['Inches'], errors='coerce')
df_lap2['Ram'] = df_lap2['Ram'].astype(int)
df_lap2['Price_std'] = StandardScaler().fit_transform(df_lap2[['Price']])
df_lap2['Price_norm'] = MinMaxScaler().fit_transform(df_lap2[['Price']])

fig, axes = plt.subplots(1, 3, figsize=(14, 4))
axes[0].hist(df_lap2['Price'], bins=30, color='#2563EB', edgecolor='white', alpha=0.85)
axes[0].set_title('Original Price Distribution'); axes[0].set_xlabel('Price (₹)')
axes[1].hist(df_lap2['Price_std'], bins=30, color='#7C3AED', edgecolor='white', alpha=0.85)
axes[1].set_title('After Standardization (Z-score)'); axes[1].set_xlabel('Standardized Price')
axes[2].hist(df_lap2['Price_norm'], bins=30, color='#059669', edgecolor='white', alpha=0.85)
axes[2].set_title('After Normalization (Min-Max)'); axes[2].set_xlabel('Normalized Price [0,1]')
for ax in axes: ax.grid(True, linestyle='--', alpha=0.5)
plt.suptitle('Q2 · Price Distribution: Original vs Standardized vs Normalized', fontweight='bold', fontsize=12)
plt.tight_layout(); plt.savefig(f'{D}/q2_scaling.png', dpi=150, bbox_inches='tight'); plt.close()

# Grouped bar — Segmentation
top6 = df_lap2['Company'].value_counts().head(6).index
seg = df_lap2[df_lap2['Company'].isin(top6)].groupby(['Company','TypeName'])['Price'].mean().unstack(fill_value=0)
fig, ax = plt.subplots(figsize=(13, 5))
seg.plot(kind='bar', ax=ax, colormap='tab10', edgecolor='white', width=0.75)
ax.set_title('Q2 · Avg Laptop Price by Company & Type — Grouped Bar (Segmentation)')
ax.set_xlabel('Company'); ax.set_ylabel('Average Price (₹)')
ax.legend(title='Type', bbox_to_anchor=(1.01,1), fontsize=8)
ax.tick_params(axis='x', rotation=0)
plt.tight_layout(); plt.savefig(f'{D}/q2_grouped.png', dpi=150, bbox_inches='tight'); plt.close()

# Label encoding visual
le = LabelEncoder()
df_lap2_enc = df_lap2.copy()
cat_cols = ['Company','TypeName','Cpu','Memory','Gpu','OpSys']
for col in cat_cols:
    df_lap2_enc[f'{col}_enc'] = le.fit_transform(df_lap2_enc[col].astype(str))

fig, ax = plt.subplots(figsize=(10, 4))
enc_sample = df_lap2_enc[cat_cols + [c+'_enc' for c in cat_cols]].head(8)
data_disp = [[str(df_lap2_enc[col].iloc[i]) + '  →  ' + str(df_lap2_enc[col+'_enc'].iloc[i])
              for col in cat_cols] for i in range(6)]
tbl = ax.table(cellText=data_disp, colLabels=cat_cols,
               cellLoc='center', loc='center', bbox=[0,0,1,1])
tbl.auto_set_font_size(False); tbl.set_fontsize(7.5)
for j in range(len(cat_cols)):
    tbl[(0,j)].set_facecolor('#2563EB'); tbl[(0,j)].set_text_props(color='white', fontweight='bold')
for i in range(1, 7):
    for j in range(len(cat_cols)):
        tbl[(i,j)].set_facecolor('#EFF6FF' if i%2==0 else 'white')
ax.axis('off'); ax.set_title('Q2 · Label Encoding: Categorical → Numerical (sample rows)', fontweight='bold', pad=12)
plt.tight_layout(); plt.savefig(f'{D}/q2_encoding.png', dpi=150, bbox_inches='tight'); plt.close()

print("Q2 plots done")

# ════════════════════════════════════════════════════════════
# Q3 PLOTS
# ════════════════════════════════════════════════════════════
male_bmi   = df_ins[df_ins['sex']=='male']['bmi']
female_bmi = df_ins[df_ins['sex']=='female']['bmi']
t1, p1 = ttest_ind(male_bmi, female_bmi)

smokers    = df_ins[df_ins['smoker']=='yes']['charges']
nonsmokers = df_ins[df_ins['smoker']=='no']['charges']
t2, p2 = ttest_ind(smokers, nonsmokers)

r3, p3 = stats.pearsonr(df_ins['age'], df_ins['charges'])

ct = pd.crosstab(df_ins['region'], df_ins['smoker'])
chi2, p4, dof, _ = chi2_contingency(ct)

women = df_ins[df_ins['sex']=='female']
g0 = women[women['children']==0]['bmi']
g1 = women[women['children']==1]['bmi']
g2 = women[women['children']==2]['bmi']
f5, p5 = f_oneway(g0, g1, g2)

# Plot Q3.1 — BMI boxplot
fig, ax = plt.subplots(figsize=(7, 5))
bp = ax.boxplot([male_bmi, female_bmi], labels=['Male','Female'], patch_artist=True,
                widths=0.45, notch=True,
                boxprops=dict(facecolor='#BFDBFE', color='#1E40AF'),
                medianprops=dict(color='#DC2626', linewidth=2.5),
                flierprops=dict(marker='o', markerfacecolor='#94A3B8', markersize=3, alpha=0.5),
                whiskerprops=dict(color='#1E40AF'), capprops=dict(color='#1E40AF'))
bp['boxes'][1].set_facecolor('#DDD6FE')
ax.set_title(f'Q3.1 · BMI: Male vs Female\nt={t1:.3f}, p={p1:.4f} → {"No difference (H₀ accepted)" if p1>0.05 else "Significant difference"}')
ax.set_ylabel('BMI')
ax.text(0.97, 0.97, f'Male μ={male_bmi.mean():.2f}\nFemale μ={female_bmi.mean():.2f}',
        transform=ax.transAxes, ha='right', va='top', fontsize=9,
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#EFF6FF', edgecolor='#BFDBFE'))
plt.tight_layout(); plt.savefig(f'{D}/q3_bmi_gender.png', dpi=150, bbox_inches='tight'); plt.close()

# Plot Q3.2 — Charges smoker vs non-smoker
fig, ax = plt.subplots(figsize=(7, 5))
bp2 = ax.boxplot([smokers, nonsmokers], labels=['Smoker','Non-Smoker'], patch_artist=True,
                 widths=0.45, notch=True,
                 boxprops=dict(facecolor='#FEE2E2'),
                 medianprops=dict(color='#DC2626', linewidth=2.5),
                 flierprops=dict(marker='o', markerfacecolor='#94A3B8', markersize=3, alpha=0.5))
bp2['boxes'][1].set_facecolor('#D1FAE5')
ax.set_title(f'Q3.2 · Medical Charges: Smoker vs Non-Smoker\nt={t2:.3f}, p≈{p2:.2e} → H₀ REJECTED (Smokers pay more)')
ax.set_ylabel('Medical Charges ($)')
ax.text(0.97, 0.97, f'Smoker μ=${smokers.mean():,.0f}\nNon-Smoker μ=${nonsmokers.mean():,.0f}',
        transform=ax.transAxes, ha='right', va='top', fontsize=9,
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#FEF2F2', edgecolor='#FECACA'))
plt.tight_layout(); plt.savefig(f'{D}/q3_charges_smoker.png', dpi=150, bbox_inches='tight'); plt.close()

# Plot Q3.3 — Age vs Charges scatter with regression
fig, ax = plt.subplots(figsize=(9, 5))
colors_s = df_ins['smoker'].map({'yes':'#EF4444','no':'#3B82F6'})
ax.scatter(df_ins['age'], df_ins['charges'], c=colors_s, alpha=0.4, s=25, edgecolors='none')
m, b = np.polyfit(df_ins['age'], df_ins['charges'], 1)
x_ln = np.array([df_ins['age'].min(), df_ins['age'].max()])
ax.plot(x_ln, m*x_ln+b, 'k--', linewidth=2, zorder=5, label=f'Regression line (r={r3:.3f})')
ax.set_title(f'Q3.3 · Charges vs Age — Pearson r={r3:.3f}, p≈{p3:.2e}\n→ Charges increase with age (H₀ rejected)')
ax.set_xlabel('Age'); ax.set_ylabel('Medical Charges ($)')
red_p = mpatches.Patch(color='#EF4444', label='Smoker')
blue_p = mpatches.Patch(color='#3B82F6', label='Non-Smoker')
ax.legend(handles=[red_p, blue_p, ax.lines[0]], fontsize=9)
plt.tight_layout(); plt.savefig(f'{D}/q3_age_charges.png', dpi=150, bbox_inches='tight'); plt.close()

# Plot Q3.4 — Smoker proportion by region
fig, ax = plt.subplots(figsize=(9, 5))
ct_pct = ct.div(ct.sum(axis=1), axis=0) * 100
ct_pct.plot(kind='bar', ax=ax, color=['#3B82F6','#EF4444'], edgecolor='white', width=0.6)
ax.set_title(f'Q3.4 · Smoker Proportion by Region\nChi²={chi2:.3f}, p={p4:.4f} → {"Significant" if p4<0.05 else "Not significantly different across regions"}')
ax.set_ylabel('Proportion (%)'); ax.set_xlabel('Region')
ax.legend(['Non-Smoker','Smoker']); ax.tick_params(axis='x', rotation=15)
for bar in ax.patches:
    h = bar.get_height()
    if h > 2:
        ax.text(bar.get_x()+bar.get_width()/2, h+0.5, f'{h:.1f}%', ha='center', va='bottom', fontsize=8)
plt.tight_layout(); plt.savefig(f'{D}/q3_region_smoker.png', dpi=150, bbox_inches='tight'); plt.close()

# Plot Q3.5 — ANOVA BMI women by children
fig, ax = plt.subplots(figsize=(8, 5))
bp5 = ax.boxplot([g0, g1, g2], labels=['0 Children','1 Child','2 Children'],
                 patch_artist=True, widths=0.45, notch=False,
                 boxprops=dict(facecolor='#EDE9FE'),
                 medianprops=dict(color='#7C3AED', linewidth=2.5),
                 flierprops=dict(marker='o', markerfacecolor='#94A3B8', markersize=3, alpha=0.5))
for i, (grp, col) in enumerate(zip([g0,g1,g2],['#BFDBFE','#DDD6FE','#FBCFE8'])):
    bp5['boxes'][i].set_facecolor(col)
ax.set_title(f'Q3.5 · BMI of Women by Number of Children (ANOVA)\nF={f5:.3f}, p={p5:.4f} → {"Significant" if p5<0.05 else "No significant difference (H₀ accepted)"}')
ax.set_ylabel('BMI')
for i, (grp, lbl) in enumerate(zip([g0,g1,g2],['0 children','1 child','2 children'])):
    ax.text(i+1, grp.max()+0.3, f'μ={grp.mean():.2f}', ha='center', fontsize=9, color='#374151')
plt.tight_layout(); plt.savefig(f'{D}/q3_anova_bmi.png', dpi=150, bbox_inches='tight'); plt.close()

print("Q3 plots done")

# ════════════════════════════════════════════════════════════
# Q4 PLOTS
# ════════════════════════════════════════════════════════════
total_yr = df_can[years].sum()

# Q4.1a Line plot
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(years, total_yr.values, color='#2563EB', linewidth=2.5,
        marker='D', markersize=5, markerfacecolor='#FBBF24',
        markeredgecolor='#92400E', linestyle='-', label='Total Immigrants')
ax.fill_between(years, total_yr.values, alpha=0.12, color='#2563EB')
ax.set_title('Q4.1 · Line Plot — Total Immigration to Canada (1980–2013)')
ax.set_xlabel('Year'); ax.set_ylabel('Total Immigrants')
ax.legend(fontsize=10); ax.set_xlim(1980, 2013)
ax.set_ylim(total_yr.min()*0.85, total_yr.max()*1.08)
ax.annotate(f'Peak: {total_yr.idxmax()}\n{total_yr.max():,}',
            xy=(total_yr.idxmax(), total_yr.max()),
            xytext=(total_yr.idxmax()-5, total_yr.max()*0.97),
            arrowprops=dict(arrowstyle='->', color='red'),
            fontsize=9, color='red')
plt.tight_layout(); plt.savefig(f'{D}/q4_line.png', dpi=150, bbox_inches='tight'); plt.close()

# Q4.1b Box plot
fig, ax = plt.subplots(figsize=(14, 5))
data_box = [df_can[y].values for y in years]
bp4 = ax.boxplot(data_box, patch_artist=True, widths=0.6,
                 boxprops=dict(facecolor='#BFDBFE', color='#1E40AF'),
                 medianprops=dict(color='#DC2626', linewidth=1.5),
                 flierprops=dict(marker='.', markersize=2, alpha=0.3),
                 whiskerprops=dict(color='#1E40AF'), capprops=dict(color='#1E40AF'))
ax.set_xticks(range(1, len(years)+1, 3))
ax.set_xticklabels([str(y) for y in years[::3]], rotation=45, fontsize=8)
ax.set_title('Q4.1 · Box Plot — Immigration Distribution per Country per Year')
ax.set_xlabel('Year'); ax.set_ylabel('Immigrants per Country')
plt.tight_layout(); plt.savefig(f'{D}/q4_box.png', dpi=150, bbox_inches='tight'); plt.close()

# Q4.1c Scatter plot
fig, ax = plt.subplots(figsize=(11, 5))
sc = ax.scatter(years, total_yr.values, c=total_yr.values, cmap='plasma',
                s=90, edgecolors='white', linewidths=0.8, zorder=3)
ax.plot(years, total_yr.values, '--', color='#94A3B8', alpha=0.6, zorder=2, linewidth=1.2)
fig.colorbar(sc, ax=ax, label='Total Immigrants')
ax.set_title('Q4.1 · Scatter Plot — Immigration Trend (color = volume)')
ax.set_xlabel('Year'); ax.set_ylabel('Total Immigrants')
ax.set_xlim(1979, 2014)
plt.tight_layout(); plt.savefig(f'{D}/q4_scatter.png', dpi=150, bbox_inches='tight'); plt.close()

# Q4.4 Frequency distribution 2013
fig, ax = plt.subplots(figsize=(10, 5))
data_2013 = df_can[2013].dropna()
n, bins, patches = ax.hist(data_2013, bins=25, edgecolor='white', linewidth=0.6)
cm_map = plt.cm.plasma
for patch, left, right in zip(patches, bins[:-1], bins[1:]):
    patch.set_facecolor(cm_map((left - bins[0])/(bins[-1]-bins[0])))
ax.set_title('Q4.4 · Frequency Distribution — New Immigrants to Canada in 2013')
ax.set_xlabel('Number of Immigrants (per country)'); ax.set_ylabel('Frequency (No. of Countries)')
ax.axvline(data_2013.mean(), color='red', linestyle='--', linewidth=1.5, label=f'Mean = {data_2013.mean():.0f}')
ax.legend()
plt.tight_layout(); plt.savefig(f'{D}/q4_freq_2013.png', dpi=150, bbox_inches='tight'); plt.close()

# Q4.5 Denmark Norway Sweden
dns_countries = ['Denmark','Norway','Sweden']
dns = df_can.loc[dns_countries, years].T
fig, ax = plt.subplots(figsize=(12, 5))
styles = [('o-','#EF4444'),('s--','#F59E0B'),('D-.','#10B981')]
for country, (ls, col) in zip(dns_countries, styles):
    ax.plot(years, dns[country], ls, color=col, linewidth=2.2, markersize=5,
            label=country, markerfacecolor='white', markeredgewidth=1.5)
ax.set_title('Q4.5 · Immigration Distribution — Denmark, Norway & Sweden (1980–2013)')
ax.set_xlabel('Year'); ax.set_ylabel('Number of Immigrants')
ax.legend(fontsize=10); ax.set_xlim(1980, 2013)
plt.tight_layout(); plt.savefig(f'{D}/q4_scand.png', dpi=150, bbox_inches='tight'); plt.close()

# Q4.6 Pie chart by continent
cont = df_can.groupby('Continent')['Total'].sum().sort_values(ascending=False)
explode = [0.05 if i == 0 else 0.02 for i in range(len(cont))]
fig, ax = plt.subplots(figsize=(9, 7))
wedges, texts, autotexts = ax.pie(
    cont, labels=cont.index, autopct='%1.1f%%',
    explode=explode, startangle=140,
    colors=plt.cm.Set2.colors[:len(cont)],
    wedgeprops=dict(edgecolor='white', linewidth=1.5))
for t in texts: t.set_fontsize(9)
for at in autotexts: at.set_fontsize(8); at.set_fontweight('bold')
ax.set_title('Q4.6 · Total Immigrants Proportion by Continent (1980–2013)', pad=20)
plt.tight_layout(); plt.savefig(f'{D}/q4_pie.png', dpi=150, bbox_inches='tight'); plt.close()

# Q4.7 Subplot — line + scatter
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), sharey=True)
fig.suptitle('Q4.7 · Line & Scatter Plot in One Row (Subplots) — Canada Immigration 1980–2013',
             fontsize=12, fontweight='bold')
ax1.plot(years, total_yr.values, 'D-', color='#2563EB', linewidth=2.2,
         markersize=5, markerfacecolor='#FBBF24')
ax1.fill_between(years, total_yr.values, alpha=0.1, color='#2563EB')
ax1.set_title('Line Plot'); ax1.set_xlabel('Year'); ax1.set_ylabel('Total Immigrants')
ax1.set_xlim(1980, 2013)
sc2 = ax2.scatter(years, total_yr.values, c=total_yr.values,
                  cmap='viridis', s=90, edgecolors='white', linewidths=0.8)
fig.colorbar(sc2, ax=ax2, label='Immigrants')
ax2.set_title('Scatter Plot'); ax2.set_xlabel('Year'); ax2.set_xlim(1979, 2014)
plt.tight_layout(); plt.savefig(f'{D}/q4_subplot.png', dpi=150, bbox_inches='tight'); plt.close()

print("Q4 plots done")
print("\nAll plots saved to:", D)
print({f for f in os.listdir(D)})
