import requests
import json

WEBHOOK = "https://discord.com/api/webhooks/1482283053517635727/Gm78jbF1vKmnseZLraPJB-8yYoTZn1P3fMI536s6lFhrM1tQ3_I-_nRwKe2_UUxgMjOa"
SCRAPER_API_KEY = "0e8de61fa7b7a1ea1dd31a94478e797d"
VIN = "LRW3E7FA9LC105966"
MARKET = "NL"
DATA_FILE = "inventory.json"
CAR_URL = "https://www.tesla.com/nl_NL/m3/order/LRW3E7FA9LC105966?titleStatus=used&redirect=no#overview"

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

def get_price():
    target_url = "https://www.tesla.com/inventory/api/v1/inventory-results?query=" + \
        json.dumps({
            "model": "m3",
            "condition": "used",
            "market": MARKET,
            "language": "en",
            "vin": VIN,
            "range": 0,
            "offset": 0,
            "count": 1
        })
    url = f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={requests.utils.quote(target_url)}"
    r = requests.get(url, timeout=60)
    if r.status_code != 200 or not r.text:
        print(f"Błąd API: status {r.status_code}")
        return None
    data = r.json()
    results = data.get("results", [])
    if not results:
        print("Nie znaleziono auta")
        return None
    car = results[0]
    price = car.get("Price") or car.get("price")
    print(f"Aktualna cena: €{price}")
    return price

def check():
    old = load_data()
    old_price = old.get(VIN)
    new_price = get_price()

    if new_price is None:
        return

    if old_price is None:
        send_discord(
            f"🚗 Tesla Model 3 — cena początkowa: €{new_price}\n{CAR_URL}"
        )
    elif new_price < old_price:
        send_discord(
            f"📉 SPADEK CENY\n€{old_price} → €{new_price}\n{CAR_URL}"
        )
    elif new_price > old_price:
        send_discord(
            f"📈 WZROST CENY\n€{old_price} → €{new_price}\n{CAR_URL}"
        )
    else:
        print(f"Brak zmiany ceny: €{new_price}")

    save_data({VIN: new_price})

check()
