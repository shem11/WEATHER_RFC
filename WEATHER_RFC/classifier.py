
# Program Starts Here
import json
import requests
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
#from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
#import joblib


with open('clothing_decisions.json', 'r') as file:
    artificial_dataset = json.load(file)


# Assuming 'artificial_dataset' contains generated data entries
weather_data = []
expected_outerwear = []
expected_top = []
expected_bottom = []
expected_shoes = []

for entry in artificial_dataset:
    weather_info = [
        entry["Precipitation"],
        entry["Wind Speed (mph)"],
        entry["Temperature (F)"],
        entry["Humidity"]
    ]
    weather_data.append(weather_info)
    
    expected_outerwear.append(entry["Expected Results"]["Outerwear"])
    expected_top.append(entry["Expected Results"]["Top"])
    expected_bottom.append(entry["Expected Results"]["Bottoms"])
    expected_shoes.append(entry["Expected Results"]["Shoes"])

df = pd.DataFrame(weather_data, columns=['Precipitation', 'Wind Speed (mph)', 'Temperature (F)', 'Humidity'])
df['Outerwear'] = expected_outerwear
df['Top'] = expected_top
df['Bottoms'] = expected_bottom
df['Shoes'] = expected_shoes

# Encoding categorical columns
label_encoder = LabelEncoder()
label_encoder_ow = LabelEncoder()
label_encoder_t = LabelEncoder()
label_encoder_b = LabelEncoder()
label_encoder_s = LabelEncoder()
df['Precipitation'] = label_encoder.fit_transform(df['Precipitation'])

# Features and targets
X = df.drop(['Outerwear', 'Top', 'Bottoms', 'Shoes'], axis=1)
y_outerwear = label_encoder_ow.fit_transform(df['Outerwear'])
y_top = label_encoder_t.fit_transform(df['Top'])
y_bottom = label_encoder_b.fit_transform(df['Bottoms'])
y_shoes = label_encoder_s.fit_transform(df['Shoes'])

# Splitting the data
X_train, X_test, y_ow_train, y_ow_test, y_top_train, y_top_test, y_bottom_train, y_bottom_test, y_shoes_train, y_shoes_test = train_test_split(X, y_outerwear, y_top, y_bottom, y_shoes, test_size=0.2, random_state=42)

# Training the models
model_outerwear = RandomForestClassifier(n_estimators=100, random_state=42)
model_outerwear.fit(X_train, y_ow_train)

model_top = RandomForestClassifier(n_estimators=100, random_state=42)
model_top.fit(X_train, y_top_train)

model_bottom = RandomForestClassifier(n_estimators=100, random_state=42)
model_bottom.fit(X_train, y_bottom_train)

model_shoes = RandomForestClassifier(n_estimators=100, random_state=42)
model_shoes.fit(X_train, y_shoes_train)

'''#Predictions
predictions_ow = model_outerwear.predict(X_test)
predictions_top = model_top.predict(X_test)
predictions_bottom = model_bottom.predict(X_test)
predictions_shoes = model_shoes.predict(X_test)

# Accuracy
accuracy_ow = accuracy_score(y_ow_test, predictions_ow)
accuracy_top = accuracy_score(y_top_test, predictions_top)
accuracy_bottom = accuracy_score(y_bottom_test, predictions_bottom)
accuracy_shoes = accuracy_score(y_shoes_test, predictions_shoes)

print(f"Outerwear Model Accuracy: {accuracy_ow * 100:.2f}%")
print(f"Top Model Accuracy: {accuracy_top * 100:.2f}%")
print(f"Bottom Model Accuracy: {accuracy_bottom * 100:.2f}%")
print(f"Shoes Model Accuracy: {accuracy_shoes * 100:.2f}%")
print(predictions_ow)

joblib.dump(model_outerwear, "Outerwear_Model.pkl")
joblib.dump(model_top, "Top_Model.pkl")
joblib.dump(model_bottom, "Bottom_Model.pkl")
joblib.dump(model_shoes, "Shoes_Model.pkl")
'''



# Label Processing
def convert_to_dic(label_list):
    label_list = {label: index for label, index in enumerate(label_list)}
    return label_list



# Retrieving Labels
original_ow_labels = label_encoder_ow.inverse_transform(range(label_encoder_ow.classes_.size))
original_t_labels = label_encoder_t.inverse_transform(range(label_encoder_t.classes_.size))
original_b_labels = label_encoder_b.inverse_transform(range(label_encoder_b.classes_.size))
original_s_labels = label_encoder_s.inverse_transform(range(label_encoder_s.classes_.size))

original_ow_labels = convert_to_dic(original_ow_labels)
original_t_labels = convert_to_dic(original_t_labels)
original_b_labels = convert_to_dic(original_b_labels)
original_s_labels = convert_to_dic(original_s_labels)

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
