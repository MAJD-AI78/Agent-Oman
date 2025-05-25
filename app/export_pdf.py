from fpdf import FPDF

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Agent-Oman Strategic Report", ln=True, align="C")

    def body(self, content):
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 10, content)

def export_to_pdf(content, filename="agent_oman_report.pdf"):
    pdf = PDFReport()
    pdf.add_page()
    pdf.body(content)
    pdf.output(filename)
    print(f"✅ PDF exported: {filename}")
