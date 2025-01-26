import streamlit as st
from pypdf import PdfReader, PdfWriter, PageObject
from datetime import datetime  # To get the current date
from io import BytesIO

# App title
st.title("PDF Letterhead Overlay Tool")
st.markdown("""
This tool overlays a fixed letterhead on every page of a multi-page report. 
Select the report format, upload your report, and generate the final PDF.
""")

# Fixed Letterhead Path (change this to the actual path of your fixed letterhead file)
FIXED_LETTERHEAD_PATH = "C:/Users/SONY/Downloads/Python/letterhead.pdf"

# Validate the existence of the fixed letterhead
try:
    letterhead_reader = PdfReader(FIXED_LETTERHEAD_PATH)
    letterhead_page = letterhead_reader.pages[0]
except Exception as e:
    st.error("Failed to load the fixed letterhead file. Please check the file path.")
    st.stop()

# Quro ID input field
quro_id = st.text_input("Enter Quro ID (e.g., QC123)")

# Validate Quro ID
if quro_id:
    if not (quro_id.startswith("QC") and quro_id[2:].isdigit() and quro_id.isupper()):
        st.error("Invalid Quro ID! It must start with 'QC' (uppercase) followed by numbers, e.g., QC123.")
        quro_id = None  # Reset the value to ensure no further processing occurs

# Dropdown to select the report format
report_format = st.selectbox(
    "Select the report format",
    ["Select format", "Format X", "Format Y", "Format Z"]
)

if report_format != "Select format":
    # File uploader for the report
    report_file = st.file_uploader("Upload Report PDF", type=["pdf"])

    if report_file and quro_id:
        try:
            # Create PdfReader for the uploaded report
            report_reader = PdfReader(report_file)

            # Create a PdfWriter for the output PDF
            output_pdf = PdfWriter()

            # Process each page of the report based on the selected format
            for report_page in report_reader.pages:
                # Create a new blank page with the dimensions based on the selected format
                if report_format == "Format X":
                    new_page = PageObject.create_blank_page(
                        width=report_page.mediabox.width,
                        height=report_page.mediabox.height
                    )
                elif report_format == "Format Y":
                    new_page = PageObject.create_blank_page(
                        width=600,  # Example fixed width for Format Y
                        height=800  # Example fixed height for Format Y
                    )
                elif report_format == "Format Z":
                    new_page = PageObject.create_blank_page(
                        width=800,  # Example fixed width for Format Z
                        height=1000  # Example fixed height for Format Z
                    )

                # Merge the letterhead with the new page
                new_page.merge_page(letterhead_page)

                # Merge the report page onto the new page with the letterhead
                new_page.merge_page(report_page)

                # Add the new page to the output PDF
                output_pdf.add_page(new_page)

            # Save the final PDF to a BytesIO object for downloading
            output_pdf_stream = BytesIO()
            output_pdf.write(output_pdf_stream)
            output_pdf_stream.seek(0)

            # Get the current date in YYYY-MMM-DD format (e.g., 2025-Jan-09)
            current_date = datetime.now().strftime("%Y-%b-%d")

            # Provide a download link for the final PDF with Quro ID and date in the file name
            st.download_button(
                label="Download Final PDF",
                data=output_pdf_stream,
                file_name=f"Qurocare_Lab_Report_{quro_id}_{current_date}.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"An error occurred while processing the PDF: {e}")


