import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import io
import ast

# 1. PAGE CONFIG
st.set_page_config(page_title="Halton Real Estate Dashboard", layout="wide")

st.title("📊 Real Estate Market Analytics")
st.markdown("Update the dashboard by pasting your data dictionary into the box on the left.")

# --- SIDEBAR: THE TEXT FIELD ---
st.sidebar.header("Manual Data Input")

# Initial placeholder data
default_data = """{
    'Metric': [
        'Sale Volume', 'Avg Sale Price', 'Med Sale Price', 
        'New Listings', 'SNLR', 'Active Listings', 'MOI'
    ],
    'Jan 2025': [136, 1364747, 1249250, 609, 22, 780, 5.78],
    'Jan 2026': [132, 1313103, 1150000, 193, 68, 703, 6.01]
}"""

raw_input = st.sidebar.text_area(
    "Paste your Data Dictionary here:", 
    value=default_data, 
    height=350,
    help="Ensure the format is exactly like the example provided."
)

# 2. DATA PROCESSING
try:
    # Safely convert the string into a Python dictionary
    data_dict = ast.literal_eval(raw_input.strip())
    df = pd.DataFrame(data_dict)
    
    # Identify Year Columns (all columns except 'Metric')
    year_cols = [c for c in df.columns if c != 'Metric']
    st.sidebar.success(f"✅ Loaded data for: {', '.join(year_cols)}")
except Exception as e:
    st.sidebar.error(f"⚠️ Data Format Error: Please check your brackets and commas.")
    st.stop() # Stop execution if data is broken

# 3. DASHBOARD GENERATION
def create_dashboard(df):
    # Styling Variables
    bg_color = '#F9F4EC' 
    c_teal = '#2C5F63'
    c_rust = '#D96C45'
    
    # High-Res Setup
    fig = plt.figure(figsize=(18, 24), facecolor=bg_color)
    gs = fig.add_gridspec(3, 1, height_ratios=[0.8, 1, 0.15], hspace=0.4)

    # --- SECTION A: FORMATTED TABLE ---
    ax_table = fig.add_subplot(gs[0])
    ax_table.axis('off')
    
    display_df = df.copy()
    
    # Format Dollars and Percentages for the table display
    for col in year_cols:
        # Format Price Rows (Index 1 and 2 usually Avg/Med Price)
        display_df.loc[1:2, col] = display_df.loc[1:2, col].apply(lambda x: f"${x:,.0f}")
        # Format SNLR Row (Index 4)
        display_df.loc[4, col] = display_df.loc[4, col].apply(lambda x: f"{x}%")

    table = ax_table.table(
        cellText=display_df.values, 
        colLabels=display_df.columns, 
        loc='center', 
        cellLoc='center', 
        bbox=[0.05, 0, 0.9, 0.85]
    )
    
    table.auto_set_font_size(False)
    table.set_fontsize(13)
    table.scale(1, 4)

    # Style Header and Alternating Rows
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor('#D1D1D1')
        if row == 0:
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor(c_teal)
        else:
            cell.set_facecolor('white' if row % 2 == 0 else '#F2EFED')

    ax_table.set_title(f"Year-Over-Year Market Comparison ({' vs '.join(year_cols)})", 
                       fontsize=30, fontweight='bold', pad=40, color='#2B3A42')

    # --- SECTION B: COMPARATIVE CHART ---
    ax_chart = fig.add_subplot(gs[1])
    ax_chart.set_facecolor(bg_color)
    
    # Mapping metrics to bar chart
    metrics_to_plot = ['Sale Volume', 'New Listings', 'Active Listings', 'SNLR']
    # Get indices for these metrics
    indices = [df[df['Metric'] == m].index[0] for m in metrics_to_plot]
    
    v1 = df.iloc[indices, 1].values
    v2 = df.iloc[indices, 2].values

    x = np.arange(len(metrics_to_plot))
    width = 0.35

    ax_chart.bar(x - width/2, v1, width, label=year_cols[0], color=c_teal, alpha=0.9)
    ax_chart.bar(x + width/2, v2, width, label=year_cols[1], color=c_rust, alpha=0.9)

    # Data Labels
    for i, v in enumerate(v1):
        ax_chart.text(i - width/2, v + 5, f"{v}", ha='center', fontweight='bold', fontsize=12)
    for i, v in enumerate(v2):
        ax_chart.text(i + width/2, v + 5, f"{v}", ha='center', fontweight='bold', fontsize=12)

    ax_chart.set_title('Market Dynamics: Inventory vs. Absorption', fontsize=26, fontweight='bold', pad=30)
    ax_chart.set_xticks(x)
    ax_chart.set_xticklabels(metrics_to_plot, fontsize=16)
    ax_chart.legend(fontsize=16, frameon=False, loc='upper right')
    ax_chart.spines['top'].set_visible(False)
    ax_chart.spines['right'].set_visible(False)
    ax_chart.yaxis.grid(True, linestyle='--', alpha=0.3)

    return fig

# 4. MAIN INTERFACE
chart_fig = create_dashboard(df)
st.pyplot(chart_fig)

# --- DOWNLOAD ACTION ---
buf = io.BytesIO()
chart_fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
st.download_button(
    label="📩 Download 8K Resolution Dashboard",
    data=buf.getvalue(),
    file_name=f"Market_Report_{year_cols[1]}.png",
    mime="image/png"
)

st.divider()
st.caption("Data processed locally. Created for Halton Region Analytics Portfolio.")
