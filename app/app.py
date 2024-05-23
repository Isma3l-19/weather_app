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
        url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no'
        response = requests.get(url)
        data = response.json()
        if 'error' not in data:
            weather_data = {
                'city': data['location']['name'],
                'temperature': data['current']['temp_c'],
                'description': data['current']['condition']['text'],
                'icon': data['current']['condition']['icon'],
            }
            return render_template('index.html', weather_data=weather_data)
        else:
            error = data['error'].get('message', 'Error retrieving weather data')
            return render_template('index.html', error=error)
    return render_template('index.html', error='City name cannot be empty')

if __name__ == '__main__':
    app.run(debug=True)
