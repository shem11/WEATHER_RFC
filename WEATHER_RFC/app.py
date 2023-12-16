from flask import Flask, request, render_template
import json
import requests
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import joblib
import classifier

app = Flask(__name__)

# Load models and label encoders
model_outerwear = joblib.load("Outerwear_Model.pkl")
model_top = joblib.load("Top_Model.pkl")
model_bottom = joblib.load("Bottom_Model.pkl")
model_shoes = joblib.load("Shoes_Model.pkl")

# Label Encoders
# Define label encoders and label conversion functions

# Function to preprocess user input
def preprocess_input(data):
    # Define a mapping for 'Precipitation' categories
    precipitation_mapping = {
        'Clear': 0,
        'Drizzle': 1,
        'Rain': 2,
        'Thunderstorm': 3,
        'Snow': 4,
        'Clouds': 5
    }

    # Map 'Precipitation' categories to numerical values
    data['Precipitation'] = data['Precipitation'].map(precipitation_mapping)
    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        zip_code = request.form['zip_code']
        complete_api_link = requests.get(f"https://api.openweathermap.org/data/2.5/weather?zip={zip_code},us&appid=51a01a1a70bc47e2f23fc0e9740d3699")
        objects = complete_api_link.json()
        print(objects)

        if objects == {'cod': '404', 'message': 'city not found'}:
            details = "Invalid Zip Code!"
            return render_template('error.html', details=details)


        precipitation = str(objects['weather'][0]['main'])
        wind_speed = float(objects['wind']['speed'])
        temperatureK = float(objects['main']['temp'])
        temperatureF = int(round(((temperatureK - 273.15) * (9/5)) + 32))
        windmph = int(round(wind_speed * 2.237))
        humidity = int(objects['main']['humidity'])


        # Create user input DataFrame
        user_input = pd.DataFrame({
            'Precipitation': [precipitation],
            'Wind Speed (mph)': [wind_speed],
            'Temperature (F)': [temperatureF],
            'Humidity': [humidity]
        })

        # Preprocess user input
        user_input = preprocess_input(user_input)



        # Make predictions
        outerwear = model_outerwear.predict(user_input)
        top = model_top.predict(user_input)
        bottoms = model_bottom.predict(user_input)
        shoes = model_shoes.predict(user_input)


        original_ow_labels = classifier.label_encoder_ow.inverse_transform(range(classifier.label_encoder_ow.classes_.size))
        original_t_labels = classifier.label_encoder_t.inverse_transform(range(classifier.label_encoder_t.classes_.size))
        original_b_labels = classifier.label_encoder_b.inverse_transform(range(classifier.label_encoder_b.classes_.size))
        original_s_labels = classifier.label_encoder_s.inverse_transform(range(classifier.label_encoder_s.classes_.size))
        original_ow_labels = classifier.convert_to_dic(original_ow_labels)
        original_t_labels = classifier.convert_to_dic(original_t_labels)
        original_b_labels = classifier.convert_to_dic(original_b_labels)
        original_s_labels = classifier.convert_to_dic(original_s_labels)
        
        # Convert predictions to labels
        outerwear = original_ow_labels.get(outerwear[0])
        top = original_t_labels.get(top[0])
        bottoms = original_b_labels.get(bottoms[0])
        shoes = original_s_labels.get(shoes[0])

        details = f'{precipitation}, {temperatureF} degrees, {windmph} mph wind, and {humidity}% humidity'

        recommendations = {"Outerwear": outerwear, 
                    "Top": top, 
                    "Bottoms":bottoms,
                    "Shoes": shoes}

        return render_template('results.html', recommendations=recommendations, details = details)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
