import os
import pandas as pd
import re

# Hardcoded paths to image directories (update these if needed)
DIGITAL_IMAGES_FOLDER = "/Users/benporho/thesis_data/Final Digital Images"
THERMAL_IMAGES_FOLDER = "/Users/benporho/thesis_data/Final Thermal Images"

# Treatment type mapping (Only for Treated wounds)
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

# Expected filename pattern regex
FILENAME_REGEX = re.compile(r"day(\d+)_mouse(\d+)_(control|treated)(_thermal)?(_\d+)?(_aug\d+)?\.jpeg")

# Initialize storage for image records
image_records = {}

# Function to process image files
def process_images(base_folder, is_thermal):
    for day_folder in sorted(os.listdir(base_folder)):
        day_path = os.path.join(base_folder, day_folder)
        if not os.path.isdir(day_path):
            continue  # Skip non-directory files
        
        for mouse_folder in sorted(os.listdir(day_path)):
            mouse_path = os.path.join(day_path, mouse_folder)
            if not os.path.isdir(mouse_path):
                continue  # Skip non-directory files
            
            for wound_type in ["treated", "control"]:
                wound_path = os.path.join(mouse_path, wound_type)
                
                if not os.path.exists(wound_path):
                    continue  # Skip if folder doesn't exist
                
                for filename in sorted(os.listdir(wound_path)):
                    match = FILENAME_REGEX.match(filename)
                    if match:
                        day, mouse, wound, thermal, num, aug = match.groups()
                        day = int(day)
                        mouse = int(mouse)
                        wound_type_label = "Treated" if wound == "treated" else "Control"
                        treatment_type = TREATMENT_MAPPING.get(mouse, "") if wound_type_label == "Treated" else ""

                        # Create a unique key based on day, mouse, wound type, and an index to keep multiple images
                        key = (day, mouse, wound_type_label)

                        if key not in image_records:
                            image_records[key] = {
                                "Mouse_ID": mouse,
                                "Imaging_Day": f"Day_{day}",
                                "Wound_Type": wound_type_label,
                                "Digital_Image_ID": [],
                                "Thermal_Image_ID": [],
                                "Wound_Size (mm²)": "",
                                "Treatment_Type": treatment_type,
                                "Digital_Image_Path": [],
                                "Thermal_Image_Path": []
                            }

                        # Append image to correct list
                        if is_thermal:
                            image_records[key]["Thermal_Image_ID"].append(filename)
                            image_records[key]["Thermal_Image_Path"].append(os.path.join(wound_path, filename))
                        else:
                            image_records[key]["Digital_Image_ID"].append(filename)
                            image_records[key]["Digital_Image_Path"].append(os.path.join(wound_path, filename))

# Process digital and thermal images
process_images(DIGITAL_IMAGES_FOLDER, is_thermal=False)
process_images(THERMAL_IMAGES_FOLDER, is_thermal=True)

# Flatten records to avoid duplication
flattened_data = []
for key, record in image_records.items():
    max_images = max(len(record["Digital_Image_ID"]), len(record["Thermal_Image_ID"]))  # Get max count

    for i in range(max_images):  # Iterate over max image count
        flattened_data.append({
            "Mouse_ID": record["Mouse_ID"],
            "Imaging_Day": record["Imaging_Day"],
            "Wound_Type": record["Wound_Type"],
            "Digital_Image_ID": record["Digital_Image_ID"][i] if i < len(record["Digital_Image_ID"]) else "",
            "Thermal_Image_ID": record["Thermal_Image_ID"][i] if i < len(record["Thermal_Image_ID"]) else "",
            "Wound_Size (mm²)": record["Wound_Size (mm²)"],
            "Treatment_Type": record["Treatment_Type"],
            "Digital_Image_Path": record["Digital_Image_Path"][i] if i < len(record["Digital_Image_Path"]) else "",
            "Thermal_Image_Path": record["Thermal_Image_Path"][i] if i < len(record["Thermal_Image_Path"]) else ""
        })

# Convert list to DataFrame
df = pd.DataFrame(flattened_data)

# Save to CSV
output_csv = "wound_image_metadata.csv"
df.to_csv(output_csv, index=False)

print(f"\nTable saved to {output_csv} and displayed.")
