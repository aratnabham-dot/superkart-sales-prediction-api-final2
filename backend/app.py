import numpy as np
import joblib
import pandas as pd
from flask import Flask, request, jsonify

superkart_api = Flask("SuperKart Sales Predictor")
model = joblib.load("superkart_model.joblib")

@superkart_api.get('/')
def home():
    return "Welcome to the SuperKart Sales Prediction API!"

@superkart_api.post('/v1/predict')
def predict_sales():
    data = request.get_json()
    input_df = pd.DataFrame([data])
    predicted_sales = model.predict(input_df)[0]
    return jsonify({'Predicted Price (in dollars)': round(float(predicted_sales), 2)})

@superkart_api.post('/v1/predictbatch')
def predict_sales_batch():
    file = request.files['file']
    input_df = pd.read_csv(file)
    predictions = model.predict(input_df).tolist()
    predicted_sales = [round(float(p), 2) for p in predictions]

    # Map predictions to index
    output_dict = dict(zip(input_df.index.astype(str).tolist(), predicted_sales))
    return jsonify(output_dict)

if __name__ == '__main__':
    superkart_api.run(debug=True)
