#!/bin/bash

# Create Streamlit config directory and config file
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = \$PORT\n\
enableXsrfProtection = false\n\
enableCORS = false\n\
" > ~/.streamlit/config.toml

# Install Python dependencies using Poetry (optional if already done)
poetry install

# Run the Streamlit app using Poetry environment
poetry run streamlit run app.py
