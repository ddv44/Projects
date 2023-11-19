import requests
from twilio.rest import Client
from datetime import datetime, timedelta

# OpenWeatherMap API settings
OWM_API_KEY = 'YOUR_OPENWEATHERMAP_API_KEY'
CITY_NAME = 'CITY_NAME'
COUNTRY_CODE = 'COUNTRY_CODE'

# Twilio settings
TWILIO_ACCOUNT_SID = 'YOUR_TWILIO_ACCOUNT_SID'
TWILIO_AUTH_TOKEN = 'YOUR_TWILIO_AUTH_TOKEN'
TWILIO_PHONE_NUMBER = 'YOUR_TWILIO_PHONE_NUMBER'
RECIPIENT_PHONE_NUMBER = 'RECIPIENT_PHONE_NUMBER'

def get_weather_data():
    url = f'http://api.openweathermap.org/data/2.5/weather?q={CITY_NAME},{COUNTRY_CODE}&appid={OWM_API_KEY}'
    response = requests.get(url)
    data = response.json()

    return data

def send_weather_update(temperature, description):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body=f'Today\'s Weather Update:\nTemperature: {temperature}°C\nDescription: {description}',
        from_=TWILIO_PHONE_NUMBER,
        to=RECIPIENT_PHONE_NUMBER
    )

    print(f'Message sent successfully. SID: {message.sid}')

def main():
    weather_data = get_weather_data()

    if 'main' in weather_data and 'weather' in weather_data:
        temperature = round(weather_data['main']['temp'] - 273.15, 2)
        description = weather_data['weather'][0]['description']

        send_weather_update(temperature, description)
    else:
        print('Error fetching weather data.')

if __name__ == "__main__":
    main()
