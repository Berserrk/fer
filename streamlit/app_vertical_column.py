import streamlit as st
import pandas as pd

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

# Display the editable or static view based on the edit mode
with st.form("main_form"):
    if st.session_state.edit_mode:
        # Editable DataFrame using st.data_editor
        st.session_state.edited_df = st.data_editor(st.session_state.final_data, key="editor")
        if st.form_submit_button("Finish Editing"):
            st.session_state.edit_mode = False
            st.session_state.final_data = st.session_state.edited_df  # Save the changes
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
        
        if st.form_submit_button("Edit Table"):
            st.session_state.edit_mode = True
            st.session_state.edited_df = st.session_state.final_data.copy()  # Store a copy for editing
