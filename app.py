import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import FuncFormatter
import io

# Page Configuration
st.set_page_config(page_title="Halton Real Estate Analytics", layout="wide")

st.title("📊 Halton Market Year-Over-Year Comparison")
st.markdown("Update the values in the sidebar or upload a CSV to generate the 8K Dashboard.")

# --- SIDEBAR INPUTS ---
st.sidebar.header("Manual Data Input")

def manual_input():
    metrics = ['Sale Volume', 'Avg Sale Price', 'Med Sale Price', 'New Listings', 'SNLR', 'Active Listings', 'MOI']
    
    col1, col2 = st.sidebar.columns(2)
    
    jan_2025 = []
    jan_2026 = []
    
    with col1:
        st.subheader("Jan 2025")
        jan_2025.append(st.number_input("Sales (25)", value=136))
        jan_2025.append(st.number_input("Avg Price (25)", value=1364747))
        jan_2025.append(st.number_input("Med Price (25)", value=1249250))
        jan_2025.append(st.number_input("New List (25)", value=609))
        jan_2025.append(st.number_input("SNLR % (25)", value=22))
        jan_2025.append(st.number_input("Active (25)", value=780))
        jan_2025.append(st.number_input("MOI (25)", value=5.78))

    with col2:
        st.subheader("Jan 2026")
        jan_2026.append(st.number_input("Sales (26)", value=132))
        jan_2026.append(st.number_input("Avg Price (26)", value=1313103))
        jan_2026.append(st.number_input("Med Price (26)", value=1150000))
        jan_2026.append(st.number_input("New List (26)", value=193))
        jan_2026.append(st.number_input("SNLR % (26)", value=68))
        jan_2026.append(st.number_input("Active (26)", value=703))
        jan_2026.append(st.number_input("MOI (26)", value=6.01))

    return pd.DataFrame({
        'Metric': metrics,
        'Jan 2025': jan_2025,
        'Jan 2026': jan_2026
    })

# --- DATA SOURCE LOGIC ---
uploaded_file = st.sidebar.file_uploader("Or Upload CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = manual_input()

# --- CHART GENERATION FUNCTION ---
def generate_plot(df):
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
    # Formatting
    display_df.loc[1:2, 'Jan 2025'] = display_df.loc[1:2, 'Jan 2025'].apply(lambda x: f"${x:,.0f}")
    display_df.loc[1:2, 'Jan 2026'] = display_df.loc[1:2, 'Jan 2026'].apply(lambda x: f"${x:,.0f}")
    display_df.loc[4, 'Jan 2025'] = f"{display_df.loc[4, 'Jan 2025']}%"
    display_df.loc[4, 'Jan 2026'] = f"{display_df.loc[4, 'Jan 2026']}%"

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

    ax_table.set_title('Year-Over-Year Market Comparison', fontsize=28, fontweight='bold', pad=40)

    # CHART SECTION
    ax_chart = fig.add_subplot(gs[1])
    ax_chart.set_facecolor(bg_color)
    
    plot_metrics = ['Sale Volume', 'New Listings', 'Active Listings', 'SNLR']
    v25 = [df.iloc[0,1], df.iloc[3,1], df.iloc[5,1], df.iloc[4,1]]
    v26 = [df.iloc[0,2], df.iloc[3,2], df.iloc[5,2], df.iloc[4,2]]

    x = np.arange(len(plot_metrics))
    width = 0.35
    ax_chart.bar(x - width/2, v25, width, label='Jan 2025', color=c_teal, alpha=0.8)
    ax_chart.bar(x + width/2, v26, width, label='Jan 2026', color=c_rust, alpha=0.8)

    for i, v in enumerate(v25):
        ax_chart.text(i - width/2, v + 5, str(v), ha='center', fontsize=10, fontweight='bold')
    for i, v in enumerate(v26):
        ax_chart.text(i + width/2, v + 5, str(v), ha='center', fontsize=10, fontweight='bold')

    ax_chart.set_xticks(x)
    ax_chart.set_xticklabels(plot_metrics, fontsize=14)
    ax_chart.legend(fontsize=14, frameon=False)
    ax_chart.spines['top'].set_visible(False)
    ax_chart.spines['right'].set_visible(False)

    return fig

# --- DISPLAY ---
col_main, col_spacer = st.columns([4, 1])

with col_main:
    chart_fig = generate_plot(df)
    st.pyplot(chart_fig)

    # Download Button
    buf = io.BytesIO()
    chart_fig.savefig(buf, format="png", dpi=300)
    st.download_button(
        label="Download Dashboard as PNG",
        data=buf.getvalue(),
        file_name="halton_report.png",
        mime="image/png"
    )
