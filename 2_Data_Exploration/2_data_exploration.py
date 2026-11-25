import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

#-----------------------------------------------------------------------------------------------------------------------
#2.Description and Analise cleaning data
#-----------------------------------------------------------------------------------------------------------------------
readme_data = {}
#Creating new folder
if not os.path.exists('2_plots'):
    os.makedirs('2_plots')
#Saving data to df
df = pd.read_csv('1_Cleaning_China_Panel_Data.csv')

#2.1. Counting full stats
#Counting ln of amihud
df['ln_amihud'] = np.log(df['amihud'] + 1e-12)
cols = ['amihud', 'volatility', 'Size', 'Leverage', 'ROA']
stats = df[cols].describe().T

#Save for readme
#-----------------------------------------------------------
readme_data['n_obs'] = len(df)
readme_data['n_companies'] = df['code'].nunique()

for col in cols:
    readme_data[f'{col}_mean'] = stats.loc[col, 'mean']
    readme_data[f'{col}_median'] = stats.loc[col, '50%']
    readme_data[f'{col}_std'] = stats.loc[col, 'std']
    readme_data[f'{col}_min'] = stats.loc[col, 'min']
    readme_data[f'{col}_max'] = stats.loc[col, 'max']
#-----------------------------------------------------------

#2.2. Plot of Amihud and Volatility from time
df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'].astype(str) + '-01')#Creating data for time
time_series = df.groupby('Date').agg({'amihud': 'median', 'volatility': 'median'}).reset_index() #Counting medians
#First axis
fig, ax1 = plt.subplots(figsize=(14, 6))
ax1.plot(time_series['Date'], time_series['amihud'], color='blue', linewidth=2, label='Median Amihud (Illiquidity)')
ax1.set_xlabel('Date', fontsize=12)
ax1.set_ylabel('Amihud (Illiquidity)', color='blue', fontsize=12)
ax1.tick_params(axis='y', labelcolor='blue')
ax1.grid(True, alpha=0.3)
#Second axis
ax2 = ax1.twinx()
ax2.plot(time_series['Date'], time_series['volatility'], color='red', linestyle='--', linewidth=2,
         label='Median Volatility')
ax2.set_ylabel('Volatility', color='red', fontsize=12)
ax2.tick_params(axis='y', labelcolor='red')
#Title and legend
plt.title('Market Liquidity and Volatility over Time (2016-2025)', fontsize=16)
fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
plt.tight_layout()
plt.savefig('2_plots/2_liquidity_time_series.png', dpi=300)
plt.close()

#2.3 Panel Balance
companies_per_month = df.groupby('Date')['code'].nunique().reset_index()

#Plot of amount of companies every month
plt.figure(figsize=(14, 4))
plt.plot(companies_per_month['Date'], companies_per_month['code'], color='black', linewidth=2)
plt.title('Number of Active Companies per Month (Panel Balance)', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Number of Companies', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('2_plots/2_companies_per_month.png', dpi=300)
plt.close()

#Save for readme
#-----------------------------------------------------------
readme_data['min_companies_month'] = companies_per_month['code'].min()
readme_data['max_companies_month'] = companies_per_month['code'].max()
#-----------------------------------------------------------



# 2.4. Robustness Check: Full Sample vs Balanced Panel
#Amount of companies (have 10 years activities)
years_per_company = df.groupby('code')['Year'].nunique()
balanced_codes = years_per_company[years_per_company == 10].index

#Save for readme
#-----------------------------------------------------------
readme_data['n_continuous'] = len(balanced_codes)
#-----------------------------------------------------------

#Amonting Amihud and volatility for full panel and balance panel
df_balanced = df[df['code'].isin(balanced_codes)]
time_series_bal = df_balanced.groupby('Date').agg({'amihud': 'median', 'volatility': 'median'}).reset_index()


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Plot 1: Amihud
ax1.plot(time_series['Date'], time_series['amihud'], label=f'All Companies ({readme_data["n_companies"]})', color='blue', linewidth=2, alpha=0.7)
ax1.plot(time_series_bal['Date'], time_series_bal['amihud'], label=f'Balanced Panel ({readme_data["n_continuous"]} firms)', color='red', linestyle='--', linewidth=2)
ax1.set_title('Median Amihud: Full Sample vs Balanced Panel', fontsize=14)
ax1.set_xlabel('Date')
ax1.set_ylabel('Amihud (Illiquidity)')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot 2: Volatility
ax2.plot(time_series['Date'], time_series['volatility'], label=f'All Companies ({readme_data["n_companies"]})', color='blue', linewidth=2, alpha=0.7)
ax2.plot(time_series_bal['Date'], time_series_bal['volatility'], label=f'Balanced Panel ({readme_data["n_continuous"]} firms)', color='red', linestyle='--', linewidth=2)
ax2.set_title('Median Volatility: Full Sample vs Balanced Panel', fontsize=14)
ax2.set_xlabel('Date')
ax2.set_ylabel('Volatility')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('2_plots/2_robustness_overlay.png', dpi=300)
plt.close()

#2.5 Comparing different sectors
tech_ts = df[df['is_tech'] == 1].groupby('Date')['amihud'].median().reset_index()
manuf_ts = df[df['is_manufacturing'] == 1].groupby('Date')['amihud'].median().reset_index()
fin_ts = df[df['is_financial'] == 1].groupby('Date')['amihud'].median().reset_index()
other_ts = df[(df['is_tech'] == 0) & (df['is_manufacturing'] == 0) & (df['is_financial'] == 0)].groupby('Date')['amihud'].median().reset_index()

#2.5.1. Polt of all sectors
plt.figure(figsize=(14, 7))
plt.plot(time_series['Date'], time_series['amihud'], label='Overall Market (All)', color='gray', linewidth=4, alpha=0.5)
plt.plot(tech_ts['Date'], tech_ts['amihud'], label='Tech', color='green', linewidth=2)
plt.plot(manuf_ts['Date'], manuf_ts['amihud'], label='Manufacturing', color='orange', linewidth=2)
plt.plot(fin_ts['Date'], fin_ts['amihud'], label='Financials', color='blue', linewidth=2)
plt.plot(other_ts['Date'], other_ts['amihud'], label='Other Sectors', color='purple', linewidth=2, linestyle='--')
plt.title('Liquidity Dynamics: All Sectors vs Overall Market', fontsize=16)
plt.legend(); plt.grid(True, alpha=0.3); plt.tight_layout()
plt.savefig('2_plots/2_sector_comparison_all.png', dpi=300); plt.close()

#2.5.2. Polt of tech and market's median
plt.figure(figsize=(12, 5))
plt.plot(time_series['Date'], time_series['amihud'], label='Overall Market', color='gray', linewidth=4, alpha=0.5)
plt.plot(tech_ts['Date'], tech_ts['amihud'], label='Tech (IT + Electronics)', color='green', linewidth=2)
plt.title('Liquidity: Tech vs Overall Market', fontsize=14)
plt.legend(); plt.grid(True, alpha=0.3); plt.tight_layout()
plt.savefig('2_plots/2_tech_vs_market.png', dpi=300); plt.close()

#2.5.3. Polt of finance and market's median
plt.figure(figsize=(12, 5))
plt.plot(time_series['Date'], time_series['amihud'], label='Overall Market', color='gray', linewidth=4, alpha=0.5)
plt.plot(fin_ts['Date'], fin_ts['amihud'], label='Financials', color='blue', linewidth=2)
plt.title('Liquidity: Financials vs Overall Market', fontsize=14)
plt.legend(); plt.grid(True, alpha=0.3); plt.tight_layout()
plt.savefig('2_plots/2_financials_vs_market.png', dpi=300); plt.close()

#2.5.4. Polt of manufacturing and other
plt.figure(figsize=(12, 5))
plt.plot(time_series['Date'], time_series['amihud'], label='Overall Market', color='gray', linewidth=4, alpha=0.5)
plt.plot(manuf_ts['Date'], manuf_ts['amihud'], label='Manufacturing', color='orange', linewidth=2)
plt.plot(other_ts['Date'], other_ts['amihud'], label='Other Sectors', color='purple', linewidth=2, linestyle='--')
plt.title('Liquidity: Manufacturing and Other vs Overall Market', fontsize=14)
plt.legend(); plt.grid(True, alpha=0.3); plt.tight_layout()
plt.savefig('2_plots/2_manuf_vs_other.png', dpi=300); plt.close()


#-----------------------------------------------------------------------------------------------------------------------
#2_README.md
#-----------------------------------------------------------------------------------------------------------------------
with open('2_README_Exploration.md', 'w', encoding='utf-8') as f:
    f.write("# Exploratory Data Analysis  Report: China A-Share\n\n")

    f.write("## 1. Descriptive Statistics (Full Sample)\n")
    f.write(f"- **Total observations:** {readme_data['n_obs']:,} (company-month)\n")
    f.write(f"- **Number of unique companies:** {readme_data['n_companies']}\n\n")
    f.write("### Summary Statistics Table\n")
    f.write("| Variable | Mean | Median (50%) | Std. Dev. | Min | Max |\n")
    f.write("| :--- | :--- | :--- | :--- | :--- | :--- |\n")
    for col in cols:
        f.write(
            f"| {col} | {readme_data[f'{col}_mean']:.4e} | {readme_data[f'{col}_median']:.4e} | {readme_data[f'{col}_std']:.4e} | {readme_data[f'{col}_min']:.4e} | {readme_data[f'{col}_max']:.4e} |\n")
    f.write("\n")

    f.write("### Key Takeaways from the Data:\n")
    f.write(
        f"1. **Amihud (Illiquidity):** The distribution of the Amihud measure is strongly right-skewed. The mean ({readme_data['amihud_mean']:.2e}) is almost four times the median ({readme_data['amihud_median']:.2e})."
        "The median indicates that the typical firm in the sample has low illiquidity, whereas the mean is pulled upward by a small number of observations with extremely high illiquidity."
        "For this reason, it makes sense either to log-transform the measure in the regressions, and to rely on the median rather than the mean when interpreting the results.\n")
    f.write(
        f"2. **Volatility:** Average monthly volatility is ({readme_data['volatility_mean']:.2e}), with a median of ({readme_data['volatility_median']:.2e}), which likewise points to right-skewness.The range is from ({readme_data['volatility_min']:.2e}) to ({readme_data['volatility_max']:.2e})."
        "The maximum value appears to fall in the period of the circuit-breaker crisis in January 2016.\n")
    f.write(
        f"3. **Size (Log Assets):** The average log assets value is {readme_data['Size_mean']:.2f}, which is consistent with the profile of large- and mid-cap firms selected from the CSI 300 and CSI 500 indices..\n")
    f.write(
        f"4. **Leverage & ROA (Caveat):** The full-sample average leverage is {readme_data['Leverage_mean']:.2%} and average ROA is {readme_data['ROA_mean']:.2%}. \n")
    f.write(
        "**However, these statistics are heavily influenced by financial institutions (banks, brokers), whose debt structure (e.g., deposits) is fundamentally different from non-financial firms.** \n")
    f.write(
        "For this reason, the econometric analysis will be conducted separately for financial and non-financial subsamples.\n\n")



    f.write("## 2. Market Dynamics (Liquidity and Volatility)\n")
    f.write("**Figure 1: Market Liquidity and Volatility over Time (2016-2025)**\n")
    f.write("![Liquidity Time Series](2_plots/2_liquidity_time_series.png)\n\n")
    f.write(
        "**Observations:** The chart illustrates the dynamics of median illiquidity (Amihud, blue line) "
        "and median volatility (red line) over the 10-year period. We observe several distinct market regimes:\n\n")

    f.write(
        "1. **Synchronous Shock (Jan 2016):** At the beginning of the period, both metrics demonstrate a synchronized peak,"
        " coinciding with the trading suspension episode (circuit breaker mechanism). This reflects the panic that temporarily froze liquidity.\n")

    f.write(
        "2. **Divergence (2018-2019):** During this period, illiquidity reaches its maximum for the sample, while volatility remains relatively low. "
        "This was likely driven by the US-China trade war and China's de-risking campaign, where liquidity tightened without subsequent price shocks. "
        "This is a classic example of a 'liquidity dry-up' without panic.\n")

    f.write(
        "3. **COVID-19 Shock and Recent Years (2020-2025):** A notable volatility spike occurred in early 2020 at the onset of the COVID-19 pandemic. "
        "However, unlike 2016, the illiquidity response was relatively muted, likely due to massive liquidity injections by the Chinese government and"
        " a surge in retail trading volumes. ")
    f.write(
        "Subsequent volatility spikes (2022, 2024, 2025) may be associated with regulatory restrictions in the IT sector,"
        " the real estate crisis (e.g., Ever grande), and geopolitical events.\n")

    f.write(
        "4. **Recent Divergence (Late 2023 - 2024):** We observe a divergence where volatility rises while illiquidity remains at historically low levels. "
        "This may indicate market adaptation to shocks, where price fluctuations increase without a systemic freeze in liquidity.\n\n")

    f.write(
        "**Implication for the Study:** These historical shocks (2016, 2018, 2020) provide an excellent natural laboratory for our research. "
        "They allow us to test whether companies with higher AI innovation (or Tech sector firms) exhibited superior liquidity resilience"
        " during periods of extreme market stress.\n\n")

    f.write("### 3. Panel Balance\n")
    f.write("**Figure 2: Number of Active Companies per Month**\n")
    f.write("![Companies per Month](2_plots/2_companies_per_month.png)\n\n")

    f.write(f"**Observations:** The chart shows that our dataset is an unbalanced panel. ")
    f.write(
        f"The number of active companies grew from {readme_data['min_companies_month']} at the beginning of the period to "
        f"{readme_data['max_companies_month']} by the end, reflecting the gradual inclusion of newly listed firms (IPOs). ")
    f.write(
        f"However, because the sample is unbalanced, the changing composition of firms (new, potentially less liquid companies) "
        f"could potentially drive the aggregate liquidity trends observed earlier. ")
    f.write(
        f"Therefore, it is necessary to compare the full sample with a balanced panel of firms that remained listed throughout the entire period.\n\n")

    f.write("### 4. Robustness Check: Full Sample vs Balanced Panel\n")
    f.write("**Figure 3: Robustness Check (Liquidity and Volatility)**\n")
    f.write("![Robustness Overlay](2_plots/2_robustness_overlay.png)\n\n")

    f.write(
        f"**Observations:** To address the unbalanced nature of our dataset, we re-estimated the market dynamics using only the **{readme_data['n_continuous']} "
        f"companies with continuous history** (i.e., those present in the sample for all 10 years). ")
    f.write("The overlay chart compares the full sample (blue lines) with the balanced panel (red dashed lines).\n\n")

    f.write(
        "**Amihud (Illiquidity):** The lines almost perfectly overlap in shape. The balanced panel is on average slightly lower, "
        "which is consistent with the fact that newly listed companies tend to be less liquid. ")
    f.write(
        "However, the general liquidity trends — including the peaks of 2016 and 2018 — are not determined by the influx of new companies, "
        "but reflect genuine market conditions.\n\n")

    f.write(
        "**Volatility:** The volatility picture remains virtually unchanged when excluding new companies. The spikes of 2020, 2022, and 2024 are present in both samples.\n\n")

    f.write(
        "**Conclusion:** The results confirm the robustness of the dataset. The findings do not depend on composition bias, "
        "which justifies the use of the full unbalanced panel for subsequent econometric analysis.\n\n")

    f.write("## 5. Sector Comparisons\n")

    f.write("### 5.1. Overall Market Dynamics by Sector\n")
    f.write("**Figure 4: Liquidity Dynamics across All Sectors vs Overall Market**\n")
    f.write("![All Sectors vs Market](2_plots/2_sector_comparison_all.png)\n\n")
    f.write("**Observations:** The chart presents the dynamics of illiquidity across sectors. ")
    f.write("The Financial sector (blue line) consistently exhibits the lowest illiquidity. ")
    f.write(
        "The Tech sector (green line) deviates from the overall market trend in recent years, "
        "while Manufacturing and the remaining sectors closely follow the general market.\n\n")

    f.write("### 5.2. Tech Sector vs Overall Market\n")
    f.write("**Figure 5: Liquidity in the Tech Sector vs Overall Market**\n")
    f.write("![Tech vs Market](2_plots/2_tech_vs_market.png)\n\n")
    f.write(
        "**Observations:** During 2023–2025, the Tech sector demonstrates lower median illiquidity compared to the overall market. ")
    f.write(
        "This indicates an increase in the liquidity of technology companies, "
        "which is likely driven by heightened investor interest in AI and digitalization (establishing causality requires further analysis).\n\n")

    f.write("### 5.3. Financial Sector vs Overall Market\n")
    f.write("**Figure 6: Liquidity in the Financial Sector vs Overall Market**\n")
    f.write("![Financials vs Market](2_plots/2_financials_vs_market.png)\n\n")
    f.write(
        "**Observations:** The Financial sector maintains lower illiquidity than the overall market throughout the entire period. ")
    f.write(
        "However, during periods of market stress (e.g., 2016, 2020), the gap between them narrows significantly, "
        "indicating that even the most liquid companies are vulnerable to systemic shocks.\n\n")

    f.write("### 5.4. Manufacturing vs Other Sectors\n")
    f.write("**Figure 7: Liquidity in Manufacturing and Other Sectors vs Overall Market**\n")
    f.write("![Manufacturing vs Other](2_plots/2_manuf_vs_other.png)\n\n")
    f.write(
        "**Observations:** The Manufacturing sector (orange line) almost perfectly tracks the overall market average (gray line). ")
    f.write(
        "The Other Sectors (purple line) exhibit higher illiquidity, especially during the stress periods of 2016–2018. ")
    f.write(
        "This may indicate a reallocation of capital from services, retail, and real estate into manufacturing during crises.\n\n")