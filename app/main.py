from app.utils import read_weather_csv, fill_weather
from app.utils.get_weather import get_weather

df = read_weather_csv("data/weather_data.csv")
fill_weather(df)

country = input("Enter the country: ").strip()
date = input("Enter the date (YYYY-MM-DD): ").strip()

result = get_weather(country, date)
print(result)