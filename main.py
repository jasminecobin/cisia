import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
TARGET_URL = "https://testcisia.it/calendario.php?tolc=cents&lingua=inglese"

def send_telegram_photo(caption, photo_path):
    
    if not TELEGRAM_TOKEN or not CHAT_ID: return
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    
    try:
        with open(photo_path, "rb") as image_file:
            files = {"photo": image_file}
            data = {"chat_id": CHAT_ID, "caption": caption}
            
            requests.post(url, data=data, files=files)
            print("✅ عکس با موفقیت به تلگرام ارسال شد.")
    except Exception as e:
        print(f"❌ خطا در ارسال عکس: {e}")

def check_cisia():
    print("🚀 شروع بررسی سایت CISIA...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get(TARGET_URL)
        time.sleep(10) 
        
        rows = driver.find_elements(By.TAG_NAME, "tr")
        found_seats = False
        message_body = ""

        print(f"📊 تعداد ردیف‌های جدول: {len(rows)}")

        for row in rows:
            text = row.text.upper()
            if "CENT@HOME" in text:
                if "AVAILABLE" in text or "OPEN" in text or "REGISTER" in text:
                    found_seats = True
                    clean_text = text.replace('\n', ' | ')
                    message_body += f"✅ {clean_text}\n\n"
                    print(f"🎉 پیدا شد: {clean_text}")

        if found_seats:
            final_msg = f"🚨 **ظرفیت CENT@HOME باز شد!** 🚨\n\n{message_body}\n🔗 لینک ثبت‌نام:\n{TARGET_URL}"
            
            screenshot_name = "status.png"
            driver.save_screenshot(screenshot_name)
            print("📸 اسکرین‌شات گرفته شد.")
            
            send_telegram_photo(final_msg, screenshot_name)
        else:
            print("❌ هیچ جای خالی برای CENT@HOME پیدا نشد.")

    except Exception as e:
        print(f"❌ خطا: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    check_cisia()
