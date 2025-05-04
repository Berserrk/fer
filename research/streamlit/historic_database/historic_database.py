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
            if st.button("Use Existing Analysis"):
                with open("/Users/firaterman/Documents/fer/research/streamlit/historic_database/inputs/insurance_fraud/entities_flagged.json", 'r') as file:
                    entities_data = json.load(file)                

                # Normalize the JSON data (flattening the 'entities' list)
                df_entities = pd.json_normalize(entities_data['entities'], sep='_')

                # Display the normalized table
                st.subheader("Entities Table")
                st.dataframe(df_entities)
        else:
            if st.button("Submit Document"):
                # Read and display document content
                st.write("ELSE2")
                st.success("Document has been successfully submitted!")
                with open("/Users/firaterman/Documents/fer/research/streamlit/historic_database/inputs/insurance_fraud/entities_flagged.json", 'r') as file:
                    entities_data = json.load(file)                

                # Normalize the JSON data (flattening the 'entities' list)
                df_entities = pd.json_normalize(entities_data['entities'], sep='_')

                # Display the normalized table
                st.subheader("Entities Table")
                st.dataframe(df_entities)

if __name__ == "__main__":
    main()
