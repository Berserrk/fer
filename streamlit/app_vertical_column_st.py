import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

# Sample DataFrame
data = {
    "Entity": [f"entity{i+1}" for i in range(18)],
    "Money Laundering": [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
    "Terrorist Financing": [False, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True],
    "Criminal Organization": [False, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True],
    "Tax evasion": [False, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True],
    "Bribery and corruption": [False, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True],
    "Sanctions evasion": [False, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True],
    "Modern slavery": [False, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True],
    "Drug trafficking": [False, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True],
    "The fraud and money laundering case involved": [False, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True],
    "AMoney Laundering": [False, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True],
    "ATerrorist Financing": [False, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True],
    "ACriminal Organization": [False, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True],
    "ATax evasion": [False, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True],
    "ABribery and corruption": [False, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True],
    "ASanctions evasion": [False, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True],
    "AModern slavery": [False, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True],
    "ADrug trafficking": [False, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True],
    "AThe fraud and money laundering case involved": [False, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True],
}

df = pd.DataFrame(data)

# Add 'Flagged' column based on whether any risk indicator is True
boolean_columns = df.columns.drop("Entity")  # Exclude 'Entity' column from checking
df["Flagged"] = df[boolean_columns].any(axis=1).apply(lambda x: "yes" if x else "no")

# Function to apply checkmarks (based on boolean values)
def apply_checkmarks(df):
    df_styled = df.copy()
    for column in boolean_columns:
        df_styled[column] = df[column].apply(lambda x: '<span style="color: green;">✔️</span>' if x else '<span style="color: red;">❌</span>')
    df_styled["Flagged"] = df["Flagged"].apply(lambda x: '<span style="color: green;">✔️</span>' if x == "yes" else '<span style="color: red;">❌</span>')
    return df_styled

# Function to recalculate the 'Flagged' column after editing
def update_flagged_column(df):
    df["Flagged"] = df[boolean_columns].any(axis=1).apply(lambda x: "yes" if x else "no")
    return df

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

# Ensure 'Entity' and 'Flagged' columns are always included in columns_to_show
if "Entity" not in columns_to_show:
    columns_to_show.insert(0, "Entity")
if "Flagged" not in columns_to_show:
    columns_to_show.append("Flagged")

# Logic to toggle the display based on edit_mode
if st.session_state.edit_mode:
    # Editable DataFrame using st.data_editor
    edited_df = st.data_editor(st.session_state.final_data, key="editor")
    
    # Finish editing button
    if st.button("Finish Editing"):
        # Save the changes
        st.session_state.final_data = edited_df  # Save the edited DataFrame
        st.session_state.final_data = update_flagged_column(st.session_state.final_data)  # Recalculate the 'Flagged' column
        st.session_state.edit_mode = False  # Exit edit mode
else:
    # Apply checkmarks to the final data (after edits)
    styled_df = apply_checkmarks(st.session_state.final_data)

    # Filter the DataFrame based on selected columns
    filtered_df = styled_df[columns_to_show]  # Use the styled DataFrame

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
        /* Add vertical space between header and first row */
        th {{
            padding-bottom: 30px; /* Adjust this value to increase/decrease spacing */
        }}
        th.rotate-header {{
            writing-mode: vertical-rl;
            transform: rotate(189deg);
            vertical-align: bottom;
            text-align: center;
            height: 150px;  /* Adjusted height */
            white-space: normal;  /* Allow text to break into multiple lines */
            word-wrap: break-word; /* Ensure long text breaks */
            max-width: 500px;  /* Adjust this value to control how long text can be before wrapping */
        }}
        th.first-column-header {{
            writing-mode: horizontal-tb; /* Keep the first column header horizontal */
            text-align: left;
            height: 5px;
            max-width: 15px;
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
                    <th class="first-column-header">{filtered_df.columns[0]}</th>
                    {" ".join(f"<th class='rotate-header'>{col}</th>" for col in filtered_df.columns[1:])}
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
