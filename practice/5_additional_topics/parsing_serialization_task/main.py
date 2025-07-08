import argparse
import json
from pathlib import Path
from typing import Dict, List

from lxml import etree

# Constants for easy configuration
COUNTRY = "Spain"
OBSERVATION_DATE = "2021-09-25"


def get_list_of_keys(hourly_list: List, key: str) -> List:
    """Extracts values for a specific key from a list of dicts."""
    return [hour_report[key] for hour_report in hourly_list if key in hour_report]


def calculate_stats(data_list: List[float]) -> Dict[str, float]:
    """Calculates min, max, and mean for a list of numbers."""
    if not data_list:
        return {"mean": 0, "max": 0, "min": 0}
    return {
        "mean": sum(data_list) / len(data_list),
        "max": max(data_list),
        "min": min(data_list),
    }


def process_weather_file(file_path: Path) -> Dict[str, float]:
    """Reads a single weather JSON file and calculates its stats."""
    with file_path.open(encoding="utf-8") as file_handle:
        city_data = json.load(file_handle).get("hourly", [])

    temps = get_list_of_keys(city_data, "temp")
    winds = get_list_of_keys(city_data, "wind_speed")

    temp_stats = calculate_stats(temps)
    wind_stats = calculate_stats(winds)

    return {
        "mean_temp": round(temp_stats["mean"], 2),
        "mean_wind_speed": round(wind_stats["mean"], 2),
        "min_temp": temp_stats["min"],
        "min_wind_speed": wind_stats["min"],
        "max_temp": temp_stats["max"],
        "max_wind_speed": wind_stats["max"],
    }


def get_spain_stats(cities_dict: Dict) -> Dict:
    """Aggregates stats for all cities to find country-wide extremes and averages."""
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

    num_of_cities = len(cities_dict)
    return {
        "mean_temp": round(total_temp / num_of_cities, 2),
        "mean_wind_speed": round(total_wind / num_of_cities, 2),
        "coldest_place": coldest_city_name,
        "warmest_place": warmest_city_name,
        "windiest_place": windiest_city_name,
    }


def create_weather_xml(summary_data: Dict, cities_data: Dict) -> etree._Element:
    """Builds the XML structure from the processed weather data."""
    root = etree.Element("weather", country=COUNTRY, date=OBSERVATION_DATE)

    summary_attribs = {key: str(value) for key, value in summary_data.items()}
    etree.SubElement(root, "summary", attrib=summary_attribs)

    cities_element = etree.SubElement(root, "cities")
    for city_name, values in cities_data.items():
        city_attribs = {key: str(value) for key, value in values.items()}
        # Replace spaces in city names to create valid XML tag names
        valid_tag_name = city_name.replace(" ", "_")
        etree.SubElement(cities_element, valid_tag_name, attrib=city_attribs)

    return root


def save_xml_file(xml_element: etree._Element, file_path: Path) -> None:
    """Saves the XML element tree to a file with pretty-printing."""
    etree.indent(xml_element, "  ")
    xml_bytes = etree.tostring(xml_element, encoding="utf-8", xml_declaration=True, pretty_print=True)
    file_path.write_bytes(xml_bytes)


def main():
    """Orchestrates the data processing and XML generation."""
    script_dir = Path(__file__).parent

    # Set up argument parser with default values
    parser = argparse.ArgumentParser(description="Process weather data to generate an XML report.")
    parser.add_argument(
        "-s",
        "--source",
        default=str(script_dir / "source_data"),
        help="Path to the source data directory.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=str(script_dir / "result.xml"),
        help="Path to save the final result.xml file.",
    )
    args = parser.parse_args()

    source_dir = Path(args.source)
    output_path = Path(args.output)

    # Process all JSON files
    weather_cities_data = {}
    for json_file_path in source_dir.glob("**/*.json"):
        weather_cities_data[json_file_path.parent.name] = process_weather_file(json_file_path)

    # Aggregate country-wide statistics
    spain_data_dict = get_spain_stats(weather_cities_data)

    # Create and save the final XML file
    weather_xml_root = create_weather_xml(spain_data_dict, weather_cities_data)
    save_xml_file(weather_xml_root, output_path)

    print(f"Successfully saved weather data to {output_path}")


if __name__ == "__main__":
    main()
