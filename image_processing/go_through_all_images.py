import os
import cv2

def browse_images(preprocessed_folder):
    """Browse through all images in the Preprocessed folder, one image at a time."""
    if not os.path.exists(preprocessed_folder):
        print(f"The folder '{preprocessed_folder}' does not exist.")
        return

    # Collect all image paths
    image_paths = []
    for root, _, files in os.walk(preprocessed_folder):
        for file in sorted(files):
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_paths.append(os.path.join(root, file))

    if not image_paths:
        print("No images found in the Preprocessed folder.")
        return

    print(f"Browsing {len(image_paths)} images from '{preprocessed_folder}'.")

    # Display each image
    index = 0
    while True:
        image_path = image_paths[index]
        image = cv2.imread(image_path)

        if image is None:
            print(f"Failed to load image: {image_path}")
            index = (index + 1) % len(image_paths)  # Move to the next image
            continue

        cv2.imshow("Image Browser", image)
        print(f"Displaying: {image_path}")

        key = cv2.waitKey(0) & 0xFF
        if key == 27:  # ESC to exit
            print("Exiting image browser.")
            break
        elif key == ord('p'):  # P for previous
            index = (index - 1) % len(image_paths)
            cv2.destroyWindow("Image Browser")  # Ensure window updates
        elif key == ord('n'):  # N for next
            index = (index + 1) % len(image_paths)
            cv2.destroyWindow("Image Browser")  # Ensure window updates

    cv2.destroyAllWindows()

if __name__ == "__main__":
    preprocessed_folder = "/Users/benporho/thesis_data/Augmented Thermal Images"
    browse_images(preprocessed_folder)
