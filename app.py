import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import io
import ast

# 1. PAGE CONFIG
st.set_page_config(page_title="Halton Real Estate Analytics", layout="wide")
st.markdown("<style>.block-container {padding-top: 5rem;}</style>", unsafe_allow_html=True)

st.title("📊 Full Market Comparison Dashboard")

# --- SIDEBAR ---
st.sidebar.header("Data Configuration")
default_data = """{
    'Metric': [
        'Sale Volume', 'Avg Sale Price', 'Med Sale Price', 
        'New Listings', 'SNLR', 'Active Listings', 'MOI'
    ],
    'Jan 2025': [136, 1364747, 1249250, 609, 22, 780, 5.78],
    'Jan 2026': [132, 1313103, 1150000, 193, 68, 703, 6.01]
}"""

raw_input = st.sidebar.text_area("Paste Data Dictionary:", value=default_data, height=300)

# 2. DATA LOADING
try:
    data_dict = ast.literal_eval(raw_input.strip())
    df = pd.DataFrame(data_dict)
    all_cols = df.columns.tolist()
    comparison_cols = all_cols[1:3] 
except Exception as e:
    st.sidebar.error(f"Format Error: {e}")
    st.stop()

# 3. DASHBOARD GENERATION
def create_dashboard(df, comparison_cols):
    bg_color = '#F9F4EC' 
    c_teal = '#2C5F63'
    c_rust = '#D96C45'
    c_gold = '#DAA520'
    
    fig = plt.figure(figsize=(20, 28), facecolor=bg_color)
    gs = fig.add_gridspec(3, 1, height_ratios=[0.7, 1, 0.1], hspace=0.4)

    # --- TABLE SECTION ---
    ax_table = fig.add_subplot(gs[0])
    ax_table.axis('off')
    display_df = df.copy()

    for col in comparison_cols:
        if 1 in display_df.index: display_df.at[1, col] = f"${float(display_df.at[1, col]):,.0f}"
        if 2 in display_df.index: display_df.at[2, col] = f"${float(display_df.at[2, col]):,.0f}"
        if 4 in display_df.index: display_df.at[4, col] = f"{display_df.at[4, col]}%"

    table = ax_table.table(cellText=display_df.values, colLabels=display_df.columns, 
                           loc='center', cellLoc='center', bbox=[0.05, 0, 0.9, 0.85])
    table.auto_set_font_size(False)
    table.set_fontsize(13)
    table.scale(1, 4)

    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor('#D1D1D1')
        if row == 0:
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor(c_teal)
        else:
            cell.set_facecolor('white' if row % 2 == 0 else '#F2EFED')

    ax_table.set_title(f"Market Report: {comparison_cols[0]} vs {comparison_cols[1]}", 
                       fontsize=32, fontweight='bold', pad=60)

    # --- CHART SECTION (DUAL AXIS ALL METRICS) ---
    ax_chart = fig.add_subplot(gs[1])
    ax_chart.set_facecolor(bg_color)

    # Group 1: Unit Based (Left Axis)
    unit_metrics = ['Sale Volume', 'New Listings', 'Active Listings', 'SNLR', 'MOI']
    indices_unit = [0, 3, 5, 4, 6]
    
    # Group 2: Price Based (Right Axis)
    price_metrics = ['Avg Sale Price', 'Med Sale Price']
    indices_price = [1, 2]

    x_units = np.arange(len(unit_metrics))
    x_prices = np.arange(len(unit_metrics), len(unit_metrics) + len(price_metrics))
    x_all = np.concatenate([x_units, x_prices])
    
    width = 0.35

    # Plot Unit Bars (Left Axis)
    v1_u = df.iloc[indices_unit, 1].values
    v2_u = df.iloc[indices_unit, 2].values
    r1 = ax_chart.bar(x_units - width/2, v1_u, width, label=f'{comparison_cols[0]} Units/%', color=c_teal)
    r2 = ax_chart.bar(x_units + width/2, v2_u, width, label=f'{comparison_cols[1]} Units/%', color=c_teal, alpha=0.5)

    # Plot Price Bars (Right Axis)
    ax_price = ax_chart.twinx()
    v1_p = df.iloc[indices_price, 1].values
    v2_p = df.iloc[indices_price, 2].values
    r3 = ax_price.bar(x_prices - width/2, v1_p, width, label=f'{comparison_cols[0]} Price', color=c_rust)
    r4 = ax_price.bar(x_prices + width/2, v2_p, width, label=f'{comparison_cols[1]} Price', color=c_rust, alpha=0.5)

    # Labels and Formatting
    ax_chart.set_ylabel('Units / Ratio / Months', fontsize=14, fontweight='bold', color=c_teal)
    ax_price.set_ylabel('Price ($)', fontsize=14, fontweight='bold', color=c_rust)
    ax_price.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x*1e-6:1.1f}M'))
    
    ax_chart.set_xticks(x_all)
    ax_chart.set_xticklabels(unit_metrics + price_metrics, fontsize=12, fontweight='bold', rotation=15)

    # Labels on top of bars
    def add_labels(rects, axis, is_price=False):
        for rect in rects:
            h = rect.get_height()
            label = f"${h/1e6:.2f}M" if is_price else f"{h:g}"
            axis.text(rect.get_x() + rect.get_width()/2., h + (h*0.01), label, ha='center', va='bottom', fontweight='bold', fontsize=10)

    add_labels(r1, ax_chart)
    add_labels(r2, ax_chart)
    add_labels(r3, ax_price, True)
    add_labels(r4, ax_price, True)

    ax_chart.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=False)
    fig.subplots_adjust(top=0.92) 

    return fig

# 4. DISPLAY
chart_fig = create_dashboard(df, comparison_cols)
st.pyplot(chart_fig)

# Download
buf = io.BytesIO()
chart_fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
st.download_button("📩 Download High-Res Dashboard", buf.getvalue(), "full_market_report.png", "image/png")
