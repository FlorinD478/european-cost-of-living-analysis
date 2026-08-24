
from pathlib import Path
import pandas as pd

GEO_COL = "geo"

def list_raw_files(raw_dir: Path) -> None:
    """Print each file in raw_dir with its size, so you can sanity-check what's available."""
    for file in raw_dir.iterdir():
        print(file.name, "-", file.stat().st_size, "bytes")


def load_csv_with_preview(path: Path, n_preview_lines: int = 10, encoding: str = "utf-8") -> pd.DataFrame:
    """
    Print the first `n_preview_lines` of a CSV (useful for eyeballing structure/encoding issues
    before pandas parses it), then load and return the full file as a DataFrame.
    """
    with open(path, "r", encoding=encoding) as file:
        for _ in range(n_preview_lines):
            line = file.readline()
            if not line:
                break
            print(line.rstrip())
    return pd.read_csv(path)


def check_data_quality(df: pd.DataFrame, id_col: str, value_col: str) -> None:
    """Print duplicate-id and missing-value counts, the two most basic sanity checks for this dataset."""
    n_duplicates = df[id_col].duplicated().sum()
    n_missing = df[value_col].isna().sum()
    print(f"Duplicate '{id_col}' values: {n_duplicates}")
    print(f"Missing '{value_col}' values: {n_missing}")


def exclude_geo_codes(df: pd.DataFrame, codes_to_exclude: list, geo_col: str = GEO_COL) -> pd.DataFrame:
    """Return a copy of df with the given geo codes (e.g. non-EU countries or an aggregate row) removed."""
    return df[~df[geo_col].isin(codes_to_exclude)].copy()


def get_reference_value(df: pd.DataFrame, geo_col: str, geo_value: str, value_col: str) -> float:
    """Look up a single scalar value for one geo code, e.g. the EU27 aggregate's OBS_VALUE."""
    return df.loc[df[geo_col] == geo_value, value_col].iloc[0]