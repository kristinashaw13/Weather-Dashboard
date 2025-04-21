import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# loading environment variables
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    st.error("API key not found. Please check your .env file.")

# URLs for OpenWeatherMap API
BASE_URL_CURRENT = "http://api.openweathermap.org/data/2.5/weather"
BASE_URL_FORECAST = "http://api.openweathermap.org/data/2.5/forecast"

# function to fetch current weather
def get_current_weather(location):
    try:
        params = {"q": location, "appid": API_KEY, "units": "metric"}
        response = requests.get(BASE_URL_CURRENT, params=params)
        response.raise_for_status()
        data = response.json()
        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching current weather: {e}")
        return None

# function to fetch the 5-day forecast
def get_forecast(location):
    try:
        params = {"q": location, "appid": API_KEY, "units": "metric"}
        response = requests.get(BASE_URL_FORECAST, params=params)
        response.raise_for_status()
        data = response.json()
        forecast_list = []
        for entry in data["list"][::8]:
            forecast_list.append({
                "date": datetime.fromtimestamp(entry["dt"]).strftime("%Y-%m-%d"),
                "temperature": entry["main"]["temp"],
                "description": entry["weather"][0]["description"]
            })
        return forecast_list
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching forecast: {e}")
        return None

# function to save search to JSON
def save_search(location):
    searches = []
    try:
        if os.path.exists("searches.json"):
            with open("searches.json", "r") as f:
                content = f.read().strip()
                if content:  # Checks to see if file is not empty
                    f.seek(0)  
                    searches = json.load(f)
        searches.append({"location": location, "timestamp": datetime.now().isoformat()})
        with open("searches.json", "w") as f:
            json.dump(searches[-5:], f)  # Keeps the last 5 searches
    except (json.JSONDecodeError, IOError) as e:
        st.error(f"Error saving search: {e}")

# setup streamlit app
st.title("Weather Forecast Dashboard")
st.write("Enter a city or ZIP code to view current weather and 5-day forecast.")

# user input form
location = st.text_input("Location (e.g., New York, 10001)", "New York")
if st.button("Get Weather"):
    if location:
        save_search(location)
        # displays current weather
        current = get_current_weather(location)
        if current:
            st.subheader(f"Current Weather in {current['city']}")
            st.write(f"Temperature: {current['temperature']}°C")
            st.write(f"Description: {current['description'].capitalize()}")
            st.write(f"Humidity: {current['humidity']}%")
            st.write(f"Wind Speed: {current['wind_speed']} m/s")
        
        # displays the 5-day forecast
        forecast = get_forecast(location)
        if forecast:
            st.subheader("5-Day Forecast")
            df = pd.DataFrame(forecast)
            st.dataframe(df[["date", "temperature", "description"]])
            # Plot temperature trend
            fig = px.line(df, x="date", y="temperature", title="Temperature Trend")
            st.plotly_chart(fig)
    else:
        st.error("Please enter a location.")

# displays recent searches
searches = []
if os.path.exists("searches.json"):
    try:
        with open("searches.json", "r") as f:
            content = f.read().strip()
            if content:
                f.seek(0)
                searches = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        st.error(f"Error reading searches: {e}")
if searches:
    st.subheader("Recent Searches")
    st.write([s["location"] for s in searches])
