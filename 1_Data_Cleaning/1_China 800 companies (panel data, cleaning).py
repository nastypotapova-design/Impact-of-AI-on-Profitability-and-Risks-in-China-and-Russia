import pandas as pd
import matplotlib.pyplot as plt
import glob
import numpy as np
#-----------------------------------------------------------------------------------------------------------------------
#1.Load all Data (800 companies China)
#-----------------------------------------------------------------------------------------------------------------------
readme_data = {}
#1.1. Load daily data of all companies
folder_path = 'main data/800 daily'
daily_data = []
all_daily_files = glob.glob(folder_path + "/*.csv")
for file in all_daily_files:
    df = pd.read_csv(file)
    daily_data.append(df)
all_daily_data = pd.concat(daily_data)

#Save for readme
#-----------------------------------------------------------
readme_data['n_companies'] = all_daily_data['code'].nunique()
readme_data['date_min'] = all_daily_data['date'].min()
readme_data['date_max'] = all_daily_data['date'].max()
readme_data['initial_daily_rows'] = len(all_daily_data)
#-----------------------------------------------------------

#1.2 Cleaning data
#Save for readme
#-----------------------------------------------------------
rows_before_clean = len(all_daily_data)
#-----------------------------------------------------------

all_daily_data = all_daily_data[all_daily_data['amount_cny'] > 0]
all_daily_data['date'] = pd.to_datetime(all_daily_data['date'])
all_daily_data.sort_values(by=['code', 'date'], inplace=True) #sort firstly by code, then by date

#Save for readme
#-----------------------------------------------------------
rows_after_clean = len(all_daily_data)
readme_data['rows_removed_zero_volume'] = rows_before_clean - rows_after_clean
readme_data['rows_after_zero_volume'] = rows_after_clean
#-----------------------------------------------------------

#1.3. Counting of profit and Amihud
all_daily_data['return'] = all_daily_data.groupby('code')['close'].pct_change() #counting return
all_daily_data = all_daily_data.dropna(subset=['return'])
all_daily_data['amihud'] = abs(all_daily_data['return']) / all_daily_data['amount_cny'] #counting amihud


#1.4. Months' return, volatility, amihud and average volume
all_daily_data['Year'] = all_daily_data['date'].dt.year
all_daily_data['Month'] = all_daily_data['date'].dt.month
all_daily_data['days_count'] = 1
monthly_data = all_daily_data.groupby(['code', 'Year', 'Month']).agg({'return': ['mean','std'], 'amihud': 'mean', 'volume_shares': 'mean','days_count': 'sum'}).reset_index()
monthly_data.columns = ['code', 'Year', 'Month',  'avg_return', 'volatility','amihud', 'avg_volume', 'days_traded']

#Save for readme
#-----------------------------------------------------------
rows_before_month_filter = len(monthly_data)
#-----------------------------------------------------------
# Filter out months with less than 10 trading days to ensure representativeness
monthly_data = monthly_data[monthly_data['days_traded'] >= 10]

#Save for readme
#-----------------------------------------------------------
rows_after_month_filter = len(monthly_data)
readme_data['rows_removed_short_months'] = rows_before_month_filter - rows_after_month_filter
readme_data['final_monthly_rows'] = rows_after_month_filter
readme_data['final_missing_total'] = monthly_data.isnull().sum().sum()
#-----------------------------------------------------------

#1.5. Load financials
folder_path = 'main data'
financials = pd.read_csv(folder_path+'/financials.csv')
financials.rename(columns={'fy': 'Year'}, inplace=True)
financials.sort_values(by=['code', 'Year'], inplace=True)

#Save for readme
#-----------------------------------------------------------
readme_data['financials_initial_rows'] = len(financials)
readme_data['financials_duplicates_removed'] = financials.duplicated(subset=['code', 'Year']).sum()
#-----------------------------------------------------------

financials = financials.drop_duplicates(subset=['code', 'Year'], keep='first')

#1.6. Counting of size, leverage, ROA for each companies
financials['Size'] = np.log(financials['total_assets_cny'])
financials['Leverage'] = financials['total_liabilities_cny'] / financials['total_assets_cny']
financials['ROA'] = financials['net_profit_cny'] / financials['total_assets_cny']
merged_data = pd.merge(monthly_data, financials, on=['code', 'Year'], how='left') #sorting firstly by code, then by year

#Save for readme
#-----------------------------------------------------------
readme_data['rows_before_merge'] = len(monthly_data)
readme_data['rows_after_financial_merge'] = len(merged_data)
#-----------------------------------------------------------

#1.7. Load type of industries
industry = pd.read_excel(folder_path+'/Industry.xlsx')
industry.rename(columns={'Stock Code': 'code'}, inplace=True)
merged_data = pd.merge(merged_data, industry, on='code', how='left')

# 1.8. Industry Distribution and Visualization

#Creatind dictionary
translate_dict = {
    '制造业--计算机、通信和其他电子设备制造业': 'Manufacturing: Computers & Electronics',
    '制造业--医药制造业': 'Manufacturing: Pharmaceuticals',
    '制造业--电气机械和器材制造业': 'Manufacturing: Electrical Machinery',
    '制造业--专用设备制造业': 'Manufacturing: Special Equipment',
    '金融业--资本市场服务': 'Financials: Capital Markets',
    '信息传输、软件和信息技术服务业--软件和信息技术服务业': 'IT: Software & Services',
    '制造业--化学原料和化学制品制造业': 'Manufacturing: Chemicals',
    '电力、热力、燃气及水生产和供应业--电力、热力生产和供应业': 'Utilities: Power & Heat',
    '金融业--货币金融服务': 'Financials: Banking',
    '制造业--汽车制造业': 'Manufacturing: Automobiles',
    '制造业--铁路、船舶、航空航天和其他运输设备制造业': 'Manufacturing: Transport Equipment',
    '制造业--有色金属冶炼和压延加工业': 'Manufacturing: Non-ferrous Metals',
    '制造业--非金属矿物制品业': 'Manufacturing: Non-metallic Minerals',
    '建筑业--土木工程建筑业': 'Construction: Civil Engineering',
    '制造业--酒、饮料和精制茶制造业': 'Manufacturing: Beverages',
    '制造业--黑色金属冶炼和压延加工业': 'Manufacturing: Ferrous Metals',
    '制造业--通用设备制造业': 'Manufacturing: General Equipment',
    '交通运输、仓储和邮政业--水上运输业': 'Transport: Water',
    '采矿业--煤炭开采和洗选业': 'Mining: Coal',
    '采矿业--有色金属矿采选业': 'Mining: Non-ferrous Metals',
    '交通运输、仓储和邮政业--航空运输业': 'Transport: Aviation',
    '制造业--化学纤维制造业': 'Manufacturing: Chemical Fibers',
    '制造业--橡胶和塑料制品业': 'Manufacturing: Rubber & Plastics',
    '房地产业--房地产业': 'Real Estate',
    '制造业--金属制品业': 'Manufacturing: Metal Products',
    '信息传输、软件和信息技术服务业--互联网和相关服务': 'IT: Internet Services',
    '金融业--其他金融业': 'Financials: Other',
    '批发和零售业--批发业': 'Wholesale & Retail: Wholesale',
    '采矿业--开采辅助活动': 'Mining: Support Activities',
    '制造业--农副食品加工业': 'Manufacturing: Food Processing',
    '批发和零售业--零售业': 'Wholesale & Retail: Retail',
    '交通运输、仓储和邮政业--道路运输业': 'Transport: Road',
    '信息传输、软件和信息技术服务业--电信、广播电视和卫星传输服务': 'IT: Telecom & Broadcasting',
    '租赁和商务服务业--商务服务业': 'Leasing & Business Services',
    '金融业--保险业': 'Financials: Insurance',
    '制造业--食品制造业': 'Manufacturing: Food',
    '水利、环境和公共设施管理业--生态保护和环境治理业': 'Utilities: Environment',
    '科学研究和技术服务业--专业技术服务业': 'Science & Tech: Professional Services',
    '采矿业--石油和天然气开采业': 'Mining: Oil & Gas',
    '农、林、牧、渔业--畜牧业': 'Agriculture: Livestock',
    '农、林、牧、渔业--农业': 'Agriculture: Crop',
    '文化、体育和娱乐业--广播、电视、电影和影视录音制作业': 'Media & Entertainment',
    '卫生和社会工作--卫生': 'Healthcare',
    '交通运输、仓储和邮政业--邮政业': 'Transport: Postal',
    '文化、体育和娱乐业--新闻和出版业': 'Media: Publishing',
    '科学研究和技术服务业--研究和试验发展': 'Science & Tech: R&D',
    '制造业--仪器仪表制造业': 'Manufacturing: Instruments',
    '制造业--其他制造业': 'Manufacturing: Other',
    '交通运输、仓储和邮政业--铁路运输业': 'Transport: Railway',
    '制造业--纺织服装、服饰业': 'Manufacturing: Apparel',
    '制造业--造纸和纸制品业': 'Manufacturing: Paper',
    '制造业--家具制造业': 'Manufacturing: Furniture',
    '电力、热力、燃气及水生产和供应业--燃气生产和供应业': 'Utilities: Gas',
    '文化、体育和娱乐业--文化艺术业': 'Media: Arts & Culture',
    '电力、热力、燃气及水生产和供应业--水的生产和供应业': 'Utilities: Water',
    '制造业--石油加工、炼焦和核燃料加工业': 'Manufacturing: Petroleum & Nuclear',
    '交通运输、仓储和邮政业--装卸搬运和运输代理业': 'Transport: Logistics',
    '制造业--文教、工美、体育和娱乐用品制造业': 'Manufacturing: Cultural & Sports Goods',
    '住宿和餐饮业--住宿业': 'Hospitality: Accommodation',
    '制造业--纺织业': 'Manufacturing: Textiles',
    '制造业--废弃资源综合利用业': 'Manufacturing: Recycling',
    '建筑业--建筑安装业': 'Construction: Installation',
    '科学研究和技术服务业--科技推广和应用服务业': 'Science & Tech: Tech Promotion',
    '租赁和商务服务业--租赁业': 'Leasing',
    '综合--综合': 'Conglomerates',
    '采矿业--黑色金属矿采选业': 'Mining: Ferrous Metals',
    '金融业--资本市场服务--期货市场服务--其他期货市场服务': 'Financials: Futures Market'
}

#Translating name's industries
merged_data['Industry_ENG'] = merged_data['CSRC Industry Name'].map(translate_dict).fillna(merged_data['CSRC Industry Name'])
industry_df = merged_data.groupby(['CSRC Industry Name', 'Industry_ENG'])['code'].nunique().reset_index()
industry_df.columns = ['CSRC Industry Name (Chinese)', 'Industry Name (English)', 'Number_of_Companies']
industry_df = industry_df.sort_values('Number_of_Companies', ascending=False)

#Saving all list of industries and them's amount
industry_df.to_csv('1_industry_full_list.csv', index=False, encoding='utf-8-sig')

#Will use for plot
industry_counts = industry_df.set_index('Industry Name (English)')['Number_of_Companies'].sort_values(ascending=False)
#Visualisation
plt.figure(figsize=(12, 8))
industry_counts.head(15).plot(kind='barh', color='skyblue', edgecolor='black')
plt.title('Top 15 Industries by Number of Companies', fontsize=14)
plt.xlabel('Number of Companies', fontsize=12)
plt.ylabel('Industry', fontsize=12)
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('1_industry_distribution.png', dpi=300)
plt.close()

#1.9 Creating new indicators for main industries
merged_data['CSRC Industry Name'] = merged_data['CSRC Industry Name'].map(translate_dict).fillna(merged_data['CSRC Industry Name']) #translating into english
#New indicators
merged_data['is_financial'] = merged_data['CSRC Industry Name'].str.contains('Financials', na=False).astype(int)
merged_data['is_tech'] = merged_data['CSRC Industry Name'].str.contains('IT:|Computers & Electronics', na=False).astype(int)
merged_data['is_manufacturing'] = (
    merged_data['CSRC Industry Name'].str.contains('Manufacturing', na=False) &
    (merged_data['is_tech'] == 0)
).astype(int)
#Save for readme
#-----------------------------------------------------------
readme_data['n_tech'] = merged_data[merged_data['is_tech'] == 1]['code'].nunique()
readme_data['n_financial'] = merged_data[merged_data['is_financial'] == 1]['code'].nunique()
readme_data['n_manufacturing'] = merged_data[merged_data['is_manufacturing'] == 1]['code'].nunique()
readme_data['n_other'] = readme_data['n_companies'] - (readme_data['n_tech'] + readme_data['n_financial'] + readme_data['n_manufacturing'])
#-----------------------------------------------------------









#1. Saving full data set
merged_data.to_csv('1_Cleaning_China_Panel_Data.csv', index=False)


#-----------------------------------------------------------------------------------------------------------------------
#1_README.md
#-----------------------------------------------------------------------------------------------------------------------
with open('1_README_Cleaning_China_Panel_Data.md', 'w', encoding='utf-8') as f:
    f.write("# Data Preprocessing Report: China A-Share (CSI 300 + CSI 500)\n\n")

    f.write("## 1. General Information\n")
    f.write(f"- **Number of companies:** {readme_data['n_companies']}\n")
    f.write(f"- **Time period:** {readme_data['date_min']} to {readme_data['date_max']}\n")

    f.write("## 2. Return Calculation & Trading Suspensions\n")
    f.write("We calculated daily returns using the previous closing price. ")
    f.write("Days with zero trading volume (`amount_cny == 0`) were removed as they represent trading suspensions. ")
    f.write("Calculating Amihud (Return / Amount) with zero volume leads to mathematical undefined values.\n\n")
    f.write(f"- **Rows removed (zero volume):** {readme_data['rows_removed_zero_volume']:,}\n")
    f.write(f"- **Rows remaining after cleaning:** {readme_data['rows_after_zero_volume']:,}\n\n")

    f.write("## 3. Monthly Aggregation & Filtering Short Months\n")
    f.write(
        "Daily data was aggregated to a monthly panel. We calculated monthly average return, volatility (std), average Amihud, and average volume. ")
    f.write(
        "To ensure the representativeness of monthly liquidity metrics, we **excluded months with fewer than 10 trading days**.\n\n")
    f.write(f"- **Rows removed (short months):** {readme_data['rows_removed_short_months']:,}\n")
    f.write(f"- **Final monthly observations:** {readme_data['final_monthly_rows']:,}\n\n")

    f.write("## 4. Financial Data Integration\n")
    f.write(
        "Annual financial data (Total Assets, Liabilities, Net Profit) was merged with the monthly liquidity panel. ")
    f.write(
        "We calculated three key control variables: **Size** (ln of total assets), **Leverage** (total liabilities / total assets), and **ROA** (net profit / total assets).\n\n")
    f.write(f"- **Initial financial records:** {readme_data['financials_initial_rows']:,}\n")
    f.write(f"- **Duplicate financial records removed:** {readme_data['financials_duplicates_removed']:,}\n")
    f.write(f"- **Rows before financial merge:** {readme_data['rows_before_merge']:,}\n")
    f.write(f"- **Rows after financial merge:** {readme_data['rows_after_financial_merge']:,}\n\n")

    f.write("## 5. Industry Classification\n")
    f.write(f"The sample covers **{readme_data['n_companies']}** companies across various CSRC industries. ")
    f.write("The distribution is concentrated in manufacturing, IT, and financial sectors.\n\n")

    f.write("![Industry Distribution](industry_distribution.png)\n\n")

    f.write("### Sector Flags Created\n")
    f.write(f"- **Tech companies:** {readme_data['n_tech']}\n")
    f.write(f"- **Financial companies:** {readme_data['n_financial']}\n")
    f.write(f"- **Manufacturing companies:** {readme_data['n_manufacturing']}\n")
    f.write(f"- **Other sectors:** {readme_data['n_other']}\n\n")

    f.write("### Full Industry Breakdown\n")
    f.write("| Industry Name | Number of Companies |\n")
    f.write("| :--- | :--- |\n")
    for _, row in industry_df.iterrows():
        f.write(f"| {row['Industry Name (English)']} | {row['Number_of_Companies']} |\n")
    f.write("\n")



