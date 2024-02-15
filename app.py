import streamlit as st
import PyPDF2
from io import BytesIO

# Function to extract text from a single PDF file
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

# Function to search for terms in the extracted text
def search_for_terms(text, key_terms):
    found_terms = set()  # Using a set to avoid duplicate terms
    for term in key_terms:
        if term.lower() in text.lower():
            found_terms.add(term)
    return found_terms

# Streamlit app to process multiple PDF uploads and search for key terms
def main():
    st.title("PDF Folder Key Terms Finder")

    # Instructions
    st.write("Upload multiple PDF files to search for key terms. Use the file dialog to select multiple files or drag and drop them.")

    # Upload PDFs
    uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)
    
    # Key terms input
    key_terms_input = st.text_input("Enter key terms separated by comma")
    key_terms = [term.strip() for term in key_terms_input.split(",") if term]  # Parse input into a list
    
    if st.button("Search"):
        if uploaded_files and key_terms:
            with st.spinner('Processing PDFs...'):
                results = {}
                for uploaded_file in uploaded_files:
                    # Read uploaded PDF file
                    bytes_data = uploaded_file.read()
                    text = extract_text_from_pdf(BytesIO(bytes_data))
                    found_terms = search_for_terms(text, key_terms)
                    
                    # Add results
                    if found_terms:
                        results[uploaded_file.name] = found_terms

                # Once processing is done, display results
                if results:
                    for filename, terms in results.items():
                        st.success(f"{filename}: {', '.join(terms)}")
                else:
                    st.info("No key terms found in the uploaded files.")
        else:
            st.warning("Please upload files and specify key terms.")

if __name__ == "__main__":
    main()