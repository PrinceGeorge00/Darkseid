from PIL import Image
from PIL.ExifTags import TAGS
import os

def extract(image_path):
    try:
        # DEBUG: Force the correct path for testing
        image_path = "/home/kali/Darkseid/images/"

        # Print the file path being used
        print(f"Looking for image at: {image_path}")

        # Ensure the file exists
        if not os.path.exists(image_path):
            return f"Metadata extraction failed: File '{image_path}' not found."

        # Open the image
        image = Image.open(image_path)

        # Extract EXIF metadata
        exif_data = image._getexif()
        
        if not exif_data:
            return "Metadata extraction failed: No EXIF metadata found."

        metadata = "🔹 Metadata Extraction:\n"

        # Convert EXIF data to readable format
        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)  # Get human-readable tag name
            metadata += f"{tag_name}: {value}\n"

        return metadata

    except Exception as e:
        return f"Metadata extraction failed: {str(e)}"
