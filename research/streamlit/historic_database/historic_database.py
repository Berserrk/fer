import streamlit as st
from docx import Document
import duckdb
import json
import pandas as pd

# Function to read the DOCX file
def read_docx(file):
    doc = Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

# Streamlit app
def main():
    st.title("DOCX File Reader")

    # Upload DOCX file
    uploaded_file = st.file_uploader("Choose a DOCX file", type="docx")
    
    if uploaded_file:
        resultt = uploaded_file.name.replace(".docx", "")
        
        # Check if this article already exists in the database
        with duckdb.connect('articles_metadata.duckdb') as conn:
            result = conn.execute(
                "SELECT strftime(date_uploaded, '%Y-%m-%d %H:%M:%S') FROM articles WHERE file_name = ?",
                (uploaded_file.name,)
            ).fetchone()

        if result:
            upload_date = result[0]
            st.warning(f"Article already exists in the database. Uploaded on {upload_date}")

            # Create columns layout for the buttons
            col1, col2 = st.columns(2)

            with col1:
                # "View Existing Analysis" button on the left
                use_existing = st.button("View Existing Analysis")
                if use_existing:
                    # Read the existing analysis JSON and display the table
                    with open("/Users/firaterman/Documents/fer/research/streamlit/historic_database/inputs/insurance_fraud/entities_flagged.json", 'r') as file:
                        entities_data = json.load(file)

                    # Normalize the JSON data (flattening the 'entities' list)
                    df_entities = pd.json_normalize(entities_data['entities'], sep='_')

                    # Display the normalized table
                    st.subheader("Entities Table")
                    st.dataframe(df_entities)

            with col2:
                # "Start New Submission" button on the right
                submit_new = st.button("Start New Submission")
                if submit_new:
                    # Process the article as a new submission
                    st.write("Processing the article as a new one...")
                    # Add logic for handling new submission (save data, etc.)
                    st.success("New article has been successfully submitted!")

        else:
            # If the article does not exist, allow the user to submit it as new
            if st.button("SSubmit as new document"):
                st.write("Processing the article as a new one...")
                # Add logic for saving the new article and analysis
                st.success("New article has been successfully submitted!")

if __name__ == "__main__":
    main()