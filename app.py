import streamlit as st
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import base64
from reportlab.lib.utils import ImageReader

def image_to_pdf(images, output_buffer):
    pdf = canvas.Canvas(output_buffer, pagesize=letter)
    width, height = letter

    for img in images:
        img_width, img_height = img.size
        img_aspect = img_height / float(img_width)

        if (width / float(height)) < img_aspect:
            pdf_height = height
            pdf_width = pdf_height / img_aspect
        else:
            pdf_width = width
            pdf_height = pdf_width * img_aspect

        x = (width - pdf_width) / 2
        y = (height - pdf_height) / 2

        pdf.drawImage(ImageReader(img), x, y, pdf_width, pdf_height, preserveAspectRatio=True)
        pdf.showPage()

    pdf.save()

def get_image_list(uploaded_images):
    images = []
    for uploaded_image in uploaded_images:
        img = Image.open(uploaded_image)
        images.append(img)
    return images

def get_binary_file_downloader_link(file_buffer, file_name):
    file_buffer.seek(0)
    b64 = base64.b64encode(file_buffer.read()).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}.pdf">VIKA TUPICA</a>'

st.title("Image to PDF Converter")

uploaded_images = st.file_uploader("Choose images (JPG or PNG)", type=["jpg", "png"], accept_multiple_files=True)
pdf_name = st.text_input("Enter the name for your PDF file:")

if st.button("Convert and Download"):
    if uploaded_images and pdf_name:
        images = get_image_list(uploaded_images)
        output_buffer = io.BytesIO()
        image_to_pdf(images, output_buffer)
        download_link = get_binary_file_downloader_link(output_buffer, pdf_name)
        st.markdown(download_link, unsafe_allow_html=True)
    else:
        st.error("Please upload images and provide a name for the PDF file.")