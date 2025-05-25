from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def scrape_full_page(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        html = page.content()
        browser.close()

        soup = BeautifulSoup(html, "html.parser")
        text_elements = soup.find_all(["p", "li", "h1", "h2", "h3"])
        return "\n".join([e.get_text(strip=True) for e in text_elements if e.text.strip()])
