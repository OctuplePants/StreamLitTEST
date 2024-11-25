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

    # Get total number of rows
    total_rows, total_columns = data.shape

    # Option 1: Row range selection
    st.write("### Select Row Range for Analysis")
    start_row = st.number_input(
        "Start Row (0-indexed)", min_value=0, max_value=total_rows - 1, value=0, step=1
    )
    end_row = st.number_input(
        "End Row (0-indexed, inclusive)", min_value=start_row, max_value=total_rows - 1, value=total_rows - 1, step=1
    )
    range_selected_data = data.iloc[start_row : end_row + 1]

    # Option 2: Specific row selection
    st.write("### Or Select Specific Rows for Analysis")
    row_indices = st.multiselect(
        "Select Specific Rows (By Index)",
        options=list(range(total_rows)),
        default=list(range(start_row, end_row + 1))
    )
    specific_rows_data = data.iloc[row_indices]

    # Final filtered data for graphing
    st.write("### Filtered Data Preview")
    filtered_data = specific_rows_data
    st.dataframe(filtered_data)

    # Column selection
    st.write("### Select Columns for Analysis")
    selected_columns = st.multiselect(
        "Select Columns",
        options=data.columns.tolist(),
        default=data.columns.tolist()  # Default to all columns
    )
    filtered_data = filtered_data[selected_columns]

    st.write("### Final Filtered Data Preview (Rows & Columns)")
    st.dataframe(filtered_data)

    # Dropdown for selecting columns for plotting
    x_column = st.selectbox("Select X-axis column", selected_columns)
    y_column = st.selectbox("Select Y-axis column", selected_columns)

    # Dropdown for graph type
    graph_type = st.selectbox(
        "Select Graph Type",
        ["Line", "Scatter", "Bar", "Pie"]
    )

    # Plot button
    if st.button("Plot Graph"):
        fig, ax = plt.subplots()

        if graph_type == "Line":
            ax.plot(filtered_data[x_column], filtered_data[y_column], marker='o')
            ax.set_title(f"{y_column} vs {x_column} (Line Plot)")

        elif graph_type == "Scatter":
            ax.scatter(filtered_data[x_column], filtered_data[y_column])
            ax.set_title(f"{y_column} vs {x_column} (Scatter Plot)")

        elif graph_type == "Bar":
            ax.bar(filtered_data[x_column], filtered_data[y_column])
            ax.set_title(f"{y_column} vs {x_column} (Bar Chart)")

        elif graph_type == "Pie":
            # Pie chart only makes sense for single-column data
            if len(filtered_data[x_column].unique()) <= 10:  # Limit to 10 unique categories for readability
                plt.pie(
                    filtered_data[y_column],
                    labels=filtered_data[x_column],
                    autopct='%1.1f%%',
                    startangle=90,
                )
                plt.title(f"{y_column} (Pie Chart)")
            else:
                st.error("Pie chart requires fewer unique categories in the X-axis.")

        if graph_type != "Pie":
            ax.set_xlabel(x_column)
            ax.set_ylabel(y_column)
            st.pyplot(fig)
        else:
            st.pyplot(plt)

    st.write("Tip: Ensure the selected columns are numeric for meaningful plots.")
else:
    st.info("Please upload a CSV file to get started.")
