import streamlit as st
import PyPDF2
from io import BytesIO

def split_pdf(uploaded_file, start_page, end_page):
    reader = PyPDF2.PdfReader(uploaded_file)
    writer = PyPDF2.PdfWriter()

    for page_num in range(start_page - 1, end_page):
        writer.add_page(reader.pages[page_num])

    output_pdf = BytesIO()
    writer.write(output_pdf)
    output_pdf.seek(0)

    return output_pdf

# UI
st.set_page_config(page_title="PDF Splitter 💥")
st.title("📄 PDF Splitter App")
st.write("Upload a PDF and select page range to split it!")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    num_pages = len(PyPDF2.PdfReader(uploaded_file).pages)
    start_page = st.number_input("Start Page", min_value=1, max_value=num_pages, value=1)
    end_page = st.number_input("End Page", min_value=1, max_value=num_pages, value=2)

    if st.button("✂️ Split PDF"):
        output = split_pdf(uploaded_file, start_page, end_page)
        st.success("PDF has been split successfully! 🎉")
        st.download_button(
            label="📥 Download Split PDF",
            data=output,
            file_name="split_output.pdf",
            mime="application/pdf"
        )
