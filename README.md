# Empirical Application of the Fama-French Three-Factor and Five-Factor Model
## Overview
The project is an implementation of the Three-Factor asset pricing model following the framework of Fama and French
introduced in *Common Risk Factors in the Returns on Stocks and Bonds (1993).*

The aim of the project is to assess the performance of factor-based models (FF3, FF5) as compared to the traditional
Capital Asset Pricing Model (CAPM). The metric that they will be judged on is **systematic average pricing error**.

Project Outline:
+ Estimation of CAPM, Fama-French Three-Factor (FF3) and Fama-French Five-Factor (FF5) models
+ Evaluation of pricing performance for each model across test portfolios
+ Comparison of systematic pricing error (α) across models
+ Gibbons-Ross-Shanken (GRS) test for joint model validity


## Three-Factor Model Explained
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

## Five-Factor Extension
The Fama-French Five-Factor Model adapted from *A five-factor asset pricing model (2015)* adds an additional two factors:
+ Profitability (RMW)
+ Investment (CMA)
The extension adds two additional risk dimensions and the evaluation process is repeated

## The Pipeline
#### 01_data_cleaning.ipynb
+ Import Fama-French FF5 and 25 portfolio data
+ Parse dates and extract the correct table on **monthly data**
+ Save dataframes in .parquet format

#### 02_regressions.ipynb
- Load and date-filter data to July 1963 - December 2013
- Convert portfolio returns to excess returns by subtracting RF
- Run time-series regressions for CAPM, FF3 and FF5 across all three portfolio sets
- Evaluate pricing performance via mean |α|, % significant alphas and R²
- Compare model performance across portfolio sets

#### 03_GRS_tests.ipynb
- Run Gibbons-Ross-Shanken (GRS) joint significance test for CAPM, FF3 and FF5
- Compare F-statistics across models and portfolio sets
- Assess whether pricing errors are jointly zero

### Results

### Regression Summaries
#### Regression Summary

| Model | Mean \|α\| | % Sig. α | Mean R² |
|-------|-----------|----------|---------|
| CAPM  | 0.246%    | 46.7%    | 0.774   |
| FF3   | 0.103%    | 24.0%    | 0.914   |
| FF5   | 0.081%    | 17.3%    | 0.927   |

*Figures are averages across the three portfolio sets (SIZE, INV, OP).*

FF5 reduces mean monthly pricing error by ~70% relative to CAPM. The largest single 
improvement comes from CAPM to FF3, with SMB and HML reducing mean |α| by ~58%. The 
addition of profitability and investment factors *(RMW, CMA)* in FF5 leads to further 
improvements, particularly in the investment and profitability portfolio sets. Under a 
correctly specified model the percentage of significant alphas *(% Sig. α)* we would 
expect to see would be ~5%, so FF3 *(24.0%)* and FF5 *(17.3%)* both remain above this 
benchmark. The size portfolio set was shown to be the hardest to price, with FF5 
exhibiting a slight increase in % significant alphas relative to FF3, consistent with 
Fama and French (2015).

### GRS Tests

| Model | SIZE F | INV F | OP F |
|-------|--------|-------|------|
| CAPM  | 4.45   | 5.51  | 2.41 |
| FF3   | 3.55   | 4.69  | 2.54 |
| FF5   | 2.89   | 3.42  | 2.20 |

All three models are rejected by the GRS test, consistent with Fama and French (2015). 
However, the F-statistic declines monotonically from CAPM to FF3 to FF5 across all 
portfolio sets, indicating progressive improvement in pricing performance. FF5 is 
particularly strong on investment and profitability portfolios where the RMW and CMA factors are 
directly relevant. The size portfolio set remains the hardest to price across all models.

### How to Run

1. Clone the repository
2. Install dependencies with Poetry: `poetry install`
3. Run notebooks in order: `01_data_cleaning.ipynb` → `02_regressions.ipynb` → `03_GRS_tests.ipynb`

### References
Fama, E. F., & French, K. R. (1993).
Common Risk Factors in the Returns on Stocks and Bonds.
Journal of Financial Economics.

Fama, E. F. & French, K. R. (2015)
A five-factor asset pricing model.
Journal of Financial Economics.
