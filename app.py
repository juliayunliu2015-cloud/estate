import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import io
import ast

# 1. PAGE CONFIG
st.set_page_config(page_title="Halton Real Estate Analytics", layout="wide")
st.markdown("<style>.block-container {padding-top: 5rem;}</style>", unsafe_allow_html=True)

st.title("📊 Market Comparison Dashboard")

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
    
    # Larger figure to accommodate two charts
    fig = plt.figure(figsize=(20, 32), facecolor=bg_color)
    gs = fig.add_gridspec(4, 1, height_ratios=[0.6, 1, 1, 0.1], hspace=0.4)

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

    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor('#D1D1D1')
        if row == 0:
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor(c_teal)
        else:
            cell.set_facecolor('white' if row % 2 == 0 else '#F2EFED')

    ax_table.set_title(f"\nMarket Report: {comparison_cols[0]} vs {comparison_cols[1]}", 
                       fontsize=32, fontweight='bold', pad=20)

    # Helper for labels
    def add_labels(rects, axis, is_price=False):
        for rect in rects:
            h = rect.get_height()
            label = f"${h/1e6:.2f}M" if is_price else f"{h:g}"
            axis.text(rect.get_x() + rect.get_width()/2., h + (h*0.01), label, ha='center', va='bottom', fontweight='bold', fontsize=11)

    width = 0.35

    # --- CHART 1: INVENTORY & ACTIVITY (Units / %) ---
    ax_vol = fig.add_subplot(gs[1])
    ax_vol.set_facecolor(bg_color)
    
    vol_metrics = ['Sale Volume', 'New Listings', 'Active Listings', 'SNLR', 'MOI']
    indices_vol = [0, 3, 5, 4, 6]
    x_vol = np.arange(len(vol_metrics))

    r1 = ax_vol.bar(x_vol - width/2, df.iloc[indices_vol, 1], width, label=comparison_cols[0], color=c_teal)
    r2 = ax_vol.bar(x_vol + width/2, df.iloc[indices_vol, 2], width, label=comparison_cols[1], color=c_teal, alpha=0.5)

    add_labels(r1, ax_vol)
    add_labels(r2, ax_vol)
    
    ax_vol.set_title('Inventory & Market Activity', fontsize=24, fontweight='bold', pad=20)
    ax_vol.set_xticks(x_vol)
    ax_vol.set_xticklabels(vol_metrics, fontsize=14, fontweight='bold')
    ax_vol.legend(loc='upper right', frameon=False)
    ax_vol.spines[['top', 'right']].set_visible(False)

    # --- CHART 2: PRICE TRENDS ($) ---
    ax_price = fig.add_subplot(gs[2])
    ax_price.set_facecolor(bg_color)

    price_metrics = ['Avg Sale Price', 'Med Sale Price']
    indices_price = [1, 2]
    x_price = np.arange(len(price_metrics))

    r3 = ax_price.bar(x_price - width/2, df.iloc[indices_price, 1], width, label=comparison_cols[0], color=c_rust)
    r4 = ax_price.bar(x_price + width/2, df.iloc[indices_price, 2], width, label=comparison_cols[1], color=c_rust, alpha=0.5)

    add_labels(r3, ax_price, is_price=True)
    add_labels(r4, ax_price, is_price=True)

    ax_price.set_title('Pricing Trends', fontsize=24, fontweight='bold', pad=20)
    ax_price.set_xticks(x_price)
    ax_price.set_xticklabels(price_metrics, fontsize=14, fontweight='bold')
    ax_price.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x*1e-6:1.1f}M'))
    ax_price.legend(loc='upper right', frameon=False)
    ax_price.spines[['top', 'right']].set_visible(False)

    fig.subplots_adjust(top=0.94) 
    return fig

# 4. DISPLAY
chart_fig = create_dashboard(df, comparison_cols)
st.pyplot(chart_fig)

# Download
buf = io.BytesIO()
chart_fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
st.download_button("📩 Download High-Res Dashboard", buf.getvalue(), "split_market_report.png", "image/png")
