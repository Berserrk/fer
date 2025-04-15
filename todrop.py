#!/bin/bash

mkdir -p ~/.streamlit/

cat <<EOF > ~/.streamlit/config.toml
[server]
headless = true
port = $PORT
enableXsrfProtection = false
enableCORS = false
EOF

poetry install
poetry run streamlit run app.py
