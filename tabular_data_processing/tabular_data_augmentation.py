import os
import pandas as pd
import numpy as np

# Load the wound measurement data
file_path = "/Users/benporho/thesis_data/wound_sizes_mm2.xlsx"  # Update with the correct path
df_wound = pd.read_excel(file_path)

# Extract available day columns dynamically
day_columns = [col for col in df_wound.columns if "Day_" in col and ("_Right" in col or "_Left" in col)]

# Extract unique days from column names
available_days = sorted(set(int(col.split("_")[1]) for col in day_columns))

# Define augmentation parameters
num_images_per_day = 10  # Each measurement needs to match 10 images
noise_std_dev = 0.2  # Standard deviation for Gaussian noise

# Prepare an empty list to store augmented data
augmented_data = []

# Iterate over each row in the dataset
for _, row in df_wound.iterrows():
    mouse_id = row["Mouse_ID"]
    
    for day in available_days:  # Use only existing days dynamically
        treated_wound_size = row.get(f"Day_{day}_Right", np.nan)
        control_wound_size = row.get(f"Day_{day}_Left", np.nan)
        
        if np.isnan(treated_wound_size) or np.isnan(control_wound_size):
            continue  # Skip missing values

        for _ in range(num_images_per_day):  # Augment each measurement 10 times
            augmented_data.append({
                "Mouse_ID": mouse_id,
                "Imaging_Day": f"Day_{day}",
                "Wound_Type": "Treated",
                "Wound_Size (mm²)": max(0, treated_wound_size + np.random.normal(0, noise_std_dev))
            })
            augmented_data.append({
                "Mouse_ID": mouse_id,
                "Imaging_Day": f"Day_{day}",
                "Wound_Type": "Control",
                "Wound_Size (mm²)": max(0, control_wound_size + np.random.normal(0, noise_std_dev))
            })

# Convert to DataFrame
df_augmented = pd.DataFrame(augmented_data)

# Save the augmented dataset
augmented_csv_path = "augmented_wound_sizes.csv"
df_augmented.to_csv(augmented_csv_path, index=False)

print(f"Augmented wound size data saved to {augmented_csv_path}")
