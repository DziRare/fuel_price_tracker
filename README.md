# fuel_price_tracker
Track and compare the price of fuel
 # FuelFinder

A full-stack web app that helps you find the cheapest fuel prices near any location in NSW, Australia. Enter a location, pick a fuel type, choose a radius, and see all nearby petrol stations plotted on an interactive map — sorted by price.

Built with Python, FastAPI, and vanilla JavaScript with no frontend framework.

## Features

- Search for fuel prices by location (any NSW address or suburb), fuel type (Unleaded 91, Premium 95/98, Ethanol 10, Diesel, Premium Diesel, LPG, Electric Charging), and radius (1–100km)
- Interactive Leaflet map with custom fuel-pump markers showing each station
- Click any marker to see the station name, price, and distance from your search location
- Horizontally scrollable fuel-type selector with arrow buttons and dynamic fade indicators
- Real-time data sourced from the official NSW Government FuelCheck API

## Stack

**Backend**
- Python 3.14
- FastAPI for the REST API
- Uvicorn as the ASGI server
- geopy (Nominatim) for geocoding user input
- NSW FuelCheck API for live fuel price data
- uv for dependency management

**Frontend**
- Vanilla HTML, CSS, and JavaScript (no framework)
- Leaflet for the interactive map
- MapTiler for the map tiles

## Project structure

```
fuel_price_tracker/
├── backend/
│   ├── api.py            # FastAPI app and endpoints
│   ├── main.py           # CLI entry point and data formatting
│   ├── fuel_api.py       # NSW FuelCheck API client
│   ├── pyproject.toml    # Python dependencies
│   └── .env              # API credentials (not committed)
└── frontend/
    ├── index.html        # Page structure
    ├── styles.css        # Styling
    ├── map.js            # Map setup, API calls, marker rendering
    ├── ui.js             # Scroll buttons and fade logic
    └── assets/           # Logo and images
```

## Getting started

### Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) for Python dependency management
- A web browser
- API credentials for the [NSW FuelCheck API](https://api.nsw.gov.au/Product/Index/22) (free, requires registration)
- A [MapTiler](https://www.maptiler.com/) API key (free tier available)

### Backend setup

```bash
cd backend
uv sync
```

Create a `.env` file in the `backend/` folder with your NSW API credentials:

```
API_KEY=your_nsw_api_key
API_SECRET=your_nsw_api_secret
```

Start the API server:

```bash
uv run uvicorn api:app --reload
```

The backend will run at `http://127.0.0.1:8000`. You can view the auto-generated API docs at `http://127.0.0.1:8000/docs`.

### Frontend setup

Add your MapTiler key to `frontend/map.js` (replace the existing `key` value):

```javascript
const key = 'your_maptiler_key';
```

Open `frontend/index.html` in your browser. With the backend running, you can submit the search form to see live fuel prices.

### CLI mode

The backend can also be run as a CLI tool for quick lookups without the frontend:

```bash
cd backend
uv run python main.py
```

It will prompt you for a location, fuel type, and radius, then print results to the terminal.

## API endpoints

### `GET /stations`

Returns nearby fuel stations matching the search criteria.

**Query parameters**
- `location` (string) — any address or place name in NSW
- `fuel_type` (string) — one of `U91`, `P95`, `P98`, `E10`, `DL`, `PDL`, `LPG`, `EV`
- `distance` (integer) — search radius in kilometres (1–100)

**Example**

```
GET /stations?location=Town+Hall+Sydney&fuel_type=U91&distance=5
```

**Response**

```json
[
  {
    "name": "Caltex Sydney CBD",
    "address": "123 George St, Sydney NSW",
    "latitude": -33.8688,
    "longitude": 151.2093,
    "distance": 0.3,
    "fuel_type": "U91",
    "price": 189.9
  }
]
```

Results are sorted by price ascending.

## Roadmap

Planned improvements for v2:

- Fetch locations for more states
- Refactor in-memory data flow to remove file-based state passing between functions
- Add error handling for invalid locations and API failures
- Implement access-token refresh for long-running sessions
- Add price history tracking using SQLite (daily snapshots)
- "Should I fill up now?" recommendations based on local price cycles
- Cheapest-station highlighting on the map
- Deploy to a public URL

## Acknowledgements

- [NSW Government FuelCheck](https://www.fuelcheck.nsw.gov.au/) for the public fuel price API
- [MapTiler](https://www.maptiler.com/) for map tiles
- [OpenStreetMap](https://www.openstreetmap.org/) contributors

## License

MIT