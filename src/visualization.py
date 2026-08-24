import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .analysis import fit_linear_regression

def plot_ranked_bar(
    categories,
    values,
    xlabel: str,
    ylabel: str,
    title: str,
    reference_line: float = None,
    reference_label: str = None,
    color=None,
    figsize=(15, 8),
):
    """Horizontal bar chart, optionally with a vertical reference line (e.g. an index baseline of 100)."""
    fig, ax = plt.subplots(figsize=figsize)
    ax.barh(categories, values, color=color)

    if reference_line is not None:
        ax.axvline(reference_line, color="red", linestyle="--", linewidth=2, label=reference_label)
        ax.legend()

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    plt.tight_layout()
    plt.show()


def plot_scatter_with_trend(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    label_col: str,
    xlabel: str,
    ylabel: str,
    title: str,
    subtitle: str = None,
    eu27_x: float = 100,
    eu27_y: float = None,
    eu27_y_label: str = None,
    color: str = "tab:blue",
    figsize=(12, 8),
) -> dict:
    """
    Scatter plot of x vs y with each point labelled, a fitted linear-trend line, and optional EU27
    reference lines on both axes. Returns the regression dict from `fit_linear_regression` so the
    caller can reuse the fit (e.g. for a residual analysis) instead of refitting it.
    """
    fig, ax = plt.subplots(figsize=figsize)
    fig.suptitle(title, fontsize=18, fontweight="bold")
    if subtitle:
        ax.set_title(subtitle, fontsize=12, pad=10)

    x, y = df[x_col], df[y_col]
    ax.scatter(x, y, color=color)

    for _, row in df.iterrows():
        ax.annotate(row[label_col], (row[x_col], row[y_col]), xytext=(5, 5), textcoords="offset points")

    reg = fit_linear_regression(x, y)
    x_line = np.linspace(x.min(), x.max(), 100)
    y_line = reg["slope"] * x_line + reg["intercept"]
    ax.plot(x_line, y_line, color="black", linewidth=2, label="Linear trend")

    if eu27_x is not None:
        ax.axvline(eu27_x, color="red", linestyle="--", linewidth=1.5, label=f"EU27 PLI = {eu27_x}")
    if eu27_y is not None:
        label = eu27_y_label or f"EU27 reference = {eu27_y:,.2f}"
        ax.axhline(eu27_y, color="green", linestyle="--", linewidth=1.5, label=label)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend()
    plt.show()

    return reg


def plot_dumbbell_chart(
    df: pd.DataFrame,
    category_col: str,
    value_1_col: str,
    value_2_col: str,
    sort_col: str,
    value_1_label: str,
    value_2_label: str,
    xlabel: str,
    ylabel: str,
    title: str,
    reference_line: float = None,
    reference_label: str = None,
    color_1: str = "steelblue",
    color_2: str = "darkorange",
    line_color: str = "gray",
    figsize=(10, 12),
):
    """
    Dumbbell-style comparison plot for two scenarios.

    Each category is represented by two values connected by a line.
    Categories are ordered according to `sort_col`.
    An optional vertical reference line can be added.
    """

    df_plot = df.sort_values(sort_col).copy()

    fig, ax = plt.subplots(figsize=figsize)

    fig.suptitle(
        title,
        fontsize=18,
        fontweight="bold"
    )

    y_positions = range(len(df_plot))

    for i, (_, row) in enumerate(df_plot.iterrows()):

        # Connecting line between the two scenarios
        ax.plot(
            [row[value_1_col], row[value_2_col]],
            [i, i],
            color=line_color,
            linewidth=2,
            alpha=0.6,
        )

        # Scenario 1
        ax.scatter(
            row[value_1_col],
            i,
            color=color_1,
            s=70,
            label=value_1_label if i == 0 else "",
        )

        # Scenario 2
        ax.scatter(
            row[value_2_col],
            i,
            color=color_2,
            s=70,
            label=value_2_label if i == 0 else "",
        )

    ax.set_yticks(list(y_positions))
    ax.set_yticklabels(df_plot[category_col])

    if reference_line is not None:
        ax.axvline(
            reference_line,
            color="black",
            linestyle="--",
            linewidth=1.5,
            alpha=0.7,
            label=reference_label,
        )

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    ax.legend()

    plt.tight_layout()
    plt.show()