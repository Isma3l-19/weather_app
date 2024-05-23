from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
api_key = os.getenv('API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form.get('city')
    if city:
        url_current = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no'
        url_forecast = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=5&aqi=no&alerts=no'
        
        response_current = requests.get(url_current)
        response_forecast = requests.get(url_forecast)
        
        data_current = response_current.json()
        data_forecast = response_forecast.json()
        
        if response_current.status_code == 200 and response_forecast.status_code == 200:
            weather_data = {
                'city': data_current['location']['name'],
                'temperature': data_current['current']['temp_c'],
                'description': data_current['current']['condition']['text'],
                'icon': data_current['current']['condition']['icon'],
                'forecast': [
                    {
                        'date': forecast['date'],
                        'max_temp': forecast['day']['maxtemp_c'],
                        'min_temp': forecast['day']['mintemp_c'],
                        'description': forecast['day']['condition']['text'],
                        'icon': forecast['day']['condition']['icon']
                    } for forecast in data_forecast['forecast']['forecastday']
                ]
            }
            return render_template('index.html', weather_data=weather_data)
        else:
            error = data_current.get('error', {}).get('message', 'Error retrieving current weather data') or \
                    data_forecast.get('error', {}).get('message', 'Error retrieving forecast data')
            return render_template('index.html', error=error)
    return render_template('index.html', error='City name cannot be empty')

if __name__ == '__main__':
    app.run(debug=True)
