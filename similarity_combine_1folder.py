import os
import pandas as pd

# Set the path to your folder containing the CSVs
main_folder = r"C:\Workspace\Thesis\coding\Github_test\output4_similarity"

# --- CONFIGURATION FOR OUTPUT ---
# Set your desired destination folder and the specific CSV file name here
output_folder = r"C:\Workspace\Thesis\coding\Github_test\output5_combined_si"
output_filename = "ATCC17978.csv" 
# --------------------------------

# List to hold DataFrames
combined_data = []

# Loop through CSV files in the folder
csv_files = [f for f in os.listdir(main_folder) if f.endswith('.csv')]

for file in csv_files:
    file_path = os.path.join(main_folder, file)
    try:
        df = pd.read_csv(file_path, usecols=[0])       # Only first column
        df.columns = ['similarity']                    # Rename first column
        df['sample_label'] = os.path.splitext(file)[0] # Use filename as label
        combined_data.append(df)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

# Combine and export
if combined_data:
    final_df = pd.concat(combined_data, ignore_index=True)
    
    # Ensure the destination folder exists (creates it if it doesn't)
    os.makedirs(output_folder, exist_ok=True)
    
    # Safely join the folder path and the filename together
    output_path = os.path.join(output_folder, output_filename)
    
    # Save to the new CSV
    final_df.to_csv(output_path, index=False)
    
    print(f"Combined CSV successfully saved to:\n{output_path}")
else:
    print("No CSV files found in the folder.")