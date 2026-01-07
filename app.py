# --- CHART SECTION (Updated with Dual Axis) ---
ax_chart = fig.add_subplot(gs[1])
ax_chart.set_facecolor(bg_color)

# 1. SETUP DATA
# Indices 0 and 3 are Volume/Listings. Indices 1 and 2 are Prices.
vol_metrics = ['Sale Volume', 'New Listings']
price_metrics = ['Avg Sale Price', 'Med Sale Price']

# Extract values
v1_vol = [df.iloc[0, 1], df.iloc[3, 1]]
v2_vol = [df.iloc[0, 2], df.iloc[3, 2]]
v1_price = [df.iloc[1, 1], df.iloc[2, 1]]
v2_price = [df.iloc[1, 2], df.iloc[2, 2]]

x = np.arange(len(vol_metrics + price_metrics))
width = 0.35

# 2. PLOT VOLUMES (Left Axis)
rects1 = ax_chart.bar(x[:2] - width/2, v1_vol, width, label=f'{comparison_cols[0]} Vol', color=c_teal, alpha=0.9)
rects2 = ax_chart.bar(x[:2] + width/2, v2_vol, width, label=f'{comparison_cols[1]} Vol', color=c_teal, alpha=0.5)

# 3. PLOT PRICES (Right Axis)
ax_price = ax_chart.twinx()  # Create the secondary axis
rects3 = ax_price.bar(x[2:] - width/2, v1_price, width, label=f'{comparison_cols[0]} Price', color=c_rust, alpha=0.9)
rects4 = ax_price.bar(x[2:] + width/2, v2_price, width, label=f'{comparison_cols[1]} Price', color=c_rust, alpha=0.5)

# 4. FORMATTING
ax_chart.set_ylabel('Volume (Units)', fontsize=14, fontweight='bold', color=c_teal)
ax_price.set_ylabel('Price ($)', fontsize=14, fontweight='bold', color=c_rust)

# Formatting the price axis to show $M
ax_price.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x*1e-6:1.1f}M'))

# Set X-Ticks
ax_chart.set_xticks(x)
ax_chart.set_xticklabels(vol_metrics + price_metrics, fontsize=14)

# Combine Legends from both axes
lines, labels = ax_chart.get_legend_handles_labels()
lines2, labels2 = ax_price.get_legend_handles_labels()
ax_chart.legend(lines + lines2, labels + labels2, loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=2, frameon=False)

# Add Value Labels
def autolabel(rects, axis, is_price=False):
    for rect in rects:
        height = rect.get_height()
        label = f"${height/1e6:.1f}M" if is_price else f"{int(height)}"
        axis.annotate(label,
                      xy=(rect.get_x() + rect.get_width() / 2, height),
                      xytext=(0, 3),  
                      textcoords="offset points",
                      ha='center', va='bottom', fontweight='bold')

autolabel(rects1, ax_chart)
autolabel(rects2, ax_chart)
autolabel(rects3, ax_price, is_price=True)
autolabel(rects4, ax_price, is_price=True)

# Remove top spines
ax_chart.spines['top'].set_visible(False)
ax_price.spines['top'].set_visible(False)

# Ensure the subplots adjust properly for the space above the title
fig.subplots_adjust(top=0.88)
