import numpy as np
import pandas as pd


def fit_linear_regression(x: pd.Series, y: pd.Series) -> dict:
    """
    Fit y = slope * x + intercept by least squares (equivalent to a single-variable OLS regression).
    Returns slope, intercept, fitted values, residuals, Pearson correlation and R-squared in one call,
    so the fit only has to be computed once and reused everywhere it's needed.
    """
    slope, intercept = np.polyfit(x, y, 1)
    predicted = slope * x + intercept
    residuals = y - predicted
    correlation = np.corrcoef(x, y)[0, 1]
    r_squared = correlation ** 2
    return {
        "slope": slope,
        "intercept": intercept,
        "predicted": predicted,
        "residuals": residuals,
        "correlation": correlation,
        "r_squared": r_squared,
    }


def compute_affordability_index(
    df: pd.DataFrame,
    pli_col: str,
    earnings_col: str,
    eu27_earnings: float,
    suffix: str = "",
) -> pd.DataFrame:
    """
    Add three derived columns to a copy of df:
      - earnings_index{suffix}:      earnings as a % of the EU27 reference (EU27 = 100)
      - earnings_to_pli{suffix}:     earnings divided by the price level index (purchasing-power proxy)
      - affordability_index{suffix}: earnings_to_pli rescaled so the EU27 average = 100,
                                      i.e. how far a country's "real" earning power is from the EU27 norm
    `suffix` lets you compute this twice in the same notebook (e.g. "_50" for the 50%-earner scenario)
    without column name clashes.
    """
    df = df.copy()
    df[f"earnings_index{suffix}"] = (df[earnings_col] / eu27_earnings) * 100
    df[f"earnings_to_pli{suffix}"] = df[earnings_col] / df[pli_col]
    df[f"affordability_index{suffix}"] = (df[f"earnings_to_pli{suffix}"] / (eu27_earnings / 100)) * 100
    return df