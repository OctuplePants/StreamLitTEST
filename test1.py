import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the app
st.title("Flexible Data Selection App")

# File uploader for CSV
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:
    # Read the CSV file
    data = pd.read_csv(uploaded_file)
    st.write("### Data Preview")
    st.dataframe(data)

    total_rows, total_columns = data.shape

    # Initialize variables to store selected data
    x_data = None
    y_data = None

    # Checkbox and dropdown for X-axis row
    use_x_row = st.checkbox("Select X-axis row")
    x_row = None
    if use_x_row:
        x_row = st.selectbox("Select X-axis row", options=data.index)

    # Checkbox and dropdown for X-axis column
    use_x_column = st.checkbox("Select X-axis column")
    x_column = None
    if use_x_column:
        x_column = st.selectbox("Select X-axis column", options=data.columns)

    # Checkbox and dropdown for Y-axis row
    use_y_row = st.checkbox("Select Y-axis row")
    y_row = None
    if use_y_row:
        y_row = st.selectbox("Select Y-axis row", options=data.index)

    # Checkbox and dropdown for Y-axis column
    use_y_column = st.checkbox("Select Y-axis column")
    y_column = None
    if use_y_column:
        y_column = st.selectbox("Select Y-axis column", options=data.columns)

    # Ensure only one X and one Y selection is made
    if sum([use_x_row, use_x_column]) != 1 or sum([use_y_row, use_y_column]) != 1:
        st.error("Please select exactly one option for the X-axis and one option for the Y-axis.")
    else:
        # Extract X-axis data
        if use_x_row:
            x_data = data.iloc[x_row, :].values  # Entire row as X
            x_label = f"Row {x_row}"
        elif use_x_column:
            x_data = data[x_column].values  # Entire column as X
            x_label = f"Column '{x_column}'"

        # Extract Y-axis data
        if use_y_row:
            y_data = data.iloc[y_row, :].values  # Entire row as Y
            y_label = f"Row {y_row}"
        elif use_y_column:
            y_data = data[y_column].values  # Entire column as Y
            y_label = f"Column '{y_column}'"

        # Plot the graph
        if st.button("Plot Graph"):
            fig, ax = plt.subplots()
            ax.scatter(x_data, y_data, color='blue', label="Data Points")
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
            ax.set_title(f"Scatter Plot: {x_label} vs {y_label}")
            ax.legend()
            st.pyplot(fig)

else:
    st.info("Please upload a CSV file to get started.")
