from google.adk.agents.llm_agent import Agent
from datetime import datetime
import pytz
import os
import requests
from dotenv import load_dotenv
from simpleeval import simple_eval

def get_current_time(city: str) -> dict:
    """
       Get the current local time for a city.

    Args:
        city: Name of the city.

    Returns:
        Current local time in that city.
    """

    city_timezones = {
        "delhi": "Asia/Kolkata",
        "london": "Europe/London",
        "new york": "America/New_York",
        "tokyo": "Asia/Tokyo"
    }

    if city.lower() not in city_timezones:
        return {
            "status": "error",
            "message": f"Sorry, I don't know the timezone for {city}."
        }

    tz = pytz.timezone(
        city_timezones.get(city.lower(), "Asia/Kolkata")
    )

    current_time = datetime.now(tz).strftime("%I:%M %p")

    return {
        "status": "success",
        "city": city,
        "time": current_time
    }

def calculate(expression: str) -> dict:
    try:
        result = simple_eval(expression)

        return {
            "status": "success",
            "expression": expression,
            "result": result
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
    

load_dotenv()

def get_weather(city: str) -> dict:
    """
    Get the current weather for a city.
    """

    api_key = os.getenv("WEATHER_API_KEY")

    if not api_key:
        return {
            "status": "error",
            "message": "Weather API key not found."
        }

    url = "https://api.weatherapi.com/v1/current.json"

    params = {
        "key": api_key,
        "q": city
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return {
            "status": "error",
            "message": f"Could not get weather for {city}"
        }

    data = response.json()

    return {
        "status": "success",
        "city": data["location"]["name"],
        "country": data["location"]["country"],
        "temperature_c": data["current"]["temp_c"],
        "condition": data["current"]["condition"]["text"]
    }



root_agent = Agent(
    model='gemini-2.0-flash',
    name='root_agent',
    description="A Smart City Assistant that provides time, weather, and calculations.",
    instruction="""
You are a Smart City Assistant.

Use:
- get_current_time for time-related questions
- get_weather for weather-related questions
- calculate for mathematical calculations

Always use the appropriate tool when available.
""",
    tools=[
        get_current_time,
        calculate,
        get_weather
    ]
)