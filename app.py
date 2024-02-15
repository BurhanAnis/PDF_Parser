import streamlit as st
import PyPDF2
from io import BytesIO
from collections import defaultdict

# Function to extract text from a single PDF file
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

# Updated function to count occurrences of each term in the text
def search_for_terms_and_count(text, key_terms):
    term_counts = defaultdict(int)  # Default to 0 for each key term
    lower_text = text.lower()
    for term in key_terms:
        count = lower_text.count(term.lower())
        if count > 0:
            term_counts[term] += count
    return term_counts

# Streamlit app to process multiple PDF uploads, search for key terms, and count occurrences
def main():
    st.title("PDF Folder Key Terms Finder")

    # Instructions
    st.write("Upload multiple PDF files to search for key terms and see how many times they appear. Use the file dialog to select multiple files or drag and drop them.")

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
                    term_counts = search_for_terms_and_count(text, key_terms)
                    
                    # Add results if any term is found
                    if term_counts:
                        results[uploaded_file.name] = term_counts

                # Sort results by total count in descending order and display
                if results:
                    for filename in sorted(results, key=lambda x: sum(results[x].values()), reverse=True):
                        terms_counts_str = ', '.join([f"{term}: {count}" for term, count in results[filename].items()])
                        st.success(f"{filename}: {terms_counts_str}")
                else:
                    st.info("No key terms found in the uploaded files.")
        else:
            st.warning("Please upload files and specify key terms.")

if __name__ == "__main__":
    main()
