# Darkseid - OSINT Automation Tool

Darkseid is a powerful OSINT (Open-Source Intelligence) automation tool designed for cybersecurity professionals and ethical hackers. It extracts metadata, performs facial recognition, conducts OSINT searches, and generates PDF reports.

## Features
- **Metadata Extraction**: Extracts EXIF data from images.
- **Face Recognition**: Identifies faces in images.
- **OSINT Analysis**: Searches for related online data.
- **PDF Reporting**: Generates detailed reports with findings.
- **ASCII Banner**: Displays a cool ASCII banner using `toilet`.

## Installation
```bash
sudo apt update && sudo apt install -y toilet python3 python3-pip
pip install -r requirements.txt
```

## Usage
```bash
python3 darkseid.py --image /path/to/image.jpg --meta --face --osint
```

## Example Output
```
Processing image: example.jpg
Extracting metadata...
Recognizing faces...
Performing OSINT scraping...
PDF report saved at: /home/kali/Darkseid/reports/example.pdf
```

## License
This project is for educational and ethical purposes only. Use responsibly.

