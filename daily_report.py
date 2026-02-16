import os
import requests
import datetime

# دریافت اطلاعات از گیت‌هاب
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_heartbeat():
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("❌ توکن یا چت آیدی پیدا نشد.")
        return

    # گرفتن زمان فعلی
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    message = (
        "💓 **گزارش وضعیت روزانه**\n\n"
        "✅ ربات کاملاً سالم و فعال است.\n"
        "📅 تاریخ سرور: " + now + "\n"
        "🔍 وضعیت: در حال چک کردن دائم برای CENT@HOME...\n\n"
        "شبت بخیر! فردا هم بیدارم. 🌙"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    
    try:
        requests.post(url, data=payload)
        print("✅ گزارش روزانه ارسال شد.")
    except Exception as e:
        print(f"❌ خطا در ارسال: {e}")

if __name__ == "__main__":
    send_heartbeat()
