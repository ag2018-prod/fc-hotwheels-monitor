# 🔥 FirstCry Hot Wheels Monitor — Setup Guide
### Telegram alerts, 24/7, even when your phone & PC are off

---

## WHAT YOU'LL NEED
- A free GitHub account → https://github.com
- A Telegram account (you already have it)
- 10 minutes

---

## STEP 1 — Create Your Telegram Bot (2 min)

1. Open Telegram and search for **@BotFather**
2. Send the message:  `/newbot`
3. BotFather will ask for a name → type anything e.g. `HotWheels Notifier`
4. Then ask for a username → type something like `hotwheels_firstcry_bot`
5. BotFather will reply with your **Bot Token** — it looks like:
   ```
   7412345678:AAFxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
   → **Copy and save this token!**

6. Now open your new bot in Telegram and press **START**

7. To get your Chat ID, open this URL in your browser
   (replace YOUR_TOKEN with your actual token):
   ```
   https://api.telegram.org/botYOUR_TOKEN/getUpdates
   ```
   Look for `"id"` inside `"chat"` — that number is your **Chat ID**
   Example: `"chat": { "id": 123456789 }`

---

## STEP 2 — Create GitHub Repository (3 min)

1. Go to → https://github.com/new
2. Repository name: `firstcry-hotwheels-monitor`
3. Set to **Private** (recommended)
4. Click **Create repository**

5. Upload these 3 files to the repo:
   - `monitor.py`
   - `requirements.txt`
   - `.github/workflows/monitor.yml`

   **How to upload:**
   - Click **"uploading an existing file"** link on the repo page
   - Drag and drop `monitor.py` and `requirements.txt`
   - Click **Commit changes**

   For the workflow file:
   - Click **"Add file" → "Create new file"**
   - Type the path: `.github/workflows/monitor.yml`
   - Paste the contents of `monitor.yml`
   - Click **Commit changes**

---

## STEP 3 — Add Your Telegram Secrets (2 min)

1. In your GitHub repo, go to:
   **Settings → Secrets and variables → Actions**

2. Click **"New repository secret"** and add:

   | Name | Value |
   |------|-------|
   | `TELEGRAM_BOT_TOKEN` | Your bot token from Step 1 |
   | `TELEGRAM_CHAT_ID` | Your chat ID from Step 1 |

---

## STEP 4 — Enable GitHub Actions (1 min)

1. In your repo, click the **"Actions"** tab
2. Click **"I understand my workflows, go ahead and enable them"**
3. Click on **"FirstCry Hot Wheels Monitor"** workflow
4. Click **"Run workflow"** → **"Run workflow"** to test it manually

5. Watch the logs — you should see it checking each category
6. Check your Telegram — if anything is in stock, you'll get a message!

---

## HOW IT WORKS AFTER SETUP

```
Every 5 minutes (automatically):
  GitHub servers wake up
      ↓
  Run monitor.py
      ↓
  Check all 4 FirstCry Hot Wheels URLs
      ↓
  Stock found? → Telegram alert on your phone instantly
  No stock?   → Sleep and try again in 5 minutes
```

✅ Works 24/7
✅ Works with your phone OFF
✅ Works with your PC OFF
✅ Completely FREE (GitHub gives 2000 minutes/month free)
✅ Only alerts you when stock is NEW (not every 5 minutes)

---

## WANT TO ADD A SPECIFIC PRODUCT?

Open `monitor.py` and add to the TARGETS list:

```python
{
    "name": "🚀 Hot Wheels Premium F1 Car",
    "url": "https://www.firstcry.com/your-specific-product-url",
},
```

---

## TROUBLESHOOTING

**Not getting Telegram messages?**
- Double-check your Bot Token and Chat ID in GitHub Secrets
- Make sure you pressed START on your bot in Telegram
- Run the workflow manually and check the logs in GitHub Actions

**Workflow not running?**
- GitHub sometimes delays scheduled workflows by up to 15 min
- Make sure Actions are enabled in your repo settings

**False alerts / missed alerts?**
- FirstCry is JS-rendered — sometimes the HTML doesn't contain stock keywords
- This is a known limitation of HTTP-based scrapers
- For 100% accuracy, upgrade to a Playwright-based script (ask me!)

---

## YOUR URLS AT A GLANCE

| Category | URL |
|----------|-----|
| All Hot Wheels | https://www.firstcry.com/hot-wheels/5/94/113 |
| Die-Cast Models | https://www.firstcry.com/toy-cars,-trains-and-vehicles/hotwheels/die-cast-models?cid=5&scid=94&character-shop=t5-7701&sub-type=t6-7966 |
| Race Tracks & Sets | https://www.firstcry.com/toy-cars,-trains-and-vehicles/race-tracks-and-playsets/hotwheels?cid=5&scid=94&type=t1-16859&character-shop=t5-7701 |
| Monster Trucks | https://www.firstcry.com/toy-cars,-trains-and-vehicles/cars-and-jeeps/hot-wheels?cid=5&scid=94&type=t1-7973&brand=113 |
