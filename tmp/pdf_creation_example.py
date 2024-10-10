from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as PlatypusImage, Table, TableStyle
from markdown2 import markdown  # Use markdown2 for better HTML conversion
from bs4 import BeautifulSoup  # Use BeautifulSoup for parsing HTML

def save_images_and_text_as_pdf(image1_path, image2_path, output_pdf_path, markdown_texts):
    # Create a PDF canvas
    doc = SimpleDocTemplate(output_pdf_path, pagesize=letter)
    story = []

    # Add text content (Markdown or plain text)
    styles = getSampleStyleSheet()

    # Process the markdown texts to convert to formatted paragraphs
    for markdown_text in markdown_texts:
        # Convert Markdown to HTML
        html_text = markdown(markdown_text)

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_text, 'html.parser')

        # Handle headers and paragraphs
        for element in soup:
            if element.name == 'h1':
                paragraph = Paragraph(element.get_text(), styles['Heading1'])
            elif element.name == 'h2':
                paragraph = Paragraph(element.get_text(), styles['Heading2'])
            elif element.name == 'h3':
                paragraph = Paragraph(element.get_text(), styles['Heading3'])
            elif element.name == 'ul':  # Handle lists
                for li in element.find_all('li'):
                    bullet_point = Paragraph(f'• {li.get_text()}', styles['Normal'])
                    story.append(bullet_point)
                continue  # Skip adding the 'ul' element itself
            else:  # Handle regular paragraphs
                paragraph = Paragraph(element.get_text(), styles['Normal'])

            story.append(paragraph)

    # Set image dimensions
    image_height = 2 * inch
    image_width = 3.5 * inch

    # Create image objects
    image1 = PlatypusImage(image1_path)
    image1.drawHeight = image_height
    image1.drawWidth = image_width

    image2 = PlatypusImage(image2_path)
    image2.drawHeight = image_height
    image2.drawWidth = image_width

    # Create a table to hold the images
    data = [[image1, image2]]
    table = Table(data)

    # Set table style to adjust image alignment
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Vertically align images
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),    # Horizontally align images
    ]))

    # Add the table containing images to the story
    story.append(table)
    story.append(Spacer(1, 12))  # Add some space after images
    
    # Process the markdown texts to convert to formatted paragraphs
    for markdown_text in markdown_texts:
        # Convert Markdown to HTML
        html_text = markdown(markdown_text)

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_text, 'html.parser')

        # Handle headers and paragraphs
        for element in soup:
            if element.name == 'h1':
                paragraph = Paragraph(element.get_text(), styles['Heading1'])
            elif element.name == 'h2':
                paragraph = Paragraph(element.get_text(), styles['Heading2'])
            elif element.name == 'h3':
                paragraph = Paragraph(element.get_text(), styles['Heading3'])
            elif element.name == 'ul':  # Handle lists
                for li in element.find_all('li'):
                    bullet_point = Paragraph(f'• {li.get_text()}', styles['Normal'])
                    story.append(bullet_point)
                continue  # Skip adding the 'ul' element itself
            else:  # Handle regular paragraphs
                paragraph = Paragraph(element.get_text(), styles['Normal'])

            story.append(paragraph)

    # Build the PDF
    doc.build(story)


# Example usage:
image1_path = "C:/DATA_SCIENCE_HAIZEA/CBR-AND-RECOMMENDATION-SYSTEM/report/Red_wines_profile.png"
image2_path = "C:/DATA_SCIENCE_HAIZEA/CBR-AND-RECOMMENDATION-SYSTEM/report/White_wines_profile.png"
output_pdf_path = "C:/DATA_SCIENCE_HAIZEA/CBR-AND-RECOMMENDATION-SYSTEM/report/output_with_text.pdf"

markdown_texts = [
    "# Header 1\nThis is an example of a Markdown header converted to text.",
    "## Header 2\nSome more text goes here, formatted like Markdown.",
    "- Item 1 in a list\n- Item 2 in a list\n- Item 3 in a list",
    "### Conclusion\nThis is the end of the document."
]

save_images_and_text_as_pdf(image1_path, image2_path, output_pdf_path, markdown_texts)