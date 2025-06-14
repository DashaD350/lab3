from app.utils import read_weather_csv, fill_weather
from app.utils.get_weather import get_weather

df = read_weather_csv("data/weather_data.csv")
fill_weather(df)

country = input("Введіть країну: ").strip()
date = input("Введіть місяць (рік, місяць, день): ").strip()

result = get_weather(country, date)
print(result)