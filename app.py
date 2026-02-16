import streamlit as st
import fitz  # PyMuPDF
import os

st.set_page_config(page_title="PDF Signature Panel Inserter", layout="centered")

st.title("PDF Signature Panel Inserter")
st.write("Upload your PDF to automatically add signature panels.")

# Hardcode the path to the font file in your GitHub repository
font_path = "times.ttf"

# Streamlit file uploader (now only asks for the PDF)
pdf_file = st.file_uploader("Upload PDF File", type=['pdf'])

if pdf_file:
    if st.button("Generate Signature Panels"):
        
        # Safety check: Ensure the font file was actually pushed to GitHub
        if not os.path.exists(font_path):
            st.error(f"Error: The font file '{font_path}' was not found in the repository. Please make sure you uploaded it to GitHub.")
        else:
            with st.spinner("Processing PDF..."):
                
                # Open PDF directly from the uploaded bytes
                doc = fitz.open(stream=pdf_file.read(), filetype="pdf")

                # Define signatories: (Label, Name)
                prepared_by = [
                    ("Tabulation Incharge", "Mr. Daipayan Mandal"),
                    ("Tabulation Member", "Mr. Prakash Jangle"),
                ]

                approvers = [
                    ("GMC Chairman", "Dr. E. Siva Prasad"),
                    ("GMC Member", "Dr. Sanjaykumar Borikar"),
                    ("GMC Member", "Mr. Pradyanshil Ramteke"),
                ]

                # Layout config
                fontname = "custom_font"  
                fontsize = 10
                line_spacing = 24
                start_y = 675
                start_x_left = 50
                start_x_right = 620

                # Left column positions
                col1_x = start_x_left
                col2_x = start_x_left + 120
                col3_x = start_x_left + 300

                # Right column positions
                col4_x = start_x_right
                col5_x = start_x_right + 120
                col6_x = start_x_right + 300

                # Add to every page
                for page in doc:
                    y = start_y

                    # Header Row
                    page.insert_text((col1_x, y), "Prepared by", fontname=fontname, fontsize=fontsize+1, fontfile=font_path)
                    page.insert_text((col2_x, y), "Name", fontname=fontname, fontsize=fontsize+1, fontfile=font_path)
                    page.insert_text((col3_x, y), "Signature", fontname=fontname, fontsize=fontsize+1, fontfile=font_path)

                    page.insert_text((col4_x, y), "Approved by", fontname=fontname, fontsize=fontsize+1, fontfile=font_path)
                    page.insert_text((col5_x, y), "Name", fontname=fontname, fontsize=fontsize+1, fontfile=font_path)
                    page.insert_text((col6_x, y), "Signature", fontname=fontname, fontsize=fontsize+1, fontfile=font_path)

                    y += line_spacing

                    # Prepared by section
                    for label, name in prepared_by:
                        page.insert_text((col1_x, y), label, fontname=fontname, fontsize=fontsize, fontfile=font_path)
                        page.insert_text((col2_x, y), name, fontname=fontname, fontsize=fontsize, fontfile=font_path)
                        page.insert_text((col3_x, y), "__________________", fontname=fontname, fontsize=fontsize, fontfile=font_path)
                        y += line_spacing

                    # Right side (approvers)
                    y_right = start_y + line_spacing
                    for label, name in approvers:
                        page.insert_text((col4_x, y_right), label, fontname=fontname, fontsize=fontsize, fontfile=font_path)
                        page.insert_text((col5_x, y_right), name, fontname=fontname, fontsize=fontsize, fontfile=font_path)
                        page.insert_text((col6_x, y_right), "__________________", fontname=fontname, fontsize=fontsize, fontfile=font_path)
                        y_right += line_spacing

                    # Additional Authority (Controller of Examination)
                    auth_x = start_x_left + 180
                    auth_y = max(y, y_right) + 20
                    page.insert_text((auth_x, auth_y), "__________________________", fontname=fontname, fontsize=fontsize+1, fontfile=font_path)
                    auth_y += 20
                    page.insert_text((auth_x, auth_y), "Dr. Anantkumar N. Dabhade", fontname=fontname, fontsize=fontsize+1, fontfile=font_path)
                    auth_y += 10
                    page.insert_text((auth_x+5, auth_y), "Controller of Examination", fontname=fontname, fontsize=fontsize+1, fontfile=font_path)

                    # Additional Authority (Principal)
                    auth_x = start_x_right + 180
                    auth_y = max(y, y_right) + 20
                    page.insert_text((auth_x, auth_y), "__________________________", fontname=fontname, fontsize=fontsize+1, fontfile=font_path)
                    auth_y += 20
                    page.insert_text((auth_x, auth_y), "Dr. Avinash N. Shrikhande", fontname=fontname, fontsize=fontsize+1, fontfile=font_path)
                    auth_y += 10
                    page.insert_text((auth_x+25, auth_y), "Principal", fontname=fontname, fontsize=fontsize+1, fontfile=font_path)

                    # Add current date at bottom-left corner
                    bottom_x = 30
                    bottom_y = page.rect.height - 30
                    current_date = "Date: _____________" 
                    page.insert_text((bottom_x, bottom_y), current_date, fontsize=10, fontname=fontname, fontfile=font_path)

                # Generate output bytes
                pdf_out_bytes = doc.tobytes()

                st.success("PDF processed successfully! Click below to download.")

                # Streamlit Download Button
                st.download_button(
                    label="Download Modified PDF",
                    data=pdf_out_bytes,
                    file_name="signature_panel_output.pdf",
                    mime="application/pdf"
                )
