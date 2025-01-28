import os
import cv2
import numpy as np
import random

def augment_image(image):
    """Applies a random augmentation to the image."""
    augmentation_type = random.choice(['flip', 'rotate', 'brightness'])

    if augmentation_type == 'flip':
        return cv2.flip(image, 1)  # Horizontal flip

    elif augmentation_type == 'rotate':
        angle = random.choice([90, 180, 270])
        h, w = image.shape[:2]
        center = (w // 2, h // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1)
        return cv2.warpAffine(image, rotation_matrix, (w, h))

    elif augmentation_type == 'brightness':
        factor = random.uniform(1.1, 1.3)  # Subtle brightness increase
        return np.clip(image * factor, 0, 255).astype(np.uint8)

    return image

def augment_to_target(preprocessed_folder, output_folder, target=10):
    """Augments images to ensure each class reaches the target count."""
    if not os.path.exists(preprocessed_folder):
        print(f"The folder '{preprocessed_folder}' does not exist.")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

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
                if not os.path.exists(wound_path):
                    continue

                # Collect images
                images = [img for img in sorted(os.listdir(wound_path)) if img.lower().endswith(('.jpg', '.jpeg', '.png'))]
                image_count = len(images)

                # Skip if already meets or exceeds target
                if image_count >= target:
                    continue

                print(f"Augmenting {day_folder} -> {mouse_folder} -> {wound_type} ({image_count}/{target})")

                # Create output folder
                output_dir = os.path.join(output_folder, day_folder, mouse_folder, wound_type)
                os.makedirs(output_dir, exist_ok=True)

                # Copy original images to the output folder
                for img in images:
                    src = os.path.join(wound_path, img)
                    dst = os.path.join(output_dir, img)
                    if not os.path.exists(dst):
                        cv2.imwrite(dst, cv2.imread(src))

                # Generate augmented images
                while image_count < target:
                    for img in images:
                        if image_count >= target:
                            break

                        image_path = os.path.join(wound_path, img)
                        image = cv2.imread(image_path)

                        if image is None:
                            print(f"Failed to load image: {image_path}")
                            continue

                        augmented_image = augment_image(image)
                        # Ensure the augmented image is 224x224
                        augmented_image = cv2.resize(augmented_image, (224, 224), interpolation=cv2.INTER_LINEAR)
                        aug_name = f"{os.path.splitext(img)[0]}_aug{image_count - len(images) + 1}.jpeg"
                        aug_path = os.path.join(output_dir, aug_name)

                        cv2.imwrite(aug_path, augmented_image)
                        print(f"Saved augmented image: {aug_path}")
                        image_count += 1

if __name__ == "__main__":
    resized_folder = "/Users/benporho/thesis_data/Resized Original Images"
    output_folder = "/Users/benporho/thesis_data/Augmented Original Images"

    augment_to_target(resized_folder, output_folder, target=10)
