import os
import requests
import threading
import subprocess
from fpdf import FPDF
from datetime import datetime

# Generate ASCII banner using 'toilet'
def generate_banner():
    try:
        banner = subprocess.check_output("toilet -f big -F metal Darkseid", shell=True).decode()
        print(banner)
    except Exception as e:
        print("Error generating banner:", e)

# Display the banner
generate_banner()

# Google API Configuration (Replace with your own)
GOOGLE_API_KEY = "AIzaSyCf_IUcwm_zojbSjiCsCfzB8X9hIHT2_mY"
GOOGLE_CSE_ID = "15c95d696f1e74485"

SOCIAL_MEDIA_PLATFORMS = [
    "https://twitter.com/{}",
    "https://www.facebook.com/{}",
    "https://www.instagram.com/{}",
    "https://www.linkedin.com/in/{}",
    "https://www.reddit.com/user/{}",
    "https://github.com/{}",
    "https://www.tiktok.com/@{}"
]

def google_reverse_image_search(image_url):
    search_url = f"https://www.googleapis.com/customsearch/v1?q={image_url}&searchType=image&key={GOOGLE_API_KEY}&cx={GOOGLE_CSE_ID}"
    try:
        response = requests.get(search_url)
        data = response.json()
        if "items" in data:
            return [item["link"] for item in data["items"]]
    except requests.exceptions.RequestException:
        pass
    return ["Search failed"]

def extract_metadata(image_path):
    try:
        output = subprocess.run(["exiftool", image_path], capture_output=True, text=True)
        metadata = {}
        for line in output.stdout.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip()
        return metadata
    except Exception as e:
        print(f"Error extracting metadata: {e}")
        return {}

def extract_gps(metadata):
    try:
        if "GPS Latitude" in metadata and "GPS Longitude" in metadata:
            lat = metadata["GPS Latitude"]
            lon = metadata["GPS Longitude"]
            return lat, lon
    except Exception as e:
        print(f"Error extracting GPS: {e}")
    return None

def track_username(username):
    results = {}
    for platform in SOCIAL_MEDIA_PLATFORMS:
        url = platform.format(username)
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                results[url] = "Found"
            else:
                results[url] = "Not Found"
        except requests.exceptions.RequestException:
            results[url] = "Error"
    return results

def generate_report(image_path, metadata, search_results, gps_coords, username, username_results):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(190, 10, "OSINT Report - Darkseid", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "Analyzed Image:", ln=True)
    pdf.ln(5)
    pdf.image(image_path, x=10, w=100)
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "Extracted Metadata:", ln=True)
    pdf.set_font("Arial", "", 10)
    for key, value in metadata.items():
        pdf.multi_cell(190, 8, f"{key}: {value}")
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "GPS Location:", ln=True)
    pdf.set_font("Arial", "", 10)
    if gps_coords:
        lat, lon = gps_coords
        maps_link = f"https://www.google.com/maps?q={lat},{lon}"
        pdf.multi_cell(190, 8, f"Latitude: {lat}, Longitude: {lon}")
        pdf.multi_cell(190, 8, f"Google Maps: {maps_link}")
    else:
        pdf.multi_cell(190, 8, "No GPS data found.")
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "Google Reverse Image Search Results:", ln=True)
    pdf.set_font("Arial", "", 10)
    for link in search_results:
        pdf.multi_cell(190, 8, link)
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, f"OSINT Username Tracking for: {username}", ln=True)
    pdf.set_font("Arial", "", 10)
    for url, status in username_results.items():
        pdf.multi_cell(190, 8, f"{url}: {status}")
    
    report_name = f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(report_name)
    print(f"Report saved: {report_name}")

def process_image(image_path, username):
    print(f"Processing: {image_path}")
    metadata = extract_metadata(image_path)
    gps_coords = extract_gps(metadata)
    search_results = google_reverse_image_search(image_path)
    username_results = track_username(username)
    generate_report(image_path, metadata, search_results, gps_coords, username, username_results)

def process_bulk_images(image_paths, username):
    threads = []
    for image_path in image_paths:
        thread = threading.Thread(target=process_image, args=(image_path, username))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    username = input("Enter the username to track: ")
    image_directory = "images/"
    os.makedirs(image_directory, exist_ok=True)
    image_files = [os.path.join(image_directory, f) for f in os.listdir(image_directory) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    
    if not image_files:
        print("No images found in the 'images' directory.")
    else:
        process_bulk_images(image_files, username)
