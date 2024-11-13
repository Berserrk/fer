import streamlit as st
import pandas as pd

# Sample DataFrame
data = {
    "column_1": [1, 2, 3],
    "column_2": [4, 5, 6],
    "column_3": [7, 8, 9],
    "column_4": [10, 11, 12],
    "column_5": [10, 11, 12],
    "column_6": [10, 11, 12],
    "column_7": [10, 11, 12],
    "column_8": [10, 11, 12],
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

# Multiselect for choosing columns to display
columns_to_show = st.multiselect(
    "Select columns to display",
    options=df.columns,
    default=df.columns  # Show all columns by default
)

# Filter the DataFrame based on selected columns
filtered_df = df[columns_to_show]

# Generate HTML table with refined CSS for rotated headers
html_table = f"""
<style>
    table.custom-table {{
        border-collapse: collapse;
        width: 100%;
    }}
    th {{
        writing-mode: vertical-rl;
        transform: rotate(195deg);
        padding: 5px;
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
