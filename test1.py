import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the app
st.title("CSV Data Visualization App")

# File uploader for CSV
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:
    # Read the CSV file
    data = pd.read_csv(uploaded_file)
    st.write("### Data Preview")
    st.dataframe(data)

    # Get total number of rows and columns
    total_rows, total_columns = data.shape

    # Row range selection
    st.write("### Select Row Range for Filtering")
    start_row = st.number_input(
        "Start Row (0-indexed)", min_value=0, max_value=total_rows - 1, value=0, step=1
    )
    end_row = st.number_input(
        "End Row (0-indexed, inclusive)", min_value=start_row, max_value=total_rows - 1, value=total_rows - 1, step=1
    )
    range_filtered_data = data.iloc[start_row : end_row + 1]

    # Column range selection
    st.write("### Select Column Range for Filtering")
    start_col = st.number_input(
        "Start Column (0-indexed)", min_value=0, max_value=total_columns - 1, value=0, step=1
    )
    end_col = st.number_input(
        "End Column (0-indexed, inclusive)", min_value=start_col, max_value=total_columns - 1, value=total_columns - 1, step=1
    )
    range_filtered_data = range_filtered_data.iloc[:, start_col : end_col + 1]

    st.write("### Filtered Data Preview (Rows & Columns)")
    st.dataframe(range_filtered_data)

    # Row selection for X and Y axes
    st.write("### Select Specific Rows for X and Y Axes")
    x_row = st.selectbox("Select X-axis row", options=range_filtered_data.index)
    y_row = st.selectbox("Select Y-axis row", options=range_filtered_data.index)

    # Column selection for X and Y axes
    st.write("### Select Columns for X and Y Axes")
    x_column = st.selectbox("Select X-axis column", options=range_filtered_data.columns)
    y_column = st.selectbox("Select Y-axis column", options=range_filtered_data.columns)

    # Prepare data for plotting
    x_data = range_filtered_data.loc[x_row, x_column]
    y_data = range_filtered_data.loc[y_row, y_column]

    # Dropdown for graph type
    graph_type = st.selectbox(
        "Select Graph Type",
        ["Line", "Scatter", "Bar"]
    )

    # Plot button
    if st.button("Plot Graph"):
        fig, ax = plt.subplots()

        if graph_type == "Line":
            ax.plot([x_data], [y_data], marker='o')
            ax.set_title(f"Data Point: ({x_column}[{x_row}] vs {y_column}[{y_row}]) (Line Plot)")

        elif graph_type == "Scatter":
            ax.scatter([x_data], [y_data])
            ax.set_title(f"Data Point: ({x_column}[{x_row}] vs {y_column}[{y_row}]) (Scatter Plot)")

        elif graph_type == "Bar":
            ax.bar([x_data], [y_data])
            ax.set_title(f"Data Point: ({x_column}[{x_row}] vs {y_column}[{y_row}]) (Bar Chart)")

        ax.set_xlabel(f"{x_column}[Row: {x_row}]")
        ax.set_ylabel(f"{y_column}[Row: {y_row}]")
        st.pyplot(fig)

    st.write("Tip: Ensure the selected data points are numeric for meaningful plots.")
else:
    st.info("Please upload a CSV file to get started.")

