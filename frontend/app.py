import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:5000"

# Set the title of the Streamlit app
st.title("SuperKart Sales Forecast Prediction")

# Section for online prediction
st.subheader("Online Prediction")

# Collect user input for sales features
Product_Id = st.text_input("Enter ProductId")
Product_Weight = st.number_input("Product Weight", min_value=4, max_value=22, value=4)
Product_Sugar_Content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar", "reg"])
Product_Allocated_Area = st.number_input("Product Allocated Area", min_value=0.004, max_value=0.298, value=0.004)
Product_Type = st.selectbox("Enter Product Type", ["Baking Goods", "Breads", "Breakfast", "Canned", "Dairy", "Frozen Foods", "Fruits and Vegetables", "Hard Drinks", "Health and Hygiene", "Household", "Meat", "Others", "Seafood", "Snack Foods", "Soft Drinks", "Starchy Foods"])
Product_MRP = st.number_input("Product MRP", min_value=31.00, max_value=266.00, value=50.00)
Store_Id = st.selectbox("Store Id", ["OUT001", "OUT002", "OUT003", "OUT004"])
Store_Establishment_Year = st.selectbox("Store Establishment Year", ["1987", "1998", "1999", "2009"])
Store_Size = st.selectbox("Store Size", ["High", "Medium", "Small"])
Store_Location_City_Type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
Store_Type = st.selectbox("Store Type", ["Departmental Store", "Food Mart", "Supermarket Type1", "Supermarket Type2"])
Product_Store_Sales_Total = st.number_input("Product Store Sales Total", min_value=33.00, max_value=8000.00, value=50.00)

# Convert user input into a DataFrame
input_data = pd.DataFrame([{
    'Product_Id': Product_Id,
    'Product_Weight': Product_Weight,
    'Product_Sugar_Content': Product_Sugar_Content,
    'Product_Allocated_Area': Product_Allocated_Area,
    'Product_Type': Product_Type,
    'Product_MRP': Product_MRP,
    'Store_Id': Store_Id,
    'Store_Establishment_Year': Store_Establishment_Year,
    'Store_Size': Store_Size,
    'Store_Location_City_Type': Store_Location_City_Type,
    'Store_Type': Store_Type,
    'Product_Store_Sales_Total': Product_Store_Sales_Total
}])

# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/sales", json=input_data.to_dict(orient='records')[0])  # Send data to Flask API
    if response.status_code == 200:
        prediction = response.json()['Predicted Sales Price (in dollars)']
        st.success(f"Predicted Sales Price (in dollars): {prediction}")
    else:
        st.error("Unable to connect to the prediction API.")

# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/salesbatch", files={"file": uploaded_file})  # Send file to Flask API
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            st.write(predictions)  # Display the predictions
        else:
            st.error("Unable to connect to the prediction API.")
