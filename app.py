import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import io
import ast

# 1. PAGE CONFIG & LAYOUT
st.set_page_config(page_title="Halton Real Estate Analytics", layout="wide")

# Precise CSS to add space at the very top of the web page
st.markdown("<style>.block-container {padding-top: 5rem;}</style>", unsafe_allow_html=True)

st.title("📊 Real Estate Market Comparison")

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
    metric_col = all_cols[0]
    comparison_cols = all_cols[1:3] 
except Exception as e:
    st.sidebar.error(f"Format Error: {e}")
    st.stop()

# 3. DASHBOARD GENERATION FUNCTION
def create_dashboard(df, comparison_cols):
    bg_color = '#F9F4EC' 
    c_teal = '#2C5F63'
    c_rust = '#D96C45'
    
    # Create figure with high resolution
    fig = plt.figure(figsize=(18, 26), facecolor=bg_color)
    gs = fig.add_gridspec(3, 1, height_ratios=[0.8, 1, 0.1], hspace=0.5)

    # --- SECTION A: TABLE ---
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

    # Styling Table Header
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor('#D1D1D1')
        if row == 0:
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor(c_teal)
        else:
            cell.set_facecolor('white' if row % 2 == 0 else '#F2EFED')

    # SPACE ABOVE TITLE: Created via pad and subplots_adjust
    ax_table.set_title(f"Market Report: {comparison_cols[0]} vs {comparison_cols[1]}", 
                       fontsize=32, fontweight='bold', pad=60)

    # --- SECTION B: CHART (DUAL AXIS) ---
    ax_chart = fig.add_subplot(gs[1])
    ax_chart.set_facecolor(bg_color)

    # Prepare Data
    vol_metrics = ['Sale Volume', 'New Listings']
    price_metrics = ['Avg Sale Price', 'Med Sale Price']
    
    v1_vol = [df.iloc[0, 1], df.iloc[3, 1]]
    v2_vol = [df.iloc[0, 2], df.iloc[3, 2]]
    v1_price = [df.iloc[1, 1], df.iloc[2, 1]]
    v2_price = [df.iloc[1, 2], df.iloc[2, 2]]

    x = np.arange(len(vol_metrics + price_metrics))
    width = 0.35

    # Plot Volume Bars (Left Y-Axis)
    rects1 = ax_chart.bar(x[:2] - width/2, v1_vol, width, label=f'{comparison_cols[0]}', color=c_teal)
    rects2 = ax_chart.bar(x[:2] + width/2, v2_vol, width, label=f'{comparison_cols[1]}', color=c_teal, alpha=0.5)

    # Plot Price Bars (Right Y-Axis)
    ax_price = ax_chart.twinx()
    rects3 = ax_price.bar(x[2:] - width/2, v1_price, width, label=f'{comparison_cols[0]} Price', color=c_rust)
    rects4 = ax_price.bar(x[2:] + width/2, v2_price, width, label=f'{comparison_cols[1]} Price', color=c_rust, alpha=0.5)

    # Labels and Formatting
    ax_chart.set_ylabel('Volume (Units)', fontsize=14, fontweight='bold', color=c_teal)
    ax_price.set_ylabel('Price ($)', fontsize=14, fontweight='bold', color=c_rust)
    ax_price.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x*1e-6:1.1f}M'))
    
    ax_chart.set_xticks(x)
    ax_chart.set_xticklabels(vol_metrics + price_metrics, fontsize=14, fontweight='bold')

    # Combined Legend
    h1, l1 = ax_chart.get_legend_handles_labels()
    h2, l2 = ax_price.get_legend_handles_labels()
    ax_chart.legend(h1 + h2, l1 + l2, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=False)

    # Adding Text Labels on Bars
    def add_labels(rects, axis, is_price=False):
        for rect in rects:
            h = rect.get_height()
            label = f"${h/1e6:.2f}M" if is_price else f"{int(h)}"
            axis.text(rect.get_x() + rect.get_width()/2., h + 3, label, ha='center', va='bottom', fontweight='bold')

    add_labels(rects1, ax_chart)
    add_labels(rects2, ax_chart)
    add_labels(rects3, ax_price, True)
    add_labels(rects4, ax_price, True)

    # Final Layout Adjustment for space at the very top of the image
    fig.subplots_adjust(top=0.92) 

    return fig

# 4. RUN AND DISPLAY
chart_fig = create_dashboard(df, comparison_cols)
st.pyplot(chart_fig)

# Download Button
buf = io.BytesIO()
chart_fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
st.download_button("📩 Download High-Res Dashboard", buf.getvalue(), "market_report.png", "image/png")
