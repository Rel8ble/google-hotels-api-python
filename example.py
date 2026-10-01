"""Scrape Google Hotels prices and ratings with Python via the Google Hotels Scraper on Apify.

pip install -r requirements.txt
set APIFY_TOKEN in your environment (or paste it below)
python example.py
"""
import csv
import os
from datetime import date, timedelta

from apify_client import ApifyClient

client = ApifyClient(os.environ.get("APIFY_TOKEN", "<YOUR_APIFY_TOKEN>"))

check_in = date.today() + timedelta(days=30)
run_input = {
    "queries": ["hotels in Paris", "hotels in Lisbon"],
    "checkIn": check_in.isoformat(),
    "checkOut": (check_in + timedelta(days=3)).isoformat(),
    "adults": 2,
    "currency": "USD",
    "maxResults": 20,                 # you pay per hotel, keep it small while testing
}

run = client.actor("rel8ble/google-hotels-scraper").call(run_input=run_input)
hotels = list(client.dataset(run["defaultDatasetId"]).iterate_items())
print(f"Got {len(hotels)} hotels")

# 4-star and up, rated 4.0+, with a price for these dates, cheapest first
picks = [h for h in hotels
         if (h.get("hotelClass") or 0) >= 4
         and (h.get("rating") or 0) >= 4.0
         and h.get("pricePerNight") is not None]
picks.sort(key=lambda h: h["pricePerNight"])

fields = ["query", "name", "hotelClass", "rating", "reviewCount", "pricePerNight",
          "totalPrice", "currency", "deal", "latitude", "longitude", "googleHotelsUrl"]
with open("google_hotels.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
    w.writeheader()
    w.writerows(picks)

for h in picks[:5]:
    print(f"${h['pricePerNight']}/night  {h['hotelClass']}*  {h['rating']}  {h['name']}  {h.get('deal') or ''}")
print(f"Saved {len(picks)} hotels to google_hotels.csv")
