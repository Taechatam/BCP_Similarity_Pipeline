import pandas as pd
import numpy as np

# --- CONFIGURATION ---
# Set to True to change "CIP1", "untreated2" to just "CIP" and "untreated"
# Set to False to keep the original labels exactly as they are
RELABEL_DATA = True 
# ---------------------

# Load CSV
file_path = r"Github_test\output1_combined_profile\test_data_annotate_cell.csv"
df = pd.read_csv(file_path)

# Extract batch number (if no number, assign "0")
df['batch'] = df['label'].str.extract(r'(\d+)', expand=False).fillna("0")

# Extract group name (CIP or untreated)
df['group'] = df['label'].str.extract(r'([A-Za-z]+)')

balanced_data = []

# Iterate over all batches (including batch "0")
for batch in df['batch'].unique():
    cip_rows = df[(df['batch'] == batch) & (df['group'] == 'CIP')]
    untreated_rows = df[(df['batch'] == batch) & (df['group'] == 'untreated')]
    
    if len(cip_rows) > 0 and len(untreated_rows) > 0:
        # Find minimum sample size
        min_size = min(len(cip_rows), len(untreated_rows))
        
        # Randomly sample equal number
        cip_sample = cip_rows.sample(n=min_size, random_state=42)
        untreated_sample = untreated_rows.sample(n=min_size, random_state=42)
        
        balanced_data.append(cip_sample)
        balanced_data.append(untreated_sample)

# Concatenate all balanced data
final_df = pd.concat(balanced_data).reset_index(drop=True)

# --- RELABELING LOGIC ---
if RELABEL_DATA:
    # Overwrite the 'label' column with the clean 'group' name
    final_df['label'] = final_df['group']
    print("Labels have been renamed to remove numbers.")
else:
    print("Original labels with numbers were kept.")
# ------------------------

# Drop the helper 'batch' and 'group' columns before saving
final_df = final_df.drop(columns=['batch', 'group'])

# Save to new CSV
final_df.to_csv(r"Github_test\output1_downsamp\test_balanced_data_annotate_cell.csv", index=False)

print("Balanced dataset saved!")
