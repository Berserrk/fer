import duckdb
import hashlib
import json
import os

# Function to compute the hash of the article content (this assumes the article is a text file)
def generate_article_hash(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

# Connect to DuckDB database (this will create the database file if it doesn't exist)
conn = duckdb.connect('articles_metadata.duckdb')

# Function to create tables (if not already created)
def create_tables():
    # Create the Articles table
    conn.execute("""
    CREATE TABLE IF NOT EXISTS articles (
        article_hash TEXT,
        file_name TEXT NOT NULL,
        date_uploaded TIMESTAMP,
        json_path TEXT
    );
    """)
    
    
    # Create the Entities table without FOREIGN KEY constraint
    conn.execute("""
    CREATE TABLE IF NOT EXISTS entities (
        article_hash TEXT NOT NULL,       -- Article hash linking to the article (no FOREIGN KEY constraint)
        name TEXT NOT NULL,               -- Entity name (e.g., "Sarah Parker")
        crime TEXT                        -- Entity's crime or flagged activity
    );
    """)
    
    # Create the Descriptions table without FOREIGN KEY constraint
    conn.execute("""
    CREATE TABLE IF NOT EXISTS descriptions (
        article_hash TEXT NOT NULL,       -- Article hash linking to the article (no FOREIGN KEY constraint)
        entity_name TEXT NOT NULL,        -- Name of the entity being described (e.g., "Sarah Parker")
        description TEXT                 -- Description of the entity
    );
    """)

# Function to insert article metadata and JSON data into tables
def insert_article_data(article_hash, file_name, json_path, entities_json, descriptions_json):
    # Insert article metadata into the articles table only if it doesn't already exist
    result = conn.execute(
        "SELECT 1 FROM articles WHERE article_hash = ?", (article_hash,)
    ).fetchone()
    if result is None:
        conn.execute("""
        INSERT INTO articles (article_hash, file_name, date_uploaded, json_path)
        VALUES (?, ?, CURRENT_TIMESTAMP, ?)
        """, (article_hash, file_name, json_path))

    # Insert entities into the entities table
    for entity in entities_json['entities']:
        conn.execute("""
        INSERT INTO entities (article_hash, name, crime)
        VALUES (?, ?, ?)
        """, (article_hash, entity['name'], entity.get('crime', None)))

    # Insert descriptions into the descriptions table
    for description in descriptions_json['entities']:
        conn.execute("""
        INSERT INTO descriptions (article_hash, entity_name, description)
        VALUES (?, ?, ?)
        """, (article_hash, description['name'], description.get('description', None)))

    conn.commit()

# Function to process articles from the repository
def process_articles(repository_path):
    # Iterate over all articles in the repository
    for article_dir in os.listdir(repository_path):
        article_path = os.path.join(repository_path, article_dir)

        if os.path.isdir(article_path):
            # Assuming the article has a .docx file and JSON files in the same directory
            docx_file = next((f for f in os.listdir(article_path) if f.endswith('.docx')), None)
            if docx_file:
                article_file_path = os.path.join(article_path, docx_file)
                article_hash = generate_article_hash(article_file_path)
                file_name = docx_file
                
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

# Run the functions
create_tables()  # Create the tables in the database
repository_path = '/Users/firaterman/Documents/fer/research/streamlit/historic_database/inputs/'  # Set your repository path here
process_articles(repository_path)  # Process the articles in the repository

conn.close()  # Close the connection