import random
import json

def Make_Decision(precipitation, windmph, temperatureF, humidity):
    outerwear = ''
    top = ''
    bottoms = ''
    shoes = ''
    # The logic for clothing decisions 
    
    #No Precipitation
    if precipitation == 'Clear':
        if temperatureF < 55:
            outerwear = "Coat or Sweater"
            bottoms = 'Pants'
            top = 'Long sleeve Shirt'
            shoes = 'Only-closed Toed shoes'
        if 55 <= temperatureF <= 75:
            bottoms = 'Any Bottoms'
            shoes = 'Sneakers'
            if windmph <= 7:
                outerwear = 'Jacket or Light Sweater'
                top = 'T-shirt'
            else:
                outerwear = 'Windbreaker'
                top = 'Long sleeve Shirt'
        if temperatureF > 75:
            outerwear = "No Outerwear"
            shoes = 'Sneakers or Sandals'
            bottoms = 'Shorts or Skirt'
            if humidity > 70:
                top = "T-shirt only"
            else:
                top = 'Any Top'

    #Drizzle
    if precipitation == 'Drizzle':
        shoes = 'Only-closed Toed shoes'
        if temperatureF < 55:
            top = 'Long sleeve Shirt'
            outerwear = 'Coat or Hoodie'
            bottom = 'Pants'
        if 55 <= temperatureF <= 75:
            top = 'Any Top'
            if windmph > 7:
                outerwear = 'Windbreaker'
            else:
                outerwear = 'Jacket or Hoodie'
        if temperatureF > 75:
            outerwear = "Jacket"
            shoes = 'Sneakers'
            bottoms = 'Shorts or Skirt'
            if humidity > 70:
                top = "T-shirt only"
            else:
                top = 'Any Top'

    #Rain

    if precipitation == 'Rain':
        shoes = 'Only-closed Toed shoes'
        if temperatureF < 55:
            top = 'Long sleeve Shirt'
            outerwear = 'Coat or Rain Jacket with Sweater'
            bottom = 'Pants'
        if 55 <= temperatureF <= 75:
            top = 'Any Top'
            if windmph > 7:
                outerwear = 'Rain Jacket'
                bottoms = 'Pants'
            else:
                outerwear = 'Jacket or Hoodie'
                bottoms = 'Any Bottoms'
        if temperatureF > 75:
            outerwear = "Jacket"
            shoes = 'Sneakers'
            bottoms = 'Shorts or Skirt'
            if humidity > 70:
                top = "T-shirt only"
            else:
                top = 'Any Top'

    #Thunderstorm

    if precipitation == 'Thunderstorm':
        shoes = 'Only-closed Toed shoes'
        bottoms = 'Pants'
        if temperatureF < 55:
            top = 'Long sleeve Shirt'
            outerwear = 'Coat or Rain Jacket with Sweater'
        if 55 <= temperatureF <= 75:
            top = 'Any Top'
            if windmph > 7:
                outerwear = 'Rain Jacket'
            else:
                outerwear = 'Jacket or Hoodie'
        if temperatureF > 75:
            outerwear = "Jacket"
            shoes = 'Sneakers'
            if humidity > 70:
                top = "T-shirt only"
            else:
                top = 'Any Top'

    #Snow

    if precipitation == 'Snow':
        bottoms = 'Pants'
        shoes = 'Only-closed Toed shoes'
        top = 'Long sleeve Shirt'
        if temperatureF < 32:
            outerwear = 'Coat'
        else:
            outerwear = 'Coat or a Hoodie'

    #Cloudy

    if precipitation == 'Clouds':
        if temperatureF < 55:
            outerwear = "Coat or Sweater"
            bottoms = 'Pants'
            top = 'Long sleeve Shirt'
            shoes = 'Only-closed Toed shoes'
        if 55 <= temperatureF <= 75:
            bottoms = 'Any Bottoms'
            shoes = 'Sneakers'
            if windmph <= 7:
                outerwear = 'Jacket or Light Sweater'
                top = 'T-shirt'
            else:
                outerwear = 'Windbreaker or Jacket'
                top = 'Long sleeve Shirt or Sweater with no Outerwear'
        if temperatureF > 75:
            outerwear = "None"
            shoes = 'Sneakers or Sandals'
            bottoms = 'Shorts or Skirt'
            if humidity > 70:
                top = "T-shirt only"
            else:
                top = 'Any Top'
    

    return {
        "Precipitation": precipitation,
        "Wind Speed (mph)": windmph,
        "Temperature (F)": temperatureF,
        "Humidity": humidity,
        "Expected Results": {"Outerwear": outerwear, 
                    "Top": top, 
                    "Bottoms":bottoms,
                    "Shoes": shoes}
    }


artificial_dataset = []
possible_precipitation = ['Clear', 'Drizzle', 'Rain', 'Thunderstorm', 'Snow', 'Clouds']
for _ in range(5000):
    precipitation = random.choice(possible_precipitation)
    windmph = random.uniform(0, 20)  # Random wind speed between 0 to 20 mph
    temperatureF = random.uniform(0, 100)  # Random temperature between 0 to 100 degrees Fahrenheit
    humidity = random.uniform(0, 100)  # Random humidity between 0% to 100%
    
    artificial_data = Make_Decision(precipitation, windmph, temperatureF, humidity)  # You can modify these values or make them random
    artificial_dataset.append(artificial_data)


with open('clothing_decisions.json', 'w') as json_file:
    json.dump(artificial_dataset, json_file, indent=4)