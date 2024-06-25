import streamlit as st
import pandas as pd
from io import StringIO

# Function to generate a reporting view
def generate_report(df):
    st.title("Dynamic Data Reporting View")

    # Display basic information about the dataframe
    st.header("Basic Information")
    buffer = StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()
    st.text(info_str)
    
    # Display basic statistics
    st.header("Basic Statistics")
    st.write(df.describe(include='all'))
    
    # Display the first few rows of the dataframe
    st.header("First Few Rows")
    st.write(df.head())
    
    # Display entire dataframe with filtering options
    st.header("Data Table")
    st.write(df)

    # Generate interactive filterable views for categorical columns
    st.header("Filter Data")
    for column in df.select_dtypes(include=['object']).columns:
        unique_vals = df[column].dropna().unique()
        selected_vals = st.multiselect(f"Filter by {column}", unique_vals, default=unique_vals)
        if selected_vals:
            df = df[df[column].isin(selected_vals)]
    
    # Display the filtered dataframe
    st.subheader("Filtered Data")
    st.write(df)

# Streamlit app layout
st.sidebar.title("Upload CSV File")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the uploaded CSV file
    df = pd.read_csv(uploaded_file)
    
    # Generate the report
    generate_report(df)
else:
    st.write("Please upload a CSV file to get started.")
