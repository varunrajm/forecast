from playwright.sync_api import sync_playwright
import time

def capture_dashboard():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:3000/dashboard")
        
        # Wait for the page to load
        page.wait_for_selector("input[type='file']")
        
        # Upload the file
        file_path = r"h:\your-project-folder\future interns\task-1\frontend\public\sample_data\retail_sales_sample.csv"
        page.set_input_files("input[type='file']", file_path)
        
        # Click the Generate forecast button (it might be the only submit button or have specific text)
        page.click("button[type='submit']")
        
        # Wait for the charts to appear. We can wait for the recharts-wrapper class or simply wait 10 seconds.
        print("Waiting for forecast to generate...")
        try:
            page.wait_for_selector(".recharts-wrapper", timeout=30000)
            # Give it a bit more time for animations to finish
            time.sleep(2)
        except Exception as e:
            print("Charts didn't appear in time:", e)
        
        # Take screenshot
        page.screenshot(path=r"C:\Users\om\.gemini\antigravity-ide\brain\23a2cf38-f131-4257-8e1b-6fb12d2a1e31\filled_dashboard.png", full_page=True)
        print("Screenshot saved.")
        browser.close()

if __name__ == "__main__":
    capture_dashboard()
