import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# --- دریافت اطلاعات حساس از تنظیمات گیت‌هاب ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
TARGET_URL = "https://example.com/login" # لینک سایت هدف
BUTTON_TEXT_TO_FIND = "Book"

def send_telegram_alert(message):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("❌ توکن تلگرام تنظیم نشده است.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
        print("✅ پیام تلگرام ارسال شد.")
    except Exception as e:
        print(f"❌ خطا در ارسال پیام: {e}")

def run_check():
    # تنظیمات مرورگر برای اجرا در سرور (Headless)
    chrome_options = Options()
    chrome_options.add_argument("--headless") # مهم: بدون نمایش گرافیکی
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    # اضافه کردن User-Agent برای اینکه سایت کمتر شک کند ربات هستیم
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        print("🚀 در حال بررسی سایت...")
        driver.get(TARGET_URL)
        time.sleep(10) # صبر برای لود کامل (در سرورها اینترنت گاهی کند است)

        # --- اگر لاگین نیاز است، اینجا کد لاگین را اضافه کن ---
        # driver.find_element(By.ID, "username").send_keys("YOUR_USER")
        # driver.find_element(By.ID, "password").send_keys("YOUR_PASS")
        # driver.find_element(By.ID, "submit").click()
        # time.sleep(5)
        
        page_source = driver.page_source
        
        if BUTTON_TEXT_TO_FIND in page_source:
            msg = f"🚨 فوری! تایم امتحان باز شد!\nمتن '{BUTTON_TEXT_TO_FIND}' پیدا شد.\nسریع چک کن!"
            print(msg)
            send_telegram_alert(msg)
        else:
            print("هنوز خبری نیست.")
            
    except Exception as e:
        print(f"❌ خطای کلی: {e}")
        # اختیاری: ارسال خطا به تلگرام تا بفهمی بات کار نمی‌کند
        # send_telegram_alert(f"بات ارور داد: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_check()
