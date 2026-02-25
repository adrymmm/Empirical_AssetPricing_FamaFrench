## Empirical Application of the Fama-French Three-Factor and Five-Factor Model
### Overview
The project is an implementation of the Three-Factor asset pricing model following the framework of Fama and French
introduced in *Common Risk Factors in the Returns on Stocks and Bonds (1993).*

The aim of the project is to assess the performance of factor-based models (FF3, FF5) as compared to the traditional
Capital Asset Pricing Model (CAPM). The metric that they will be judged on is **systematic average pricing error**.

Project Outline:
+ Estimation of CAPM, Fama-French Three-Factor (FF3) and Fama-French Five-Factor (FF5) models
+ Evaluation of pricing performance for each model across test portfolios
+ Comparison of systematic pricing error (α) across models
+ Gibbons-Ross-Shanken (GRS) test for joint model validity


### Three-Factor Model Explained
Fama and French argue that that firm size and book-to-market characteristic can accurately proxy for a firm's exposure to
systematic risk. Since the risk 
factors are not directly observable, they construct **factor-mimicking** portfolios to capture common sources of variation
in stock returns. 

Stocks are ranked market equity and divided into *Small* and *Big* groups. Each size group is then sorted into three
book-to-market categories: Low, Medium and High. This results in the construction of six value-weighted portfolios
corresponding to stock size and BE/ME group.

The factors are then constructed as such:

+ Excess market return (MKT) - overall market factor
  + Excess return on a portfolio of all stocks in the sample less the one-month Treasury bill rate
  + $RM - RF$ 
+ Small Minus Big (SMB)
  + Monthly difference between the value-weighted average returns of the three small portfolios and the three big portfolios
+ High Minus Low (HML)
  + Monthly difference between the average returns of the two high BE/ME portfolios and the two low BE/ME portfolios.

These factors are used in time-series regressions where excess portfolio returns are regressed on the exposure to risk
factors:

$$R_{i,t} - R_{f,t} = \alpha_i + \beta_{i,M}(R_M - R_f)_t + \beta_{i,S}SMB_t + \beta_{i,H}HML_t + \varepsilon_{i,t}$$

The coefficients estimated then represent **factor loadings**, the sensitivity of portfolio returns to each risk factor.

Given that we are correctly appraising an asset the expected asset returns should be explained in full by the
explanatory factors:

$$E[R_{i,t} - R_{f,t}] =  E[\beta_{i,M}(R_M - R_f)_t] + E[\beta_{i,S}SMB_t] + E[\beta_{i,H}HML_t]$$

So that $α_i = 0$.

Model quality is then evaluated on the systematic average pricing error of each portfolio: $α_i$.
If alpha is **not statistically significant from zero**, we have a good indication that the model predicts returns accurately on average. 

The 
**Gibbons-Ross-Shanken (GRS)** test is then testing the null hypothesis that the alphas for all portfolios are jointly zero:

$$ H_0 : α_1 = α_2 =...= α_n=0 $$

By failing to reject the null we receive a strong signal that the model is not pricing with systematic error, while if
we reject then at least one portfolio is being priced with systematic error.

### Five-Factor Extension
The Fama-French Five-Factor Model adapted from *A five-factor asset pricing model (2015)* adds an additional two factors:
+ Profitability (RMW)
+ Investment (CMA)
The extension adds two additional risk dimensions and the evaluation process is repeated

### Extension

### The Pipeline
#### 01_data_cleaning.ipynb
+ Import Fama-French FF5 and 25 portfolio data
  + 25 Portfolios 5x5 Size/ME 
    + Portfolios formed from sort of stocks into five **size** quintiles and five **B/M** quintiles
  + 25 Portfolios 5x5 Size/OP
    + Portfolios from sort of stocks into five **size** quintiles and five **profitability** quintiles
  + 25 Portfolios 5x5 Size/INV
    + Portfolios from sort of stocks into five **size** quintiles and five **investment** quintiles
  + 32 Portfolio 2x4x4 Size/ME/OP
    + Portfolios from sort of stocks into two **size** groups and independently into four
    **B/M** and four **profitability** groups
  + 32 Portfolio 2x4x4 Size/ME/INV
    + Portfolios from sort of stocks into two **size** groups and independently into four
    **B/M** and four **investment** groups
+ Parse dates and extract the correct table on **monthly data**
+ Save dataframes in .parquet format

#### 02_regressions.ipynb
+ Load processed dataframes
+ WIPP...
+ Parse dates
+ Regress **each portfolio's** excess return ($R_{i,t} - R_{f,t}$) on:
  + Market excess return ($R_{M,t} - R_{f,t}$)
  + Size factor (${SMB}_t$)
  + Value factor (${HML}_t$)
+ Run CAPM regressions on each portfolio
+ Compare CAPM with FF3 on pricing errors (α) and explanatory power ($R^2$)
+ Run Gibson-Ross-Shanken (GRS) test for joint model validity

### 03_GRS_test.ipynb

### References
Fama, E. F., & French, K. R. (1993).
Common Risk Factors in the Returns on Stocks and Bonds.
Journal of Financial Economics.

Fama, E. F. & French, K. R. (2015)
A five-factor asset pricing model.
Journal of Financial Economics.
