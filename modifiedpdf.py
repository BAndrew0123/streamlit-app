import os
import pandas as pd
import streamlit as st
from fpdf import FPDF
import img2pdf
import pdfkit
import subprocess
from tempfile import NamedTemporaryFile

# -------------------
# Conversion Functions
# -------------------

def libreoffice_to_pdf(input_path, output_path):
    subprocess.run([
        "libreoffice", "--headless", "--convert-to", "pdf", "--outdir",
        os.path.dirname(output_path) or ".", input_path
    ], check=True)

def convert_to_pdf(input_path, output_path):
    ext = os.path.splitext(input_path)[1].lower()

    if ext in [".doc", ".docx", ".ppt", ".pptx"]:
        libreoffice_to_pdf(input_path, output_path)

    elif ext in [".jpg", ".jpeg", ".png"]:  # Image → PDF
        with open(output_path, "wb") as f:
            f.write(img2pdf.convert(input_path))

    elif ext == ".txt":  # Text → PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read()
        pdf.multi_cell(0, 10, content)
        pdf.output(output_path)

    elif ext == ".csv":  # CSV → PDF (via HTML)
        df = pd.read_csv(input_path)
        html = df.to_html(index=False)
        pdfkit.from_string(html, output_path)

    elif ext == ".html":  # HTML → PDF
        pdfkit.from_file(input_path, output_path)

    else:
        raise ValueError(f"Unsupported file extension: {ext}")


# -------------------
# Streamlit App
# -------------------

st.title("📄 File to PDF Converter")
st.write("Upload any file (.docx, .pptx, .csv, .txt, .html, .jpg, .png) and convert it into a PDF.")

uploaded_file = st.file_uploader("Upload your file", type=["docx", "doc", "ppt", "pptx", "csv", "txt", "html", "jpg", "jpeg", "png"])

if uploaded_file:
    # Save uploaded file temporarily
    with NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp.write(uploaded_file.read())
        input_path = tmp.name

    output_path = os.path.splitext(input_path)[0] + ".pdf"

    try:
        convert_to_pdf(input_path, output_path)

        # Download button
        with open(output_path, "rb") as pdf_file:
            st.download_button(
                label="⬇️ Download PDF",
                data=pdf_file,
                file_name=os.path.splitext(uploaded_file.name)[0] + ".pdf",
                mime="application/pdf"
            )

        st.success("✅ Conversion successful!")

    except Exception as e:
        st.error(f"❌ Error: {e}")
