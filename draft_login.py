import streamlit as st
import pandas as pd

def initialize_data():
    """Initialize the session state if it doesn't exist"""
    if 'data' not in st.session_state:
        st.session_state.data = pd.DataFrame(columns=['entity', 'money laundering', 'fraud', 'summary'])

def add_data(entity, money_laundering, fraud, summary):
    """Add a new row to the dataframe"""
    new_data = pd.DataFrame({
        'entity': [entity],
        'money laundering': [money_laundering],
        'fraud': [fraud],
        'summary': [summary]
    })
    st.session_state.data = pd.concat([st.session_state.data, new_data], ignore_index=True)

def main():
    st.title("Data Entry Form")
    
    # Initialize the data
    initialize_data()
    
    # Create the input form
    with st.form("data_entry_form"):
        # Text input for entity
        entity = st.text_input("Entity Name")
        
        # Checkboxes for money laundering and fraud
        col1, col2 = st.columns(2)
        with col1:
            money_laundering = st.checkbox("Money Laundering")
        with col2:
            fraud = st.checkbox("Fraud")
            
        # Text area for summary
        summary = st.text_area("Summary", height=100, 
                            help="Enter any additional details or notes about this entity")
        
        # Submit button
        submitted = st.form_submit_button("Add Entry")
        
        if submitted:
            if entity.strip():  # Check if entity is not empty
                add_data(entity, money_laundering, fraud, summary)
                st.success("Data added successfully!")
            else:
                st.error("Please enter an entity name")
    
    # Display the current data
    st.subheader("Current Data")
    
    # Configure the display of the dataframe
    # Use a style formatter to wrap text in the summary column
    if not st.session_state.data.empty:
        st.dataframe(
            st.session_state.data,
            column_config={
                "summary": st.column_config.TextColumn(
                    "Summary",
                    width="medium",
                    help="Entity summary and additional notes"
                )
            }
        )
    
    # Add download button
    if not st.session_state.data.empty:
        csv = st.session_state.data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name="data.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()