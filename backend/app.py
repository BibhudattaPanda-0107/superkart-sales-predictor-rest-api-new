# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
superkart_sales_predictor_api = Flask("SuperKart Sales Forecast Predictor")

# Load the trained machine learning model
# model = joblib.load("backend_files/SuperKart_future_prediction_model_v1_0.joblib")
model = saved_model

# Define a route for the home page (GET request)
@superkart_sales_predictor_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the SuperKart Sales Forecast Predictor API!"

# Define an endpoint for single store sales prediction (POST request)
@superkart_sales_predictor_api.post('/v1/sales')
def predict_sales_price():
    """
    This function handles POST requests to the '/v1/sales' endpoint.
    It expects a JSON payload containing Superkart details and returns
    the predicted sales as a JSON response.
    """
    # Get the JSON data from the request body
    superkart_data = request.get_json()

    # Extract relevant features from the JSON data
    sample = {
        'Product_Id': superkart_data['Product_Id'],
        'Product_Weight': superkart_data['Product_Weight'],
        'Product_Sugar_Content': superkart_data['Product_Sugar_Content'],
        'Product_Allocated_Area': superkart_data['Product_Allocated_Area'],
        'Product_Type': superkart_data['Product_Type'],
        'Product_MRP': superkart_data['Product_MRP'],
        'Store_Id': superkart_data['Store_Id'],
        'Store_Establishment_Year': superkart_data['Store_Establishment_Year'],
        'Store_Size': superkart_data['Store_Size'],
        'Store_Location_City_Type': superkart_data['Store_Location_City_Type'],
        'Store_Type': superkart_data['Store_Type'],
        'Product_Store_Sales_Total': superkart_data['Product_Store_Sales_Total']

    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction (get predicted_sales)
    predicted_log_price = model.predict(input_data)[0]

    # Calculate actual price
    predicted_price = np.exp(predicted_log_price)

    # Convert predicted_price to Python float
    predicted_price = round(float(predicted_price), 2)
    # The conversion above is needed as we convert the model prediction (log price) to actual price using np.exp, which returns predictions as NumPy float32 values.
    # When we send this value directly within a JSON response, Flask's jsonify function encounters a datatype error

    # Return the actual price
    return jsonify({'Predicted Price (in dollars)': predicted_price})


# Define an endpoint for batch prediction (POST request)
@superkart_sales_predictor_api.post('/v1/salesbatch')
def predict_sales_price_batch():
    """
    This function handles POST requests to the '/v1/salesbatch' endpoint.
    It expects a CSV file containing superkart details for multiple stores
    and returns the predicted sales prices as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all stores in the DataFrame (get log_prices)
    predicted_log_prices = model.predict(input_data).tolist()

    # Calculate actual prices
    predicted_prices = [round(float(np.exp(log_price)), 2) for log_price in predicted_log_prices]

    # Create a dictionary of predictions with property IDs as keys
    product_ids = input_data['id'].tolist()  # Assuming 'id' is the product ID column
    output_dict = dict(zip(product_ids, predicted_prices))  # Use actual prices

    # Return the predictions dictionary as a JSON response
    return output_dict

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    superkart_sales_predictor_api.run(debug=True)
