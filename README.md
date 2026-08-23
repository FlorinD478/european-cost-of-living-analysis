# European Cost of Living and Net Earnings

## EU27 comparison of earnings, price levels and affordability

This project investigates the relationship between **price levels and net earnings across the 27 European Union Member States**.

The central question is:

> **Where does income provide the greatest relative purchasing power after accounting for differences in price levels?**

The analysis compares two standardized worker scenarios:

- **100% of average earnings**
    
- **50% of average earnings**
    

The second scenario provides an additional perspective on workers entering the labour market who may initially earn substantially less than the national average.

* * *

## Project Overview

A country's wages cannot be evaluated independently of its cost of living.

A country may have:

- high wages but also high prices;
    
- low wages and low prices;
    
- or a combination of relatively favorable earnings and prices.
    

This project therefore combines **net earnings** with the **Price Level Index (PLI)** to investigate relative affordability across the EU.

The analysis includes:

- data loading and validation;
    
- descriptive statistics;
    
- comparison of earnings and price levels;
    
- Pearson correlation;
    
- linear regression;
    
- predicted earnings;
    
- earnings residuals;
    
- earnings-to-price ratios;
    
- affordability indices;
    
- comparison between 100% and 50% earnings scenarios.
    

* * *

# Research Questions

The analysis addresses the following questions:

1.  **How strongly are price levels and net earnings related across the EU27?**
    
2.  **Which countries have the highest earnings relative to their price levels?**
    
3.  **Which countries earn more or less than expected given their price level?**
    
4.  **How does relative affordability change for a worker earning 50% rather than 100% of average earnings?**
    
5.  **Which countries appear particularly favorable for lower-paid workers based on earnings relative to prices?**
    

* * *

# Data

The analysis uses European statistical data for the **27 EU Member States**.

The main variables are:

### Price Level Index

The Price Level Index (PLI) measures the relative price level of household consumption.

The EU27 average is:

**PLI = 100**

Therefore:

- `PLI > 100` → prices are above the EU27 average
    
- `PLI < 100` → prices are below the EU27 average
    

### Net Earnings

The analysis uses annual net earnings for a:

> **Single person without children**

Two earnings scenarios are examined:

- **100% of average earnings**
    
- **50% of average earnings**
    

* * *

# Methodology

## 1\. Earnings vs. Price Level

The relationship between net earnings and the Price Level Index is examined using a scatter plot and linear regression.

The regression estimates:

```text
Predicted earnings = intercept + slope × PLI
```

The predicted earnings represent the earnings level expected by the linear model for a given price level.

* * *

## 2\. Pearson Correlation

Pearson's correlation coefficient measures the strength and direction of the linear relationship between price levels and net earnings.

The results are:

| Scenario | Pearson correlation |
| --- | ---: |
| 100% earnings | **0.937** |
| 50% earnings | **0.904** |

Both indicate a **very strong positive relationship**.

* * *

## 3\. Coefficient of Determination

The coefficient of determination, R², measures how much of the cross-country variation in earnings is associated with the linear relationship with price levels.

| Scenario | R²  |
| --- | ---: |
| 100% earnings | **0.877** |
| 50% earnings | **0.817** |

For the 100% scenario, approximately **87.7%** of the variation in net earnings is associated with the linear relationship with the Price Level Index.

For the 50% scenario, the corresponding value is approximately **81.7%**.

The relationship therefore remains very strong for lower-paid workers, although it becomes somewhat less tightly aligned.

* * *

# Earnings Residuals

The regression model allows actual earnings to be compared with the earnings predicted from the country's price level.

The residual is calculated as:

```text
Residual = Actual earnings − Predicted earnings
```

A:

- **positive residual** → actual earnings are higher than predicted;
    
- **negative residual** → actual earnings are lower than predicted.
    

This allows countries to be identified where earnings appear particularly high or low relative to their price level.

For example, Luxembourg has a large positive residual, while Hungary has a substantial negative residual.

* * *

# Earnings-to-Price Ratio

A simple relative affordability measure is calculated as:

```text
Earnings-to-PLI = Net earnings / PLI
```

This compares nominal net earnings with the country's relative price level.

Higher values indicate a more favorable relationship between earnings and general prices.

* * *

# Affordability Index

The earnings-to-PLI ratio is normalized against the EU27 benchmark:

```text
Affordability Index =
Country earnings-to-PLI / EU27 earnings-to-PLI × 100
```

The interpretation is:

| Index | Interpretation |
| ---: | --- |
| **100** | EU27 benchmark |
| **\>100** | Above EU27 benchmark |
| **<100** | Below EU27 benchmark |

The index is therefore a **relative measure of affordability**, not a direct measure of disposable income or quality of life.

* * *

# Key Findings

## 1\. Price levels and earnings are strongly related

There is a very strong positive relationship between price levels and net earnings.

For average earners:

**r = 0.937**

**R² = 0.877**

For workers earning 50% of average earnings:

**r = 0.904**

**R² = 0.817**

This demonstrates that countries with higher price levels generally also have higher net earnings.

However, the slightly weaker relationship at 50% suggests that lower-paid workers experience somewhat greater variation in earnings relative to their country's price level.

* * *

## 2\. Low prices do not necessarily mean high affordability

Countries such as Romania, Bulgaria and Hungary have relatively low price levels, but they also have relatively low net earnings.

Consequently, their affordability indices remain below the EU27 benchmark.

This demonstrates why comparing countries based solely on prices or wages can be misleading.

* * *

## 3\. Luxembourg performs exceptionally well

Luxembourg has the highest affordability index in both scenarios.

### 100% of average earnings

**Affordability Index: 153.2**

### 50% of average earnings

**Affordability Index: 164.2**

Despite having one of Europe's highest price levels, its exceptionally high earnings more than compensate for those prices under this measure.

* * *

## 4\. The Netherlands improves substantially at 50% earnings

The Netherlands shows the largest improvement in relative affordability when moving from 100% to 50% of average earnings.

|     | Affordability Index |
| --- | ---: |
| 100% | **115.1** |
| 50% | **146.8** |
| Change | **+31.6** |

This makes the Netherlands particularly interesting when considering a lower-paid worker.

* * *

## 5\. Some lower-income countries deteriorate substantially

Several countries experience a significant decline in relative affordability when moving from average earnings to 50% earnings.

Examples include:

| Country | Change in affordability |
| --- | ---: |
| Cyprus | **−15.7** |
| Bulgaria | **−15.1** |
| Romania | **−13.6** |
| Slovenia | **−12.4** |
| Hungary | **−12.1** |

This suggests that a country's attractiveness can change substantially depending on the income level of the individual being considered.

* * *

# 100% vs. 50% Earnings

One of the main purposes of the project is to demonstrate that the economic position of an individual cannot necessarily be represented by national average earnings alone.

The affordability comparison shows that countries respond differently when earnings are reduced to 50% of the average.

Some countries improve their relative position, while others deteriorate.

### \[Insert 100% vs. 50% affordability comparison figure here\]

* * *

# Visualizations

## Earnings and Price Levels

### 100% of Average Earnings

\[Insert figure\]

### 50% of Average Earnings

\[Insert figure\]

* * *

## Affordability

### 100% of Average Earnings

\[Insert figure\]

### 50% of Average Earnings

\[Insert figure\]

* * *

## 100% vs. 50% Comparison

\[Insert figure\]

* * *

# Project Structure

```text
European-Cost-of-Living/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   └── european_cost_of_living_analysis.ipynb
│
├── src/
│   ├── data_preparation.py
│   ├── analysis.py
│   └── visualization.py
│
├── figures/
│
├── streamlit/
│   └── app.py
│
├── powerbi/
│
└── report/
```

* * *

# Tools and Technologies

The project uses:

- **Python**
    
- **Pandas** — data manipulation
    
- **NumPy** — numerical analysis
    
- **Matplotlib** — data visualization
    
- **Jupyter Notebook** — exploratory analysis
    
- **Streamlit** — interactive web application
    
- **Power BI** — interactive dashboard
    
- **Git / GitHub** — version control and project documentation
    

* * *

# Limitations

This analysis focuses on the relationship between general price levels and net earnings.

The affordability index should therefore not be interpreted as a complete measure of quality of life or financial well-being.

The analysis does not currently include:

- housing and rent;
    
- unemployment;
    
- employment opportunities;
    
- career prospects;
    
- taxation beyond its effect on the net earnings measure;
    
- transport;
    
- healthcare;
    
- quality of life;
    
- individual consumption patterns.
    

The Price Level Index is an aggregate measure and therefore does not necessarily represent the expenses of a specific individual.

The 50% earnings scenario is a standardized analytical scenario and does not imply that every young worker earns exactly 50% of the national average.

Finally, correlation does not imply causation. The strong relationship between price levels and earnings should not be interpreted as evidence that higher prices directly cause higher wages.

* * *

# Future Work

This project represents the first stage of a broader investigation into the economic attractiveness of European countries for workers.

Potential future stages include:

### Stage 2 — Labour Market

- youth unemployment;
    
- employment opportunities;
    
- job availability;
    
- employment rates;
    
- career prospects.
    

### Stage 3 — Housing and Real Cost of Living

- rent;
    
- housing costs;
    
- disposable income after housing;
    
- location-specific cost differences.
    

These variables could eventually be combined with the current affordability analysis to create a more comprehensive assessment of the attractiveness of European countries for young workers.

* * *

# Project Outputs

The project is intended to provide four complementary outputs:

### GitHub Repository

The technical and reproducible foundation of the project.

### Streamlit Application

An interactive web application for exploring the data and results.

### Power BI Dashboard

A professional business-intelligence dashboard presenting the key findings interactively.

### PDF Report

A formal documentation of the methodology, analysis, findings and conclusions.

* * *

# Conclusion

The analysis shows that **earnings and price levels are strongly associated across the EU**, but that the relationship between the two varies between countries and income levels.

For average earners, the relationship is particularly strong, with a Pearson correlation of **0.937** and an R² of **0.877**.

For workers earning 50% of average earnings, the relationship remains strong at **0.904**, with an R² of **0.817**.

However, the affordability analysis reveals important differences that are hidden when looking only at average wages or price levels.

Luxembourg consistently performs exceptionally well, while the Netherlands shows the largest improvement when considering the 50% earnings scenario.

At the same time, countries such as Romania, Bulgaria and Hungary demonstrate that **low prices alone do not guarantee favorable purchasing power**.

The results therefore support a broader approach to evaluating where a European worker might choose to live and work:

> **The relevant question is not simply "Where are wages highest?" or "Where is life cheapest?", but rather "Where does my income provide the greatest purchasing power relative to the cost of living?"**

This project establishes the analytical foundation for answering that question in greater detail.