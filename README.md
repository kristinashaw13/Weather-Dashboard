# Weather Forecast Dashboard

A Python web application built with Streamlit that fetches the current weather and the 5-day forecast with a given location using
the OpenWeatherMap API. This project demonstrates API integration, interactive data visualization, and environment variable
management, showcasing skills in Python, Streamlit, and web development.

# Features
- Displays current weather (temperature, humidity, wind speed, and a description).
- Shows a 5-day forecast with aa temperature trend chart.
- Saves and displays recent searches in a JSON file.
- Uses '.env' for secure API key management

# Setup
Follow these steps to run the application locally:

1. **Clone or download the repository**
    - Clone with Git:
      '''bash
      git clone https://github.com/kristinashaw13/Weather-Dashboard.git
      (or download the ZIP from GitHub and extract it)

2. Create a virtual environment:
    python -m venv venv

3. Activate the virtual environment:
    - On Windows:
      .\venv\Scripts\activate
    - On macOS/Linux:
      source venv/bin/activate

4. Install dependencies:
    pip install -r requirements.txt

5. Create a .env file:
    - Copy the .env.example to .env:
    - Obtain a free API key from openweathermap.org, place the API key in .env
  
6. Run the app:
    streamlit run app.py
