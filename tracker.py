import requests
import json
from bs4 import BeautifulSoup

WEBHOOK = "https://discord.com/api/webhooks/1482283053517635727/Gm78jbF1vKmnseZLraPJB-8yYoTZn1P3fMI536s6lFhrM1tQ3_I-_nRwKe2_UUxgMjOa"
VIN = "LRW3E7FA9LC105966"
DATA_FILE = "inventory.json"
EV_URL = "https://ev-inventory.com/car/NL-LRW3E7FA9LC105966"
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
    r = requests.get(EV_URL, headers={"User-Agent": "Mozilla/5.0"})
    if r.status_code != 200:
        print(f"Błąd: status {r.status_code}")
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    title = soup.find("title")
    if title:
        text = title.text
        import re
        match = re.search(r"€([\d,]+)", text)
        if match:
            price = int(match.group(1).replace(",", ""))
            print(f"Aktualna cena: €{price}")
            return price
    print("Nie znaleziono ceny")
    return None

def check():
    old = load_data()
    old_price = old.get(VIN)
    new_price = get_price()

    if new_price is None:
        return

    if old_price is None:
        send_discord(f"🚗 Tesla Model 3 — cena początkowa: €{new_price}\n{CAR_URL}")
    elif new_price < old_price:
        send_discord(f"📉 SPADEK CENY\n€{old_price} → €{new_price}\n{CAR_URL}")
    elif new_price > old_price:
        send_discord(f"📈 WZROST CENY\n€{old_price} → €{new_price}\n{CAR_URL}")
    else:
        print(f"Brak zmiany ceny: €{new_price}")

    save_data({VIN: new_price})

check()
```

I zaktualizuj `requirements.txt` — dodaj `beautifulsoup4`:
```
requests
beautifulsoup4
