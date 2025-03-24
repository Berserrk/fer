import streamlit as st
from io import BytesIO
from docx import Document

st.title("Upload Multiple .docx Files")

uploaded_files = st.file_uploader("Choose .docx files", type="docx", accept_multiple_files=True)

if uploaded_files:
    doc_contents = {}  # Dictionary to store file content separately
    
    for file in uploaded_files:
        file_bytes = BytesIO(file.read())  # Convert to BytesIO
        doc = Document(file_bytes)  # Read .docx content
        text = "\n".join([para.text for para in doc.paragraphs])  # Extract text
        doc_contents[file.name] = text  # Store in dictionary

    # Display contents
    for filename, content in doc_contents.items():
        st.subheader(f"Contents of {filename}")
        st.text_area(f"Content of {filename}", content, height=200)


from datetime import datetime

def generate_folder_name():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"data_folder_{timestamp}"
