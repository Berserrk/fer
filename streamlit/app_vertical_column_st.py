import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

# Sample DataFrame
data = {
    "Money Laundering": [True, False, True],
    "Terrorist Financing": [True, False, True],
    "Criminal Organization": [True, False, True],
    "Tax evasion": [True, False, True],
    "Bribery and corruption": [True, False, True],
    "Sanctions evasion": [True, False, True],
    "Modern slavery": [True, False, True],
    "Drug trafficking": [True, False, True],
    "The fraud and money laundering case involved": [True, False, True],
    "AMoney Laundering": [True, False, True],
    "ATerrorist Financing": [True, False, True],
    "ACriminal Organization": [True, False, True],
    "ATax evasion": [True, False, True],
    "ABribery and corruption": [True, False, True],
    "ASanctions evasion": [True, False, True],
    "AModern slavery": [True, False, True],
    "ADrug trafficking": [True, False, True],
    "AThe fraud and money laundering case involved": [True, False, True],
}

df = pd.DataFrame(data)

# Style for the checkmark and cross symbols
green_checkmark = '<span style="color: green;">✔️</span>'
red_cross = '<span style="color: red;">❌</span>'

# Replace True with a green checkmark and False with a red cross
df_styled = df.applymap(lambda x: green_checkmark if x else red_cross)

# Initialize the session state for edit mode and storing data
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False
if "final_data" not in st.session_state:
    st.session_state.final_data = df.copy()  # Store the original data

# Non-editable HTML table view (outside of form)
columns_to_show = st.multiselect(
    "Select columns to display",
    options=st.session_state.final_data.columns,
    default=st.session_state.final_data.columns  # Show all columns by default
)

if len(columns_to_show) == 0:
    # Default to all columns if none selected
    columns_to_show = st.session_state.final_data.columns

# Logic to toggle the display based on edit_mode
if st.session_state.edit_mode:
    # Editable DataFrame using st.data_editor
    st.session_state.edited_df = st.data_editor(st.session_state.final_data, key="editor")
    
    # Finish editing button
    if st.button("Finish Editing"):
        st.session_state.edit_mode = False
        st.session_state.final_data = st.session_state.edited_df  # Save the changes
else:
    # Filter the DataFrame based on selected columns
    filtered_df = df_styled[columns_to_show]

    # Generate HTML table with refined CSS for rotated headers and scrollbars
    html_table = f"""
    <style>
        .table-container {{
            width: 100%;
            height: 600px; /* Ensure a fixed height for the container */
            overflow-x: auto;  /* Always show horizontal scrollbar */
            overflow-y: auto;  /* Always show vertical scrollbar */
        }}
        table.custom-table {{
            border-collapse: collapse;
            width: 100%;  /* Set table width to 100% */
            table-layout: auto; /* Allow table to automatically adjust column widths */
        }}
        th, td {{
            min-width: 150px; /* Adjust the minimum column width as needed */
            padding: 12px;  /* Increased padding for better visibility */
            font-size: 14px;  /* Increased font size */
        }}
        th {{
            writing-mode: vertical-rl;
            transform: rotate(189deg);
            border: none;  /* Removed border for column names */
            vertical-align: bottom;
            text-align: center;
            height: 150px;  /* Adjusted height */
            white-space: normal;  /* Allow text to break into multiple lines */
            word-wrap: break-word; /* Ensure long text breaks */
            max-width: 500px;  /* Adjust this value to control how long text can be before wrapping */
            font-size: 14px;  /* Increased font size for better visibility */
            background-color: transparent;  /* Remove background */
        }}
        td {{
            border: 1px solid #dddddd;
            text-align: center;
            font-size: 14px;  /* Increased font size for better visibility */
        }}
        /* Freeze the first column */
        td:first-child, th:first-child {{
            position: sticky;
            left: 0;
            background-color: #fff;
            z-index: 1; /* Ensure it appears above other cells when scrolling */
        }}
    </style>
    <div class="table-container">
        <table class="custom-table">
            <thead>
                <tr>
                    {" ".join(f"<th>{col}</th>" for col in filtered_df.columns)}
                </tr>
            </thead>
            <tbody>
                {" ".join(
                    f"<tr>{''.join(f'<td>{cell}</td>' for cell in row)}</tr>"
                    for row in filtered_df.values
                )}
            </tbody>
        </table>
    </div>
    """

    # Display the custom HTML table with vertical headers and scrollbars in Streamlit
    st.markdown(html_table, unsafe_allow_html=True)
    
    # Edit table button
    if st.button("Edit Table"):
        st.session_state.edit_mode = True

# Configure grid options to freeze a specific column (if needed)
gb = GridOptionsBuilder.from_dataframe(df_styled)
gb.configure_default_column(groupable=True, editable=True)
gb.configure_column("Money Laundering", pinned='left')  # Freeze the 'Money Laundering' column
grid_options = gb.build()

# Display AgGrid with frozen column (if needed)
# response = AgGrid(df_styled, gridOptions=grid_options, allow_unsafe_jscode=True)
