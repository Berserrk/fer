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
    "The fraud and money laundering case involved": [10, 11, 12],
}
df = pd.DataFrame(data)

st.markdown(
    """
    <style>
    div[data-baseweb="select"] > div {
        width: 100% !important; /* Make the multiselect wider */
    }
    .spacing {
        margin-top: 20px; /* Adjust the margin for more spacing */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='spacing'></div>", unsafe_allow_html=True)
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
    st.markdown(
        """
        <style>
        div[data-baseweb="select"] > div {
            width: 100% !important; /* Make the multiselect wider */
        }
        .spacing {
            margin-top: 20px; /* Adjust the margin for more spacing */
        }
        .header-row {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-bottom: 15px;
        }
        .header-row div {
            writing-mode: vertical-rl;
            transform: rotate(180deg);
            font-size: 10px; /* Smaller font size */
            font-weight: normal; /* Remove bold styling */
            text-align: center;
            color: #333;  /* Adjust color as needed */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    columns_to_show = st.multiselect(
        "Select columns to display",
        options=st.session_state.final_data.columns,
        default=st.session_state.final_data.columns  # Show all columns by default
    )
    # Add space between the multiselect and the table
    st.write("")  # Adds a blank line (can add more if needed)
    st.write("")  # Adds a blank line (can add more if needed)
    st.write("")  # Adds a blank line (can add more if needed)
    st.write("")  # Adds a blank line (can add more if needed)
    st.markdown("<div class='spacing'></div>", unsafe_allow_html=True)

    
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
            border: none;  /* Removed border for column names */
            vertical-align: bottom;
            text-align: center;
            height: 150px;  /* Adjusted height */
            white-space: normal;  /* Allow text to break into multiple lines */
            word-wrap: break-word; /* Ensure long text breaks */
            max-width: 500px;  /* Adjust this value to control how long text can be before wrapping */
            font-size: 10px;  /* Smaller font size */
            background-color: transparent;  /* Remove background */
        }}
        td {{
            border: 1px solid #dddddd;
            padding: 5px;
            text-align: center;
            font-size: 12px;  /* Consistent font size with headers */
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
