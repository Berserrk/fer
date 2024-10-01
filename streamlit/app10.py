import streamlit as st
import json
import pandas as pd
import duckdb
from pandas import Timestamp

# Load the countries JSON file
with open('countries.json', 'r') as f:
    country_status = json.load(f)
with open('categories_label.json', 'r') as f:
    categories_label = json.load(f)
with open('dict_response_full_text.json', 'r') as f:
    capitals = json.load(f)

# List of countries
countries = list(country_status.keys())

# Extract the list of all activities
all_activities = set()
for country_info in categories_label.values():
    all_activities.update(country_info["activities"])
all_activities = sorted(all_activities)

# Create an empty DataFrame with countries as rows and activities as columns
data = {"Country": []}
for activity in all_activities:
    data[activity] = []

# Populate the DataFrame with existing data
for country, info in categories_label.items():
    row = {activity: True if activity in info["activities"] else False for activity in all_activities}
    row["Country"] = country
    data["Country"].append(country)
    for activity in all_activities:
        data[activity].append(row[activity])

df = pd.DataFrame(data)

# Display the editable table using st.data_editor
st.header("Activities Table (Editable)")
edited_df = st.data_editor(df, use_container_width=True, num_rows="fixed")

# Function to save changes to DuckDB
def save_to_database(df):
    try:
        # Connect to the DuckDB database (or create it if it doesn't exist)
        conn = duckdb.connect('activities.db')

        # Create the activities_table if it doesn't exist using BOOLEAN instead of INTEGER
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS activities_table (
            Country VARCHAR,
            {},
            timestamp TIMESTAMP,
            PRIMARY KEY (Country, timestamp)
        )
        '''.format(", ".join([f'"{activity}" BOOLEAN' for activity in all_activities]))

        # Print the CREATE TABLE statement for debugging
        print(f"Executing: {create_table_query}")
        conn.execute(create_table_query)
        print(f"Executing2: {create_table_query}")

        # Prepare a list of tuples for inserting data
        insert_data = []
        for _, row in df.iterrows():
            country = row["Country"].replace("'", "''")  # Escape single quotes
            activities = tuple(bool(row[activity]) for activity in all_activities)  # Convert activities to booleans
            current_timestamp = pd.Timestamp.now()  # Get current timestamp

            # Prepare the data to insert: include country, activities, and timestamp
            data_row = (country,) + activities + (current_timestamp,)
            
            # Check if the last entry for this country is different
            query = f'SELECT * FROM activities_table WHERE Country = ? ORDER BY timestamp DESC LIMIT 1'
            last_entry = conn.execute(query, (country,)).fetchone()

            # Check if the last entry exists and if there is a change
            if last_entry:
                # Compare activities to see if there's a change
                if last_entry[1:-1] != activities:  # Exclude Country and timestamp for comparison
                    insert_data.append(data_row)
            else:
                # If no previous entry, add the current data
                insert_data.append(data_row)

        # Use parameterized query to insert new rows in the table
        query = f"""
        INSERT INTO activities_table VALUES ({', '.join(['?'] * (len(all_activities) + 2))})
        """

        # Print the INSERT statement for debugging
        print(f"Executing HERE HERE: {query} with data: {insert_data}")
        conn.executemany(query, insert_data)  # Use executemany for batch inserts

        # Commit the changes
        conn.commit()

    except Exception as e:
        st.error(f"Error saving to database: {e}")
    finally:
        # Close the connection
        conn.close()

# Add a button to confirm edits
if st.button("Update Table"):
    # Create an updated HTML table based on the edited DataFrame
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

    # Combine header and rows into a complete table
    table_html = f"""
    <table style='border-collapse: collapse; width: 100%;'>
        <thead style='border-bottom: 2px solid black;'>{header_html}</thead>
        <tbody>{rows_html}</tbody>
    </table>
    """

    # Display the updated table
    st.header("Updated Activities Table")
    st.markdown(table_html, unsafe_allow_html=True)

    # Save edited DataFrame to the database
    save_to_database(edited_df)

# Add a new section for the description
st.header("Description")

# Create a selectbox for the list of countries
selected_country = st.selectbox('Select a country', countries)

# Display the description of the selected country
if selected_country in capitals:
    st.info(f'{capitals[selected_country]} is the capital of {selected_country}.')