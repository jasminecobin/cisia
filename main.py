import os
import requests

# دریافت اطلاعات
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def debug_telegram():
    print("--- شروع عیب‌یابی ---")
    
    # 1. بررسی اینکه آیا توکن اصلاً وجود دارد؟
    if not TELEGRAM_TOKEN:
        print("❌ خطا: TELEGRAM_TOKEN در Secrets پیدا نشد! (خالی است)")
        return
    else:
        # چاپ 5 کاراکتر اول برای اطمینان
        if len(TELEGRAM_TOKEN) > 5:
            print(f"✅ توکن خوانده شد (شروع با: {TELEGRAM_TOKEN[:5]}...)")
        else:
            print("⚠️ توکن خیلی کوتاه است! احتمالاً اشتباه وارد شده.")

    if not CHAT_ID:
        print("❌ خطا: CHAT_ID در Secrets پیدا نشد! (خالی است)")
        return
    else:
        print(f"✅ چت آیدی خوانده شد: {CHAT_ID}")

    # 2. تلاش برای ارسال پیام تست
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": "🔔 تست ارتباط با تلگرام - اگر این را می‌خوانی یعنی درست شد!"}
    
    try:
        print(f"📤 در حال ارسال درخواست به تلگرام...")
        response = requests.post(url, data=payload)
        
        # 3. چاپ دقیق جواب سرور تلگرام
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 200:
            print("🎉 موفقیت! پیام باید رسیده باشد.")
        elif response.status_code == 401:
            print("⛔ خطا 401: توکن ربات اشتباه است (Unauthorized).")
        elif response.status_code == 400:
            print("⛔ خطا 400: چت آیدی اشتباه است یا ربات استارت نشده.")
        else:
            print(f"⛔ خطای ناشناخته: {response.status_code}")
            
    except Exception as e:
        print(f"❌ خطای پایتون: {e}")

if __name__ == "__main__":
    debug_telegram()
