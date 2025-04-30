import streamlit as st
import pandas as pd

# Sample DataFrame
data = {
    "Entity": [f"entity{i+1}" for i in range(18)],
    "Summary": ["summary"] * 18,
    "Money Laundering": [False] * 18,
    "Terrorist Financing": [False, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True],
    "Criminal Organization": [False, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True],
    "Tax evasion": [False, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True],
}

col_boolean_list = [
    "Money Laundering",
    "Terrorist Financing",
    "Criminal Organization",
    "Tax evasion",
]

# Initialize session state if not exists
if "df" not in st.session_state:
    # Create initial DataFrame
    df = pd.DataFrame(data)
    df["Comments"] = ""
    df["Flagged"] = df[col_boolean_list].any(axis=1).apply(lambda x: "yes" if x else "no")
    st.session_state.df = df

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

# Function to apply checkmarks
def apply_checkmarks(df):
    df_checkmarked_applied = df.copy()
    for column in col_boolean_list:
        df_checkmarked_applied[column] = df[column].apply(
            lambda x: '<span style="color: green;">✔️</span>' if x else '<span style="color: red;">❌</span>'
        )
    df_checkmarked_applied["Flagged"] = df["Flagged"].apply(
        lambda x: '<span style="color: green;">✔️</span>' if x == "yes" else '<span style="color: red;">❌</span>'
    )
    return df_checkmarked_applied

# Display section
st.markdown("### Entity Table")

# Column selection
columns_to_show = st.multiselect(
    "Select columns to display",
    options=st.session_state.df.columns,
    default=st.session_state.df.columns,
)

if st.session_state.edit_mode:
    # Show the editable table
    edited_df = st.data_editor(
        st.session_state.df[columns_to_show],
        num_rows="dynamic",
        use_container_width=True
    )
    
    # Apply changes when the user finishes editing
    if st.button("Finish Editing"):
        # Update the session state DataFrame with edited values
        st.session_state.df.update(edited_df)
        st.session_state.df["Flagged"] = st.session_state.df[col_boolean_list].any(axis=1).apply(lambda x: "yes" if x else "no")
        st.session_state.edit_mode = False
else:
    # Display the styled static table
    styled_df = apply_checkmarks(st.session_state.df)
    filtered_df = styled_df[columns_to_show]
    st.markdown(
        filtered_df.to_html(escape=False, index=False),
        unsafe_allow_html=True,
    )
    if st.button("Edit Table"):
        st.session_state.edit_mode = True

# Add new entity section
st.markdown("### Add New Entity")

# Create a form for adding new entities
with st.form("add_entity_form"):
    new_entity = st.text_input("Entity Name")
    new_summary = st.text_area("Summary")
    
    col1, col2 = st.columns(2)
    new_flags = {
        "Money Laundering": col1.checkbox("Money Laundering"),
        "Terrorist Financing": col1.checkbox("Terrorist Financing"),
        "Criminal Organization": col2.checkbox("Criminal Organization"),
        "Tax evasion": col2.checkbox("Tax evasion"),
    }
    new_comments = st.text_area("Comments")
    submitted = st.form_submit_button("Add Entity")
    
    if submitted:
        if new_entity:
            new_row = {
                "Entity": new_entity,
                "Summary": new_summary,
                **new_flags,
                "Comments": new_comments,
                "Flagged": "yes" if any(new_flags.values()) else "no",
            }
            st.session_state.df = pd.concat(
                [st.session_state.df, pd.DataFrame([new_row])],
                ignore_index=True,
            )
            st.success(f"Entity '{new_entity}' added successfully!")
            st.experimental_set_query_params(refresh="true")  # Trigger a refresh
        else:
            st.error("Please provide an entity name.")
