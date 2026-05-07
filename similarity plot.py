import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib.lines import Line2D

# Load your CSV file
df = pd.read_csv(r"C:\Workspace\Thesis\coding\Github_test\output5_combined_si\ATCC17978.csv")

# Define a color map for each sample label
sample_colors = {
    'ATCC17978': 'green',
    'AB1': 'green',
    'AB2': 'green',
    'AB3': 'green',
    'AB4': 'red',
    'AB5': 'red',
    'AB6': 'red',
    'AB5075': 'red',
}

# Cap widths
MEAN_CAP   = 0.08
SD_CAP     = 0.05
TEXT_OFFSET = 0.02  # how close the text sits to the cap (was 0.1–0.12)

# Preserve order of appearance in CSV
order = list(dict.fromkeys(df['sample_label']))

# Setup figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

# Draw all points in one stripplot call
sns.stripplot(
    data=df,
    x='sample_label',
    y='similarity',
    order=order,
    palette=sample_colors,
    jitter=0.01,
    size=6,
    ax=ax,
)

# Explicitly set x-tick labels
ax.set_xticks(range(len(order)))
ax.set_xticklabels(order, rotation=30, ha='right', fontsize=11)

# Compute group stats
group_stats = df.groupby("sample_label")["similarity"].agg(['mean', 'std']).reset_index()

# Draw mean ± SD
for i, sample in enumerate(order):
    row = group_stats[group_stats['sample_label'] == sample]
    if row.empty:
        continue

    mean  = row['mean'].values[0]
    std   = row['std'].values[0]
    lower = mean - std
    upper = mean + std

    # Mean line (bold)
    ax.hlines(mean,  i - MEAN_CAP, i + MEAN_CAP, color='black', linewidth=2,   zorder=2)
    # SD vertical line
    ax.vlines(i,     lower, upper,                color='black', linewidth=0.7, zorder=1)
    # SD caps
    ax.hlines(upper, i - SD_CAP,   i + SD_CAP,   color='black', linewidth=0.5)
    ax.hlines(lower, i - SD_CAP,   i + SD_CAP,   color='black', linewidth=0.5)

    # Text labels — right next to the caps
    ax.text(i + MEAN_CAP + TEXT_OFFSET, mean,  f"{mean:.3f}",       va='center', fontsize=8)
    ax.text(i + SD_CAP   + TEXT_OFFSET, upper, f"{upper:.3f}(+SD)", va='bottom', fontsize=8)
    ax.text(i + SD_CAP   + TEXT_OFFSET, lower, f"{lower:.3f}(-SD)", va='top',    fontsize=8)

# Threshold line (no legend)
plt.axhline(y=0.3768, color="red", linestyle="--", linewidth=1, alpha=0.6)

# Formatting
ax.set_title("Similarity Index")
ax.set_ylabel("Similarity Index")
ax.set_xlabel("Strains")
ax.set_ylim(0, 1.1)
ax.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()

output_dir = r"C:\Workspace\Thesis\coding\Github_test\output6_similarity_plot"
os.makedirs(output_dir, exist_ok=True)
plt.savefig(os.path.join(output_dir, 'ATCC17978.png'), dpi=600)
plt.show()

