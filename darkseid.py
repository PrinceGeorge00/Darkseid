import os
import requests
import threading
import exifread
from fpdf import FPDF
from datetime import datetime
import urllib.parse

# Constants
REPORTS_DIR = "reports/"
os.makedirs(REPORTS_DIR, exist_ok=True)

# Function to extract metadata
def extract_metadata(image_path):
    with open(image_path, "rb") as img_file:
        tags = exifread.process_file(img_file)
    
    metadata = {tag: str(value) for tag, value in tags.items()}
    
    if not metadata:
        print(f"Warning: No metadata found for {image_path}")
    
    return metadata

# Function to perform Google reverse image search
def reverse_image_search(image_path):
    search_url = "https://www.google.com/searchbyimage?image_url="
    
    try:
        with open(image_path, "rb") as img:
            files = {"encoded_image": img, "image_content": ""}
            response = requests.post("https://www.google.com/searchbyimage/upload", files=files, allow_redirects=False)
            google_search_url = response.headers.get("Location", "Search failed")
    except requests.exceptions.RequestException:
        google_search_url = "Error"

    return {"Google": google_search_url}

# Function to extract possible usernames from metadata and filenames
def extract_username(image_path, metadata):
    possible_keys = ["Image Artist", "Owner Name", "Copyright", "Make"]
    
    for key in possible_keys:
        if key in metadata:
            return metadata[key].replace(" ", "").lower()

    # Try extracting from filename
    filename = os.path.basename(image_path).split(".")[0]
    return filename.lower() if filename else None

# Function to perform OSINT social media tracking
def osint_social_media(username):
    if not username:
        username = input("Enter a username for OSINT tracking (or press Enter to skip): ").strip()
    
    if not username:
        print("No username provided. Skipping OSINT tracking.")
        return {}

    platforms = {
        "Twitter": f"https://twitter.com/{username}",
        "Instagram": f"https://www.instagram.com/{username}/",
        "Facebook": f"https://www.facebook.com/{username}",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "GitHub": f"https://github.com/{username}",
        "Pinterest": f"https://www.pinterest.com/{username}/",
        "LinkedIn": f"https://www.linkedin.com/in/{username}/",
        "Snapchat": f"https://www.snapchat.com/add/{username}",
        "YouTube": f"https://www.youtube.com/{username}",
    }

    results = {}
    for platform, url in platforms.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                results[platform] = url
            else:
                results[platform] = "Not found"
        except requests.exceptions.RequestException:
            results[platform] = "Not found"
    
    return results

# Function to generate a PDF report
def generate_report(image_path, metadata, reverse_search_results, osint_results):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(190, 10, "OSINT Report - Darkseid", ln=True, align="C")
    pdf.ln(10)
    
    # Image
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "Analyzed Image:", ln=True)
    pdf.ln(5)
    pdf.image(image_path, x=10, w=100)
    pdf.ln(10)

    # Metadata
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "Extracted Metadata:", ln=True)
    pdf.set_font("Arial", "", 10)
    if metadata:
        for key, value in metadata.items():
            pdf.multi_cell(190, 8, f"{key}: {value}")
    else:
        pdf.multi_cell(190, 8, "No metadata found.")
    pdf.ln(5)

    # Reverse Image Search Results
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "Reverse Image Search Results:", ln=True)
    pdf.set_font("Arial", "", 10)
    for engine, link in reverse_search_results.items():
        pdf.multi_cell(190, 8, f"{engine}: {link}")
    pdf.ln(5)

    # OSINT Social Media Tracking
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "OSINT Social Media Tracking:", ln=True)
    pdf.set_font("Arial", "", 10)
    if osint_results:
        for platform, result in osint_results.items():
            pdf.multi_cell(190, 8, f"{platform}: {result}")
    else:
        pdf.multi_cell(190, 8, "No OSINT results found.")
    
    # Save Report
    report_name = f"{REPORTS_DIR}report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(report_name)
    print(f"Report saved: {report_name}")

# Function to process an image
def process_image(image_path):
    print(f"Processing: {image_path}")
    metadata = extract_metadata(image_path)
    reverse_search_results = reverse_image_search(image_path)
    
    # Extract or ask for username
    username = extract_username(image_path, metadata)
    osint_results = osint_social_media(username)

    generate_report(image_path, metadata, reverse_search_results, osint_results)

# Multithreading for bulk processing
def process_bulk_images(image_paths):
    threads = []
    for image_path in image_paths:
        thread = threading.Thread(target=process_image, args=(image_path,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

# Main execution
if __name__ == "__main__":
    image_directory = "images/"
    os.makedirs(image_directory, exist_ok=True)
    image_files = [os.path.join(image_directory, f) for f in os.listdir(image_directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not image_files:
        print("No images found in the 'images' directory.")
    else:
        process_bulk_images(image_files)
