import requests
import json
import os

WEBHOOK = os.environ["https://discord.com/api/webhooks/1482283053517635727/Gm78jbF1vKmnseZLraPJB-8yYoTZn1P3fMI536s6lFhrM1tQ3_I-_nRwKe2_UUxgMjOa"]
PRICE_LIMIT = 20000
MARKETS = [
    ("DE","Germany"),
    ("NL","Netherlands")
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
    with open(DATA_FILE,"w") as f:
        json.dump(data,f)

def get_inventory(market):
    url = "https://www.tesla.com/inventory/api/v1/inventory-results"
    payload = {
        "query":{
            "model":"m3",
            "condition":"used",
            "arrangeby":"Price",
            "market":market,
            "language":"en",
            "range":0,
            "offset":0,
            "count":50
        }
    }
    r = requests.post(url,json=payload)
    data = r.json()
    cars = []
    for car in data["results"]:
        price = car["price"]
        cars.append({
            "vin":car["VIN"],
            "price":price,
            "url":"https://www.tesla.com"+car["VehicleUrl"]
        })
    return cars

def check():
    old = load_data()
    new = {}
    for market,market_name in MARKETS:
        cars = get_inventory(market)
        for car in cars:
            vin = car["vin"]
            price = car["price"]
            new[vin] = price
            old_price = old.get(vin)
            if price <= PRICE_LIMIT:
                if old_price is None:
                    send_discord(
                        f"""🚗 NOWA TESLA ≤20k
Cena: €{price}
Rynek: {market_name}
{car['url']}"""
                    )
                elif price < old_price:
                    send_discord(
                        f"""📉 SPADEK CENY
€{old_price} → €{price}
Rynek: {market_name}
{car['url']}"""
                    )
    save_data(new)

check()
