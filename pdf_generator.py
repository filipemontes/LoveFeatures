import re
from io import BytesIO
from fpdf import FPDF

def clean_pdf_text(text):
    """Sanitizes text for PDF compatibility by replacing problematic characters."""
    replacements = {
        '’': "'", '‘': "'", '“': '"', '”': '"',
        '–': '-', '—': '-', '…': '...', 'ñ': 'n',
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u'
    }
    
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)

    return re.sub(r'[^\x00-\x7F]', '?', text)

def create_pdf_report(df, happy_summary, sad_summary, figures):
    """Generates a PDF report for the relationship analysis."""
    pdf = FPDF()
    
    # Clean summaries
    happy_summary = clean_pdf_text(happy_summary)
    sad_summary = clean_pdf_text(sad_summary)

    # Add a page and set font
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Relationship Analysis Report", 0, 1, 'C')
    pdf.ln(10)

    # Add charts
    pdf.set_font("Arial", 'B', 12)
    for idx, fig in enumerate(figures):
        try:
            img_bytes = fig.to_image(format="png")
            img_buffer = BytesIO(img_bytes)
            pdf.cell(0, 10, f"Chart {idx+1}", 0, 1)
            pdf.image(img_buffer, x=10, w=190)
            pdf.ln(5)
        except Exception as e:
            print(f"Error adding chart {idx+1}: {str(e)}")

    # Add summaries
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "AI Analysis Summary", 0, 1)
    pdf.ln(5)
    
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 8, "Happiest Week:\n" + happy_summary)
    pdf.ln(10)
    pdf.multi_cell(0, 8, "Toughest Week:\n" + sad_summary)
    
    return bytes(pdf.output(dest='S'))
