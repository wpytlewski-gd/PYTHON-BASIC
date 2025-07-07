import json

# from decimal import Decimal
from pathlib import Path
from typing import Dict, List

# import lxml


def get_list_of_keys(hourly_list: List, key: str) -> List:
    return [hour_report[key] for hour_report in hourly_list if key in hour_report]


def calculate_stats(data_list: List[float]) -> Dict[str, float]:
    if not data_list:
        return {"mean": 0, "max": 0, "min": 0}
    return {
        "mean": sum(data_list) / len(data_list),
        "max": max(data_list),
        "min": min(data_list),
    }


def process_weather_file(file_path: Path) -> Dict[str, float]:
    with file_path.open(encoding="utf-8") as file_handle:
        city_data = json.load(file_handle).get("hourly", [])

    temps = get_list_of_keys(city_data, "temp")
    winds = get_list_of_keys(city_data, "wind_speed")

    temp_stats = calculate_stats(temps)
    wind_stats = calculate_stats(winds)

    return {
        "mean_temp": round(temp_stats["mean"], 2),
        "max_temp": temp_stats["max"],
        "min_temp": temp_stats["min"],
        "mean_wind_speed": round(wind_stats["mean"], 2),
        "max_wind_speed": wind_stats["max"],
        "min_wind_speed": wind_stats["min"],
    }


def get_spain_stats(cities_dict: Dict) -> Dict:
    if not cities_dict:
        return {}

    coldest_city_name = None
    warmest_city_name = None
    windiest_city_name = None

    lowest_temp = float("inf")
    highest_temp = float("-inf")
    highest_wind = float("-inf")

    total_temp = 0
    total_wind = 0
    num_of_cities = len(cities_dict)

    for city_name, values in cities_dict.items():
        if values["mean_temp"] < lowest_temp:
            lowest_temp = values["mean_temp"]
            coldest_city_name = city_name

        if values["mean_temp"] > highest_temp:
            highest_temp = values["mean_temp"]
            warmest_city_name = city_name

        if values["mean_wind_speed"] > highest_wind:
            highest_wind = values["mean_wind_speed"]
            windiest_city_name = city_name

        total_temp += values["mean_temp"]
        total_wind += values["mean_wind_speed"]

    return {
        "coldest_place": coldest_city_name,
        "warmest_place": warmest_city_name,
        "windiest_place": windiest_city_name,
        "mean_temp": round(total_temp / num_of_cities, 2),
        "mean_wind_speed": round(total_wind / num_of_cities, 2),
    }


def main():
    source_dir = Path(__file__).parent / "source_data"

    weather_cities_data = {}
    for json_file in source_dir.glob("**/*.json"):
        weather_cities_data[json_file.parent.name] = process_weather_file(json_file)

    # print(weather_cities_data)

    spain_data_dict = get_spain_stats(weather_cities_data)

    print(spain_data_dict)


if __name__ == "__main__":
    main()
