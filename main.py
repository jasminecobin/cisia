import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --- دریافت اطلاعات از تنظیمات گیت‌هاب ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def debug_telegram():
    print("--- شروع عیب‌یابی ---")
    
    # 1. بررسی اینکه آیا توکن اصلاً وجود دارد؟
    if not TELEGRAM_TOKEN:
        print("❌ خطا: TELEGRAM_TOKEN در Secrets پیدا نشد! (خالی است)")
        return
    else:
        # چاپ 5 کاراکتر اول برای اطمینان (کل توکن را چاپ نمی‌کنیم که لو برود)
        print(f"✅ توکن خوانده شد (شروع با: {TELEGRAM_TOKEN[:5]}...)")

    if not CHAT_ID:
        print("❌ خطا: CHAT_ID در Secrets پیدا نشد! (خالی است)")
        return
    else:
        print(f"✅ چت آیدی خوانده شد: {CHAT_ID}")

    # 2. تلاش برای ارسال پیام تست
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": "🔔 تست ارتباط با تلگرام - اگر این را می‌خوانی یعنی درست شد!"}
    
    try:
        print(f"📤 در حال ارسال درخواست به: {url.replace(TELEGRAM_TOKEN, 'HIDDEN_TOKEN')}")
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
            print("⛔ خطای ناشناخته.")
            
    except Exception as e:
        print(f"❌ خطای پایتون: {e}")

if __name__ == "__main__":
    debug_telegram()

# لینک تقویم CISIA (انگلیسی)
TARGET_URL = "https://testcisia.it/calendario.php?tolc=cents&lingua=inglese"

def send_telegram(msg):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("❌ توکن تلگرام یا چت آیدی تنظیم نشده است.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=payload)

def check_cisia():
    send_telegram("سلام! من وصل هستم و دارم تست می‌کنم.")  # <--- این خط را اضافه کن
    print("🚀 شروع بررسی سایت CISIA...")
    
    
    # تنظیمات مرورگر (Headless برای سرور)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get(TARGET_URL)
        time.sleep(8)  # صبر برای لود شدن جدول جاوااسکریپتی
        
        # پیدا کردن تمام ردیف‌های جدول (tr)
        rows = driver.find_elements(By.TAG_NAME, "tr")
        
        found_seats = False
        message_body = ""

        print(f"📊 تعداد ردیف‌های پیدا شده: {len(rows)}")

        for row in rows:
            text = row.text.upper()
            
            # شرط مهم: فقط اگر آزمون آنلاین (HOME) بود چک کن
            if "CENT@HOME" in text:
                # کلماتی که نشان‌دهنده باز بودن جا هستند
                # معمولاً در سایت انگلیسی می‌نویسد: "OPEN" یا "AVAILABLE" یا "REGISTER"
                if "AVAILABLE" in text or "OPEN" in text or "REGISTER" in text:
                    found_seats = True
                    # متن ردیف را تمیز می‌کنیم تا در تلگرام خوانا باشد
                    clean_text = text.replace('\n', ' | ')
                    message_body += f"✅ {clean_text}\n\n"
                    print(f"🎉 پیدا شد: {clean_text}")

        if found_seats:
            final_msg = f"🚨 **ظرفیت CENT@HOME باز شد!** 🚨\n\n{message_body}\n🔗 لینک ثبت‌نام:\n{TARGET_URL}"
            send_telegram(final_msg)
        else:
            print("❌ هیچ جای خالی برای CENT@HOME پیدا نشد.")

    except Exception as e:
        print(f"❌ خطا در اجرای بات: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    check_cisia()
