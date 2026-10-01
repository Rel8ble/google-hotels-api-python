# Google Hotels API in Python: scrape hotel prices, ratings and amenities from Google Hotels to JSON/CSV

A short tutorial for pulling **Google Hotels search results** (nightly price, total stay price with taxes, deal badge, rating, review count, star class, amenities, coordinates, nearby places) into Python with the [Google Hotels Scraper](https://apify.com/rel8ble/google-hotels-scraper) on Apify. Google has no public Hotels API; this works as an unofficial one.

> Disclosure: I built this actor; it's a paid tool on Apify ($3.50 per 1,000 hotels). The code in this repo is MIT-licensed.

## How it works

The actor requests the Google Hotels results page over plain HTTPS through Apify Proxy and parses the structured data Google already embeds in it. No headless browser, no cookies, no Google account. It pages through results until it reaches `maxResults` and removes duplicates across pages.

## Quick start (Python)

```bash
pip install apify-client
```

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")

run = client.actor("rel8ble/google-hotels-scraper").call(run_input={
    "queries": ["hotels in Paris", "hotels near Times Square"],
    "checkIn": "2026-11-12",
    "checkOut": "2026-11-15",
    "adults": 2,
    "currency": "USD",
    "maxResults": 20,
})

for h in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(h["pricePerNight"], h["totalPrice"], h["rating"], h["name"])
```

[`example.py`](example.py) is the runnable version: it keeps 4-star-and-up hotels rated 4.0+, ranks them by nightly price and writes a CSV.

## Quick start (Node.js)

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('rel8ble/google-hotels-scraper').call({
    queries: ['hotels in Lisbon'], checkIn: '2026-11-12', checkOut: '2026-11-15', maxResults: 20,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items.length, 'hotels');
```

## Input

| Field | Default | What it does |
|---|---|---|
| `queries` | `["hotels in Charlotte"]` | Searches as a person types them: `hotels in Paris`, `hotels near Times Square`, or a hotel name |
| `checkIn` / `checkOut` | Google's pick | Stay dates, `YYYY-MM-DD`, up to 30 nights |
| `adults` | 2 | Guests, 1-12 (prices depend on occupancy) |
| `currency` | `USD` | Any ISO 4217 code: `EUR`, `GBP`, `JPY`... |
| `maxResults` | 50 | Hotels per query; `0` = all Google serves (~150-250) |
| `includeVacationRentals` | `false` | Also return apartments and houses |
| `includeDetails` | `false` | Adds street address and phone (one extra request per hotel) |
| `language` / `country` | `en` / `us` | Google `hl` / `gl`; `country` changes which partners and prices appear |

## Output sample (one real hotel, trimmed)

```json
{
  "query": "hotels in Charlotte",
  "position": 1,
  "name": "Sonesta Select Charlotte University Research Park",
  "propertyType": "hotel",
  "pricePerNight": 75,
  "pricePerNightWithTaxes": 88,
  "currency": "USD",
  "totalPrice": 263,
  "totalPriceBeforeTaxes": 208,
  "totalTaxesAndFees": 54.5,
  "deal": "DEAL 19% less than usual",
  "checkIn": "2026-10-15",
  "checkOut": "2026-10-18",
  "nights": 3,
  "rating": 3.9,
  "reviewCount": 915,
  "ratingBreakdown": { "5star": 433, "4star": 231, "3star": 100, "2star": 52, "1star": 99 },
  "hotelClass": 3,
  "latitude": 35.3072356,
  "longitude": -80.7534261,
  "checkInTime": "4:00 PM",
  "checkOutTime": "11:00 AM",
  "amenities": ["Breakfast ($)", "Free Wi-Fi", "Parking ($)", "Pool", "Air conditioning", "Pet-friendly", "Fitness center", "Restaurant"],
  "nearbyPlaces": [
    { "name": "Charlotte Douglas International Airport", "type": "airport",
      "transport": [{ "mode": "car", "duration": "24 min" }, { "mode": "transit", "duration": "1 hr 26 min" }] }
  ],
  "entityToken": "ChYIl4r5ruWLqpcWGgovbS8wejlfbDlqEAE",
  "googleMapsUrl": "https://www.google.com/maps?cid=16387801168794899843"
}
```

Each row has about 40 fields in total, including the description, official website, thumbnail and up to 10 photos, the Google Hotels URL and the Maps feature ID.

## Use cases

- **Hotel price monitoring**: schedule the same query and dates daily and track `pricePerNight` by `entityToken` (it stays stable across runs).
- **Rate-parity and revenue checks**: compare your property's Google "from" price against the competitive set around it.
- **Trip planning tools**: filter by `hotelClass`, `rating` and `amenities`, then rank by `totalPrice` for the whole stay.
- **Market research**: map a city's supply and pricing with `latitude` / `longitude` and `ratingBreakdown`.

## Price

**$3.50 per 1,000 hotels**, pay per result. No start fee, no monthly rental. Apify's free plan includes $5 of monthly credit.

## Limits

- About 150-250 unique hotels per query; Google stops serving new ones after that. Split big cities into areas (`hotels in Shinjuku`, `hotels in Shibuya`...).
- Prices are Google's lowest "from" rate across booking partners for your dates and occupancy. Properties with no availability come back with `pricePerNight: null`.
- Street address and phone need `includeDetails` (slower, more proxy traffic).
- Amenity and deal labels follow `language` and are most complete with `en`.
- Per-partner price lists (Booking.com vs Expedia vs direct) and review texts are not included.

## Links

- Actor on the Apify Store: https://apify.com/rel8ble/google-hotels-scraper
- Apify Python client docs: https://docs.apify.com/api/client/python

## License

MIT
