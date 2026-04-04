from playwright.sync_api import sync_playwright
import time

URL = "https://splitlogic.streamlit.app" 

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    
    print(f"Mengunjungi {URL} ...")
    page.goto(URL, wait_until="networkidle")
    
    time.sleep(10)
    
    print("Berhasil mengunjungi dan menahan koneksi. Streamlit aman!")
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
