import os
import cv2
import numpy as np

def resize_images(preprocessed_folder, output_folder, target_size=(224, 224)):
    """Resize all images to the target size, filling empty areas using nearest valid pixel."""
    if not os.path.exists(preprocessed_folder):
        print(f"The folder '{preprocessed_folder}' does not exist.")
        return

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, _, files in os.walk(preprocessed_folder):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                # Paths for input and output
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, preprocessed_folder)
                output_dir = os.path.join(output_folder, relative_path)
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, file)

                # Load the image
                image = cv2.imread(input_path)
                if image is None:
                    print(f"Failed to load image: {input_path}")
                    continue

                # Get original dimensions
                h, w, _ = image.shape

                # Calculate the scale and new dimensions
                scale = min(target_size[0] / h, target_size[1] / w)
                new_w = int(w * scale)
                new_h = int(h * scale)

                # Resize the image
                resized_image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

                # Create a blank canvas of the target size
                canvas = np.zeros((target_size[0], target_size[1], 3), dtype=np.uint8)

                # Center the resized image on the canvas
                x_offset = (target_size[1] - new_w) // 2
                y_offset = (target_size[0] - new_h) // 2
                canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized_image

                # Fill empty areas using nearest valid pixels
                canvas = cv2.copyMakeBorder(
                    resized_image,
                    top=y_offset,
                    bottom=target_size[0] - new_h - y_offset,
                    left=x_offset,
                    right=target_size[1] - new_w - x_offset,
                    borderType=cv2.BORDER_REPLICATE
                )

                # Save the final image
                cv2.imwrite(output_path, canvas)
                print(f"Saved resized image to: {output_path}")

if __name__ == "__main__":
    preprocessed_folder = "/Users/benporho/thesis_data/Preprocessed"
    output_folder = "/Users/benporho/thesis_data/Resized"

    resize_images(preprocessed_folder, output_folder)
