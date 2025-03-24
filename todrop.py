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



import streamlit as st
import os
import hashlib
from datetime import datetime
from io import BytesIO
from docx import Document

def generate_folder(uploaded_files, base_dir="uploads"):
    """Creates a folder based on the number of uploaded files."""
    
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)  # Ensure base directory exists

    if len(uploaded_files) == 1:
        # Use the file name as the folder name (without extension)
        folder_name = os.path.splitext(uploaded_files[0].name)[0]
    else:
        # Create a unique folder name using a hash and timestamp
        filenames = sorted([file.name for file in uploaded_files])
        unique_string = "_".join(filenames)
        folder_hash = hashlib.md5(unique_string.encode()).hexdigest()[:6]  # Short hash
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = f"data_{folder_hash}_{timestamp}"

    folder_path = os.path.join(base_dir, folder_name)
    os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist
    return folder_path

st.title("Upload and Process Multiple .docx Files")

uploaded_files = st.file_uploader("Choose .docx files", type="docx", accept_multiple_files=True)

if uploaded_files:
    folder_path = generate_folder(uploaded_files)
    
    st.success(f"Files will be saved in: `{folder_path}`")

    for file in uploaded_files:
        file_bytes = BytesIO(file.read())  # Convert to BytesIO
        doc = Document(file_bytes)  # Read .docx content
        text = "\n".join([para.text for para in doc.paragraphs])  # Extract text

        # Save each file inside the created folder
        file_save_path = os.path.join(folder_path, file.name)
        with open(file_save_path, "wb") as f:
            f.write(file_bytes.getbuffer())

        # Display file content preview
        st.subheader(f"Contents of {file.name}")
        st.text_area(f"Preview of {file.name}", text, height=200)
