import requests
import os
import json
import time
from datetime import datetime

# ── CONFIG ─────────────────────────────────────────────────────────────────
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID   = os.environ.get("TELEGRAM_CHAT_ID")

# FirstCry Hot Wheels URLs to monitor
TARGETS = [
    {
        "name": "🏎️ All Hot Wheels",
        "url": "https://www.firstcry.com/hot-wheels/5/94/113",
    },
    {
        "name": "🚗 Die-Cast Models",
        "url": "https://www.firstcry.com/toy-cars,-trains-and-vehicles/hotwheels/die-cast-models?cid=5&scid=94&character-shop=t5-7701&sub-type=t6-7966",
    },
    {
        "name": "🏁 Race Tracks & Sets",
        "url": "https://www.firstcry.com/toy-cars,-trains-and-vehicles/race-tracks-and-playsets/hotwheels?cid=5&scid=94&type=t1-16859&character-shop=t5-7701",
    },
    {
        "name": "🚛 Monster Trucks",
        "url": "https://www.firstcry.com/toy-cars,-trains-and-vehicles/cars-and-jeeps/hot-wheels?cid=5&scid=94&type=t1-7973&brand=113",
    },
]

# Keywords that mean IN STOCK on FirstCry
IN_STOCK_KEYWORDS  = ["add to cart", "buy & earn", "club cash upto", "add to bag"]
# Keywords that mean OUT OF STOCK on FirstCry
OUT_STOCK_KEYWORDS = ["notify me", "out of stock", "sold out", "coming soon"]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-IN,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

STATE_FILE = "last_state.json"

# ── HELPERS ────────────────────────────────────────────────────────────────

def send_telegram(message: str):
    """Send a message via Telegram bot."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️  Telegram credentials not set. Skipping notification.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False,
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        if r.status_code == 200:
            print("✅ Telegram notification sent!")
        else:
            print(f"❌ Telegram error: {r.status_code} — {r.text}")
    except Exception as e:
        print(f"❌ Telegram request failed: {e}")


def check_stock(url: str) -> dict:
    """Fetch a FirstCry page and detect stock status."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        html = resp.text.lower()

        matched_in  = [kw for kw in IN_STOCK_KEYWORDS  if kw in html]
        matched_out = [kw for kw in OUT_STOCK_KEYWORDS if kw in html]

        if matched_in:
            return {"status": "IN_STOCK",     "keywords": matched_in}
        elif matched_out:
            return {"status": "OUT_OF_STOCK", "keywords": matched_out}
        else:
            return {"status": "UNKNOWN",      "keywords": []}

    except Exception as e:
        return {"status": "ERROR", "error": str(e), "keywords": []}


def load_state() -> dict:
    """Load previous stock states from file."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_state(state: dict):
    """Save current stock states to file."""
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


# ── MAIN ───────────────────────────────────────────────────────────────────

def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'='*50}")
    print(f"  FirstCry Hot Wheels Monitor — {now}")
    print(f"{'='*50}")

    prev_state = load_state()
    curr_state = {}
    found_items = []

    for target in TARGETS:
        name = target["name"]
        url  = target["url"]
        print(f"\n🔍 Checking {name}...")

        result = check_stock(url)
        status = result["status"]
        curr_state[name] = status

        prev_status = prev_state.get(name, "UNKNOWN")

        print(f"   Status   : {status}")
        print(f"   Keywords : {result.get('keywords', [])}")
        print(f"   Previous : {prev_status}")

        # Alert if newly in stock (wasn't in stock before)
        if status == "IN_STOCK" and prev_status != "IN_STOCK":
            print(f"   🔥 NEW STOCK DETECTED!")
            found_items.append({"name": name, "url": url})

        elif status == "IN_STOCK":
            print(f"   ✅ Still in stock (already notified)")

        time.sleep(2)  # Small delay between requests to be polite

    # Send a single Telegram message if any new stock found
    if found_items:
        lines = ["🔥 *HOT WHEELS RESTOCK ALERT!*", ""]
        for item in found_items:
            lines.append(f"✅ *{item['name']}* is now available!")
            lines.append(f"👉 [Shop Now]({item['url']})")
            lines.append("")
        lines.append("⚡ _Hurry — limited stock on FirstCry!_")
        message = "\n".join(lines)
        send_telegram(message)
    else:
        print("\n📭 No new stock found this run.")
        # Optional: send a daily heartbeat so you know it's working
        # Uncomment the lines below if you want a daily "still watching" message
        # hour = datetime.now().hour
        # if hour == 9:  # 9 AM heartbeat
        #     send_telegram("👀 *Hot Wheels Monitor* is running. No stock yet — still watching!")

    save_state(curr_state)
    print(f"\n✅ Run complete. State saved.\n")


if __name__ == "__main__":
    main()
