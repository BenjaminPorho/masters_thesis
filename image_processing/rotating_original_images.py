import os
import cv2
import numpy as np
import random

def rotate_image(image, angle):
    """Rotates the image by a specified angle, filling empty areas using the nearest pixels."""
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

    # Perform rotation with border replication for empty areas
    rotated_image = cv2.warpAffine(image, rotation_matrix, (w, h), borderMode=cv2.BORDER_REPLICATE)
    return rotated_image

def randomly_rotate_images(input_folder, output_folder):
    """Randomly rotates original images without '_aug' and copies '_aug' images to the output folder."""
    if not os.path.exists(input_folder):
        print(f"The folder '{input_folder}' does not exist.")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, _, files in os.walk(input_folder):
        for file in sorted(files):
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                # Paths for input and output
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_folder)
                output_dir = os.path.join(output_folder, relative_path)
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, file)

                # Load the image
                image = cv2.imread(input_path)
                if image is None:
                    print(f"Failed to load image: {input_path}")
                    continue

                if '_aug' in file:
                    # Directly copy augmented images
                    cv2.imwrite(output_path, image)
                    print(f"Copied augmented image: {output_path}")
                else:
                    # Rotate and save the image if it is an original
                    angle = random.uniform(-45, 45)  # Generate random rotation angle
                    rotated_image = rotate_image(image, angle)

                    # Append '_rotated' to the filename
                    rotated_filename = f"{os.path.splitext(file)[0]}_rotated.jpeg"
                    rotated_output_path = os.path.join(output_dir, rotated_filename)
                    cv2.imwrite(rotated_output_path, rotated_image)
                    print(f"Saved rotated image: {rotated_output_path}")

if __name__ == "__main__":
    input_folder = "/Users/benporho/thesis_data/Augmented Original Images"
    output_folder = "/Users/benporho/thesis_data/Randomly Rotated Original Images with Augmentation"

    randomly_rotate_images(input_folder, output_folder)