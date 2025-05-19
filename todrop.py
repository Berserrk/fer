import os
import json

def process_articles(repository_path):
    # Iterate over all articles in the repository
    for article_dir in os.listdir(repository_path):
        article_path = os.path.join(repository_path, article_dir)

        if os.path.isdir(article_path):
            # Construct expected file names based on article_dir
            expected_docx = f"{article_dir}.docx"
            expected_pdf = f"{article_dir}.pdf"
            
            article_file_path = None
            file_name = None

            # Check which file exists
            if expected_docx in os.listdir(article_path):
                article_file_path = os.path.join(article_path, expected_docx)
                file_name = expected_docx
            elif expected_pdf in os.listdir(article_path):
                article_file_path = os.path.join(article_path, expected_pdf)
                file_name = expected_pdf

            if article_file_path:
                article_hash = generate_document_hash(article_file_path)  # this handles both docx and pdf

                # Load entities and descriptions from the JSON files
                entities_json_path = os.path.join(article_path, 'entities_flagged.json')
                descriptions_json_path = os.path.join(article_path, 'entities_description.json')

                if os.path.exists(entities_json_path) and os.path.exists(descriptions_json_path):
                    with open(entities_json_path, 'r') as f:
                        entities_json = json.load(f)
                    with open(descriptions_json_path, 'r') as f:
                        descriptions_json = json.load(f)

                    # Insert data into DuckDB tables
                    insert_article_data(article_hash, file_name, article_path, entities_json, descriptions_json)
