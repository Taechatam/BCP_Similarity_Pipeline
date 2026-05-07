import pandas as pd
import os

# Load the uploaded CSV file
file_path = r"C:\Workspace\Thesis\coding\output00_all\output2-2\coordinate_TM00_sensitive_27.csv"
output_path = r"C:\Workspace\Thesis\coding\output00_all\output2-2"
output_file = 'coordinate_AB00_300_14f.csv'
cell_number = 300

data = pd.read_csv(file_path)
# Randomly select 100 samples from each group in the 'label' column
sampled_data = data.groupby('label').apply(lambda x: x.sample(n=cell_number, random_state=42, replace=len(x) < 100)).reset_index(drop=True)

output = os.path.join(output_path, output_file)
sampled_data.to_csv(output, index=False)