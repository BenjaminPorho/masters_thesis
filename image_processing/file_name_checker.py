import os
import re

# Hardcoded paths to image directories (update these if needed)
DIGITAL_IMAGES_FOLDER = "/Users/benporho/thesis_data/Final Original Images"
THERMAL_IMAGES_FOLDER = "/Users/benporho/thesis_data/Augmented Thermal Images"

# Define the expected filename patterns
VALID_PATTERNS = [
    r"day\d+_mouse\d+_(control|treated)\.jpeg",
    r"day\d+_mouse\d+_(control|treated)_aug\d+\.jpeg",
    r"day\d+_mouse\d+_(control|treated)_\d+\.jpeg",
    r"day\d+_mouse\d+_(control|treated)_\d+_aug\d+\.jpeg",
    r"day\d+_mouse\d+_(control|treated)_thermal\.jpeg",
    r"day\d+_mouse\d+_(control|treated)_thermal_aug\d+\.jpeg",
    r"day\d+_mouse\d+_(control|treated)_thermal_\d+\.jpeg",
    r"day\d+_mouse\d+_(control|treated)_thermal_\d+_aug\d+\.jpeg"
]

# Function to check if filename matches expected patterns
def is_valid_filename(filename):
    return any(re.fullmatch(pattern, filename) for pattern in VALID_PATTERNS)

# Function to scan a directory and validate filenames
def check_filenames(base_folder):
    inconsistent_files = []
    
    for day_folder in os.listdir(base_folder):
        day_path = os.path.join(base_folder, day_folder)
        
        if not os.path.isdir(day_path):
            continue  # Skip non-directory files
        
        for mouse_folder in os.listdir(day_path):
            mouse_path = os.path.join(day_path, mouse_folder)
            
            if not os.path.isdir(mouse_path):
                continue  # Skip non-directory files
            
            for wound_type in ["treated", "control"]:
                wound_path = os.path.join(mouse_path, wound_type)
                
                if not os.path.exists(wound_path):
                    continue  # Skip if folder doesn't exist
                
                for filename in os.listdir(wound_path):
                    if not is_valid_filename(filename):
                        inconsistent_files.append(os.path.join(wound_path, filename))
    
    return inconsistent_files

# Run the checks
inconsistent_digital = check_filenames(DIGITAL_IMAGES_FOLDER)
inconsistent_thermal = check_filenames(THERMAL_IMAGES_FOLDER)

# Print out inconsistent filenames
if inconsistent_digital:
    print("\nInconsistent Digital Image Filenames:")
    for f in inconsistent_digital:
        print(f)

if inconsistent_thermal:
    print("\nInconsistent Thermal Image Filenames:")
    for f in inconsistent_thermal:
        print(f)

if not inconsistent_digital and not inconsistent_thermal:
    print("\nAll filenames match expected patterns!")
