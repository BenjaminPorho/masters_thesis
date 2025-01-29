import os
from collections import defaultdict

def count_images(preprocessed_folder):
    """Counts the number of images for each mouse from each day."""
    distribution = defaultdict(lambda: defaultdict(lambda: {'treated': 0, 'control': 0}))

    # Traverse through the preprocessed folder
    for day_folder in sorted(os.listdir(preprocessed_folder)):
        day_path = os.path.join(preprocessed_folder, day_folder)
        if not os.path.isdir(day_path):
            continue

        for mouse_folder in sorted(os.listdir(day_path)):
            mouse_path = os.path.join(day_path, mouse_folder)
            if not os.path.isdir(mouse_path):
                continue

            for wound_type in ['treated', 'control']:
                wound_path = os.path.join(mouse_path, wound_type)
                if os.path.exists(wound_path):
                    num_images = len([img for img in os.listdir(wound_path) if img.lower().endswith(('.jpg', '.jpeg', '.png'))])
                    distribution[day_folder][mouse_folder][wound_type] += num_images

    return distribution

def display_distribution(distribution):
    """Displays the class distribution in a readable format."""
    print("Class Distribution:\n")
    for day, mice in distribution.items():
        print(f"{day}:")
        for mouse, counts in mice.items():
            treated_count = counts['treated']
            control_count = counts['control']
            print(f"  {mouse} -> Treated: {treated_count}, Control: {control_count}")
        print()

if __name__ == "__main__":
    preprocessed_folder = "/Users/benporho/thesis_data/Preprocessed Thermal Images"  # Change this if your folder is named differently

    # Count images and display the distribution
    distribution = count_images(preprocessed_folder)
    display_distribution(distribution)
