import streamlit as st
import json
import pandas as pd
import sqlite3  # Use sqlite3 for database interaction
from datetime import datetime  # For managing timestamps

# Load JSON files
with open('countries.json', 'r') as f:
    country_status = json.load(f)
with open('categories_label.json', 'r') as f:
    categories_label = json.load(f)
with open('dict_response_full_text.json', 'r') as f:
    capitals = json.load(f)

# Prepare the list of countries and activities
countries = list(country_status.keys())
all_activities = set()
for country_info in categories_label.values():
    all_activities.update(country_info["activities"])
all_activities = sorted(all_activities)

# Create a DataFrame to hold the current activity statuses
data = {"Country": []}
for activity in all_activities:
    data[activity] = []
for country, info in categories_label.items():
    row = {activity: True if activity in info["activities"] else False for activity in all_activities}
    row["Country"] = country
    data["Country"].append(country)
    for activity in all_activities:
        data[activity].append(row[activity])

df = pd.DataFrame(data)

# Editable table in Streamlit
st.header("Activities Table (Editable)")
edited_df = st.data_editor(df, use_container_width=True, num_rows="fixed")

# Function to save changes to SQLite database
def save_to_database(df):
    try:
        conn = sqlite3.connect('activitiessql.db')

        # Create the activities_table if it doesn't exist using BOOLEAN
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS activities_table (
            Country TEXT,
            {},
            timestamp TEXT,
            PRIMARY KEY (Country, timestamp)
        )
        '''.format(", ".join([f'"{activity}" BOOLEAN' for activity in all_activities]))

        conn.execute(create_table_query)

        insert_data = []
        for _, row in df.iterrows():
            country = row["Country"].replace("'", "''")  # Escape single quotes
            activities = tuple(bool(row[activity]) for activity in all_activities)  # Convert activities to booleans
            current_timestamp = datetime.now().isoformat()  # Get current timestamp as ISO format string

            data_row = (country,) + activities + (current_timestamp,)

            # Check if the last entry for this country is different
            query = 'SELECT * FROM activities_table WHERE Country = ? ORDER BY timestamp DESC LIMIT 1'
            last_entry = conn.execute(query, (country,)).fetchone()

            # Check if there is a change in the activities
            if last_entry:
                if last_entry[1:-1] != activities:  # Exclude Country and timestamp for comparison
                    insert_data.append(data_row)
            else:
                insert_data.append(data_row)  # New entry for a country

        # Insert new rows into the table
        if insert_data:  # Only execute if there is data to insert
            query = f"""
            INSERT INTO activities_table VALUES ({', '.join(['?'] * (len(all_activities) + 2))})
            """
            conn.executemany(query, insert_data)  # Batch insert
            conn.commit()

    except Exception as e:
        st.error(f"Error saving to database: {e}")
    finally:
        conn.close()

# Button to confirm edits
if st.button("Update Table"):
    # Create and display updated HTML table based on edited DataFrame
    header_html = "<tr><th>Country</th>"
    for activity in all_activities:
        header_html += f"<th>{activity}</th>"
    header_html += "</tr>"

    rows_html = ""
    for _, row in edited_df.iterrows():
        row_html = f"<tr><td>{row['Country']}</td>"
        for activity in all_activities:
            if row[activity]:
                row_html += "<td style='color: green;'>✅</td>"
            else:
                row_html += "<td></td>"
        row_html += "</tr>"
        rows_html += row_html

    table_html = f"""
    <table style='border-collapse: collapse; width: 100%;'>
        <thead style='border-bottom: 2px solid black;'>{header_html}</thead>
        <tbody>{rows_html}</tbody>
    </table>
    """
    st.header("Updated Activities Table")
    st.markdown(table_html, unsafe_allow_html=True)

    # Save edited DataFrame to the database
    save_to_database(edited_df)

# Add description section
st.header("Description")
selected_country = st.selectbox('Select a country', countries)
if selected_country in capitals:
    st.info(f'{capitals[selected_country]} is the capital of {selected_country}.')
