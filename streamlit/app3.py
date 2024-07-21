import streamlit as st
import time

# Create two columns
col1, col2 = st.columns(2)

# Add headers and place the buttons in the first column and the checkboxes in the second
col1.header("MESSAGE")

# List of countries
countries = ['Germany', 'France', 'Italy', 'Spain', 'Portugal', 'Netherlands', 'Belgium', 'Switzerland', 'Brazil', 'Argentina', 'Colombia', 'Chile', 'Peru']

# Loop through the list of countries and create a button for each one
for country in countries:
    if col1.button(country):
        # If a country button is clicked, store the country name in the session state
        st.session_state.country_clicked = country

col2.header("CHECKBOX")
if col2.checkbox('Check me out'):
    # If the checkbox is checked, display a message
    st.write('Look, a checkbox!')

# Add a new section for the description
st.header("DESCRIPTION")

# Loop through the list of countries and create a description button for each one
for country in countries:
    if st.button(f'{country} Description') or ('country_clicked' in st.session_state and st.session_state.country_clicked == country):
        # If a description button is clicked or the country was selected in the previous step, display a message
        st.info(f'{country} is selected.')

# Reset the session state after displaying the description
st.session_state.country_clicked = ''  

# Define the scroll operation as a function and pass in something unique for each
# page load that it needs to re-evaluate where "bottom" is
js = f"""
<script>
    function scroll(dummy_var_to_force_repeat_execution){{
        // Select all 'section.main' elements on the page
        var textAreas = parent.document.querySelectorAll('section.main');
        for (let index = 0; index < textAreas.length; index++) {{
            // Scroll to the bottom of each 'section.main' element
            textAreas[index].scrollTop = textAreas[index].scrollHeight;
        }}
    }}
    // Call the scroll function with the current time in milliseconds as an argument
    scroll({int(time.time() * 1000)})
</script>
"""

# Insert the JavaScript code into the page and set the height of the component to 0 to hide it
st.components.v1.html(js, height=0)