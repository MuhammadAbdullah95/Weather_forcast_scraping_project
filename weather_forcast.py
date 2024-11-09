import os
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Set API key
api_key = os.getenv("OPEN_WEATHER_API")


# Function to fetch weather data from OpenWeatherMap API
def fetch_weather_data(cities):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    data = []

    for city in cities:
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric",  # Use "imperial" for Fahrenheit
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            weather_info = response.json()
            city_name = weather_info["name"]
            temperature = weather_info["main"]["temp"]
            condition = weather_info["weather"][0]["description"]

            data.append(
                {"City": city_name, "Temperature": temperature, "Condition": condition}
            )
        else:
            print(f"Could not retrieve data for {city}")

    return pd.DataFrame(data)


def main():
    st.title("Weather Forecast for Multiple Cities")

    city_input = st.sidebar.text_area(
        "Enter cities separated by commas (e.g., Sahiwal, Lahore, Karachi)"
    )

    if api_key and city_input:
        cities = [city.strip() for city in city_input.split(",")]

        # Fetch weather data
        weather_df = fetch_weather_data(cities)

        # Sidebar options for search and sorting
        st.sidebar.header("Filter Options")
        city_search = st.sidebar.text_input("Search by City")
        sort_option = st.sidebar.selectbox("Sort by", ["City", "Temperature"], index=1)

        # Filter data based on search input
        if city_search:
            weather_df = weather_df[
                weather_df["City"].str.contains(city_search, case=False)
            ]

        # Sort data based on user selection
        if sort_option == "Temperature":
            weather_df = weather_df.sort_values("Temperature")
        else:
            weather_df = weather_df.sort_values("City")

        # Display filtered and sorted data
        st.dataframe(weather_df)
    else:
        st.write("Please enter city or list of cities to get weather data.")


if __name__ == "__main__":
    main()
