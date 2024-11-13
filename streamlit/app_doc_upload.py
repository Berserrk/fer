import streamlit as st
import pandas as pd
import os
import sys

# Configuration for custom port

def main():
    st.title("Document Upload System")
    
    # File uploader section
    st.header("Upload your document")
    uploaded_file = st.file_uploader(
        "Choose a file", 
        type=['csv', 'txt', 'pdf']
    )
    
    if uploaded_file is not None:
        # Display file details
        file_details = {
            "Filename": uploaded_file.name,
            "File type": uploaded_file.type,
            "File size": f"{uploaded_file.size / 1024:.2f} KB"
        }
        
        # Show file info
        st.write("### File Details:")
        for key, value in file_details.items():
            st.write(f"- {key}: {value}")
            
        # Preview section based on file type
        st.write("### Preview:")
        
        if uploaded_file.type == "text/csv":
            try:
                df = pd.read_csv(uploaded_file)
                st.write("First 5 rows of the CSV file:")
                st.dataframe(df.head())
                
                # Basic statistics
                st.write("### Basic Statistics:")
                st.write(f"- Number of rows: {len(df)}")
                st.write(f"- Number of columns: {len(df.columns)}")
                st.write("- Columns:", ', '.join(df.columns))
                
            except Exception as e:
                st.error(f"Error reading CSV file: {e}")
                
        elif uploaded_file.type == "text/plain":
            try:
                content = uploaded_file.read().decode()
                st.text_area("File content", content, height=200)
            except Exception as e:
                st.error(f"Error reading text file: {e}")
                
        elif uploaded_file.type == "application/pdf":
            st.write("PDF file detected. Preview not available.")

if __name__ == "__main__":
    main()