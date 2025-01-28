import os
import zipfile
from PIL import Image
import rawpy
import numpy as np

def unzip_and_convert(zip_path, output_dir):
    """
    Unzips a .zip file containing .CR2 images and converts them to .jpeg format.

    Args:
        zip_path (str): Path to the .zip file.
        output_dir (str): Directory to store the extracted and converted files.
    """
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Extract the zip file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)

    print(f"Extracted files to {output_dir}")

    # Find all .CR2 files and convert them to .jpeg
    for root, _, files in os.walk(output_dir):
        for file in files:
            if file.lower().endswith('.cr2'):
                cr2_file_path = os.path.join(root, file)
                jpeg_file_path = os.path.splitext(cr2_file_path)[0] + '.jpeg'

                # Convert .CR2 to .jpeg
                try:
                    with rawpy.imread(cr2_file_path) as raw:
                        # Use camera's white balance settings
                        rgb_image = raw.postprocess(use_camera_wb=True)

                        img = Image.fromarray(rgb_image)
                        img.save(jpeg_file_path, "JPEG")
                        print(f"Converted {cr2_file_path} to {jpeg_file_path}")

                    # Remove the original .CR2 file
                    os.remove(cr2_file_path)
                    print(f"Deleted original file {cr2_file_path}")

                except Exception as e:
                    print(f"Failed to convert {cr2_file_path}: {e}")

if __name__ == "__main__":
    # Replace these paths with your zip file path and desired output directory
    zip_file_path = "/Users/benporho/Downloads/Kuvat.zip"
    output_directory = "/Users/benporho/thesis_data/Converted Original Images"

    unzip_and_convert(zip_file_path, output_directory)
