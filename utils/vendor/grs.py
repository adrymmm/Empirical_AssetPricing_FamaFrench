import numpy as np
from numpy.linalg import inv
from scipy.stats import f

"""
GRS Test Implementation

Original author: <anusar80>
Source: https://github.com/anusar80/GRS

Modifications:  - added scipy.stats f module
                - fixed factor covariance calculation
                - Switched @ instead of np.matmul
                - np.squeeze() squeezes redundant dimensions in line 33, giving python scalar

"""

def GRS(alpha, resids, mu):
    # GRS test statistic
    # N assets, L factors, and T time points
    # alpha is a Nx1 vector of intercepts of the time-series regressions,
    # resids is a TxN matrix of residuals,
    # mu is a TxL matrix of factor returns
    T, N = resids.shape
    L = mu.shape[1]
    mu_mean = np.nanmean(mu, axis=0)
    cov_resids = np.matmul(resids.T, resids) / (T-L-1)
    # cov_fac = np.matmul(np.array(mu - np.nanmean(mu, axis=0)).T, np.array(mu - np.nanmean(mu, axis=0))) / T-1
    cov_fac = ((mu - np.nanmean(mu, axis=0)).T @ (mu - np.nanmean(mu, axis=0))) / (T - 1)
    GRS_stat = (T / N) * ((T - N - L) / (T - L - 1)) * (
                (alpha.T @ inv(cov_resids) @ alpha) / (1 + (mu_mean.T @ inv(cov_fac) @ mu_mean)))
    GRS_stat = float(np.squeeze(GRS_stat))  # flatten (1,1) matrix to scalar
    pVal = float(np.squeeze(1 - f.cdf(GRS_stat, N, T - N - L)))
    return GRS_stat, pVal
