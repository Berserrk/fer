import streamlit as st
import pandas as pd

# Sample DataFrame
data = {
    "Money Laundering": [13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
    "Terrorist Financing": [13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
    "Criminal Organization": [13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
    "Tax evasion": [13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
    "Bribery and corruption": [13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
    "Sanctions evasion": [13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
    "Modern slavery": [13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
    "Drug trafficking": [13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
    "The fraud and money laundering case involved": [13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
    "AMoney Laundering": [13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
    "ATerrorist Financing": [13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
    "ACriminal Organization": [13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
    "ATax evasion": [13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
    "ABribery and corruption": [13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
    "ASanctions evasion": [13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
    "AModern slavery": [13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
    "ADrug trafficking": [13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
    "AThe fraud and money laundering case involved": [13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
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
        filtered_df = st.session_state.final_data[columns_to_show]

        # Generate HTML table with refined CSS for rotated headers and scrollbars
        html_table = f"""
        <style>
            .table-container {{
                width: 100%;
                max-height: 400px;
                overflow-x: scroll;  /* Always show horizontal scrollbar */
                overflow-y: scroll;  /* Always show vertical scrollbar */
            }}
            table.custom-table {{
                border-collapse: collapse;
                width: max-content;
                min-width: 100%;
            }}
            th, td {{
                min-width: 150px; /* Adjust the minimum column width as needed */
                padding: 8px;
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
                text-align: center;
                font-size: 12px;  /* Consistent font size with headers */
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
