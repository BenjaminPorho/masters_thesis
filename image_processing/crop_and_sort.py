import os
import cv2
import shutil

# Define global variables
current_mouse_number = 1
image_count = {}
cropping = False
crop_start = (0, 0)
crop_end = (0, 0)
discarded_image = None
last_image = None


def create_directory_structure(output_folder, day_key):
    """Create the required directory structure for saving processed images."""
    day_folder_path = os.path.join(output_folder, day_key)
    if os.path.exists(day_folder_path):
        shutil.rmtree(day_folder_path)
    for mouse_type in ["treated", "control"]:
        os.makedirs(os.path.join(day_folder_path, f"mouse1", mouse_type))

def save_cropped_image(image, start_x, start_y, end_x, end_y, folder_path, base_filename):
    """Crop the specified region and save it, ensuring unique filenames."""
    h, w, _ = image.shape
    x1 = max(min(start_x, end_x), 0)
    y1 = max(min(start_y, end_y), 0)
    x2 = min(max(start_x, end_x), w)
    y2 = min(max(start_y, end_y), h)

    cropped_image = image[y1:y2, x1:x2]

    # Ensure unique filename
    counter = 1
    filename = f"{base_filename}.jpeg"
    while os.path.exists(os.path.join(folder_path, filename)):
        filename = f"{base_filename}_{counter}.jpeg"
        counter += 1

    save_path = os.path.join(folder_path, filename)
    cv2.imwrite(save_path, cropped_image)
    print(f"Saved image as {filename}")

def mouse_callback(event, x, y, flags, param):
    global treated_clicked, control_clicked, cropping, crop_start, crop_end
    image, output_folder, day_key, filename = param

    if event == cv2.EVENT_LBUTTONDOWN:
        cropping = True
        crop_start = (x, y)

    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping:
            crop_end = (x, y)
            temp_image = image.copy()
            cv2.rectangle(temp_image, crop_start, (x, y), (0, 255, 0), 2)
            cv2.imshow("Image", temp_image)

    elif event == cv2.EVENT_LBUTTONUP:
        cropping = False
        crop_end = (x, y)

        if not treated_clicked:
            subfolder = "treated"
            treated_clicked = True
        elif not control_clicked:
            subfolder = "control"
            control_clicked = True
        else:
            return

        output_dir = os.path.join(output_folder, day_key, f"mouse{current_mouse_number}", subfolder)
        os.makedirs(output_dir, exist_ok=True)

        # Generate the base filename
        base_filename = f"{day_key.replace(' ', '')}_mouse{current_mouse_number}_{subfolder}"
        save_cropped_image(image, crop_start[0], crop_start[1], crop_end[0], crop_end[1], output_dir, base_filename)

def process_images(day_folder, input_folder, output_folder):
    global current_mouse_number, treated_clicked, control_clicked, discarded_image, last_image

    # Initialize image count tracking
    day_key = day_folder.lower().replace(" ", "")
    image_count[day_key] = {}

    day_path = os.path.join(input_folder, day_folder)
    if not os.path.isdir(day_path):
        print(f"Day folder {day_folder} does not exist.")
        return

    create_directory_structure(output_folder, day_key)

    for filename in sorted(os.listdir(day_path)):
        file_path = os.path.join(day_path, filename)
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        # Load the image or handle revert
        if discarded_image and discarded_image[2] == filename:
            image, day_key, filename = discarded_image
            discarded_image = None
        else:
            image = cv2.imread(file_path)
            if image is None:
                continue

        # Store the last image for potential revert
        last_image = (image.copy(), day_key, filename)

        # Display the image
        print(f"Processing: {filename} from {day_folder}")
        cv2.imshow("Image", image)
        treated_clicked = False
        control_clicked = False

        cv2.setMouseCallback("Image", mouse_callback, param=(image, output_folder, day_key, filename))

        while True:
            key = cv2.waitKey(0) & 0xFF

            if key == ord('d'):  # Discard the image
                print(f"Discarded {filename}")
                discarded_image = last_image
                last_image = None
                cv2.destroyWindow("Image")
                break

            elif key == ord('r') and discarded_image:  # Revert discard
                print(f"Reverted discard for {discarded_image[2]}")
                image, day_key, filename = discarded_image
                discarded_image = None
                cv2.imshow("Image", image)
                treated_clicked = False
                control_clicked = False

            elif key == ord('n'):  # Skip to the next phase
                if not treated_clicked:
                    treated_clicked = True
                    print("Skipped treated wound cropping.")
                elif not control_clicked:
                    control_clicked = True
                    print("Skipped control wound cropping.")

            elif key == ord('m'):  # Change mouse number
                new_mouse_number = input("Enter new mouse number: ").strip()
                if new_mouse_number.isdigit():
                    current_mouse_number = int(new_mouse_number)
                    print(f"Changed to mouse {current_mouse_number}")

            elif key == 27:  # ESC key to safely close
                print("Exiting program.")
                cv2.destroyAllWindows()
                exit()

            if treated_clicked and control_clicked:
                print(f"Finished processing {filename}")
                break

        # Ensure the window closes only after the loop ends
        cv2.destroyWindow("Image")

if __name__ == "__main__":
    input_folder = "/Users/benporho/thesis_data/Converted Original Images/Kuvat"
    output_folder = "/Users/benporho/thesis_data/Preprocessed"

    day_folder = input("Enter the Day folder to process (e.g., 'Day 0'): ").strip()
    process_images(day_folder, input_folder, output_folder)

    print("Processing complete. Saved images by day and mouse:")
    for day, mice in image_count.items():
        for mouse, count in mice.items():
            print(f"{day}, Mouse {mouse}: {count} images")
