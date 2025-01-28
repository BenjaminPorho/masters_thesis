import os
import cv2
import matplotlib.pyplot as plt

def display_images(folder_path):
    """Displays all images from the given folder at the same time."""
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return

    images = [img for img in sorted(os.listdir(folder_path)) if img.lower().endswith(('.jpg', '.jpeg', '.png'))]

    if not images:
        print(f"No images found in the folder '{folder_path}'.")
        return

    print(f"Displaying all images from: {folder_path}")

    # Load all images
    loaded_images = []
    for image_name in images:
        image_path = os.path.join(folder_path, image_name)
        image = cv2.imread(image_path)
        if image is not None:
            # Convert from BGR to RGB for displaying with matplotlib
            loaded_images.append((cv2.cvtColor(image, cv2.COLOR_BGR2RGB), image_name))
        else:
            print(f"Failed to load image: {image_name}")

    # Display images
    if loaded_images:
        cols = 4  # Number of columns for the grid
        rows = (len(loaded_images) + cols - 1) // cols

        plt.figure(figsize=(15, rows * 4))
        for idx, (img, title) in enumerate(loaded_images):
            plt.subplot(rows, cols, idx + 1)
            plt.imshow(img)
            plt.title(title, fontsize=8)
            plt.axis('off')

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    # Example usage
    folder_path = "/Users/benporho/thesis_data/Preprocessed/day6/mouse1/control"
    display_images(folder_path)