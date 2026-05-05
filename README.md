# 📊 Data Visualization & Analytics (DVA) Project 2

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data_Wrangling-150458?style=for-the-badge&logo=pandas)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI_Dashboard-8CAAE6?style=for-the-badge)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualizations-11557c?style=for-the-badge)

A comprehensive interactive Social Media Trends Analytics Dashboard demonstrating professional data visualization, data wrangling, and analytics. This project processes a dataset with 2000 records of social media trend data to generate a multi-page interactive dashboard.

---

## ✨ Project Highlights

### 1. Dashboard Pages
- **Overview:** Executive summary displaying key KPIs, platform reach, category distribution, top hashtags, and average engagement rates.
- **Platform Analysis:** Detailed metrics comparison across 5 platforms (Twitter, Instagram, YouTube, Facebook, TikTok) with multi-metric bar charts.
- **Category Trends:** Engagement and reach metrics by content category (Entertainment, Sports, Technology, etc.) including top hashtags and content output distribution.
- **Hashtag Rankings:** Comprehensive ranking table for top and bottom performing hashtags by total views.
- **Heatmap & Correlations:** Statistical relationships shown via a Correlation Matrix and Platform vs Category engagement intensity heatmap.

### 2. Custom GUI & Styling
- **Midnight Purple Theme:** A modern, sleek appearance with high contrast and carefully selected colors.
- **Responsive Layouts:** Designed to adapt to the screen, providing scrollable data tables and interactive visual modules.
- **Standardized Visualizations:** Integrating customized Matplotlib charts embedded in a Tkinter GUI.

### 3. Data Processing & Validation
- **Dynamic Aggregation:** Rapid and efficient pandas aggregation for calculating platform metrics and engagement.
- **Robust formatting:** Cleaned labels and formatted large numeric values for better UI representation.
- **Data Validation:** Included data integrity checks before visualization processing.

---

## 🛠️ Architecture & Files

The project is structured into modular Python scripts to separate logic, visualization, and generation tasks:

| File | Purpose |
|------|---------|
| `dashboard.py` | The main dashboard application. Defines UI pages, handles aggregations, and embeds Matplotlib plots. |
| `generate_pdf.py` | The report generator. Creates a polished `.docx` academic report of the assignment, followed by conversion to PDF. |
| `Social_Media_Trends_India.csv` | The custom social media dataset containing 2000 records. |
| `DVA_Assignment_2_Akshat_Tripathi.pdf` | The final rendered, 21-page academic project report. |

---

## 🚀 How to Run

1. **Install Dependencies:**
   ```bash
   pip install pandas numpy matplotlib python-docx docx2pdf
   ```
2. **Run the Dashboard:**
   ```bash
   python dashboard.py
   ```
3. **Generate the Report:**
   ```bash
   python generate_pdf.py
   ```

---
*Developed by Akshat Tripathi*
