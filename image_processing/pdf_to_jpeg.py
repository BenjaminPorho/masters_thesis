import os
from pdf2image import convert_from_path

# Fixed input and output directories
INPUT_FOLDER = "/Users/benporho/thesis_data/Original Thermal PDFs/mouse4"
OUTPUT_FOLDER = "/Users/benporho/thesis_data/Converted Thermal Images/mouse4"

def convert_pdfs_to_jpegs(input_folder, output_folder):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # List all PDF files in the input folder
    pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print("No PDF files found in the input directory.")
        return

    # Convert each PDF to images
    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_folder, pdf_file)
        images = convert_from_path(pdf_path)  # Convert PDF to images (one per page)

        # Save each page as a JPEG file
        for i, image in enumerate(images):
            output_filename = f"{os.path.splitext(pdf_file)[0]}_page{i+1}.jpg"
            output_path = os.path.join(output_folder, output_filename)
            image.save(output_path, "JPEG")
            print(f"Saved: {output_path}")

    print("PDF to JPEG conversion completed.")

if __name__ == "__main__":
    convert_pdfs_to_jpegs(INPUT_FOLDER, OUTPUT_FOLDER)
