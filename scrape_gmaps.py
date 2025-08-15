import os
import time
import random
import pandas as pd
from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent
def scrape_google_maps(search_query, no_of_result = 10):
    with sync_playwright() as p:
        user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/111.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Version/13.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Opera/77.0.4054.90 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Brave/1.37.109 Chrome/111.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"] 

        proxy = {
            "server" : "https://gate.decodo.com:7000",
            "username" : "user-spw50bkk9l-country-us-city-san_francisco",
            "password" : "gKzbT~V2xb9c5kk0Yb"
               }
        results = []
        user_data_dir = os.path.join(os.getcwd(), "playwright_data")
        ua = UserAgent()
        user_agent = ua.random
        browser = p.chromium.launch_persistent_context( user_data_dir =  user_data_dir,
                                    headless=False,
                                    user_agent=random.choice(user_agent))
        page = browser.new_page()
        page.goto("https://maps.google.com", wait_until="load")
        page.wait_for_timeout(4000)
        page.mouse.move(random.randint(100,400), random.randint(100,400))
        page.screenshot(path='map.png', full_page=True)
        search_box= page.locator('#searchboxinput')
        page.wait_for_selector('#searchboxinput', state='visible', timeout=600000)
        search_box.scroll_into_view_if_needed()
        search_box.click()
        search_box.fill(search_query)
        search_box.press('Enter')
        count = 0 
        page.wait_for_timeout(random.randint(3000,6000))

        for x in range(no_of_result):
                button = page.locator("a.hfpxzc").nth(x)
                page.hover("a.hfpxzc")
                name = str(button.get_attribute("aria-label")).replace('"','')
                page.mouse.wheel(0,random.randint(70,150))
                button.scroll_into_view_if_needed()
                button.click()
                #You can ajdust the timeout here to make it faster or slower 
                page.wait_for_timeout(random.randint(1000,3000))

                #Parsing search results
                if page.locator("div.rogA2c:not(.ITvuef) div.Io6YTe"):
                    addr=page.locator("div.rogA2c:not(.ITvuef) div.Io6YTe").first.inner_text().replace('"','')
                else:
                     addr = ''
                if page.query_selector('div.AeaXub:has(span.NhBTye) div.Io6YTe'):
                     phone = page.query_selector('div.AeaXub:has(span.NhBTye) div.Io6YTe').inner_text()
                else:
                     phone =''
                if page.query_selector('div.AeaXub:has(.ITvuef) div.Io6YTe'):
                    website = page.query_selector('div.AeaXub:has(.ITvuef) div.Io6YTe').inner_text()
                else:
                     website=''
                count+=1
                results.append({"Name":name, "Address": addr, "Phone No":phone, "Website":website})
        print(f'Found {count} results')
        return results    
search_query = input(">>Please enter your search query: ")
search_results = int(input(">>Please enter your desired number of results: "))
scraped_data = scrape_google_maps(search_query,search_results)
df = pd.DataFrame(scraped_data)
df.to_csv("Google maps data", index=False, encoding="utf-8")

