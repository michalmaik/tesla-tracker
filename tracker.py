import requests
import json

WEBHOOK = "https://discord.com/api/webhooks/1482283053517635727/Gm78jbF1vKmnseZLraPJB-8yYoTZn1P3fMI536s6lFhrM1tQ3_I-_nRwKe2_UUxgMjOa"
PRICE_LIMIT = 20000
MARKETS = [
    ("DE", "Germany"),
    ("NL", "Netherlands")
]
DATA_FILE = "inventory.json"

def send_discord(msg):
    requests.post(WEBHOOK, json={"content": msg})

def load_data():
    try:
        with open(DATA_FILE) as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def get_inventory(market):
    url = "https://www.tesla.com/inventory/api/v1/inventory-results"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
    }
    params = {
        "query": json.dumps({
            "model": "m3",
            "condition": "used",
            "arrangeby": "Price",
            "market": market,
            "language": "en",
            "range": 0,
            "offset": 0,
            "count": 50
        })
    }
    r = requests.get(url, params=params, headers=headers)
    if r.status_code != 200 or not r.text:
        print(f"Błąd API dla {market}: status {r.status_code}")
        return []
    data = r.json()
    cars = []
    for car in data.get("results", []):
        price = car.get("Price") or car.get("price")
        vin = car.get("VIN") or car.get("vin")
        vehicle_url = car.get("VehicleUrl", "")
        if price and vin:
            cars.append({
                "vin": vin,
                "price": price,
                "url": "https://www.tesla.com" + vehicle_url
            })
    return cars

def check():
    old = load_data()
    new = {}
    for market, market_name in MARKETS:
        cars = get_inventory(market)
        for car in cars:
            vin = car["vin"]
            price = car["price"]
            new[vin] = price
            old_price = old.get(vin)
            if price <= PRICE_LIMIT:
                if old_price is None:
                    send_discord(
                        f"🚗 NOWA TESLA ≤20k\nCena: €{price}\nRynek: {market_name}\n{car['url']}"
                    )
                elif price < old_price:
                    send_discord(
                        f"📉 SPADEK CENY\n€{old_price} → €{price}\nRynek: {market_name}\n{car['url']}"
                    )
    save_data(new)

check()
