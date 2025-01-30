import pandas as pd

# Load the previously generated metadata CSV
metadata_csv_path = "/Users/benporho/thesis_data/wound_measurements.csv"  # Update with correct path
augmented_csv_path = "/Users/benporho/thesis_data/augmented_wound_sizes copy.csv"  # Update with correct path
merged_csv_path = "/Users/benporho/thesis_data/final_tabular_data.csv"  # Update with correct path

# Load both datasets
df_metadata = pd.read_csv(metadata_csv_path)
df_augmented = pd.read_csv(augmented_csv_path)

# Ensure the augmented dataset has the same number of rows as the metadata dataset
if len(df_augmented) != len(df_metadata):
    print("Warning: The number of augmented wound sizes does not match the number of images.")

# Add a unique index column to ensure one-to-one mapping
if "Image_Index" not in df_metadata.columns:
    df_metadata["Image_Index"] = df_metadata.groupby(["Mouse_ID", "Imaging_Day", "Wound_Type"]).cumcount()
    df_augmented["Image_Index"] = df_augmented.groupby(["Mouse_ID", "Imaging_Day", "Wound_Type"]).cumcount()

# Merge the datasets based on Mouse_ID, Imaging_Day, Wound_Type, and Image_Index
df_merged = df_metadata.merge(
    df_augmented[["Mouse_ID", "Imaging_Day", "Wound_Type", "Wound_Size (mm^2)", "Image_Index"]],
    on=["Mouse_ID", "Imaging_Day", "Wound_Type", "Image_Index"],
    how="left",
    suffixes=("_x", "_y")
)

# Replace the original "Wound_Size (mm^2)" column with the newly merged values
df_merged["Wound_Size (mm^2)"] = df_merged["Wound_Size (mm^2)_y"]

# Drop extra columns created during merging
df_merged.drop(columns=["Wound_Size (mm^2)_x", "Wound_Size (mm^2)_y"], inplace=True, errors='ignore')

# Save the merged dataset with full precision
df_merged.to_csv(merged_csv_path, index=False, float_format="%.10f")

print(f"Merged wound data saved to {merged_csv_path}")
