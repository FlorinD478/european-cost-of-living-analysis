# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    HRFlowable, KeepTogether, ListFlowable, ListItem
)
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import Image
#---
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
CHARTS_DIR = SCRIPT_DIR / "charts"
#---

# ---------------------------------------------------------------
# Palette (kept close to the dashboard's palette for a consistent look)
# ---------------------------------------------------------------
INK = colors.HexColor("#1A1F2B")
MUTED = colors.HexColor("#6B7280")
PRIMARY = colors.HexColor("#1F4E79")
PRIMARY_DARK = colors.HexColor("#16324F")
ACCENT = colors.HexColor("#C9A227")
POSITIVE = colors.HexColor("#2E7D5B")
NEGATIVE = colors.HexColor("#B3462C")
BORDER = colors.HexColor("#E5E7EB")
CARD = colors.HexColor("#F7F8FA")
WHITE = colors.white

PAGE_W, PAGE_H = letter

# ---------------------------------------------------------------
# Styles
# ---------------------------------------------------------------
ss = getSampleStyleSheet()

styles = {
    "CoverTitle": ParagraphStyle(
        "CoverTitle", parent=ss["Title"], fontName="Helvetica-Bold",
        fontSize=27, leading=33, textColor=WHITE, alignment=TA_LEFT,
        spaceAfter=10,
    ),
    "CoverSub": ParagraphStyle(
        "CoverSub", parent=ss["Normal"], fontName="Helvetica",
        fontSize=12.5, leading=18, textColor=colors.HexColor("#D7E0EA"),
        alignment=TA_LEFT,
    ),
    "CoverEyebrow": ParagraphStyle(
        "CoverEyebrow", parent=ss["Normal"], fontName="Helvetica-Bold",
        fontSize=10, leading=12, textColor=ACCENT, alignment=TA_LEFT,
        spaceAfter=8,
    ),
    "H1": ParagraphStyle(
        "H1", parent=ss["Heading1"], fontName="Helvetica-Bold",
        fontSize=17, leading=21, textColor=PRIMARY, spaceBefore=22,
        spaceAfter=10, keepWithNext=True,
    ),
    "H2": ParagraphStyle(
        "H2", parent=ss["Heading2"], fontName="Helvetica-Bold",
        fontSize=13, leading=17, textColor=PRIMARY_DARK, spaceBefore=14,
        spaceAfter=6, keepWithNext=True,
    ),
    "H3": ParagraphStyle(
        "H3", parent=ss["Heading3"], fontName="Helvetica-Bold",
        fontSize=11, leading=14, textColor=INK, spaceBefore=10,
        spaceAfter=4, keepWithNext=True,
    ),
    "Body": ParagraphStyle(
        "Body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6,
        leading=14.5, textColor=INK, alignment=TA_JUSTIFY, spaceAfter=7,
    ),
    "Bullet": ParagraphStyle(
        "Bullet", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6,
        leading=14, textColor=INK, alignment=TA_LEFT, spaceAfter=3,
        leftIndent=0,
    ),
    "Quote": ParagraphStyle(
        "Quote", parent=ss["Normal"], fontName="Helvetica-Oblique",
        fontSize=11, leading=16, textColor=PRIMARY_DARK, alignment=TA_LEFT,
        leftIndent=14, spaceBefore=8, spaceAfter=8,
    ),
    "Formula": ParagraphStyle(
        "Formula", parent=ss["Normal"], fontName="Helvetica-Oblique",
        fontSize=10, leading=15, textColor=INK, alignment=TA_CENTER,
        spaceBefore=4, spaceAfter=4,
    ),
    "Caption": ParagraphStyle(
        "Caption", parent=ss["Normal"], fontName="Helvetica-Oblique",
        fontSize=8.3, leading=11, textColor=MUTED, alignment=TA_LEFT,
        spaceAfter=8,
    ),
    "TableHead": ParagraphStyle(
        "TableHead", parent=ss["Normal"], fontName="Helvetica-Bold",
        fontSize=8.6, leading=11, textColor=WHITE, alignment=TA_LEFT,
    ),
    "TableCell": ParagraphStyle(
        "TableCell", parent=ss["Normal"], fontName="Helvetica", fontSize=8.6,
        leading=11, textColor=INK, alignment=TA_LEFT,
    ),
    "TableCellR": ParagraphStyle(
        "TableCellR", parent=ss["Normal"], fontName="Helvetica", fontSize=8.6,
        leading=11, textColor=INK, alignment=TA_LEFT,
    ),
    "Code": ParagraphStyle(
        "Code", parent=ss["Normal"], fontName="Courier", fontSize=8.4,
        leading=12.5, textColor=INK, backColor=CARD, borderColor=BORDER,
        borderWidth=0.6, borderPadding=8, alignment=TA_LEFT, spaceBefore=6,
        spaceAfter=10,
    ),
    "SectionNum": ParagraphStyle(
        "SectionNum", parent=ss["Normal"], fontName="Helvetica-Bold",
        fontSize=9, leading=11, textColor=ACCENT,
    ),
    "TOCEntry": ParagraphStyle(
        "TOCEntry", parent=ss["Normal"], fontName="Helvetica", fontSize=10,
        leading=18, textColor=INK,
    ),
    "FooterNote": ParagraphStyle(
        "FooterNote", parent=ss["Normal"], fontName="Helvetica-Oblique",
        fontSize=8, leading=11, textColor=MUTED,
    ),
    "CaptionCenter": ParagraphStyle(
    "CaptionCenter", parent=ss["Title"], alignment=TA_CENTER,
    ),
}


def P(text, style="Body"):
    return Paragraph(text, styles[style])


def bullets(items, style="Bullet"):
    return ListFlowable(
        [ListItem(P(i, style), leftIndent=6, spaceAfter=3) for i in items],
        bulletType="bullet", start="•", leftIndent=14, bulletFontSize=8,
        bulletColor=PRIMARY,
    )


def hr():
    return HRFlowable(width="100%", thickness=0.7, color=BORDER,
                       spaceBefore=6, spaceAfter=12)


def data_table(header, rows, col_widths=None, align_right_from=1, zebra=True):
    """Styled table: dark header row, right-aligned numeric columns, zebra body."""
    header_cells = [Paragraph(h, styles["TableHead"]) for h in header]
    body = [header_cells]
    for row in rows:
        body.append([Paragraph(str(c), styles["TableCell"]) for c in row])

    t = Table(body, colWidths=col_widths, repeatRows=1)

    ts = [
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.6),
        ("TOPPADDING", (0, 0), (-1, -1), 4.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (align_right_from, 1), (-1, -1), "RIGHT"),
        ("ALIGN", (align_right_from, 0), (-1, 0), "RIGHT"),
    ]
    if zebra:
        for i in range(1, len(body)):
            if i % 2 == 0:
                ts.append(("BACKGROUND", (0, i), (-1, i), CARD))
    t.setStyle(TableStyle(ts))
    return t


def two_col_table(header, rows_a, rows_b, widths=None):
    """Side-by-side pair of small tables (used for highest/lowest earnings etc.)."""
    left = data_table(header, rows_a, col_widths=widths)
    right = data_table(header, rows_b, col_widths=widths)
    outer = Table([[left, right]], colWidths=[2.65 * inch, 2.65 * inch])
    outer.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (0, -1), 10),
        ("RIGHTPADDING", (1, 0), (1, -1), 0),
    ]))
    return outer


def formula_box(text):
    t = Table([[P(text, "Formula")]], colWidths=[6.4 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CARD),
        ("BOX", (0, 0), (-1, -1), 0.7, BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
    ]))
    return t


def code_block(text):
    return P(text.replace("\n", "<br/>").replace(" ", "&nbsp;"), "Code")


def section(num, title):
    return P(f'<font color="#C9A227">{num}</font> &nbsp; {title}', "H1")


def chart_image(path, caption_text, width=6.4 * inch):
    img = Image(path)
    aspect = img.imageHeight / img.imageWidth
    img.drawWidth = width
    img.drawHeight = width * aspect
    img.hAlign = "CENTER"
    return KeepTogether([img, Spacer(1, 4), P(caption_text, "Caption")])

# =================================================================
# Cover page
# =================================================================
story = []

cover_bg = Table([[""]], colWidths=[PAGE_W - 1.4 * inch], rowHeights=[3.6 * inch])
cover_bg.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), PRIMARY_DARK),
]))

story.append(Spacer(1, 1.6 * inch))
cover_inner = Table(
    [[Paragraph("EUROSTAT · 2025 EDITION", styles["CoverEyebrow"])],
     [Paragraph("European Cost of Living Analysis", styles["CoverTitle"])],
     [Paragraph(
         "A detailed project report on income, price levels and effective "
         "purchasing power across the 27 EU member states — combining a "
         "Python analytics pipeline, statistical modelling, a Power BI "
         "dashboard, and an interactive Streamlit application.",
         styles["CoverSub"])],
     ],
    colWidths=[6.6 * inch],
)
cover_inner.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), PRIMARY_DARK),
    ("LEFTPADDING", (0, 0), (-1, -1), 40),
    ("RIGHTPADDING", (0, 0), (-1, -1), 40),
    ("TOPPADDING", (0, 0), (0, 0), 46),
    ("BOTTOMPADDING", (0, -1), (0, -1), 46),
    ("TOPPADDING", (0, 1), (0, 1), 6),
    ("TOPPADDING", (0, 2), (0, 2), 14),
]))
story.append(cover_inner)
story.append(Spacer(1, 0.5 * inch))

meta_table = Table(
    [["Scope", "27 EU member states, 2025"],
     ["Primary sources", "Eurostat earn_nt_net · Eurostat prc_ppp_ind_1"],
     ["Methods", "Linear regression · Pearson correlation · residual analysis · affordability index"],
     ["Delivery", "Python (pandas, NumPy, matplotlib) · Power BI · Streamlit"]],
    colWidths=[1.6 * inch, 5.0 * inch],
)
meta_table.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
    ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
    ("FONTSIZE", (0, 0), (-1, -1), 9.3),
    ("TEXTCOLOR", (0, 0), (0, -1), PRIMARY),
    ("TEXTCOLOR", (1, 0), (1, -1), INK),
    ("LINEBELOW", (0, 0), (-1, -2), 0.5, BORDER),
    ("TOPPADDING", (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
]))
story.append(meta_table)

story.append(PageBreak())

# =================================================================
# 1. Executive Summary
# =================================================================
story.append(section("1.", "Executive Summary"))
story.append(P(
    'This project investigates the relationship between <b>income levels, '
    'consumer price levels, and effective purchasing power across the 27 '
    'European Union member states in 2025</b>.'
))
story.append(P("The analysis combines two Eurostat datasets:"))
story.append(bullets([
    "<b>Annual net earnings</b> for a single person without children earning "
    "100% of the national average wage.",
    "<b>Price Level Indices (PLI)</b> for household final consumption "
    "expenditure, with the EU27 average normalized to 100.",
]))
story.append(P("The core objective was not simply to identify which countries have the "
               "highest salaries or lowest prices, but to examine the more meaningful "
               "question:"))
story.append(P(
    "How does the purchasing power implied by national earnings change once "
    "differences in price levels are taken into account?", "Quote"))
story.append(P(
    "The project developed a reusable Python data-analysis pipeline for "
    "importing, validating, cleaning, transforming and analysing the datasets. "
    "Statistical analysis included linear regression, Pearson correlation, "
    "residual analysis and derived affordability measures. The results were "
    "then exposed through both a <b>Power BI dashboard</b> and an interactive "
    "<b>Streamlit application</b>."
))
story.append(P(
    "The results show a very strong positive relationship between price levels "
    "and nominal net earnings. For the 100%-average-earner scenario, the "
    "analysis produced a <b>Pearson correlation of 0.937</b> and an "
    "<b>R\u00b2 of 0.877</b>. In other words, countries with higher consumer "
    "price levels generally also report substantially higher nominal net "
    "earnings."
))
story.append(P(
    "However, the regression also reveals important deviations from this "
    "general pattern. Some countries have substantially higher or lower "
    "earnings than would be expected from their price level alone. This is "
    "where the affordability analysis becomes more informative than a simple "
    "salary ranking."
))
story.append(P("Using the project's affordability index, where the EU27 average is set to 100:"))
story.append(bullets([
    "<b>Luxembourg</b> had the highest affordability index at approximately <b>153.2</b>.",
    "<b>Austria</b> followed at approximately <b>120.9</b>.",
    "<b>Ireland</b> was approximately <b>120.7</b>.",
    "<b>Netherlands</b> was approximately <b>115.1</b>.",
    "<b>Hungary</b> had the lowest index at approximately <b>62.1</b>.",
    "<b>Greece</b> followed at approximately <b>63.9</b>.",
    "<b>Slovakia</b> was approximately <b>68.4</b>.",
    "<b>Estonia</b> was approximately <b>73.6</b>.",
    "<b>Romania</b> was approximately <b>75.5</b>.",
]))
story.append(P(
    "The alternative 50%-earnings scenario produced a lower affordability "
    "index across most countries and demonstrated that <b>income level "
    "materially changes the relative purchasing-power picture</b>, even "
    "though the underlying price levels remain unchanged."
))
story.append(P(
    "The project therefore demonstrates an important distinction between "
    "<b>nominal earnings</b>, <b>price levels</b>, and <b>effective "
    "affordability</b>."
))

# =================================================================
# 2. Project Objectives
# =================================================================
story.append(section("2.", "Project Objectives"))
story.append(P("The project was designed around several analytical objectives."))
story.append(P("Primary objective", "H2"))
story.append(P("To compare the economic position of EU countries by combining:"))
story.append(bullets([
    "national net earnings;",
    "consumer price levels;",
    "earnings relative to the EU average;",
    "earnings relative to national price levels.",
]))
story.append(P("Secondary objectives", "H2"))
story.append(P("The project also aimed to:"))
story.append(bullets([
    "build a reproducible data-processing workflow;",
    "validate Eurostat data before analysis;",
    "remove non-country aggregate observations where appropriate;",
    "calculate derived purchasing-power indicators;",
    "quantify the relationship between earnings and prices;",
    "identify countries performing above or below the expected earnings-price relationship;",
    "compare different income scenarios;",
    "communicate the results through interactive visualizations.",
]))
story.append(P(
    "The project was therefore intentionally designed as a complete <b>data "
    "analytics workflow</b>, rather than a single statistical exercise."
))

# =================================================================
# 3. Research Questions
# =================================================================
story.append(section("3.", "Research Questions"))
story.append(P("The analysis addresses the following questions."))

rqs = [
    ("RQ1", "Where are consumer prices highest and lowest?",
     "How different are household consumption price levels across EU countries?"),
    ("RQ2", "Where are nominal net earnings highest and lowest?",
     "Which countries provide the highest and lowest annual net earnings for the "
     "selected worker profile?"),
    ("RQ3", "Are high prices associated with high earnings?",
     "Is there a systematic relationship between a country's price level and its "
     "nominal net earnings?"),
    ("RQ4", "Which countries earn more or less than expected?",
     "Given a country's price level, does its actual net earnings level sit above "
     "or below the regression trend?"),
    ("RQ5", "Which countries offer greater effective affordability?",
     "When earnings are considered together with price levels, which countries "
     "appear to provide stronger or weaker purchasing power?"),
    ("RQ6", "How does the picture change at a lower earnings level?",
     "Does the relative affordability ranking change when the worker earns 50% "
     "rather than 100% of the national average wage?"),
]
for code, q, desc in rqs:
    story.append(P(f'<font color="#C9A227"><b>{code}</b></font> \u2014 <b>{q}</b>', "H3"))
    story.append(P(desc))

# =================================================================
# 4. Data Sources
# =================================================================
story.append(section("4.", "Data Sources"))
story.append(P("The project uses publicly available Eurostat data."))
story.append(P("4.1 Annual net earnings", "H2"))
story.append(P(
    "The earnings dataset used was Eurostat's <b>earn_nt_net \u2014 Annual net "
    "earnings</b> dataset. Eurostat describes this as an annual dataset and its "
    "current coverage extends through 2025."
))
story.append(P("The selected earnings definition was:"))
story.append(P("Single person without children earning 100% of the average earnings.", "Quote"))
story.append(P("The analysis used <b>net annual earnings in euros</b>."))
story.append(P("A second dataset was used for the 50%-earnings scenario."))
story.append(P("The project therefore distinguishes between:"))
story.append(bullets(["net_earnings_eur", "net_earnings_50_eur"]))
story.append(P("rather than treating \u201caverage salary\u201d as a single universal concept."))

story.append(P("4.2 Price Level Index", "H2"))
story.append(P(
    "The second major source was Eurostat's <b>prc_ppp_ind_1</b> dataset covering "
    "Purchasing Power Parities, Price Level Indices and related expenditure measures."
))
story.append(P("The selected indicator was:"))
story.append(P("Price Level Indices \u2014 Household final consumption expenditure.", "Quote"))
story.append(P("The index is normalized so that:"))
story.append(formula_box("EU27 = 100"))
story.append(P("Therefore:"))
story.append(bullets([
    "PLI = 100 \u2192 approximately EU-average price level",
    "PLI &gt; 100 \u2192 more expensive than the EU average",
    "PLI &lt; 100 \u2192 less expensive than the EU average",
]))
story.append(P(
    "Eurostat's 2025 publication confirms that household consumption price "
    "levels varied considerably across the EU, from approximately 63% of the "
    "EU average in Bulgaria to approximately 140% in Denmark."
))
story.append(P(
    "Eurostat also explicitly notes that these price-level comparisons "
    "<b>are not adjusted for differences in income or wage levels</b>. That "
    "distinction is central to this project because the analysis combines PLI "
    "with earnings to construct an additional affordability measure."
))

# =================================================================
# 5. Analytical Scope
# =================================================================
story.append(section("5.", "Analytical Scope"))
story.append(P("The main analysis covers the <b>27 EU member states</b>."))
story.append(P("The Eurostat files also contain aggregate observations such as:"))
story.append(code_block("EU27_2020"))
story.append(P("These observations were excluded from country-level calculations where appropriate."))
story.append(P("Similarly, countries outside the EU were excluded from the main EU comparison."))
story.append(P("This distinction is important because including the EU aggregate in country "
               "statistics would artificially alter:"))
story.append(bullets(["means;", "standard deviations;", "correlations;",
                       "regression coefficients;", "rankings."]))
story.append(P(
    "The project therefore separates <b>country observations</b> from "
    "<b>reference/aggregate observations</b>."
))

# =================================================================
# 6. Data Processing Pipeline
# =================================================================
story.append(section("6.", "Data Processing Pipeline"))
story.append(P("The project was organized into a reusable Python structure rather "
               "than keeping all calculations inside a single notebook."))
story.append(P("The main components were separated into:"))
story.append(code_block("src/\n\u251c\u2500\u2500 data_processing.py\n\u251c\u2500\u2500 analysis.py\n\u2514\u2500\u2500 visualization.py"))
story.append(P("This separation provides three conceptual layers."))

story.append(P("Data processing", "H2"))
story.append(P("Responsible for:"))
story.append(bullets([
    "loading CSV files;", "previewing datasets;", "checking data quality;",
    "identifying duplicates;", "checking missing observations;",
    "excluding unwanted geographic codes;", "retrieving reference values.",
]))
story.append(P("Analysis", "H2"))
story.append(P("Responsible for:"))
story.append(bullets([
    "regression;", "correlation;", "earnings indices;",
    "earnings-to-PLI calculations;", "affordability calculations;",
    "residual analysis.",
]))
story.append(P("Visualization", "H2"))
story.append(P("Responsible for:"))
story.append(bullets([
    "ranked bar charts;", "scatter plots;", "regression lines;",
    "dumbbell/change charts;", "presentation-oriented plotting.",
]))
story.append(P(
    "This architecture makes the analytical logic reusable and reduces "
    "dependence on notebook-specific variables."
))

story.append(PageBreak())

# =================================================================
# 7. Data Quality Checks
# =================================================================
story.append(section("7.", "Data Quality Checks"))
story.append(P("Before calculations were performed, the data was systematically inspected."))
story.append(P("The checks included:"))
story.append(bullets([
    "dataset dimensions;", "column names;", "data types;", "missing values;",
    "duplicate geographic codes;", "selected year;", "selected currency;",
    "selected earnings case;", "selected earnings structure;",
    "geographic coverage.",
]))
story.append(P("For the main earnings dataset, the analysis found:"))
story.append(bullets([
    "28 observations initially;",
    "27 country observations after excluding the EU aggregate;",
    "no duplicate country codes;",
    "no missing OBS_VALUE values.",
]))
story.append(P("For the PLI dataset:"))
story.append(bullets([
    "32 observations initially;",
    "27 EU country observations after excluding non-EU countries and the EU aggregate;",
    "no duplicate country codes;",
    "no missing OBS_VALUE values.",
]))
story.append(P(
    "This validation was particularly important because Eurostat SDMX/CSV "
    "exports contain numerous metadata columns, many of which are "
    "intentionally empty for the observations being used."
))

story.append(PageBreak())

# =================================================================
# 8. Price Level Analysis
# =================================================================
story.append(section("8.", "Price Level Analysis"))
story.append(P("The 2025 PLI results show substantial differences in household "
               "consumption prices across the EU."))
story.append(P("The project's values were approximately:"))

pli_rows = [
    ("Denmark", "139.7"), ("Ireland", "136.2"), ("Luxembourg", "131.5"),
    ("Finland", "120.8"), ("Sweden", "121.0"), ("Belgium", "116.2"),
    ("Netherlands", "115.6"), ("Austria", "113.0"), ("France", "110.3"),
    ("Germany", "108.3"), ("Estonia", "101.2"), ("Italy", "97.1"),
    ("Malta", "91.9"), ("Spain", "91.6"), ("Slovenia", "89.3"),
    ("Czechia", "89.4"), ("Cyprus", "89.2"), ("Greece", "87.4"),
    ("Portugal", "86.6"), ("Slovakia", "85.2"), ("Lithuania", "82.8"),
    ("Latvia", "83.2"), ("Croatia", "78.4"), ("Hungary", "77.5"),
    ("Poland", "73.3"), ("Romania", "65.1"), ("Bulgaria", "62.5"),
]
half = (len(pli_rows) + 1) // 2
story.append(two_col_table(
    ["Country", "PLI"], pli_rows[:half], pli_rows[half:],
    widths=[1.9 * inch, 0.75 * inch],
))

#Chart
story.append(chart_image(
    str(CHARTS_DIR / "Affordability index.png"),
    "Figure 1. Price Level Index by country, EU27 = 100."
))

story.append(Spacer(1, 8))
story.append(P(
    "The broad pattern is consistent with Eurostat's published 2025 results. "
    "Denmark, Ireland and Luxembourg are among the highest-price EU countries, "
    "while Bulgaria, Romania and Poland are among the lowest."
))
story.append(P("The difference between the extremes is substantial."))
story.append(P("Using the project's values:"))
story.append(formula_box("Denmark / Bulgaria \u2248 2.24"))
story.append(P(
    "Therefore, the Danish household-consumption price level is more than "
    "twice the Bulgarian level relative to the EU benchmark."
))
story.append(P(
    "This illustrates why nominal income alone is insufficient for a "
    "meaningful cross-country purchasing-power comparison."
))

story.append(PageBreak())

# =================================================================
# 9. Net Earnings Analysis
# =================================================================
story.append(section("9.", "Net Earnings Analysis"))
story.append(P("For the 100%-average-earner scenario, the project found an EU27 "
               "reference value of:"))
story.append(formula_box("\u20ac26,928.97"))
story.append(P("The highest observed annual net earnings were:"))

top_earn = [
    ("Luxembourg", "\u20ac54,259.93"), ("Ireland", "\u20ac44,263.30"),
    ("Denmark", "\u20ac41,981.24"), ("Austria", "\u20ac36,797.90"),
    ("Netherlands", "\u20ac35,836.93"), ("Belgium", "\u20ac34,642.30"),
    ("Sweden", "\u20ac34,624.37"), ("Finland", "\u20ac33,641.04"),
]
story.append(data_table(["Country", "Net earnings"], top_earn,
                         col_widths=[2.2 * inch, 1.3 * inch]))
story.append(Spacer(1, 8))
story.append(P("At the lower end:"))
low_earn = [
    ("Hungary", "\u20ac12,967.22"), ("Romania", "\u20ac13,232.74"),
    ("Bulgaria", "\u20ac13,016.65"), ("Greece", "\u20ac15,049.76"),
    ("Slovakia", "\u20ac15,685.92"), ("Poland", "\u20ac16,163.12"),
]
story.append(data_table(["Country", "Net earnings"], low_earn,
                         col_widths=[2.2 * inch, 1.3 * inch]))
story.append(Spacer(1, 8))
story.append(P("The important observation is that these rankings cannot be "
               "interpreted independently from price levels."))
story.append(P("For example:"))
story.append(bullets([
    "Luxembourg has exceptionally high earnings <b>and</b> exceptionally high prices.",
    "Romania has relatively low earnings <b>but also relatively low prices</b>.",
    "Denmark has very high earnings <b>and</b> the highest PLI.",
    "Bulgaria has very low earnings <b>and</b> the lowest PLI.",
]))
story.append(P("This motivates the project's combined affordability analysis."))

story.append(PageBreak())

# =================================================================
# 10. Earnings vs. Price Level Regression
# =================================================================
story.append(section("10.", "Earnings vs. Price Level Regression"))
story.append(P("One of the central analyses was a linear regression of:"))
story.append(P("Net earnings vs. Price Level Index", "Quote"))
story.append(P("The model can be represented as:"))
story.append(formula_box("Earnings_i = \u03b2\u2080 + \u03b2\u2081 \u00d7 PLI_i + \u03b5_i"))
story.append(P("The project calculated the regression using:"))
story.append(code_block("fit_linear_regression(x, y)"))
story.append(P("The function returns:"))
story.append(bullets([
    "slope;", "intercept;", "predicted earnings;", "residuals;",
    "Pearson correlation;", "R\u00b2.",
]))
story.append(P("For the 100%-earnings scenario:"))

reg_table = data_table(
    ["Metric", "Value"],
    [["Pearson correlation (r)", "0.937"], ["Coefficient of determination (R\u00b2)", "0.877"]],
    col_widths=[3.2 * inch, 1.4 * inch],
)
story.append(reg_table)
story.append(Spacer(1, 8))
story.append(P("This is a very strong positive relationship."))
story.append(P(
    "An R\u00b2 of 0.877 means that approximately <b>87.7% of the variation "
    "in nominal net earnings across the analyzed countries is associated "
    "with the linear relationship with PLI in this sample</b>."
))

#Chart
story.append(chart_image(
    str(CHARTS_DIR / "Price levels vs. net earnings 100.png"),
    "Figure 2. Earnings vs. Price Level, EU27 = 100."
))

story.append(P("However, this should <b>not</b> be interpreted as proof that higher "
               "prices cause higher wages."))
story.append(P("There are many potential underlying factors, including:"))
story.append(bullets([
    "productivity;", "taxation;", "labor-market institutions;",
    "economic structure;", "sector composition;", "housing costs;",
    "national wage-setting systems;", "capital intensity;",
    "education and skills;", "general economic development.",
]))
story.append(P("The regression is therefore best interpreted as a <b>descriptive "
               "cross-country relationship</b>, not a causal model."))

story.append(PageBreak())

# =================================================================
# 11. Regression Residual Analysis
# =================================================================
story.append(section("11.", "Regression Residual Analysis"))
story.append(P("The regression becomes particularly useful when examining the residuals."))
story.append(P("The residual is defined as:"))
story.append(formula_box("Residual_i = ActualEarnings_i \u2212 PredictedEarnings_i"))
story.append(P("A positive residual means:"))
story.append(P("Actual earnings are higher than the regression would predict given "
               "the country's PLI.", "Quote"))
story.append(P("A negative residual means:"))
story.append(P("Actual earnings are lower than predicted given the country's PLI.", "Quote"))
story.append(P("The largest positive residuals in the project included:"))

pos_res = [
    ("Luxembourg", "+\u20ac12,230.92"), ("Bulgaria", "+\u20ac4,296.97"),
    ("Austria", "+\u20ac3,699.65"), ("Romania", "+\u20ac3,257.93"),
    ("Malta", "+\u20ac2,631.60"), ("Spain", "+\u20ac2,495.21"),
]
neg_res = [
    ("Estonia", "\u2212\u20ac7,357.16"), ("Greece", "\u2212\u20ac5,690.24"),
    ("Denmark", "\u2212\u20ac4,006.27"), ("Slovakia", "\u2212\u20ac3,992.05"),
    ("Finland", "\u2212\u20ac3,222.61"), ("Hungary", "\u2212\u20ac2,993.62"),
]
story.append(data_table(["Country", "Residual"], pos_res, col_widths=[2.2 * inch, 1.3 * inch]))
story.append(Spacer(1, 6))
story.append(P("The largest negative residuals included:"))
story.append(data_table(["Country", "Residual"], neg_res, col_widths=[2.2 * inch, 1.3 * inch]))
story.append(Spacer(1, 8))

story.append(P("This is an important analytical result."))
story.append(P(
    "For example, Denmark has very high nominal earnings, but its earnings "
    "are <b>below what the regression would predict given its extremely high "
    "price level</b>."
))
story.append(P(
    "Luxembourg is the opposite: its earnings are dramatically above the "
    "level predicted by its PLI."
))
story.append(P("This provides information that a simple \u201chighest salary\u201d "
               "ranking would miss."))

story.append(PageBreak())

# =================================================================
# 12. Affordability Index
# =================================================================
story.append(section("12.", "Affordability Index"))
story.append(P("The project's central derived measure is the <b>affordability index</b>."))
story.append(P("The calculation is based on:"))
story.append(formula_box("EarningsToPLI_i = NetEarnings_i / PLI_i"))
story.append(P("This gives a simplified measure of earnings relative to the price-level index."))
story.append(P("The result is then normalized so that the EU reference equals 100:"))
story.append(formula_box(
    "AffordabilityIndex_i = [(Earnings_i / PLI_i) / (EU27Earnings / 100)] \u00d7 100"
))
story.append(P("Interpretation:"))
story.append(bullets([
    "<b>100</b> \u2192 EU27 reference level;",
    "<b>&gt;100</b> \u2192 above the EU reference;",
    "<b>&lt;100</b> \u2192 below the EU reference.",
]))
story.append(P("This is the project's primary purchasing-power proxy."))

story.append(PageBreak())

# =================================================================
# 13. Affordability Results — 100% Earnings
# =================================================================
story.append(section("13.", "Affordability Results \u2014 100% Earnings"))
story.append(P("The results were:"))

afford_rows = [
    (1, "Luxembourg", "153.23"), (2, "Austria", "120.93"), (3, "Ireland", "120.68"),
    (4, "Netherlands", "115.12"), (5, "Denmark", "111.59"), (6, "Belgium", "110.71"),
    (7, "Germany", "106.30"), (8, "Sweden", "106.26"), (9, "Malta", "103.22"),
    (10, "France", "103.80"), (11, "Finland", "103.41"), (12, "Spain", "102.42"),
    (13, "Cyprus", "97.93"), (14, "Italy", "93.59"), (15, "Slovenia", "93.58"),
    (16, "Portugal", "84.51"), (17, "Lithuania", "83.64"), (18, "Poland", "81.88"),
    (19, "Croatia", "81.73"), (20, "Czechia", "81.28"), (21, "Bulgaria", "77.34"),
    (22, "Romania", "75.48"), (23, "Latvia", "74.95"), (24, "Estonia", "73.55"),
    (25, "Slovakia", "68.37"), (26, "Greece", "63.94"), (27, "Hungary", "62.13"),
]
story.append(data_table(
    ["Rank", "Country", "Affordability"], afford_rows,
    col_widths=[0.6 * inch, 2.3 * inch, 1.1 * inch], align_right_from=2,
))
story.append(Spacer(1, 8))
story.append(P("The most striking result is <b>Luxembourg</b>."))
story.append(P(
    "Its PLI is among the highest in Europe, but its earnings are "
    "sufficiently high that it remains the strongest country under this "
    "affordability measure."
))
story.append(P("This is an important demonstration of why:"))
story.append(P("High prices do not automatically imply low purchasing power.", "Quote"))
story.append(P("What matters is the relationship between earnings and prices."))

# =================================================================
# 14–17: Country case studies
# =================================================================
story.append(section("14.", "Country Case Studies"))
story.append(P("14.1 Romania", "H2"))
story.append(P("Romania provides a particularly interesting case for the analysis."))
story.append(P("The country has:"))
story.append(bullets([
    "PLI \u2248 <b>65.1</b>",
    "Net earnings \u2248 <b>\u20ac13,232.74</b>",
    "Affordability index \u2248 <b>75.48</b>",
]))
story.append(P(
    "This means Romania is among the least expensive EU countries according "
    "to the PLI, but its relatively low earnings more than offset the "
    "benefit of low prices in this simplified affordability measure."
))
story.append(P("Romania therefore illustrates an important analytical distinction:"))
story.append(P("Low cost of living is not necessarily equivalent to high purchasing power.", "Quote"))
story.append(P(
    "A country can be inexpensive relative to the EU while still providing "
    "relatively weak purchasing power because local earnings are also "
    "substantially lower."
))

story.append(P("14.2 Bulgaria", "H2"))
story.append(P("Bulgaria represents a similar but slightly different case."))
story.append(P("It had:"))
story.append(bullets([
    "the lowest PLI in the analyzed EU sample: <b>62.5</b>",
    "net earnings of approximately <b>\u20ac13,016.65</b>",
    "affordability index of approximately <b>77.34</b>",
]))
story.append(P(
    "Interestingly, Bulgaria has a <b>positive regression residual</b> "
    "despite its low affordability index."
))
story.append(P(
    "This means that its earnings are somewhat higher than what the overall "
    "earnings-price regression would predict at such a low PLI."
))
story.append(P("This distinction is useful:"))
story.append(P("Regression residual", "H3"))
story.append(P("Answers:"))
story.append(P("\u201cDoes the country earn more or less than expected given its price level?\u201d", "Quote"))
story.append(P("Affordability index", "H3"))
story.append(P("Answers:"))
story.append(P("\u201cHow does the country's earnings-to-price relationship compare with the EU reference?\u201d", "Quote"))
story.append(P("They are therefore related but conceptually different measures."))

story.append(P("14.3 Luxembourg", "H2"))
story.append(P("Luxembourg is the clearest high-performing outlier in the analysis."))
story.append(P("It had:"))
story.append(bullets([
    "PLI: <b>131.5</b>", "Net earnings: <b>\u20ac54,259.93</b>",
    "Affordability index: <b>153.23</b>",
    "Regression residual: approximately <b>+\u20ac12,231</b>",
]))
story.append(P("The country therefore combines:"))
story.append(bullets(["very high prices;", "exceptionally high earnings;",
                       "the highest affordability index in the project."]))
story.append(P(
    "This is precisely the kind of result that would be missed by looking "
    "only at a cost-of-living ranking."
))
story.append(P(
    "Luxembourg's result also demonstrates why the analysis should not "
    "equate \u201cexpensive\u201d with \u201cunaffordable.\u201d"
))

story.append(P("14.4 Denmark", "H2"))
story.append(P("Denmark presents the opposite analytical lesson."))
story.append(P("It had:"))
story.append(bullets([
    "the highest PLI: <b>139.7</b>", "net earnings: <b>\u20ac41,981.24</b>",
    "affordability index: <b>111.59</b>",
]))
story.append(P(
    "Therefore, despite being the most expensive EU country in the project's "
    "dataset, Denmark still sits above the EU affordability benchmark."
))
story.append(P("However, its regression residual was approximately:"))
story.append(formula_box("\u2212\u20ac4,006"))
story.append(P(
    "This means that, relative to the cross-country earnings-price "
    "relationship, Danish earnings were lower than the model would predict "
    "given the country's very high price level."
))
story.append(P("This shows why several complementary metrics are useful."))

story.append(PageBreak())

# =================================================================
# 15. 50% Earnings Scenario
# =================================================================
story.append(section("15.", "50% Earnings Scenario"))
story.append(P("The project also repeated the analysis for workers earning 50% of the "
               "average wage."))

#Chart
story.append(chart_image(
    str(CHARTS_DIR / "Price levels vs. net earnings 50.png"),
    "Figure 3. Price levels vs. net earnings 50%"
))

story.append(P("The EU27 reference earnings were:"))
story.append(formula_box("\u20ac16,722.37"))
story.append(P("The 50%-earnings affordability results showed a lower overall "
               "purchasing-power position."))
story.append(P("Examples include:"))

scenario_rows = [
    ("Luxembourg", "153.23", "164.22"), ("Netherlands", "115.12", "146.76"),
    ("Belgium", "110.71", "130.44"), ("Ireland", "120.68", "133.62"),
    ("Austria", "120.93", "122.34"), ("Romania", "75.48", "61.93"),
    ("Bulgaria", "77.34", "62.27"), ("Hungary", "62.13", "50.03"),
    ("Greece", "63.94", "59.19"), ("Slovakia", "68.37", "58.88"),
]
story.append(data_table(
    ["Country", "Affordability \u2014 100%", "Affordability \u2014 50%"],
    scenario_rows, col_widths=[2.0 * inch, 1.6 * inch, 1.6 * inch],
))

#Chart
story.append(chart_image(
    str(CHARTS_DIR / "Afford 100 vs 50.png"),
    "Figure 4. Affordability 100% vs 50%."
))

story.append(Spacer(1, 8))
story.append(P(
    "An important observation is that the relationship is <b>not simply a "
    "uniform 50% reduction</b> in the final index because the 50%-earnings "
    "scenario is based on a separate Eurostat earnings dataset and "
    "corresponding country values."
))
story.append(P(
    "The scenario therefore provides a useful sensitivity analysis of how "
    "the affordability picture changes under a lower-income worker profile."
))

# =================================================================
# 16. Change in Affordability
# =================================================================
story.append(section("16.", "Change in Affordability"))
story.append(P("The project calculated:"))
story.append(formula_box("AffordabilityChange = Affordability_50 \u2212 Affordability_100"))
story.append(P("The largest positive changes included:"))
pos_change = [("Netherlands", "+31.64"), ("Belgium", "+19.73"), ("Ireland", "+12.94"),
              ("Luxembourg", "+11.00"), ("Portugal", "+9.46")]
story.append(data_table(["Country", "Change"], pos_change, col_widths=[2.4 * inch, 1.1 * inch]))
story.append(Spacer(1, 6))
story.append(P("The largest negative changes included:"))
neg_change = [("Cyprus", "\u221215.71"), ("Bulgaria", "\u221215.07"), ("Romania", "\u221213.56"),
              ("Slovenia", "\u221212.37"), ("Hungary", "\u221212.10")]
story.append(data_table(["Country", "Change"], neg_change, col_widths=[2.4 * inch, 1.1 * inch]))

#Chart
story.append(chart_image(
    str(CHARTS_DIR / "afford change.png"),
    "Figure 5. Affordability change."
))

story.append(Spacer(1, 8))
story.append(P(
    "This comparison highlights that the relationship between income "
    "scenario and affordability is not identical across countries."
))

story.append(PageBreak())

# =================================================================
# 17. Why both metrics should be used
# =================================================================
story.append(section("17.", "Why the Regression and Affordability Index Should Both Be Used"))
story.append(P("One of the strongest aspects of the project is that it does not rely "
               "on one metric."))
story.append(P("The analysis provides three complementary perspectives."))

story.append(P("1. Net earnings", "H3"))
story.append(P("Measures:"))
story.append(P("How much money does the worker earn?", "Quote"))

story.append(P("2. Regression residual", "H3"))
story.append(P("Measures:"))
story.append(P("Does the country's earnings level exceed or fall below what would be "
               "expected from its price level?", "Quote"))

story.append(P("3. Affordability index", "H3"))
story.append(P("Measures:"))
story.append(P("How strong is the country's earnings-to-price relationship relative "
               "to the EU benchmark?", "Quote"))

story.append(P("This produces a more nuanced analysis than a simple ranking."))

#story.append(PageBreak())

# =================================================================
# 18. Power BI Dashboard
# =================================================================
story.append(section("18.", "Power BI Dashboard"))
story.append(P("The analytical results were translated into an interactive Power BI "
               "dashboard."))
story.append(P("The dashboard includes:"))

story.append(P("KPI cards", "H3"))
story.append(P("Providing high-level indicators such as:"))
story.append(bullets(["average net earnings;", "affordability measures;",
                       "reference values;", "other headline statistics."]))

story.append(P("Affordability visualization", "H3"))
story.append(P("Shows the relative affordability position of EU countries."))

story.append(P("Scatter plot", "H3"))
story.append(P("Visualizes:"))
story.append(P("Price Level Index vs. Net Earnings", "Quote"))
story.append(P("with:"))
story.append(bullets(["country labels;", "regression/trend relationship;",
                       "EU reference;", "earnings information."]))

story.append(P("Affordability change chart", "H3"))
story.append(P("Compares:"))
story.append(P("100% earnings vs. 50% earnings", "Quote"))
story.append(P("and uses conditional formatting to distinguish positive and negative changes."))

story.append(P("Country slicer", "H3"))
story.append(P("Allows users to select one or multiple countries."))

story.append(P("This makes the dashboard useful both for:"))
story.append(bullets(["high-level comparison;", "individual country exploration."]))

# =================================================================
# 19. Streamlit Application
# =================================================================
story.append(section("19.", "Streamlit Application"))
story.append(P("In addition to Power BI, the project was developed into an "
               "interactive <b>Streamlit application</b>."))
story.append(P(
    "The Streamlit application provides a Python-native interactive "
    "interface and complements the Power BI dashboard."
))
story.append(P("The application includes:"))
story.append(bullets([
    "headline KPIs;", "affordability analysis;",
    "earnings and PLI comparison;", "interactive scatter analysis;",
    "country-level detail;", "100% vs. 50% earnings comparison.",
]))
story.append(P("The presentation layer was subsequently refactored to improve:"))
story.append(bullets([
    "spacing;", "visual hierarchy;", "typography;", "consistency;",
    "section organization;", "overall professional appearance.",
]))
story.append(P(
    "The country-detail section also uses the full country name rather than "
    "displaying only Eurostat geographic codes."
))
story.append(P("This gives the project two distinct presentation environments:"))
story.append(bullets([
    "<b>Power BI</b> \u2192 business intelligence / dashboard presentation",
    "<b>Streamlit</b> \u2192 interactive Python analytics application",
]))

# =================================================================
# 20. Technical Implementation
# =================================================================
story.append(section("20.", "Technical Implementation"))
story.append(P("The project uses:"))
story.append(bullets([
    "Python", "pandas", "NumPy", "matplotlib", "Streamlit", "Power BI",
    "Git/GitHub",
]))
story.append(P("The Python pipeline separates:"))
story.append(KeepTogether(code_block(
    "Raw data\n  \u2193\nData loading\n  \u2193\nValidation\n  \u2193\n"
    "Filtering\n  \u2193\nDataset merging\n  \u2193\nDerived metrics\n  \u2193\n"
    "Statistical analysis\n  \u2193\nVisualization\n  \u2193\n"
    "Processed dataset\n  \u2193\nPower BI / Streamlit"
)))
story.append(P("The processed analytical dataset contains variables such as:"))
story.append(KeepTogether(code_block(
    "geo\nGeopolitical entity (reporting)\npli\nnet_earnings_eur\n"
    "predicted_earnings\nearnings_residual\nearnings_index\nearnings_to_pli\n"
    "affordability_index\nnet_earnings_50_eur\npredicted_earnings_50\n"
    "earnings_residual_50\nearnings_index_50\nearnings_to_pli_50\n"
    "affordability_index_50\naffordability_change"
)))
story.append(P("This structure makes the final dataset suitable for both statistical "
               "analysis and BI visualization."))

story.append(PageBreak())

# =================================================================
# 21. Reproducibility
# =================================================================
story.append(section("21.", "Reproducibility"))
story.append(P("An important design goal was reproducibility."))
story.append(P(
    "Instead of performing all transformations manually inside the "
    "notebook, the project moved reusable logic into src/."
))
story.append(P("For example, the regression function is generalized:"))
story.append(code_block("def fit_linear_regression(x, y):"))
story.append(P("rather than being hard-coded specifically for PLI and earnings."))
story.append(P("Likewise, the affordability calculation accepts configurable columns "
               "and a suffix:"))
story.append(code_block(
    "def compute_affordability_index(\n    df,\n    pli_col,\n    earnings_col,\n"
    "    eu27_earnings,\n    suffix=\"\"\n):"
))
story.append(P("This allows the same function to calculate:"))
story.append(code_block("affordability_index"))
story.append(P("and:"))
story.append(code_block("affordability_index_50"))
story.append(P("without duplicating analytical logic."))
story.append(P("That makes the pipeline more maintainable and easier to extend to "
               "other scenarios."))

# =================================================================
# 22. Limitations
# =================================================================
story.append(section("22.", "Limitations"))
story.append(P("The project has several important limitations."))

story.append(P("25.1 Affordability is a proxy", "H2"))
story.append(P("The affordability index is <b>not an official Eurostat purchasing-power "
               "measure</b>."))
story.append(P("It is a project-specific analytical indicator based on:"))
story.append(formula_box("NetEarnings / PLI"))
story.append(P("It should therefore be interpreted as a <b>simplified purchasing-power "
               "proxy</b>."))

story.append(P("25.2 PLI is not a complete cost-of-living measure", "H2"))
story.append(P(
    "The PLI covers household final consumption expenditure, but the cost "
    "experienced by an individual depends on their specific consumption "
    "basket."
))
story.append(P("For example:"))
story.append(bullets(["housing;", "food;", "transport;", "healthcare;",
                       "education;", "energy"]))
story.append(P("can differ considerably in importance between individuals."))
story.append(P(
    "Eurostat itself publishes more detailed PLI categories because overall "
    "household consumption is only one level of analysis."
))

story.append(P("25.3 Gross vs. net earnings distinction", "H2"))
story.append(P(
    "The project uses <b>net earnings</b>, which is appropriate for an "
    "affordability-oriented analysis because net income is closer to the "
    "amount actually available to households."
))
story.append(P("However, differences in:"))
story.append(bullets(["taxation;", "social contributions;", "benefits;",
                       "household structure"]))
story.append(P("can influence the comparison."))

story.append(P("25.4 Worker profile", "H2"))
story.append(P("The analysis focuses on a specific worker profile:"))
story.append(P("Single person without children earning 100% of average earnings.", "Quote"))
story.append(P("Therefore, the results should not automatically be generalized to:"))
story.append(bullets([
    "families;", "households with children;", "part-time workers;",
    "retirees;", "unemployed people;", "high-income workers;",
    "minimum-wage workers.",
]))

story.append(P("25.5 Cross-sectional analysis", "H2"))
story.append(P("The main analysis focuses on <b>2025</b>."))
story.append(P(
    "Therefore, the regression identifies a cross-country relationship for "
    "one period rather than a time-series relationship."
))
story.append(P("A future version could examine:"))
story.append(code_block("2015 \u2192 2016 \u2192 ... \u2192 2025"))
story.append(P("to investigate how affordability has evolved over time."))

story.append(P("25.6 Correlation does not imply causation", "H2"))
story.append(P("The correlation of <b>0.937</b> is strong, but it does not demonstrate "
               "that higher prices cause higher wages."))
story.append(P("The relationship likely reflects broader economic differences between "
               "countries."))
story.append(P("The regression should therefore be interpreted as <b>descriptive</b>, "
               "not causal."))

story.append(PageBreak())

# =================================================================
# 23. Key Findings
# =================================================================
story.append(section("23.", "Key Findings"))
story.append(P("The project produces several major findings."))

findings = [
    ("Finding 1 \u2014 Price levels differ dramatically across Europe",
     "The 2025 household-consumption PLI ranged from approximately "
     "<b>62.5 in Bulgaria</b> to <b>139.7 in Denmark</b>. Eurostat "
     "independently reports the same broad range."),
    ("Finding 2 \u2014 High prices tend to coexist with high earnings",
     "The correlation between PLI and net earnings was <b>r = 0.937</b> "
     "with <b>R\u00b2 = 0.877</b>. This represents a very strong descriptive "
     "relationship in the 27-country sample."),
    ("Finding 3 \u2014 High salaries do not automatically mean poor affordability",
     "Luxembourg demonstrates this particularly clearly. It has very high "
     "consumer prices, but its exceptionally high net earnings result in "
     "the highest affordability index."),
    ("Finding 4 \u2014 Low prices do not automatically mean strong purchasing power",
     "Romania and Bulgaria have among the lowest price levels in the EU, "
     "but their lower earnings result in affordability indices below the "
     "EU benchmark."),
    ("Finding 5 \u2014 Denmark illustrates the importance of relative analysis",
     "Denmark has the highest PLI, but still has an affordability index "
     "above 100. Its position would look considerably worse if only price "
     "levels were considered."),
    ("Finding 6 \u2014 Income scenarios matter",
     "The 50%-earnings scenario changes the relative affordability picture "
     "significantly for several countries. This demonstrates why a single "
     "\u201caverage salary\u201d metric is insufficient for understanding "
     "household economic conditions."),
    ("Finding 7 \u2014 The regression identifies important outliers",
     "Luxembourg's earnings are dramatically above the regression "
     "expectation, while Estonia and Greece are among the countries with "
     "the largest negative residuals. This provides a useful second layer "
     "of analysis beyond simple rankings."),
]
for title, body in findings:
    story.append(P(title, "H3"))
    story.append(P(body))

story.append(PageBreak())
# =================================================================
# 24. Overall Interpretation
# =================================================================
story.append(section("24.", "Overall Interpretation"))
story.append(P("The central conclusion of the project is:"))
story.append(P("Cost of living should not be evaluated independently from income.", "Quote"))
story.append(P("A country can be:"))
story.append(bullets([
    "expensive but highly affordable;", "inexpensive but relatively unaffordable;",
    "high-income but expensive;", "low-income but inexpensive.",
]))
story.append(P("The economically meaningful comparison is therefore not simply:"))
story.append(P("\u201cWhere are prices lowest?\u201d", "Quote"))
story.append(P("or:"))
story.append(P("\u201cWhere are salaries highest?\u201d", "Quote"))
story.append(P("but rather:"))
story.append(P("\u201cHow does the income available to a representative worker compare "
               "with the price level they face?\u201d", "Quote"))
story.append(P("The project attempts to answer this question through the "
               "affordability index."))


# =================================================================
# 25. Project Value
# =================================================================
story.append(section("25.", "Project Value"))
story.append(P("From a data analytics perspective, the project demonstrates a "
               "complete workflow:"))

value_items = [
    ("Data acquisition", "Working with real-world Eurostat datasets."),
    ("Data cleaning", "Handling metadata-heavy statistical exports and "
                       "selecting relevant observations."),
    ("Data validation", "Checking missing values, duplicates, geography and "
                         "reference observations."),
    ("Data transformation", "Merging earnings and PLI datasets."),
    ("Statistical analysis", "Using correlation, linear regression, R\u00b2, "
                              "residual analysis."),
    ("Feature engineering", "Creating earnings index, earnings-to-PLI, "
                             "affordability index, scenario comparison."),
    ("Data visualization", "Creating ranked charts, scatter plots, "
                            "regression visualizations, dumbbell/change charts."),
    ("Business intelligence", "Building an interactive Power BI dashboard."),
    ("Application development", "Building an interactive Streamlit application."),
    ("Software engineering", "Organizing reusable functions into a src "
                              "package and maintaining the project through Git/GitHub."),
]
for title, body in value_items:
    story.append(P(title, "H3"))
    story.append(P(body))

story.append(P("This makes the project considerably broader than a simple exploratory "
               "notebook."))

# =================================================================
# 26. Future Improvements
# =================================================================
story.append(section("26.", "Future Improvements"))
story.append(P("Several extensions would make the analysis significantly stronger."))

story.append(P("Historical analysis", "H2"))
story.append(P("Instead of only 2025:"))
story.append(code_block("2015\u20132025"))
story.append(P("could be analyzed to determine whether affordability has improved or "
               "deteriorated."))

story.append(P("More detailed consumption categories", "H2"))
story.append(P("Instead of overall household consumption, the project could examine:"))
story.append(bullets([
    "food;", "housing;", "transport;", "energy;", "restaurants;",
    "recreation;", "healthcare;", "education.",
]))
story.append(P("This would allow the creation of category-specific affordability "
               "measures."))
story.append(P("Eurostat's PPP data provides detailed categories for this purpose."))

story.append(P("Household scenarios", "H2"))
story.append(P("Additional profiles could include:"))
story.append(bullets([
    "single person;", "couple;", "couple with children;",
    "minimum-wage worker;", "median worker;", "high-income worker.",
]))

story.append(P("Housing-adjusted affordability", "H2"))
story.append(P(
    "Housing is one of the largest household expenditure categories and "
    "varies significantly between countries. Eurostat's 2025 publication "
    "shows particularly large differences in housing-related price levels."
))
story.append(P(
    "A housing-adjusted index could therefore provide a more realistic "
    "measure of disposable purchasing power."
))

story.append(P("More sophisticated statistical models", "H2"))
story.append(P("The linear regression could eventually be extended using:"))
story.append(bullets([
    "multiple regression;", "robust regression;", "clustering;", "PCA;",
    "panel-data models.",
]))
story.append(P("Additional explanatory variables could include:"))
story.append(bullets([
    "GDP per capita;", "productivity;", "unemployment;", "taxation;",
    "housing costs;", "social expenditure.",
]))

story.append(PageBreak())

# =================================================================
# 27. Final Conclusion
# =================================================================
story.append(section("27.", "Final Conclusion"))
story.append(P(
    "This project demonstrates that comparing European living standards "
    "requires more than comparing salaries or consumer prices individually."
))
story.append(P(
    "The 2025 data reveals a strong relationship between national price "
    "levels and net earnings, but the relationship is far from uniform. "
    "Countries such as Luxembourg demonstrate that exceptionally high "
    "earnings can compensate for high prices, while Romania and Bulgaria "
    "demonstrate that very low prices do not necessarily translate into "
    "high purchasing power."
))
story.append(P(
    "The project's affordability index provides a practical way to combine "
    "these two dimensions into a single comparative measure. The regression "
    "and residual analysis then adds another layer by identifying countries "
    "whose earnings are unusually high or low relative to their price level."
))
story.append(P("The overall analysis therefore moves through three increasingly "
               "meaningful questions:"))
story.append(P("How much do things cost? \u2192 PLI", "Quote"))
story.append(P("How much do people earn? \u2192 Net earnings", "Quote"))
story.append(P("How much purchasing power does that income imply? \u2192 Affordability index", "Quote"))
story.append(P(
    "The combination of <b>Python analytics, statistical modelling, Power "
    "BI and Streamlit</b> turns the project into a complete end-to-end data "
    "analytics portfolio piece, demonstrating not only the ability to "
    "analyze a dataset but also to transform raw statistical data into "
    "reusable analytical logic, interactive dashboards and an interpretable "
    "economic narrative."
))

story.append(Spacer(1, 14))
story.append(hr())
story.append(P("Data references", "H3"))
story.append(P(
    "The primary data sources are Eurostat's <b>Annual net earnings "
    "(earn_nt_net)</b> dataset and its <b>Purchasing Power Parities / Price "
    "Level Indices (prc_ppp_ind_1)</b> data."
))
story.append(P(
    '<link href="https://ec.europa.eu/eurostat/en/web/products-datasets/-/EARN_NT_NET" '
    'color="#1F4E79">Eurostat \u2014 Annual net earnings dataset</link>',
    "Body",
))
story.append(P(
    '<link href="https://ec.europa.eu/eurostat/en/web/purchasing-power-parities" '
    'color="#1F4E79">Eurostat \u2014 Purchasing Power Parities</link>',
    "Body",
))


# ---------------------------------------------------------------
# Page decoration: header / footer / page numbers
# ---------------------------------------------------------------
def on_page(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setStrokeColor(BORDER)
        canvas.setLineWidth(0.6)
        canvas.line(0.85 * inch, PAGE_H - 0.75 * inch, PAGE_W - 0.85 * inch, PAGE_H - 0.75 * inch)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(MUTED)
        canvas.drawString(0.85 * inch, PAGE_H - 0.68 * inch, "European Cost of Living Analysis")
        canvas.drawRightString(PAGE_W - 0.85 * inch, PAGE_H - 0.68 * inch, "Detailed Project Report")

        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 8.3)
        canvas.drawCentredString(PAGE_W / 2, 0.55 * inch, f"{doc.page - 1}")
        canvas.drawString(0.85 * inch, 0.55 * inch, "Eurostat, 2025")
        canvas.drawRightString(PAGE_W - 0.85 * inch, 0.55 * inch, "European Cost of Living & Affordability Analysis")
    canvas.restoreState()


doc = SimpleDocTemplate(
    str(SCRIPT_DIR / "European_Cost_of_Living_Analysis_Report.pdf"),
    pagesize=letter,
    leftMargin=0.85 * inch, rightMargin=0.85 * inch,
    topMargin=0.95 * inch, bottomMargin=0.9 * inch,
    title="European Cost of Living Analysis — Detailed Project Report",
    author="European Cost of Living & Affordability Analysis Project",
)

doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print("PDF built successfully.")
