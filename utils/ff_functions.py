import pandas as pd
from utils.GRS.GRS import GRS
import numpy as np
import statsmodels.api as sm

def ff_monthly_loader(path, skiprows):
    """ Loads monthly data from Ken French CSV file with multiple yearly/monthly data tables.
    It finds the first monthly observation and the end of the table, dropping everything else"""

    df = pd.read_csv(path, skiprows=skiprows)

    date_col = df.columns[0]
    # Converting to string
    s = df[date_col].astype(str)

    # Matches observation with the format
    is_month = s.str.match(r'^\d{6}$')

    # First monthly observation
    start = is_month.idxmax()

    # Keep rows from first obvs until next row breaks pattern
    end = start
    while end + 1 in is_month.index and is_month.loc[end + 1]:
        end += 1

    # Slicing df
    df = df.loc[start:end].copy()

    # Renaming date col to Date
    df = df.rename(columns={date_col: 'Date'})
    #Parsing to datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%Y%m')

    return df

def create_coef_table(result: dict, factors: list[str]) -> pd.DataFrame:
    """ Creates coefficient table from result dictionary """
    rows = []

    for p, m in result.items():
        row = {
            'Portfolio': p,
            'alpha': m.params.get('const'),
            't_alpha': m.tvalues.get('const'),
            'p_alpha': round(m.pvalues.get('const'), 4),
            'R2': m.rsquared,
        }

        # Additional betas
        for f in factors:
            row[f"beta{f}"] = m.params.get(f)

        rows.append(row)

    return pd.DataFrame(rows)

def summarise_table(coef_table: pd.DataFrame, sig_level: float = 0.05):
    """
    Summarises coefficient table giving mean absolute alpha, percentage of portfolios with significant alphas,
    mean R squared and no. of portfolios.
    """
    rows = pd.Series({
        'mean[|alpha|)' : coef_table['alpha'].abs().mean(),     # average of abs value
        f"% sig alpha (<{sig_level})": (coef_table['p_alpha'] < sig_level).mean() * 100, # stat significant portfolio a
        "mean(R2)": coef_table['R2'].mean(),
        'n_portfolios' : len(coef_table),
    })
    return rows

def run_GRS(df, portfolio_cols, factor_cols):
    """Fits time-series regressions for each portfolio and runs GRS test using alphas, residuals and factor returns"""
    X = sm.add_constant(df[factor_cols])
    T = df.shape[0]
    N = len(portfolio_cols)

    alphas = np.empty((N, 1), dtype=float)
    resids = np.empty((T, N), dtype=float)

    for j, p in enumerate(portfolio_cols):
        y = df[p]
        fit = sm.OLS(y, X).fit()
        alphas[j, 0] = fit.params["const"]
        resids[:, j] = fit.resid.to_numpy()

    mu = df[factor_cols].to_numpy()
    F_stat, pVal = GRS(alphas, resids, mu)

    return F_stat, pVal, alphas, resids