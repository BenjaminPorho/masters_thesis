import os
import cv2

# Define global variables
current_day = "day0"
cropping = False
crop_start = (0, 0)
crop_end = (0, 0)
treated_clicked = False
control_clicked = False
current_image = None

def create_directory_structure(output_folder, day, mouse):
    """Create the required directory structure for saving processed images."""
    treated_path = os.path.join(output_folder, day, mouse, "treated")
    control_path = os.path.join(output_folder, day, mouse, "control")
    os.makedirs(treated_path, exist_ok=True)
    os.makedirs(control_path, exist_ok=True)

def save_cropped_image(image, start_x, start_y, end_x, end_y, folder_path, base_filename):
    """Crop the specified region and save it, ensuring unique filenames."""
    h, w, _ = image.shape
    x1 = max(0, min(start_x, end_x))
    y1 = max(0, min(start_y, end_y))
    x2 = min(w, max(start_x, end_x))
    y2 = min(h, max(start_y, end_y))

    if x1 >= x2 or y1 >= y2:
        print("Error: Invalid cropping coordinates.")
        return

    cropped_image = image[y1:y2, x1:x2]

    # Ensure unique filename format
    counter = 1
    filename = f"{base_filename}_thermal.jpeg"
    while os.path.exists(os.path.join(folder_path, filename)):
        filename = f"{base_filename}_thermal_{counter}.jpeg"
        counter += 1

    save_path = os.path.join(folder_path, filename)
    cv2.imwrite(save_path, cropped_image)
    print(f"Saved image as {filename}")

def mouse_callback(event, x, y, flags, param):
    global treated_clicked, control_clicked, cropping, crop_start, crop_end, current_image
    image, output_folder, day, mouse, filename = param

    if event == cv2.EVENT_LBUTTONDOWN:
        cropping = True
        crop_start = (x, y)
        crop_end = (x, y)

    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping:
            crop_end = (x, y)
            temp_image = image.copy()
            cv2.rectangle(temp_image, crop_start, crop_end, (0, 255, 0), 2)
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

        output_dir = os.path.join(output_folder, day, mouse, subfolder)
        os.makedirs(output_dir, exist_ok=True)

        # Generate the base filename
        base_filename = f"{day}_{mouse}_{subfolder}"
        save_cropped_image(image, crop_start[0], crop_start[1], crop_end[0], crop_end[1], output_dir, base_filename)

def process_images(input_folder, output_folder):
    global current_day, treated_clicked, control_clicked, current_image

    mouse = input("Enter the mouse identifier (e.g., 'mouse1'): ").strip()
    print(f"Processing images for {mouse}. Default day is {current_day}.")
    create_directory_structure(output_folder, current_day, mouse)

    for filename in sorted(os.listdir(input_folder)):
        file_path = os.path.join(input_folder, filename)
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        # Load the image
        image = cv2.imread(file_path)
        if image is None:
            continue

        current_image = image.copy()
        # Display the image
        print(f"Processing: {filename}")
        cv2.imshow("Image", current_image)
        treated_clicked = False
        control_clicked = False

        cv2.setMouseCallback("Image", mouse_callback, param=(current_image, output_folder, current_day, mouse, filename))

        while True:
            key = cv2.waitKey(0) & 0xFF

            if key == ord('d'):  # Discard the image
                print(f"Discarded {filename}")
                cv2.destroyWindow("Image")
                break

            elif key == ord('i'):  # Change imaging day
                new_day = input("Enter new imaging day (e.g., 'day2'): ").strip()
                if new_day.startswith("day") and new_day[3:].isdigit():
                    current_day = new_day
                    print(f"Changed to {current_day}")
                    create_directory_structure(output_folder, current_day, mouse)

            elif key == ord('n'):  # Skip to the next phase
                if not treated_clicked:
                    treated_clicked = True
                    print("Skipped treated wound cropping.")
                elif not control_clicked:
                    control_clicked = True
                    print("Skipped control wound cropping.")

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
    input_folder = "/Users/benporho/thesis_data/Converted Thermal Images/mouse4"
    output_folder = "/Users/benporho/thesis_data/Preprocessed Thermal Images"

    process_images(input_folder, output_folder)
    print("Processing complete.")
