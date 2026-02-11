## Reproduction and extension of common risk factors in the returns on stocks and bonds (Fama and French, 1993)
### Paper Overview
In Common Risk Factors in the Returns on Stocks and Bonds (1993), Fama and French identify patterns in average stock
returns which the traditional Capital Asset Pricing Model fails to explain. In particular, they note that the market βs
taken from the CAPM model show little explanatory paper on the average returns of U.S. stocks in their 
cross-sectional analysis. They then determine two variables that reliably explain the cross-section of average returns:

+ Size (ME) - Market equity
+ Book-to-Market Equity (BE/ME) - Ratio of the book value of a firm's stock to its market value

They conclude that there is a negative relation between size and average return, and a strong positive relation between
BE/ME and average return.

### Replication
The project begins at the stage where Fama and French investigate proxies for common risk factors in average stock
returns. The assumption is that if assets are priced rationally, such factors as firm size and BE/ME can accurately
stand in for a firms sensitivity to undiversifiable risk factors, shared by all firms in the market. Since the risk 
factors are not observable, Fama and French construct **factor-mimicking** portfolios to act as proxies. They begin by 
ranking stocks by size and splitting them into a *Small* and *Big* group. They then sort the small and big stocks into 3
book-to-market groups:Low, Medium and High. This results in the construction of six portfolios corresponding to stock
size and BE/ME group.

The factors are then constructed as such:

+ Excess market return (MKT) - overall market factor
  + Excess return on a portfolio of all stocks in the sample less the one-month Treasury bill rate
  + $RM - RF$ 
+ Small Minus Big (SMB)
  + Monthly difference between the value-weighted average returns of the three small portfolios and the three big portfolios
+ High Minus Low (HML)
  + Monthly difference between the average returns of the two high BE/ME portfolios and the two low BE/ME portfolios.

These factors are used in time-series regressions where monthly returns on various portfolios are regressed on the
returns of the risk factors:

$$R_i,t - R_f,t = α_i + β_iF_t + ε_i,t$$

The coefficients estimated then represent **factor loadings**, the sensitivty of an asset's
return to a given risk factor.

Given that we are correctly appraising an asset the expected asset returns should be explained in full by the
explanatory factors:

$$E[R_i-R_f] = β_iE[f]$$

So that $α_i = 0$. Model quality is then evaluated on the systematic average pricing error of each portfolio: $α_i$.
If alpha is small and significant we have a good indication that the model predicts returns accurately on average. The 
Gibson-Ross-Shanken test is then testing the null that the alphas for all portfolios are jointly zero:
$$ H_0 : α_1 = α_2 =...= α_n=0 $$
By failing to reject the null we receive a strong signal that the model is not pricing with systematic error, while if
we reject then at least one portfolio is being priced with systematic error.


### Extension

### The Pipeline
#### 01_data_cleaning.ipynb
+ Import Fama-French FF5 and 25 size-to-book portfolio data
+ Parse dates and extract the correct table on **monthly data**
+ Save dataframes in .parquet format

#### 02_replication.ipynb
+ Load processed dataframes
+ Restrict FF5 portfolio columns to only cover FF3 factors
+ Filter dates to date range Fama and French used (1963-1991)
+ Exploratory analysis with descriptive statistics
+ Regress **each portfolio's** excess return ($R_{i,t} - R_{f,t}$) on:
  + Market excess return ($R_{M,t} - R_{f,t}$)
  + Size factor (${SMB}_t$)
  + Value factor (${HML}_t$)
+ Run CAPM regressions on each portfolio
+ Compare CAPM with FF3 on pricing errors (α) and explanatory power ($R^2$)
+ Run Gibson-Ross-Shanken (GRS) test for joint model validity

### 03_extensions.ipynb

