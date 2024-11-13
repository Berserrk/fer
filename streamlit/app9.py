import streamlit as st
import time
import json

# Load the countries JSON file
with open('countries.json', 'r') as f:
    country_status = json.load(f)
with open('categories_label.json', 'r') as f:
    categories_label = json.load(f)

# Load the capitals JSON file
with open('dict_response_full_text.json', 'r') as f:
    capitals = json.load(f)

# Create a row for the headers
header_cols = st.columns(2)
header_cols[0].header("COUNTRY")
header_cols[1].header("FLAG")

# List of countries
countries = list(country_status.keys())

# Loop through the list of countries and create a button and a checkbox for each one
for country in countries:
    cols = st.columns(2)
    if cols[0].button(country):
        # If a country button is clicked, store the country name in the session state
        st.session_state.country_clicked = country

    if country_status[country][0] == 'yes':
        checkbox_label = " ✅"
        cols[1].markdown(checkbox_label)
# Add a new section for the description

st.header("DESCRIPTION")

# Create a selectbox for the list of countries
selected_country = st.selectbox('Select a country', countries)

# Display the description of the selected country
if selected_country in capitals:
    st.info(f'{capitals[selected_country]} is the capital of {selected_country}.')

# Define the scroll operation as a function and pass in something unique for each
# page load that it needs to re-evaluate where "bottom" is
js = f"""
<script>
    function scroll(dummy_var_to_force_repeat_execution){{
        setTimeout(function(){{
            // Select all 'section.main' elements on the page
            var textAreas = parent.document.querySelectorAll('section.main');
            for (let index = 0; index < textAreas.length; index++) {{
                // Scroll to the bottom of each 'section.main' element
                textAreas[index].scrollTop = textAreas[index].scrollHeight;
            }}
        }}, 1000);  // Delay of 1 second
    }}
    // Call the scroll function with the current time in milliseconds as an argument
    scroll({int(time.time() * 1000)})
</script>
"""

# Insert the JavaScript code into the page and set the height of the component to 0 to hide it
st.components.v1.html(js, height=0)