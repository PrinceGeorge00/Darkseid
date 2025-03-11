from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "OSINT Report", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_pdf_report(image_name, metadata, face_results, osint_results):
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)  # Set automatic page breaks
    pdf.add_page()
    pdf.set_left_margin(15)  # Left margin to prevent cut-off text
    pdf.set_right_margin(15)  # Right margin

    # Set font
    pdf.set_font("Arial", size=12)

    # Title
    pdf.cell(200, 10, f"Report for: {image_name}", ln=True, align="C")
    pdf.ln(10)

    # Add Metadata Section
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "🔹 Metadata Extraction:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 8, metadata)  # Multi-cell ensures wrapping
    pdf.ln(5)

    # Add Face Recognition Section
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "🔹 Face Recognition Results:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 8, face_results)
    pdf.ln(5)

    # Add OSINT Results Section
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "🔹 OSINT Search Results:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 8, osint_results)
    pdf.ln(5)

    # Save PDF
    report_path = os.path.join("/home/kali/Darkseid/reports", f"{image_name}.pdf")
    pdf.output(report_path)
    
    print(f"PDF report saved at: {report_path}")
