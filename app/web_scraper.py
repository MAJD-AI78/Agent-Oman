# web_scraper.py
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import requests

HEADERS = {"User-Agent": "Mozilla/5.0"}

def scrape_google(query):
    try:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        res = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")
        snippets = soup.select(".BNeawe.s3v9rd.AP7Wnd")
        return "\n".join([s.text for s in snippets[:5]])
    except Exception as e:
        return f"❌ Google scraping failed: {e}"

def scrape_full_page(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.goto(url, timeout=60000)
            html = page.content()
            browser.close()

        soup = BeautifulSoup(html, "html.parser")
        text_elements = soup.find_all(["p", "li", "h1", "h2", "h3"])
        return "\n".join([e.get_text(strip=True) for e in text_elements if e.get_text(strip=True)])
    except Exception as e:
        return f"❌ Error scraping page: {str(e)}"