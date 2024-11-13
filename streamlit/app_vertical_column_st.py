import streamlit as st
import pandas as pd

# Sample DataFrame
data = {
    "Money Laundering": [1, 2, 3],
    "Terrorist Financing": [4, 5, 6],
    "Criminal Organization": [7, 8, 9],
    "Tax evasion": [10, 11, 12],
    "Bribery and corruption": [10, 11, 12],
    "Sanctions evasion": [10, 11, 12],
    "Modern slavery": [10, 11, 12],
    "Drug trafficking": [10, 11, 12],
    "column_9": [10, 11, 12],
    "column_10": [10, 11, 12],
    "column_11": [10, 11, 12],
    "column_12": [10, 11, 12],
    "column_13": [10, 11, 12],
    "column_14": [10, 11, 12],
    "column_15": [10, 11, 12],
    "column_16": [10, 11, 12],
    "column_17": [10, 11, 12],
    "column_18": [10, 11, 12],
    "column_19": [10, 11, 12],
    "column_20": [10, 11, 12],
    "column_21": [10, 11, 12],
    "column_22": [10, 11, 12],
    "column_23": [10, 11, 12],
    "column_24": [10, 11, 12],
    "column_25": [10, 11, 12],
    "column_26": [10, 11, 12],
    "column_27": [10, 11, 12],
}
df = pd.DataFrame(data)

# Initialize the session state for edit mode and storing data
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False
if "final_data" not in st.session_state:
    st.session_state.final_data = df.copy()  # Store the original data

# Toggle edit mode based on button clicks
if st.session_state.edit_mode:
    if st.button("Finish Editing"):
        st.session_state.edit_mode = False
else:
    if st.button("Edit Table"):
        st.session_state.edit_mode = True

# Display the editable or static view based on the edit mode
if st.session_state.edit_mode:
    # Editable DataFrame using st.data_editor
    edited_df = st.data_editor(st.session_state.final_data, key="editor")
    
    # Update the stored final data with edited values on finishing edit mode
    st.session_state.final_data = edited_df
else:
    # Non-editable HTML table view
    # Multiselect for choosing columns to display
    columns_to_show = st.multiselect(
        "Select columns to display",
        options=st.session_state.final_data.columns,
        default=st.session_state.final_data.columns  # Show all columns by default
    )
    
    # Filter the DataFrame based on selected columns
    filtered_df = st.session_state.final_data[columns_to_show]
    
    # Generate HTML table with refined CSS for rotated headers
    html_table = f"""
    <style>
        table.custom-table {{
            border-collapse: collapse;
            width: 100%;
        }}
        th {{
            writing-mode: vertical-rl;
            transform: rotate(189deg);
            # padding: 5px;
            border: 1px solid #dddddd;
            vertical-align: bottom;
            text-align: center;
            height: 80px;  /* Adjusted height */
            white-space: nowrap;
            font-size: 14px;  /* Smaller font size */
        }}
        td {{
            border: 1px solid #dddddd;
            padding: 5px;
            text-align: center;
            font-size: 14px;  /* Consistent font size with headers */
        }}
    </style>
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
    """
    
    # Display the custom HTML table with vertical headers in Streamlit
    st.markdown(html_table, unsafe_allow_html=True)
