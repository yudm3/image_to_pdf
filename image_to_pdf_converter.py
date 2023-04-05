from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

def image_to_pdf(images, output_buffer):
    pdf = canvas.Canvas(output_buffer, pagesize=letter)
    width, height = letter

    for img in images:
        img_width, img_height = img.size
        img_aspect = img_height / float(img_width)

        if (width / float(height)) < img_aspect:
            pdf_width = width
            pdf_height = pdf_width * img_aspect
        else:
            pdf_height = height
            pdf_width = pdf_height / img_aspect

        x = (width - pdf_width) / 2
        y = (height - pdf_height) / 2

        img_buffer = io.BytesIO()
        img.save(img_buffer, format=img.format)
        img_buffer.seek(0)

        pdf.drawImage(img_buffer, x, y, pdf_width, pdf_height, preserveAspectRatio=True)
        pdf.showPage()

    pdf.save()
