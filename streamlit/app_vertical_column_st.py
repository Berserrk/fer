import streamlit as st
import pandas as pd

# Sample DataFrame
data = {
    "Entity": [f"entity{i+1}" for i in range(18)],
    "Summary": ["summary", "qeqweeeeeeeasdasdasdasdasdasdddddddddasdasdasdasdasdasdasdsadasdasdsadsadadadadadadadadadadadadadadaddadadadadadadadadadadadadadaad", "summary", "summary", "summary", "summary", "summary", "summary", "summary", "summary", "summary", "summary", "summary", "summary", "summary", "summary", "summary", "summary"],
    "Money Laundering": [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
    "Terrorist Financing": [False, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True],
    "Criminal Organization": [False, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True],
    "Tax evasion": [False, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True]
}

col_boolean_list = [
    "Money Laundering",
    "Terrorist Financing",
    "Criminal Organization",
    "Tax evasion"
]

# Create initial DataFrame
df = pd.DataFrame(data)

# Add 'Flagged' column based on whether any risk indicator is True
df["Comments"] = ""  # Initialize with empty strings
boolean_columns = df[col_boolean_list].columns# Exclude 'Entity' column from checking

#Create boolean columns 
df["Flagged"] = df[boolean_columns].any(axis=1).apply(lambda x: "yes" if x else "no")


# Add 'Comments' column for user input
# column_new_order = ["Entity", "Flagged", "Comments"] + col_boolean_list
# # Reorder DataFrame columns
# df = df[column_new_order]

# Function to apply checkmarks (based on boolean values)
def apply_checkmarks(df):
    df_checkmarked_applied = df.copy()
    df_checkmarked_applied = df_checkmarked_applied
    for column in boolean_columns:
        df_checkmarked_applied[column] = df[column].apply(lambda x: '<span style="color: green;">✔️</span>' if x else '<span style="color: red;">❌</span>')
    df_checkmarked_applied["Flagged"] = df["Flagged"].apply(lambda x: '<span style="color: green;">✔️</span>' if x == "yes" else '<span style="color: red;">❌</span>')
    return df_checkmarked_applied



# Function to recalculate the 'Flagged' column after editing
def update_flagged_column(df):
    df["Flagged"] = df[boolean_columns].any(axis=1).apply(lambda x: "yes" if x else "no")
    return df

# Initialize the session state for edit mode and storing data
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False
if "final_data" not in st.session_state:
    st.session_state.final_data = df.copy()# Store the original data

# Non-editable HTML table view (outside of form)
columns_to_show_in_multiselect = st.multiselect(
    "Select columns to display",
    options=st.session_state.final_data.columns,
    default=st.session_state.final_data.columns # Show all columns by default
)


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
    col_boolean_list.append("Flagged")
    styled_df = apply_checkmarks(st.session_state.final_data)
    # Filter the DataFrame based on selected columns
    filtered_df = styled_df[columns_to_show_in_multiselect]  # Use the styled DataFrame
    cols_to_exclude = ["Entity", "Comments", "Flagged"]
    cols_to_keep = [col for col in filtered_df.columns if col not in cols_to_exclude]
    all_cols = list(filtered_df.columns)
    all_cols.remove('Entity')
    all_cols.remove('Comments')
    all_cols.remove('Flagged')
    desired_cols = cols_to_exclude + all_cols
    filtered_df = filtered_df[desired_cols]

# Select all columns except the specified ones
    
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
        /* Custom style for second column (Terrorist Financing) */
        th.second-column-header {{
            writing-mode: horizontal-tb; /* Keep the first column header horizontal */
            text-align: left;
            height: 5px;
            max-width: 15px;
        }}
        /* Custom style for third column (Money Laundering) */
        th.third-column-header {{
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
        /* Freeze the second column */
        td:nth-child(2), th:nth-child(2) {{
        position: sticky;
        left: /* width of first column, e.g. */ 100px;
        background-color: #fff;
        z-index: 1;
        }}
        /* Freeze the third column */
        td:nth-child(3), th:nth-child(3) {{
        position: sticky;
        left:200px;
        background-color: #fff;
        z-index: 1;
        }}
    </style>
    <div class="table-container">
        <table class="custom-table">
            <thead>
                <tr>
                    <th class="first-column-header">{"Entity"}</th>
                    <th class="second-column-header">{"Comments"}</th>
                    <th class="third-column-header">{"Flagged"}</th>
                    {" ".join(f"<th class='rotate-header'>{col}</th>" for col in filtered_df.columns if col not in cols_to_exclude)}
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
                    # for row in filtered_df.loc[:, ~filtered_df.columns.isin(cols_to_exclude)].values 
