import asyncio
from pathlib import Path

import aiohttp
import requests

API_KEY = "MY_API_KEY"
APOD_ENDPOINT = "https://api.nasa.gov/planetary/apod"
SCRIPT_DIR = Path(__file__).parent
OUTPUT_IMAGES_DIR = SCRIPT_DIR / "output"


def get_apod_metadata(start_date: str, end_date: str, api_key: str) -> list:
    """Fetches APOD image metadata for a specified date range."""
    params = {"api_key": api_key, "start_date": start_date, "end_date": end_date}

    response = requests.get(APOD_ENDPOINT, params=params, timeout=60)
    response.raise_for_status()

    image_metadata = [item for item in response.json() if item.get("media_type") == "image"]

    if not image_metadata:
        print("No images found in the selected date range.")
    else:
        print(f"Metadata for {len(image_metadata)} images fetched successfully.")

    return image_metadata


def download_apod_images(metadata: list):
    """Triggers the asynchronous download of images from metadata."""
    if not metadata:
        print("No image metadata provided to download.")
        return
    asyncio.run(_run_downloads(metadata=metadata))


async def _run_downloads(metadata: list):
    """Runs the image download tasks concurrently."""
    async with aiohttp.ClientSession() as session:
        tasks = [download_one_image(session, item) for item in metadata]
        await asyncio.gather(*tasks, return_exceptions=True)

    print("All downloads complete.")


async def download_one_image(session: aiohttp.ClientSession, image_data: dict):
    """Downloads and saves a single image asynchronously."""
    image_url = image_data.get("url") or image_data.get("hdurl")
    if not image_url:
        print(f"No URL found for date {image_data['date']}.")
        return

    try:
        async with session.get(image_url) as response:
            response.raise_for_status()
            image_bytes = await response.read()
            filename = f"{image_data['date']}_{image_url.split('/')[-1]}"
            filepath = OUTPUT_IMAGES_DIR / filename

            with open(filepath, "wb") as f:
                f.write(image_bytes)
            print(f"Successfully downloaded {filename}")
    except Exception as e:
        print(f"An error occurred while downloading for date {image_data['date']}: {e}")


def main():
    OUTPUT_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    metadata = get_apod_metadata(
        start_date="2025-07-01",
        end_date="2025-07-15",
        api_key=API_KEY,
    )
    download_apod_images(metadata=metadata)


if __name__ == "__main__":
    main()
