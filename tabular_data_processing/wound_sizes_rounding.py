import pandas as pd

# File paths
input_file = "/Users/benporho/thesis_data/accurate_values_tabular_data.csv"
output_file = "/Users/benporho/thesis_data/final_tabular_data.csv"

# Load the dataset
df = pd.read_csv(input_file)

# Round the "Wound_Size (mm^2)" column to one decimal place
df["Wound_Size (mm^2)"] = df["Wound_Size (mm^2)"].round(1)

# Save the rounded dataset
df.to_csv(output_file, index=False)

print(f"Rounded wound data saved to {output_file}")
