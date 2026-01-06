import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import io
import ast

# 1. PAGE CONFIG
st.set_page_config(page_title="Dynamic Market Analytics", layout="wide")
st.write("")
st.title("📊 Flexible Market Comparison Dashboard")
st.markdown("Paste any data dictionary. The app will automatically detect your Months/Years.")

# --- SIDEBAR ---
st.sidebar.header("Data Configuration")

default_data = """{
    'Metric': [
        'Sale Volume', 'Avg Sale Price', 'Med Sale Price', 
        'New Listings', 'SNLR', 'Active Listings', 'MOI'
    ],
    'Feb 2024': [120, 1250000, 1100000, 500, 24, 600, 5.0],
    'Feb 2025': [145, 1380000, 1200000, 550, 26, 620, 4.2]
}"""

raw_input = st.sidebar.text_area("Paste Python Data Dict Here:", value=default_data, height=300)

# 2. DYNAMIC DATA LOADING
try:
    data_dict = ast.literal_eval(raw_input.strip())
    df = pd.DataFrame(data_dict)
    
    # DYNAMICALLY IDENTIFY COLUMNS
    # The first column is our Metric labels, the rest are our "Comparison Variables"
    all_cols = df.columns.tolist()
    metric_col = all_cols[0]
    comparison_cols = all_cols[1:3] # Automatically picks the next two keys you provide
    
    st.sidebar.success(f"✅ Comparing: {comparison_cols[0]} vs {comparison_cols[1]}")
except Exception as e:
    st.sidebar.error("⚠️ Formatting Error. Check your commas and brackets.")
    st.stop()

# 3. DASHBOARD GENERATION
def create_dashboard(df, comparison_cols):
    bg_color = '#F9F4EC' 
    c_teal = '#2C5F63'
    c_rust = '#D96C45'
    
    fig = plt.figure(figsize=(18, 22), facecolor=bg_color)
    gs = fig.add_gridspec(3, 1, height_ratios=[0.8, 1, 0.1], hspace=0.4)

    # --- TABLE SECTION ---
    ax_table = fig.add_subplot(gs[0])
    ax_table.axis('off')
    display_df = df.copy()

    # Dynamic Formatting Logic
    for col in comparison_cols:
        if 1 in display_df.index: # Avg Price
            display_df.at[1, col] = f"${float(display_df.at[1, col]):,.0f}"
        if 2 in display_df.index: # Med Price
            display_df.at[2, col] = f"${float(display_df.at[2, col]):,.0f}"
        if 4 in display_df.index: # SNLR %
            display_df.at[4, col] = f"{display_df.at[4, col]}%"

    table = ax_table.table(cellText=display_df.values, colLabels=display_df.columns, 
                           loc='center', cellLoc='center', bbox=[0.05, 0, 0.9, 0.85])
    table.auto_set_font_size(False)
    table.set_fontsize(13)
    table.scale(1, 4)
    fig.subplots_adjust(top=0.90)
    # Style Header and Rows
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor('#D1D1D1')
        if row == 0:
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor(c_teal)
        else:
            cell.set_facecolor('white' if row % 2 == 0 else '#F2EFED')

    ax_table.set_title(f"Market Report: {comparison_cols[0]} vs {comparison_cols[1]}", 
                       fontsize=30, fontweight='bold', pad=40)

    # --- CHART SECTION ---
    ax_chart = fig.add_subplot(gs[1])
    ax_chart.set_facecolor(bg_color)
    
    plot_metrics = ['Sale Volume', 'New Listings', 'Active Listings', 'SNLR']
    # Match plot metrics to their index in your data
    indices = [df[df[metric_col] == m].index[0] for m in plot_metrics if m in df[metric_col].values]
    
    v1 = df.iloc[indices, 1].values
    v2 = df.iloc[indices, 2].values

    x = np.arange(len(plot_metrics))
    width = 0.35
    ax_chart.bar(x - width/2, v1, width, label=comparison_cols[0], color=c_teal, alpha=0.9)
    ax_chart.bar(x + width/2, v2, width, label=comparison_cols[1], color=c_rust, alpha=0.9)

    # Add Value Labels
    for i, v in enumerate(v1):
        ax_chart.text(i - width/2, v + 2, f"{v}", ha='center', fontweight='bold')
    for i, v in enumerate(v2):
        ax_chart.text(i + width/2, v + 2, f"{v}", ha='center', fontweight='bold')

    ax_chart.set_xticks(x)
    ax_chart.set_xticklabels(plot_metrics, fontsize=14)
    ax_chart.legend(fontsize=14, frameon=False)
    ax_chart.spines['top'].set_visible(False)
    ax_chart.spines['right'].set_visible(False)

    return fig

# 4. RUN DASHBOARD
if not df.empty:
    chart_fig = create_dashboard(df, comparison_cols)
    st.pyplot(chart_fig)
    
    # Export Download Button
    buf = io.BytesIO()
    chart_fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
    st.download_button("Download Image", buf.getvalue(), f"Report_{comparison_cols[1]}.png", "image/png")
