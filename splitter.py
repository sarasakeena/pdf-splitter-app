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

def split_custom_ranges(uploaded_file, page_ranges_str):
    reader = PyPDF2.PdfReader(uploaded_file)
    writer = PyPDF2.PdfWriter()

    pages = []
    for part in page_ranges_str.split(','):
        part = part.strip()
        if '-' in part:
            start, end = map(int, part.split('-'))
            pages.extend(range(start - 1, end))
        else:
            pages.append(int(part) - 1)

    for p in pages:
        if 0 <= p < len(reader.pages):
            writer.add_page(reader.pages[p])

    output_pdf = BytesIO()
    writer.write(output_pdf)
    output_pdf.seek(0)
    return output_pdf

# UI
st.set_page_config(page_title="PDF Splitter")
st.title("PDF Splitter")
st.write("Upload a PDF and choose how you want to split it:")

uploaded_file = st.file_uploader("📤 Upload your PDF", type="pdf")

if uploaded_file:
    num_pages = len(PyPDF2.PdfReader(uploaded_file).pages)
    
    split_mode = st.radio("Choose Split Mode", ["Start-End Range", "Custom Pages"])

    if split_mode == "Start-End Range":
        start_page = st.number_input("Start Page", min_value=1, max_value=num_pages, value=1)
        end_page = st.number_input("End Page", min_value=1, max_value=num_pages, value=2)
        if st.button("✂️ Split PDF"):
            output = split_pdf(uploaded_file, start_page, end_page)
            st.success("✅ Split successful!")
            st.download_button(
                label="📥 Download",
                data=output,
                file_name="split_range.pdf",
                mime="application/pdf"
            )

    else:
        page_input = st.text_input("Enter custom pages (e.g. 1,3,5-7,10)", value="1,8-12,18")
        if st.button("✂️ Split Custom Pages"):
            try:
                output = split_custom_ranges(uploaded_file, page_input)
                st.success("✅ Custom page split successful!")
                st.download_button(
                    label="📥 Download",
                    data=output,
                    file_name="split_custom.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"❌ Error: {e}")
