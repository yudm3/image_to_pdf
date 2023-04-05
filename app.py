import streamlit as st
from PIL import Image
import io
from image_to_pdf_converter import image_to_pdf

st.title("Image to PDF Converter")

uploaded_files = st.file_uploader("Choose JPG or PNG files", type=['jpg', 'png'], accept_multiple_files=True)

if uploaded_files:
    images = [Image.open(file) for file in uploaded_files]

    output_name = st.text_input("Enter the output PDF file name (without .pdf extension)")

    if output_name:
        output_buffer = io.BytesIO()
        image_to_pdf(images, output_buffer)

        output_buffer.seek(0)

        if st.button("Download PDF"):
            st.download_button("Download PDF", output_buffer, file_name=f"{output_name}.pdf", mime="application/pdf")