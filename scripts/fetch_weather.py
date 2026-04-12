#!/usr/bin/env python3
"""Fetch weather data for Toronto using Open-Meteo (free, no API key)."""

import json
import os
from datetime import datetime
import requests

# Toronto coordinates
LATITUDE = 43.6532
LONGITUDE = -79.3832
CITY = "Toronto, ON, Canada"

def get_weather_description(code):
    """Convert WMO weather code to description."""
    codes = {
        0: "Clear sky ☀️",
        1: "Mainly clear 🌤️",
        2: "Partly cloudy ⛅",
        3: "Overcast ☁️",
        45: "Foggy 🌫️",
        48: "Depositing rime fog 🌫️",
        51: "Light drizzle 🌧️",
        53: "Moderate drizzle 🌧️",
        55: "Dense drizzle 🌧️",
        61: "Slight rain 🌧️",
        63: "Moderate rain 🌧️",
        65: "Heavy rain 🌧️",
        66: "Light freezing rain 🌨️",
        67: "Heavy freezing rain 🌨️",
        71: "Slight snow ❄️",
        73: "Moderate snow ❄️",
        75: "Heavy snow ❄️",
        77: "Snow grains ❄️",
        80: "Slight rain showers 🌦️",
        81: "Moderate rain showers 🌦️",
        82: "Violent rain showers ⛈️",
        85: "Slight snow showers 🌨️",
        86: "Heavy snow showers 🌨️",
        95: "Thunderstorm ⛈️",
        96: "Thunderstorm with slight hail ⛈️",
        99: "Thunderstorm with heavy hail ⛈️",
    }
    return codes.get(code, "Unknown")

def fetch_weather():
    """Fetch current weather from Open-Meteo API."""
    
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={LATITUDE}&longitude={LONGITUDE}"
        f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,"
        f"weather_code,wind_speed_10m,wind_direction_10m"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max"
        f"&timezone=America/Toronto"
    )
    
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        
        current = data.get('current', {})
        daily = data.get('daily', {})
        
        weather_data = {
            'updated_at': datetime.utcnow().isoformat() + 'Z',
            'location': CITY,
            'coordinates': {
                'latitude': LATITUDE,
                'longitude': LONGITUDE
            },
            'current': {
                'temperature_c': current.get('temperature_2m'),
                'feels_like_c': current.get('apparent_temperature'),
                'humidity_percent': current.get('relative_humidity_2m'),
                'wind_speed_kmh': current.get('wind_speed_10m'),
                'wind_direction': current.get('wind_direction_10m'),
                'condition': get_weather_description(current.get('weather_code', 0)),
                'weather_code': current.get('weather_code')
            },
            'today': {
                'high_c': daily.get('temperature_2m_max', [None])[0],
                'low_c': daily.get('temperature_2m_min', [None])[0],
                'precipitation_chance': daily.get('precipitation_probability_max', [None])[0]
            }
        }
        
    except Exception as e:
        weather_data = {
            'updated_at': datetime.utcnow().isoformat() + 'Z',
            'location': CITY,
            'error': str(e),
            'current': {
                'condition': 'Unable to fetch weather data'
            }
        }
    
    # Save to file
    os.makedirs('data', exist_ok=True)
    with open('data/weather.json', 'w') as f:
        json.dump(weather_data, f, indent=2)
    
    if 'error' not in weather_data:
        curr = weather_data['current']
        print(f"✅ Weather for {CITY}")
        print(f"   {curr['condition']}")
        print(f"   Temperature: {curr['temperature_c']}°C (feels like {curr['feels_like_c']}°C)")
        print(f"   Humidity: {curr['humidity_percent']}%")
    else:
        print(f"⚠️ Weather fetch failed: {weather_data['error']}")

if __name__ == '__main__':
    fetch_weather()
