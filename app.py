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
    st.dataframe(df)

    # Generate interactive filterable views for categorical columns
    st.header("Filter Data")
    for column in df.select_dtypes(include=['object']).columns:
        unique_vals = df[column].dropna().unique()
        selected_vals = st.multiselect(f"Filter by {column}", unique_vals, default=unique_vals)
        if selected_vals:
            df = df[df[column].isin(selected_vals)]
    
    # Display the filtered dataframe
    st.subheader("Filtered Data")
    st.dataframe(df)

# Function to detect delimiter
def detect_delimiter(file):
    sample = file.read(2048).decode('utf-8')
    file.seek(0)
    delimiters = [',', ';', '\t', '|']
    for delimiter in delimiters:
        if delimiter in sample:
            return delimiter
    return ','  # default to comma if no delimiter is found

# Function to read CSV with detected delimiter
def read_csv(file):
    delimiter = detect_delimiter(file)
    try:
        df = pd.read_csv(file, delimiter=delimiter)
        return df, delimiter
    except pd.errors.ParserError:
        return None, None

# Function to summarize the CSV file
def summarize_csv(df):
    summary = {}

    # Basic statistics
    summary['basic_stats'] = df.describe(include='all')

    # Unique values and their counts
    unique_counts = {col: df[col].nunique() for col in df.columns}
    summary['unique_counts'] = unique_counts

    # Identify columns with missing values
    missing_values = df.isnull().sum().to_dict()
    summary['missing_values'] = missing_values

    # Column data types
    dtypes = df.dtypes.apply(lambda x: x.name).to_dict()  # Convert to string for display
    summary['dtypes'] = dtypes

    return summary

# Streamlit app layout
st.sidebar.title("Upload CSV File")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df, delimiter = read_csv(uploaded_file)
    
    if df is not None:
        st.success(f"File successfully read with delimiter '{delimiter}'")
        
        # Show the first few rows for debugging
        st.write(df.head())

        # Generate the report
        generate_report(df)

        # Summarize the CSV file
        st.header("CSV File Summary")
        summary = summarize_csv(df)

        # Display summary details in a readable format
        st.subheader("Basic Statistics")
        st.write(summary['basic_stats'])

        st.subheader("Unique Counts")
        unique_counts_df = pd.DataFrame.from_dict(summary['unique_counts'], orient='index', columns=['Unique Count'])
        st.write(unique_counts_df)

        st.subheader("Missing Values")
        missing_values_df = pd.DataFrame.from_dict(summary['missing_values'], orient='index', columns=['Missing Values'])
        st.write(missing_values_df)

        st.subheader("Column Data Types")
        dtypes_df = pd.DataFrame.from_dict(summary['dtypes'], orient='index', columns=['Data Type'])
        st.write(dtypes_df)

    else:
        st.error("The file could not be parsed. Please ensure it is a valid CSV file.")
else:
    st.write("Please upload a CSV file to get started.")
