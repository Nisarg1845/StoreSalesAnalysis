import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit UI
st.title("Store Product Sales Analysis")
st.write("Upload your sales data in CSV format to analyze which products are performing the best.")

# File Upload
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv","xlsx"])

if uploaded_file is not None:
    # Step 1: Load the Dataset
    try:
        data = pd.read_csv(uploaded_file,encoding="latin1")
        st.write("Data Preview:")
        st.dataframe(data)

        # Step 2: User Input to Identify Columns
        st.subheader("Select Relevant Columns")
        product_column = st.selectbox("Select the Product Column", data.columns)
        sales_column = st.selectbox("Select the Sales Column", data.select_dtypes(include='number').columns)

        # Step 3: Aggregate Sales Data by Product
        st.subheader("Product Sales Summary")
        sales_summary = data.groupby(product_column)[sales_column].sum().reset_index()
        sales_summary = sales_summary.sort_values(by=sales_column, ascending=False)
        st.write(sales_summary)

        # Step 4: Highlight Best and Worst Performing Products
        max_sale_product = sales_summary.iloc[0]
        min_sale_product = sales_summary.iloc[-1]

        st.write(f"### Product with Maximum Sales: *{max_sale_product[product_column]}*")
        st.write(f"Sales: {max_sale_product[sales_column]}")

        st.write(f"### Product with Minimum Sales: *{min_sale_product[product_column]}*")
        st.write(f"Sales: {min_sale_product[sales_column]}")

        # Step 5: Visualization
        st.subheader("Sales Distribution by Product")
        plt.figure(figsize=(12, 6))
        plt.bar(sales_summary[product_column], sales_summary[sales_column], color="skyblue")
        plt.xlabel("Products")
        plt.ylabel("Total Sales")
        plt.title("Total Sales by Product")
        plt.xticks(rotation=45)
        st.pyplot(plt)

    except Exception as e:
        st.error(f"An error occurred: {e}")