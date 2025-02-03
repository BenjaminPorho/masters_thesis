import pandas as pd
import os
import re

# File paths
file_path = "/Users/benporho/thesis_data/final_tabular_data.csv"
wound_sizes_path = "/Users/benporho/thesis_data/wound_sizes_mm2.csv"

# Load the datasets
df = pd.read_csv(file_path)
df_wound_sizes = pd.read_csv(wound_sizes_path)

# Define treatment type mapping
TREATMENT_MAPPING = {
    1: "NFC_without_glucose",
    3: "NFC_without_glucose",
    5: "NFC_without_glucose",
    7: "NFC_without_glucose",
    2: "NFC_with_glucose",
    4: "NFC_with_glucose",
    8: "NFC_with_glucose",
    9: "NFC_with_glucose",
    10: "NFC_with_glucose"
}

# Regular expression to extract Mouse_ID, Imaging_Day, and Wound_Type from filenames
FILENAME_REGEX = re.compile(r"day(\d+)_mouse(\d+)_(control|treated)(_thermal)?")

# Initialize an error log
errors = []

# Iterate through each row to validate
for index, row in df.iterrows():
    mouse_id = row["Mouse_ID"]
    imaging_day = row["Imaging_Day"].replace("Day_", "")
    wound_type = row["Wound_Type"].lower()
    
    # Extract data from Digital Image ID
    digital_match = FILENAME_REGEX.match(row["Digital_Image_ID"])
    thermal_match = FILENAME_REGEX.match(row["Thermal_Image_ID"])
    
    if digital_match:
        day_digital, mouse_digital, wound_digital, _ = digital_match.groups()
        if int(mouse_digital) != mouse_id:
            errors.append(f"Row {index}: Mouse_ID mismatch in Digital_Image_ID {row['Digital_Image_ID']}")
        if day_digital != imaging_day:
            errors.append(f"Row {index}: Imaging_Day mismatch in Digital_Image_ID {row['Digital_Image_ID']}")
        if wound_digital != wound_type:
            errors.append(f"Row {index}: Wound_Type mismatch in Digital_Image_ID {row['Digital_Image_ID']}")
    else:
        errors.append(f"Row {index}: Digital_Image_ID format error {row['Digital_Image_ID']}")
    
    if thermal_match:
        day_thermal, mouse_thermal, wound_thermal, _ = thermal_match.groups()
        if int(mouse_thermal) != mouse_id:
            errors.append(f"Row {index}: Mouse_ID mismatch in Thermal_Image_ID {row['Thermal_Image_ID']}")
        if day_thermal != imaging_day:
            errors.append(f"Row {index}: Imaging_Day mismatch in Thermal_Image_ID {row['Thermal_Image_ID']}")
        if wound_thermal != wound_type:
            errors.append(f"Row {index}: Wound_Type mismatch in Thermal_Image_ID {row['Thermal_Image_ID']}")
    else:
        errors.append(f"Row {index}: Thermal_Image_ID format error {row['Thermal_Image_ID']}")
    
    # Validate image path matches image ID
    if not row["Digital_Image_Path"].endswith(row["Digital_Image_ID"]):
        errors.append(f"Row {index}: Digital_Image_Path does not match Digital_Image_ID")
    
    if not row["Thermal_Image_Path"].endswith(row["Thermal_Image_ID"]):
        errors.append(f"Row {index}: Thermal_Image_Path does not match Thermal_Image_ID")
    
    # Validate treatment type
    expected_treatment = TREATMENT_MAPPING.get(mouse_id, "Unknown")
    if wound_type == "treated" and row["Treatment_Type"] != expected_treatment:
        errors.append(f"Row {index}: Treatment_Type mismatch for Mouse_ID {mouse_id}")
    
    # Validate Wound_Size (mm^2) against original wound sizes
    wound_size_column = f"Day_{imaging_day}_Right" if wound_type == "treated" else f"Day_{imaging_day}_Left"
    if wound_size_column in df_wound_sizes.columns:
        original_wound_size = df_wound_sizes.loc[df_wound_sizes["Mouse_ID"] == mouse_id, wound_size_column].values
        if len(original_wound_size) > 0:
            if abs(row["Wound_Size (mm^2)"] - original_wound_size[0]) > 0.6:
                errors.append(f"Row {index}: Wound_Size (mm^2) out of range for Mouse_ID {mouse_id}, Imaging_Day {imaging_day}, Wound_Type {wound_type}. Found: {row['Wound_Size (mm^2)']}, Expected: {original_wound_size[0]}")

# Output validation results
if errors:
    print("Validation errors found:")
    for error in errors:
        print(error)
else:
    print("All data entries are correctly formatted and valid!")
