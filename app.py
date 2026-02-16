import streamlit as st
import fitz  # PyMuPDF
import os

st.set_page_config(page_title="PDF Signature & Background Inserter", layout="centered")

st.title("PDF Signature Panel & Background Inserter")
st.write("Upload your PDF. The app will automatically apply the institutional background and add the signature panels.")

# Hardcode the paths to the files in your GitHub repository
font_path = "times.ttf"
bg_path = "TR background.pdf"

# Streamlit file uploader (asks for the PDF data)
pdf_file = st.file_uploader("Upload PDF File", type=['pdf'])

if pdf_file:
    if st.button("Generate Document"):
        
        # Safety check: Ensure the required files are in the GitHub repo
        missing_files = []
        if not os.path.exists(font_path): missing_files.append(font_path)
        if not os.path.exists(bg_path): missing_files.append(bg_path)
            
        if missing_files:
            st.error(f"Error: The following required files were not found in the repository: {', '.join(missing_files)}. Please upload them to GitHub.")
        else:
            with st.spinner("Processing PDF..."):
                
                # Open uploaded PDF and Background PDF
                doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
                bg_doc = fitz.open(bg_path)
                
                # Create a completely new document for the output
                out_doc = fitz.open()

                # Define signatories
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

                col1_x = start_x_left
                col2_x = start_x_left + 120
                col3_x = start_x_left + 300

                col4_x = start_x_right
                col5_x = start_x_right + 120
                col6_x = start_x_right + 300

                # Process each page
                for i in range(len(doc)):
                    page = doc[i]
                    
                    # 1. Create a new page with the exact same dimensions as the original
                    new_page = out_doc.new_page(width=page.rect.width, height=page.rect.height)
                    
                    # 2. Draw the background PDF (layer 1 - bottom)
                    # We assume the background PDF has 1 page, hence bg_doc, 0
                    new_page.show_pdf_page(new_page.rect, bg_doc, 0)
                    
                    # 3. Draw the user's uploaded PDF page over the background (layer 2 - middle)
                    new_page.show_pdf_page(new_page.rect, doc, i)

                    # 4. Draw the signature panels (layer 3 - top)
                    y = start_y

                    # Header Row
                    new_page.insert_text((col1_x, y), "Prepared by", fontname=fontname, fontsize=fontsize+1, fontfile=font_path)
                    new_page.insert_text((col2_x, y), "Name", fontname=fontname, fontsize=fontsize+1, fontfile=font_path)
                    new_page.insert_text((col3_x, y), "Signature", fontname=fontname, fontsize=fontsize+1, fontfile=font_path)

                    new_page.insert_text((col4_x, y), "Approved by", fontname=fontname, fontsize=fontsize+1, fontfile=font_path)
                    new_page.insert_text((col5_x, y), "Name", fontname=fontname, fontsize=fontsize+1, fontfile=font_path)
                    new_page.insert_text((col6_x, y), "Signature", fontname=fontname, fontsize=fontsize+1, fontfile=font_path)

                    y += line_spacing

                    # Prepared by section
                    for label, name in prepared_by:
                        new_page.insert_text((col1_x, y), label, fontname=fontname, fontsize=fontsize, fontfile=font_path)
                        new_page.insert_text((col2_x, y), name, fontname=fontname, fontsize=fontsize, fontfile=font_path)
                        new_page.insert_text((col3_x, y), "__________________", fontname=fontname, fontsize=fontsize, fontfile=font_path)
                        y += line_spacing

                    # Right side (approvers)
                    y_right = start_y + line_spacing
                    for label, name in approvers:
                        new_page.insert_text((col4_x, y_right), label, fontname=fontname, fontsize=fontsize, fontfile=font_path)
                        new_page.insert_text((col5_x, y_right), name, fontname=fontname, fontsize=fontsize, fontfile=font_path)
                        new_page.insert_text((col6_x, y_right), "__________________", fontname=fontname, fontsize=fontsize, fontfile=font_path)
                        y_right += line_spacing

                    # Additional Authority (Controller of Examination)
                    auth_x = start_x_left + 180
                    auth_y = max(y, y_right) + 20
                    new_page.insert_text((auth_x, auth_y), "__________________________", fontname=fontname, fontsize=fontsize+1, fontfile=font_path)
                    auth_y += 20
                    new_page.insert_text((auth_x, auth_y), "Dr. Anantkumar N. Dabhade", fontname=fontname, fontsize=fontsize+1, fontfile=font_path)
                    auth_y += 10
                    new_page.insert_text((auth_x+5, auth_y), "Controller of Examination", fontname=fontname, fontsize=fontsize+1, fontfile=font_path)

                    # Additional Authority (Principal)
                    auth_x = start_x_right + 180
                    auth_y = max(y, y_right) + 20
                    new_page.insert_text((auth_x, auth_y), "__________________________", fontname=fontname, fontsize=fontsize+1, fontfile=font_path)
                    auth_y += 20
                    new_page.insert_text((auth_x, auth_y), "Dr. Avinash N. Shrikhande", fontname=fontname, fontsize=fontsize+1, fontfile=font_path)
                    auth_y += 10
                    new_page.insert_text((auth_x+25, auth_y), "Principal", fontname=fontname, fontsize=fontsize+1, fontfile=font_path)

                    # Add current date at bottom-left corner
                    bottom_x = 30
                    bottom_y = new_page.rect.height - 30
                    current_date = "Date: _____________" 
                    new_page.insert_text((bottom_x, bottom_y), current_date, fontsize=10, fontname=fontname, fontfile=font_path)

                # Generate output bytes
                pdf_out_bytes = out_doc.tobytes()

                st.success("PDF processed successfully with background and signatures! Click below to download.")

               # Streamlit Download Button
                st.download_button(
                    label="Download Final PDF",  # <--- Make sure this line has the closing quote and comma
                    data=pdf_out_bytes,
                    file_name="final_document_with_background.pdf",
                    mime="application/pdf"
                )
