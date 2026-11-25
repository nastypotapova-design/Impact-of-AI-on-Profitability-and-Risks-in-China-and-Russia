# Data Preprocessing Report: China A-Share (CSI 300 + CSI 500)

## 1. General Information
- **Number of companies:** 799
- **Time period:** 2016-01-04 to 2025-12-31
## 2. Return Calculation & Trading Suspensions
We calculated daily returns using the previous closing price. Days with zero trading volume (`amount_cny == 0`) were removed as they represent trading suspensions. Calculating Amihud (Return / Amount) with zero volume leads to mathematical undefined values.

- **Rows removed (zero volume):** 7,239
- **Rows remaining after cleaning:** 1,637,759

## 3. Monthly Aggregation & Filtering Short Months
Daily data was aggregated to a monthly panel. We calculated monthly average return, volatility (std), average Amihud, and average volume. To ensure the representativeness of monthly liquidity metrics, we **excluded months with fewer than 10 trading days**.

- **Rows removed (short months):** 333
- **Final monthly observations:** 81,041

## 4. Financial Data Integration
Annual financial data (Total Assets, Liabilities, Net Profit) was merged with the monthly liquidity panel. We calculated three key control variables: **Size** (ln of total assets), **Leverage** (total liabilities / total assets), and **ROA** (net profit / total assets).

- **Initial financial records:** 8,000
- **Duplicate financial records removed:** 0
- **Rows before financial merge:** 81,041
- **Rows after financial merge:** 81,041

## 5. Industry Classification
The sample covers **799** companies across various CSRC industries. The distribution is concentrated in manufacturing, IT, and financial sectors.

![Industry Distribution](industry_distribution.png)

### Sector Flags Created
- **Tech companies:** 179
- **Financial companies:** 86
- **Manufacturing companies:** 357
- **Other sectors:** 177

### Full Industry Breakdown
| Industry Name | Number of Companies |
| :--- | :--- |
| Manufacturing: Computers & Electronics | 128 |
| Manufacturing: Pharmaceuticals | 50 |
| Manufacturing: Electrical Machinery | 47 |
| Manufacturing: Special Equipment | 44 |
| Financials: Capital Markets | 43 |
| IT: Software & Services | 38 |
| Manufacturing: Chemicals | 34 |
| Utilities: Power & Heat | 31 |
| Financials: Banking | 30 |
| Manufacturing: Automobiles | 26 |
| Manufacturing: Transport Equipment | 23 |
| Manufacturing: Non-ferrous Metals | 23 |
| Manufacturing: Non-metallic Minerals | 15 |
| Construction: Civil Engineering | 15 |
| Manufacturing: Beverages | 15 |
| Manufacturing: Ferrous Metals | 13 |
| Manufacturing: General Equipment | 13 |
| Transport: Water | 12 |
| Mining: Coal | 12 |
| Mining: Non-ferrous Metals | 11 |
| Transport: Aviation | 10 |
| Manufacturing: Chemical Fibers | 10 |
| Manufacturing: Rubber & Plastics | 9 |
| Real Estate | 9 |
| Manufacturing: Metal Products | 8 |
| IT: Internet Services | 8 |
| Financials: Other | 7 |
| Wholesale & Retail: Wholesale | 7 |
| Mining: Support Activities | 7 |
| Manufacturing: Food Processing | 7 |
| Wholesale & Retail: Retail | 5 |
| Transport: Road | 5 |
| IT: Telecom & Broadcasting | 5 |
| Leasing & Business Services | 5 |
| Financials: Insurance | 5 |
| Manufacturing: Food | 5 |
| Utilities: Environment | 4 |
| Science & Tech: Professional Services | 4 |
| Mining: Oil & Gas | 4 |
| Agriculture: Livestock | 4 |
| Agriculture: Crop | 3 |
| Media & Entertainment | 3 |
| Healthcare | 3 |
| Transport: Postal | 3 |
| Media: Publishing | 3 |
| Science & Tech: R&D | 2 |
| Manufacturing: Instruments | 2 |
| Manufacturing: Other | 2 |
| Transport: Railway | 2 |
| Manufacturing: Apparel | 2 |
| Manufacturing: Paper | 2 |
| Manufacturing: Furniture | 2 |
| Utilities: Gas | 2 |
| Media: Arts & Culture | 2 |
| Utilities: Water | 2 |
| Manufacturing: Petroleum & Nuclear | 2 |
| Transport: Logistics | 1 |
| Manufacturing: Cultural & Sports Goods | 1 |
| Hospitality: Accommodation | 1 |
| Manufacturing: Textiles | 1 |
| Manufacturing: Recycling | 1 |
| Construction: Installation | 1 |
| Science & Tech: Tech Promotion | 1 |
| Leasing | 1 |
| Conglomerates | 1 |
| Mining: Ferrous Metals | 1 |
| Financials: Futures Market | 1 |

