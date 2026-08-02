import streamlit as st
import pandas as pd
import requests

BACKEND_URL = "http://backend:7860"

st.title("SuperKart Retail Sales Prediction")
st.write("Forecast total product sales based on historical store and product data.")

st.subheader("Online Prediction")
Product_Weight = st.number_input("Product Weight", min_value=0.0, value=12.66)
Product_Sugar_Content = st.selectbox("Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
Product_Allocated_Area = st.number_input("Allocated Display Area Ratio", min_value=0.0, max_value=1.0, value=0.027)
Product_MRP = st.number_input("Product MRP", min_value=0.0, value=117.08)
Store_Size = st.selectbox("Store Size", ["Small", "Medium", "High"])
Store_Location_City_Type = st.selectbox("City Type", ["Tier 1", "Tier 2", "Tier 3"])
Store_Type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Supermarket Type3", "Departmental Store", "Food Mart"])
Product_Id_char = st.selectbox("Product ID Category", ["FD", "NC", "DR"])
Store_Age_Years = st.number_input("Store Age (Years)", min_value=0, value=16)
Product_Type_Category = st.selectbox("Product Category", ['Food', 'Non Perishables', 'Beverages', 'Others'])

input_data = {
    'Product_Weight': Product_Weight,
    'Product_Sugar_Content': Product_Sugar_Content,
    'Product_Allocated_Area': Product_Allocated_Area,
    'Product_MRP': Product_MRP,
    'Store_Size': Store_Size,
    'Store_Location_City_Type': Store_Location_City_Type,
    'Store_Type': Store_Type,
    'Product_Id_char': Product_Id_char,
    'Store_Age_Years': Store_Age_Years,
    'Product_Type_Category': Product_Type_Category
}

if st.button("Predict Sales", type='primary'):
    response = requests.post(f"{BACKEND_URL}/v1/predict", json=input_data)
    if response.status_code == 200:
        res = response.json()
        st.success(f"🛒 Forecasted Revenue: **${res['Predicted Price (in dollars)']}**")
    else:
        st.error("Error communicating with backend.")

st.subheader("Batch Prediction")
uploaded_file = st.file_uploader("Upload CSV file for batch inference", type=["csv"])

if uploaded_file is not None:
    if st.button("Predict Batch", type='primary'):
        response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files={"file": uploaded_file})
        if response.status_code == 200:
            st.success("Batch predictions completed!")
            st.write(response.json())
        else:
            st.error("Error in batch API request.")
