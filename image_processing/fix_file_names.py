import os
import re

# Hardcoded paths to image directories (update these if needed)
DIGITAL_IMAGES_FOLDER = "/Users/benporho/thesis_data/Final Original Images"
THERMAL_IMAGES_FOLDER = "/Users/benporho/thesis_data/Augmented Thermal Images"

# Regular expressions to detect incorrect patterns
INVALID_TAGS = ["rotated", "copy"]

# Expected filename pattern
VALID_PATTERNS = [
    r"(day\d+_mouse\d+_(control|treated)(?:_thermal)?)",  # Base pattern
    r"(_\d+)?",  # Optional number
    r"(_aug\d+)?",  # Optional augmentation number
    r"\.jpeg"  # File extension
]
VALID_PATTERN_REGEX = re.compile("".join(VALID_PATTERNS))

def sanitize_filename(filename):
    """Fix filename inconsistencies while preserving structure."""
    # Skip system files like .DS_Store
    if filename.startswith("."):
        return None
    
    # Remove invalid tags
    name, ext = os.path.splitext(filename)
    
    # Ensure it's a JPEG file
    if ext.lower() != ".jpeg":
        return None  # Skip non-JPEG files
    
    # Remove " copy" from anywhere in the name
    name = name.replace(" copy", "")

    # Remove unwanted words like "rotated"
    parts = name.split("_")
    cleaned_parts = [part for part in parts if part not in INVALID_TAGS]
    
    # Reconstruct the filename
    fixed_filename = "_".join(cleaned_parts) + ext

    # Ensure the filename still matches the expected pattern
    if VALID_PATTERN_REGEX.fullmatch(fixed_filename):
        return fixed_filename
    else:
        return None  # If it doesn't match after cleaning, leave unchanged

def rename_files_in_directory(base_folder):
    """Traverse and rename files inside the given base directory."""
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
                
                existing_files = set(os.listdir(wound_path))  # Track existing filenames
                
                for filename in existing_files.copy():  # Copy to avoid modification during iteration
                    if filename.startswith("."):  
                        continue  # Skip hidden/system files like .DS_Store
                    
                    fixed_filename = sanitize_filename(filename)
                    
                    if fixed_filename and fixed_filename != filename:
                        new_path = os.path.join(wound_path, fixed_filename)
                        
                        # Prevent duplicates by adding "_fixedX"
                        counter = 1
                        while os.path.exists(new_path):
                            name, ext = os.path.splitext(fixed_filename)
                            new_path = os.path.join(wound_path, f"{name}_fixed{counter}{ext}")
                            counter += 1
                        
                        # Rename file
                        old_path = os.path.join(wound_path, filename)
                        os.rename(old_path, new_path)
                        print(f"Renamed: {old_path} -> {new_path}")

# Run the renaming process
rename_files_in_directory(DIGITAL_IMAGES_FOLDER)
rename_files_in_directory(THERMAL_IMAGES_FOLDER)

print("\nFilename inconsistencies fixed!")
