# filename: create_pdf.py

from fpdf import FPDF

pdf = FPDF()

# Add a page
pdf.add_page()

# Set font
pdf.set_font("Arial", size = 12)

# Add a cell
pdf.cell(200, 10, txt = "Python Internet Search Script Report", ln = True, align = 'C')

# Add more cells for the content
pdf.cell(200, 10, txt = "Script Description:", ln = True)
pdf.cell(200, 10, txt = "The script uses the 'googlesearch-python' library to perform Google searches.", ln = True)
pdf.cell(200, 10, txt = "It takes a search query as input and returns URLs of the search results.", ln = True)

pdf.cell(200, 10, txt = "Script Usage:", ln = True)
pdf.cell(200, 10, txt = "Run the script and enter the search keywords when prompted.", ln = True)

pdf.cell(200, 10, txt = "Script Output:", ln = True)
pdf.cell(200, 10, txt = "The script prints the URLs of the search results.", ln = True)

# Save the pdf with name .pdf
pdf.output("Python_Script_Report.pdf")