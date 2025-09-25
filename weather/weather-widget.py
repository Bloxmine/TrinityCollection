#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Weather Widget SuperKaramba Widget
#  Shows weather information (simulated data for demo)
#  Compatible with Trinity Desktop / KDE 3.5
#  Note: This is a demo version with simulated data
#  For real weather data, you would need to integrate with a weather API

import karamba
import time
import random
import os

# Configuration
CITY_NAME = "Your City"
USE_CELSIUS = True

# Simulated weather data for demo purposes
weather_conditions = [
    "Sunny", "Partly Cloudy", "Cloudy", "Overcast", 
    "Light Rain", "Heavy Rain", "Thunderstorm", 
    "Snow", "Fog", "Windy"
]

def initWidget(widget):
    """Initialize the widget"""
    karamba.changeText(widget, "location_display", "Location: %s" % CITY_NAME)
    updateWeather(widget)
    karamba.redrawWidget(widget)

def widgetUpdated(widget):
    """Called periodically to update weather information"""
    updateWeather(widget)

def updateWeather(widget):
    """Update weather display with simulated data"""
    try:
        # Generate simulated weather data
        weather_data = generateSimulatedWeather()
        
        # Update temperature
        if USE_CELSIUS:
            temp_str = "%d°C" % weather_data['temperature_c']
        else:
            temp_str = "%d°F" % weather_data['temperature_f']
        karamba.changeText(widget, "temperature_display", temp_str)
        
        # Update condition
        karamba.changeText(widget, "condition_display", weather_data['condition'])
        
        # Update additional info
        karamba.changeText(widget, "humidity_display", 
                          "Humidity: %d%%" % weather_data['humidity'])
        karamba.changeText(widget, "wind_display", 
                          "Wind: %d km/h" % weather_data['wind_speed'])
        karamba.changeText(widget, "pressure_display", 
                          "Pressure: %d hPa" % weather_data['pressure'])
        karamba.changeText(widget, "visibility_display", 
                          "Visibility: %d km" % weather_data['visibility'])
        
        # Update forecast
        karamba.changeText(widget, "forecast_display", 
                          "Today: %s" % weather_data['forecast'])
        
        # Change colors based on weather condition
        updateWeatherColors(widget, weather_data['condition'])
        
        # Update timestamp
        current_time = time.strftime("%H:%M")
        karamba.changeText(widget, "last_update", "Last updated: %s" % current_time)
        
    except Exception, e:
        karamba.changeText(widget, "temperature_display", "Error")
        karamba.changeText(widget, "condition_display", str(e))

def generateSimulatedWeather():
    """Generate realistic simulated weather data"""
    # Base this on time of day and some randomness
    hour = time.localtime().tm_hour
    
    # Simulate temperature variation by time of day
    if 6 <= hour < 12:  # Morning
        base_temp = 15 + random.randint(-5, 5)
    elif 12 <= hour < 18:  # Afternoon
        base_temp = 22 + random.randint(-3, 8)
    elif 18 <= hour < 22:  # Evening
        base_temp = 18 + random.randint(-4, 6)
    else:  # Night
        base_temp = 12 + random.randint(-6, 4)
    
    condition = random.choice(weather_conditions)
    
    # Adjust other parameters based on condition
    if "Rain" in condition:
        humidity = random.randint(70, 95)
        visibility = random.randint(5, 15)
        wind_speed = random.randint(10, 25)
    elif "Snow" in condition:
        base_temp = random.randint(-5, 2)
        humidity = random.randint(80, 95)
        visibility = random.randint(3, 10)
        wind_speed = random.randint(5, 20)
    elif "Sunny" in condition:
        humidity = random.randint(30, 60)
        visibility = random.randint(20, 40)
        wind_speed = random.randint(3, 12)
    else:  # Other conditions
        humidity = random.randint(50, 80)
        visibility = random.randint(10, 25)
        wind_speed = random.randint(5, 18)
    
    return {
        'temperature_c': base_temp,
        'temperature_f': int(base_temp * 9/5 + 32),
        'condition': condition,
        'humidity': humidity,
        'wind_speed': wind_speed,
        'pressure': random.randint(995, 1025),
        'visibility': visibility,
        'forecast': generateForecast(condition)
    }

def generateForecast(current_condition):
    """Generate a simple forecast based on current conditions"""
    forecasts = {
        "Sunny": "Clear skies continuing",
        "Partly Cloudy": "Mix of sun and clouds",
        "Cloudy": "Overcast conditions",
        "Light Rain": "Showers expected",
        "Heavy Rain": "Heavy downpours likely",
        "Thunderstorm": "Storms with lightning",
        "Snow": "Snowfall continuing",
        "Fog": "Misty conditions",
        "Windy": "Breezy weather"
    }
    
    return forecasts.get(current_condition, "Variable conditions")

def updateWeatherColors(widget, condition):
    """Update widget colors based on weather condition"""
    if "Sunny" in condition:
        # Bright, warm colors
        karamba.changeTextColor(widget, "temperature_display", 255, 200, 50)
        karamba.changeTextColor(widget, "condition_display", 255, 255, 100)
    elif "Rain" in condition or "Storm" in condition:
        # Cool, blue colors
        karamba.changeTextColor(widget, "temperature_display", 100, 150, 255)
        karamba.changeTextColor(widget, "condition_display", 150, 200, 255)
    elif "Snow" in condition:
        # White/light blue colors
        karamba.changeTextColor(widget, "temperature_display", 200, 220, 255)
        karamba.changeTextColor(widget, "condition_display", 255, 255, 255)
    elif "Cloud" in condition:
        # Gray colors
        karamba.changeTextColor(widget, "temperature_display", 200, 200, 200)
        karamba.changeTextColor(widget, "condition_display", 180, 180, 180)
    else:
        # Default colors
        karamba.changeTextColor(widget, "temperature_display", 255, 200, 100)
        karamba.changeTextColor(widget, "condition_display", 150, 255, 150)

def widgetClicked(widget, x, y, button):
    """Handle mouse clicks - toggle Celsius/Fahrenheit"""
    global USE_CELSIUS
    
    if button == 1:  # Left click
        USE_CELSIUS = not USE_CELSIUS
        updateWeather(widget)
    elif button == 3:  # Right click - refresh weather
        updateWeather(widget)

def widgetMouseMoved(widget, x, y, button):
    """Handle mouse movement"""
    pass

# Note: In a real implementation, you would:
# 1. Use a weather API like OpenWeatherMap
# 2. Store API key securely
# 3. Handle network errors gracefully
# 4. Cache data to avoid excessive API calls
# 5. Allow user to configure location