from app.utils import read_weather_csv, write_weather
from app.utils.get_weather import get_weather

df = read_weather_csv("data/weather_data.csv")
write_weather(df)

country = input("Введіть країну: ").strip()
date = input("Введіть місяць (рік, місяць, день): ").strip()

result = get_weather(country, date)
print(result)