import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import FuncFormatter
import io
import ast

# Page Configuration
st.set_page_config(page_title="Halton Real Estate Analytics", layout="wide")

st.title("📊 Halton Market Comparison Dashboard")
st.markdown("Paste your Python-style data dictionary in the sidebar to update the report instantly.")

# --- SIDEBAR INPUTS ---
st.sidebar.header("Data Configuration")

# Default data string for the text area
default_data_str = """{
    'Metric': [
        'Sale Volume', 'Avg Sale Price', 'Med Sale Price', 
        'New Listings', 'SNLR', 'Active Listings', 'MOI'
    ],
    'Jan 2025': [136, 1364747, 1249250, 609, 22, 780, 5.78],
    'Jan 2026': [132, 1313103, 1150000, 193, 68, 703, 6.01]
}"""

# Text box for raw data input
raw_input = st.sidebar.text_area("Paste Python Data Dict Here:", value=default_data_str, height=300)

# Process the input data
try:
    # Safely evaluate the string as a Python dictionary
    data_dict = ast.literal_eval(raw_input)
    df = pd.DataFrame(data_dict)
    st.sidebar.success("✅ Data parsed successfully!")
except Exception as e:
    st.sidebar.error(f"❌ Error in data format: {e}")
    # Fallback to empty/dummy dataframe to prevent crash
    df = pd.DataFrame(columns=['Metric', 'Jan 2025', 'Jan 2026'])

# --- CHART GENERATION FUNCTION ---
def generate_plot(df):
    if df.empty: return None
    
    bg_color = '#F9F4EC' 
    text_color = '#2B3A42'
    c_teal = '#2C5F63'
    c_rust = '#D96C45'
    
    fig = plt.figure(figsize=(18, 22), facecolor=bg_color)
    gs = fig.add_gridspec(3, 1, height_ratios=[0.8, 1, 0.1], hspace=0.4)

    # TABLE SECTION
    ax_table = fig.add_subplot(gs[0])
    ax_table.axis('off')
    
    display_df = df.copy()
    
    # Identify columns dynamically (exclude 'Metric')
    data_cols = [c for c in display_df.columns if c != 'Metric']
    
    # Formatting (Price and Percentages)
    for col in data_cols:
        display_df.loc[1:2, col] = display_df.loc[1:2, col].apply(lambda x: f"${float(x):,.0f}")
        display_df.loc[4, col] = display_df.loc[4, col].apply(lambda x: f"{x}%")

    table = ax_table.table(cellText=display_df.values, colLabels=display_df.columns, 
                           loc='center', cellLoc='center', bbox=[0.05, 0, 0.9, 0.8])
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 3.5)

    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor('#D1D1D1')
        if row == 0:
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor(c_teal)
        else:
            cell.set_facecolor('white' if row % 2 == 0 else '#F5F2ED')

    ax_table.set_title(f'Market Comparison: {data_cols[0]} vs {data_cols[1]}', fontsize=28, fontweight='bold', pad=40)

    # CHART SECTION
    ax_chart = fig.add_subplot(gs[1])
    ax_chart.set_facecolor(bg_color)
    
    plot_metrics = ['Sale Volume', 'New Listings', 'Active Listings', 'SNLR']
    
    # Extract indices based on metric names
    idx_map = {name: i for i, name in enumerate(df['Metric'])}
    
    v1_indices = [idx_map['Sale Volume'], idx_map['New Listings'], idx_map['Active Listings'], idx_map['SNLR']]
    v1 = df.iloc[v1_indices, 1].tolist()
    v2 = df.iloc[v1_indices, 2].tolist()

    x = np.arange(len(plot_metrics))
    width = 0.35
    ax_chart.bar(x - width/2, v1, width, label=data_cols[0], color=c_teal, alpha=0.8)
    ax_chart.bar(x + width/2, v2, width, label=data_cols[1], color=c_rust, alpha=0.8)

    for i, v in enumerate(v1):
        ax_chart.text(i - width/2, v + 5, str(v), ha='center', fontsize=10, fontweight='bold')
    for i, v in enumerate(v2):
        ax_chart.text(i + width/2, v + 5, str(v), ha='center', fontsize=10, fontweight='bold')

    ax_chart.set_xticks(x)
    ax_chart.set_xticklabels(plot_metrics, fontsize=14)
    ax_chart.legend(fontsize=14, frameon=False)
    ax_chart.spines['top'].set_visible(False)
    ax_chart.spines['right'].set_visible(False)

    return fig

# --- DISPLAY ---
if not df.empty:
    chart_fig = generate_plot(df)
    st.pyplot(chart_fig)

    # Download Button
    buf = io.BytesIO()
    chart_fig.savefig(buf, format="png", dpi=300)
    st.download_button(
        label="Download Dashboard as PNG",
        data=buf.getvalue(),
        file_name="halton_market_comparison.png",
        mime="image/png"
    )
else:
    st.warning("Please enter valid data in the sidebar to generate the report.")
