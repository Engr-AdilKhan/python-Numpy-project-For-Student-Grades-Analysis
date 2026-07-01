"""
================================================================================
PAKISTAN POPULATION ANALYTICS DASHBOARD — MATPLOTLIB & SEABORN FOCUS
================================================================================
A single-file project analyzing Pakistan's population trends by province
(1990-2023), with special emphasis on Matplotlib and Seaborn: 5 different
chart types from EACH library, all in one file.

⚠️ NOTE ON DATA: The province-level population shares used here are based on
   approximate, publicly known census figures (1998 & 2017 censuses, and the
   2023 census total of ~241 million). The yearly series in between is
   MODELED using compound growth — not official year-by-year government
   data — so treat the numbers as realistic estimates for learning purposes,
   not as a citable source.

WHAT THIS PROJECT DOES:
    1. Builds a 34-year (1990-2023) population dataset for Pakistan's
       4 provinces + Islamabad Capital Territory
    2. Uses NUMPY to calculate growth rate, CAGR, density, and projections
    3. Uses PANDAS to group, compare, and pivot the data
    4. Uses MATPLOTLIB for 5 distinct chart types:
           - Line chart        : population trend per region over time
           - Stacked area chart: each region's share of the total over time
           - Horizontal bar chart: population density comparison (with labels)
           - Pie chart         : 2023 population share by region
           - Subplot grid      : 6 mini line charts (one per region) in 1 figure
    5. Uses SEABORN for 5 distinct chart types:
           - Heatmap           : population by region across census years
           - Grouped barplot   : urban vs rural population split
           - Lineplot w/ shading: growth rate trend with variability band
           - Violin plot       : full distribution shape of growth rates
           - Regression plot   : does land area predict population size?

HOW TO RUN:
    pip install numpy pandas matplotlib seaborn
    python pakistan_population_viz_focus.py

OUTPUT:
    - Full console report with all calculated statistics
    - 10 chart images saved automatically to ./output/
================================================================================
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ------------------------------------------------------------------------------
# SMALL HELPER FUNCTIONS — for nicely formatted console output
# ------------------------------------------------------------------------------

def print_title(text):
    width = 80
    print("\n╔" + "═" * (width - 2) + "╗")
    print("║" + text.center(width - 2) + "║")
    print("╚" + "═" * (width - 2) + "╝")


def print_section(text):
    width = 80
    print("\n┌" + "─" * (width - 2) + "┐")
    print("│ " + text.ljust(width - 3) + "│")
    print("└" + "─" * (width - 2) + "┘")


def print_table(headers, rows, col_widths):
    border = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
    print(border)
    header_row = "|"
    for h, w in zip(headers, col_widths):
        header_row += f" {h:^{w}} |"
    print(header_row)
    print(border)
    for row in rows:
        row_str = "|"
        for cell, w in zip(row, col_widths):
            row_str += f" {str(cell):^{w}} |"
        print(row_str)
    print(border)


# ==============================================================================
# STEP 1: BUILD THE POPULATION DATASET (modeled from approximate census data)
# ==============================================================================
def generate_population_data():
    """Builds a yearly (1990-2023) population series for each region using
    NumPy's compound growth formula, anchored to the approximate 2023
    census total of ~241 million people."""

    years = np.arange(1990, 2024)  # 1990 to 2023 inclusive

    # Approximate 2023 population (millions) and area (km²) per region,
    # based on general public census knowledge.
    region_info = {
        "Punjab":       dict(pop_2023=127.7, area_km2=205344, annual_growth=0.021, urban_share=0.40),
        "Sindh":        dict(pop_2023=55.7,  area_km2=140914, annual_growth=0.025, urban_share=0.53),
        "Khyber Pakhtunkhwa": dict(pop_2023=40.9, area_km2=101741, annual_growth=0.028, urban_share=0.19),
        "Balochistan":  dict(pop_2023=14.9,  area_km2=347190, annual_growth=0.031, urban_share=0.28),
        "Islamabad":    dict(pop_2023=2.36,  area_km2=906,    annual_growth=0.040, urban_share=0.50),
    }

    records = []
    for region, info in region_info.items():
        pop_2023 = info["pop_2023"]
        rate = info["annual_growth"]

        # NUMPY: project backward from 2023 using the compound growth formula
        #   population(year) = population(2023) / (1 + rate)^(2023 - year)
        # This single vectorized line calculates all 34 years at once —
        # no loop needed.
        years_from_2023 = 2023 - years
        population_millions = pop_2023 / np.power(1 + rate, years_from_2023)

        for year, pop in zip(years, population_millions):
            records.append({
                "Year": int(year),
                "Region": region,
                "Population_Millions": round(float(pop), 3),
                "Area_KM2": info["area_km2"],
                "Urban_Share": info["urban_share"],
            })

    df = pd.DataFrame(records)
    return df


# ==============================================================================
# MAIN PROGRAM
# ==============================================================================
def main():
    os.makedirs("output", exist_ok=True)
    sns.set_theme(style="whitegrid")

    print_title("🇵🇰  PAKISTAN POPULATION ANALYTICS — MATPLOTLIB & SEABORN FOCUS  🇵🇰")

    df = generate_population_data()

    print(f"\n  Regions covered : {df['Region'].nunique()}")
    print(f"  Years covered   : {df['Year'].min()} to {df['Year'].max()}")
    print(f"  Total rows      : {len(df)}")

    print_section("DATA SAMPLE: Year 2023 Snapshot")
    snapshot = df[df["Year"] == 2023].sort_values("Population_Millions", ascending=False)
    rows = [[r.Region, f"{r.Population_Millions:.2f}M", f"{r.Area_KM2:,} km²"]
            for r in snapshot.itertuples()]
    print_table(["Region", "Population (2023)", "Area"], rows, [22, 18, 14])

    # ==========================================================================
    # STEP 2: NUMPY — growth rates, density, and projections
    # ==========================================================================
    print_section("NUMPY: Growth Rate & Density Calculations")

    # --- Population density = population / area (vectorized with NumPy) ---
    snapshot = snapshot.copy()
    pop_array = snapshot["Population_Millions"].to_numpy() * 1_000_000   # convert to actual people
    area_array = snapshot["Area_KM2"].to_numpy()
    density = np.round(pop_array / area_array, 1)
    snapshot["Density_per_km2"] = density

    print("  Population density (people per km²) — calculated with NumPy:")
    for region, dens in zip(snapshot["Region"], snapshot["Density_per_km2"]):
        print(f"    {region:22s} : {dens:>8,.1f} people/km²")

    # --- CAGR (Compound Annual Growth Rate) per region, 1990 -> 2023 ---
    print("\n  Compound Annual Growth Rate (CAGR), 1990 -> 2023:")
    print("  Formula: CAGR = (End/Start)^(1/years) - 1")
    cagr_results = {}
    for region in df["Region"].unique():
        region_df = df[df["Region"] == region].sort_values("Year")
        start_pop = region_df.iloc[0]["Population_Millions"]
        end_pop = region_df.iloc[-1]["Population_Millions"]
        n_years = region_df.iloc[-1]["Year"] - region_df.iloc[0]["Year"]
        cagr = (end_pop / start_pop) ** (1 / n_years) - 1   # NumPy-style math (works with plain floats too)
        cagr_results[region] = cagr
        print(f"    {region:22s} : {cagr*100:.2f}% per year")

    fastest_growing = max(cagr_results, key=cagr_results.get)
    slowest_growing = min(cagr_results, key=cagr_results.get)
    print(f"\n  🚀  Fastest growing region : {fastest_growing} ({cagr_results[fastest_growing]*100:.2f}%/yr)")
    print(f"  🐢  Slowest growing region : {slowest_growing} ({cagr_results[slowest_growing]*100:.2f}%/yr)")

    # --- 10-year future projection using NumPy's compound growth formula ---
    print_section("NUMPY: 10-Year Population Projection (2024-2033)")
    future_years = np.arange(2024, 2034)
    rows = []
    for region in df["Region"].unique():
        pop_2023 = df[(df["Region"] == region) & (df["Year"] == 2023)]["Population_Millions"].values[0]
        rate = cagr_results[region]
        # Vectorized projection for all 10 future years in one line
        projected = pop_2023 * np.power(1 + rate, future_years - 2023)
        rows.append([region, f"{projected[0]:.2f}M", f"{projected[-1]:.2f}M",
                     f"+{(projected[-1] - pop_2023):.2f}M"])
    print_table(["Region", "2024 (proj.)", "2033 (proj.)", "10-Yr Growth"], rows, [22, 14, 14, 14])

    # ==========================================================================
    # STEP 3: PANDAS — grouping, comparison, pivoting
    # ==========================================================================
    print_section("PANDAS: National Totals Per Year (sample years)")
    national_totals = df.groupby("Year")["Population_Millions"].sum()
    sample_years = [1990, 2000, 2010, 2017, 2023]
    rows = [[y, f"{national_totals[y]:.1f}M"] for y in sample_years]
    print_table(["Year", "National Population"], rows, [10, 20])

    print_section("PANDAS: Province Share of National Population (2023)")
    total_2023 = snapshot["Population_Millions"].sum()
    snapshot["Share_%"] = (snapshot["Population_Millions"] / total_2023 * 100).round(1)
    rows = [[row["Region"], f"{row['Population_Millions']:.2f}M", f"{row['Share_%']}%"]
            for _, row in snapshot.iterrows()]
    print_table(["Region", "Population", "Share of Pakistan"], rows, [22, 14, 18])

    # --- Pivot table: Region x Year matrix for selected years (used later in heatmap) ---
    pivot_years = [1990, 1998, 2008, 2017, 2023]
    pivot = df[df["Year"].isin(pivot_years)].pivot_table(
        index="Region", columns="Year", values="Population_Millions"
    )
    print_section("PANDAS: Pivot Table (Region x Year)")
    print(pivot.round(2).to_string())

    # ==========================================================================
    # STEP 4: MATPLOTLIB IN DEPTH — 5 different chart types
    # ==========================================================================
    pivot_full = df.pivot_table(index="Year", columns="Region", values="Population_Millions")
    snapshot_sorted = snapshot.sort_values("Density_per_km2", ascending=False)

    # --- 4.1 Line chart: population growth over time per region ---
    plt.figure(figsize=(11, 6))
    for region in df["Region"].unique():
        region_df = df[df["Region"] == region].sort_values("Year")
        plt.plot(region_df["Year"], region_df["Population_Millions"], label=region, linewidth=2)
    plt.title("Pakistan: Population Growth by Region (1990-2023)")
    plt.xlabel("Year")
    plt.ylabel("Population (Millions)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("output/01_population_growth_line.png", dpi=120)
    plt.close()

    # --- 4.2 Stacked area chart: each region's share of total population over time ---
    plt.figure(figsize=(11, 6))
    plt.stackplot(pivot_full.index, pivot_full.values.T, labels=pivot_full.columns,
                  colors=sns.color_palette("Set2"))
    plt.title("Pakistan: Population Composition by Region (Stacked)")
    plt.xlabel("Year")
    plt.ylabel("Population (Millions)")
    plt.legend(loc="upper left")
    plt.tight_layout()
    plt.savefig("output/02_population_stacked_area.png", dpi=120)
    plt.close()

    # --- 4.3 Horizontal bar chart: population density comparison ---
    plt.figure(figsize=(9, 5))
    bars = plt.barh(snapshot_sorted["Region"], snapshot_sorted["Density_per_km2"], color="teal")
    plt.bar_label(bars, fmt="%.0f", padding=3)   # labels the exact value on each bar
    plt.title("Population Density by Region (2023)")
    plt.xlabel("People per km²")
    plt.gca().invert_yaxis()   # highest density at the top
    plt.tight_layout()
    plt.savefig("output/03_density_bar_chart.png", dpi=120)
    plt.close()

    # --- 4.4 Pie chart: 2023 population share by region ---
    plt.figure(figsize=(7, 7))
    plt.pie(snapshot["Population_Millions"], labels=snapshot["Region"],
            autopct="%1.1f%%", startangle=90, colors=sns.color_palette("pastel"),
            explode=[0.06 if r == fastest_growing else 0 for r in snapshot["Region"]])
    plt.title("Pakistan: Share of National Population by Region (2023)")
    plt.tight_layout()
    plt.savefig("output/04_population_share_pie.png", dpi=120)
    plt.close()

    # --- 4.5 Multi-panel subplot grid: one mini chart per region, all in one figure ---
    # This is a key Matplotlib skill: plt.subplots() creates a GRID of axes that
    # we loop through, so multiple related charts can be compared side by side.
    regions = df["Region"].unique()
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    axes = axes.flatten()   # turn the 2x3 grid into a simple list of 6 slots
    for i, region in enumerate(regions):
        region_df = df[df["Region"] == region].sort_values("Year")
        axes[i].plot(region_df["Year"], region_df["Population_Millions"], color="darkorange")
        axes[i].fill_between(region_df["Year"], region_df["Population_Millions"], alpha=0.2, color="darkorange")
        axes[i].set_title(region, fontsize=11)
        axes[i].set_xlabel("Year")
        axes[i].set_ylabel("Population (M)")
    for j in range(len(regions), len(axes)):   # hide any unused empty subplot slots
        axes[j].axis("off")
    fig.suptitle("Pakistan: Individual Region Growth Trends (1990-2023)", fontsize=14)
    plt.tight_layout()
    plt.savefig("output/05_region_subplots_grid.png", dpi=120)
    plt.close()

    print_section("MATPLOTLIB charts saved (5 chart types)")
    print("  📈  output/01_population_growth_line.png   (line chart)")
    print("  🗺️   output/02_population_stacked_area.png  (stacked area chart)")
    print("  📊  output/03_density_bar_chart.png         (horizontal bar chart)")
    print("  🥧  output/04_population_share_pie.png      (pie chart)")
    print("  🔲  output/05_region_subplots_grid.png       (multi-panel subplot grid)")

    # ==========================================================================
    # STEP 5: SEABORN IN DEPTH — 5 different statistical chart types
    # ==========================================================================

    # --- 5.1 Heatmap: population by region across selected census years ---
    plt.figure(figsize=(9, 5))
    sns.heatmap(pivot, annot=True, fmt=".1f", cmap="YlOrRd", linewidths=0.5)
    plt.title("Population (Millions) by Region Across Key Census Years")
    plt.xlabel("Year")
    plt.ylabel("Region")
    plt.tight_layout()
    plt.savefig("output/06_population_heatmap.png", dpi=120)
    plt.close()

    # --- 5.2 Grouped barplot: urban vs rural population split per region (2023) ---
    urban_rural_rows = []
    for _, row in snapshot.iterrows():
        urban_pop = row["Population_Millions"] * row["Urban_Share"]
        rural_pop = row["Population_Millions"] * (1 - row["Urban_Share"])
        urban_rural_rows.append({"Region": row["Region"], "Type": "Urban", "Population": urban_pop})
        urban_rural_rows.append({"Region": row["Region"], "Type": "Rural", "Population": rural_pop})
    urban_rural_df = pd.DataFrame(urban_rural_rows)

    plt.figure(figsize=(10, 5))
    sns.barplot(data=urban_rural_df, x="Region", y="Population", hue="Type", palette="muted")
    plt.title("Urban vs Rural Population by Region (2023, Millions)")
    plt.xlabel("Region")
    plt.ylabel("Population (Millions)")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig("output/07_urban_rural_barplot.png", dpi=120)
    plt.close()

    # --- 5.3 Lineplot with confidence shading: national year-over-year growth rate ---
    variation_rows = []
    for region in df["Region"].unique():
        region_df = df[df["Region"] == region].sort_values("Year").reset_index(drop=True)
        region_df["Growth_Rate_%"] = region_df["Population_Millions"].pct_change() * 100
        variation_rows.append(region_df)
    growth_variation_df = pd.concat(variation_rows, ignore_index=True)

    plt.figure(figsize=(11, 5))
    sns.lineplot(data=growth_variation_df, x="Year", y="Growth_Rate_%",
                 errorbar="sd", color="darkblue")
    plt.title("Pakistan: Year-over-Year Population Growth Rate\n(line = average across regions, shaded band = variation between regions)")
    plt.xlabel("Year")
    plt.ylabel("Growth Rate (%)")
    plt.tight_layout()
    plt.savefig("output/08_growth_rate_trend.png", dpi=120)
    plt.close()

    # --- 5.4 Violin plot: distribution of each region's yearly growth rate ---
    # A violin plot shows the FULL SHAPE of the data's distribution (like a
    # boxplot, but smoother) — useful for seeing which regions had more
    # volatile/erratic growth vs. stable, predictable growth.
    plt.figure(figsize=(10, 5))
    sns.violinplot(data=growth_variation_df, x="Region", y="Growth_Rate_%",
                    hue="Region", palette="coolwarm", legend=False)
    plt.title("Distribution of Yearly Growth Rates by Region (1990-2023)")
    plt.xlabel("Region")
    plt.ylabel("Growth Rate (%)")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig("output/09_growth_rate_violinplot.png", dpi=120)
    plt.close()

    # --- 5.5 Scatter/regression plot: does land area relate to population size? ---
    plt.figure(figsize=(8, 6))
    sns.regplot(data=snapshot, x="Area_KM2", y="Population_Millions",
                scatter_kws={"s": 100, "color": "firebrick"}, line_kws={"color": "gray"})
    for _, row in snapshot.iterrows():   # label each point with its region name
        plt.text(row["Area_KM2"] * 1.02, row["Population_Millions"], row["Region"], fontsize=9)
    plt.title("Does Land Area Predict Population? (2023)")
    plt.xlabel("Area (km²)")
    plt.ylabel("Population (Millions)")
    plt.tight_layout()
    plt.savefig("output/10_area_vs_population_regplot.png", dpi=120)
    plt.close()

    print_section("SEABORN charts saved (5 chart types)")
    print("  🔥  output/06_population_heatmap.png            (heatmap)")
    print("  📊  output/07_urban_rural_barplot.png            (grouped barplot)")
    print("  📉  output/08_growth_rate_trend.png              (lineplot with conf. band)")
    print("  🎻  output/09_growth_rate_violinplot.png         (violin plot)")
    print("  📐  output/10_area_vs_population_regplot.png     (regression scatter plot)")

    # ==========================================================================
    # FINAL SUMMARY
    # ==========================================================================
    print_title("📋  FINAL POPULATION REPORT  📋")

    total_2023_people = total_2023 * 1_000_000
    summary_rows = [
        ["Total population (2023, est.)", f"{total_2023:.1f} Million"],
        ["Most populous region", f"{snapshot.iloc[0]['Region']} ({snapshot.iloc[0]['Population_Millions']:.1f}M)"],
        ["Least populous region", f"{snapshot.iloc[-1]['Region']} ({snapshot.iloc[-1]['Population_Millions']:.1f}M)"],
        ["Highest density region", f"{snapshot_sorted.iloc[0]['Region']} ({snapshot_sorted.iloc[0]['Density_per_km2']:.0f}/km²)"],
        ["Fastest growing region", f"{fastest_growing} ({cagr_results[fastest_growing]*100:.2f}%/yr)"],
        ["Slowest growing region", f"{slowest_growing} ({cagr_results[slowest_growing]*100:.2f}%/yr)"],
        ["Population growth 1990->2023", f"{national_totals[2023] - national_totals[1990]:.1f}M added"],
    ]
    print()
    print_table(["Metric", "Value"], summary_rows, [28, 36])

    print("\n✨ Done! This project used NumPy for growth/density/projection math and")
    print("   pandas for grouping/pivoting, then went deep on visualization: 5 chart")
    print("   types from Matplotlib (line, stacked area, bar, pie, subplot grid) and")
    print("   5 chart types from Seaborn (heatmap, barplot, lineplot, violin, regplot)")
    print("   — 10 charts total, all in one file.\n")
    print("⚠️  Reminder: population figures are modeled estimates based on public")
    print("   census knowledge, not official year-by-year government statistics.\n")


if __name__ == "__main__":
    main()
