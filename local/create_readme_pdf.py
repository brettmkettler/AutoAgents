# filename: create_readme_pdf.py
from fpdf import FPDF

# Create instance of FPDF class
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", size=12)

# Add a title
pdf.set_font("Arial", style='B', size=16)
pdf.cell(200, 10, "Script Readme", ln=True, align='C')
pdf.set_font("Arial", size=12)
pdf.ln(10)

# Add content
content = """
This is a PDF readme file generated for the script that searches the internet.
Replace this text with relevant information about the script and its functionality.
"""

pdf.multi_cell(0, 10, content)

# Save the pdf with name .pdf
pdf.output("script_readme.pdf")