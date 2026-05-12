import requests
from bs4 import BeautifulSoup
import time
import random

BASE_URL = "https://www.cnbc.com"

SECTIONS = [
    "world",
    "business",
    "markets",
    "technology",
    "politics",
    "economy"
]

SITEMAP_INDEX = "https://www.cnbc.com/sitemapAll.xml"

MAX_PAGES = 20
DELAY = (1, 3)

HEADERS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)"
]

def get_headers():
    return {"User-Agent": random.choice(HEADERS)}

def request(url):
    try:
        return requests.get(url, headers=get_headers(), timeout=10)
    except:
        return None

def sleep():
    time.sleep(random.uniform(*DELAY))

def scrape_sections():
    links = set()

    for section in SECTIONS:
        print(f"\n[SECTION] {section}")

        for page in range(1, MAX_PAGES + 1):
            url = f"{BASE_URL}/{section}/?page={page}"
            res = request(url)

            if not res or res.status_code != 200:
                print("Failed:", url)
                continue

            soup = BeautifulSoup(res.text, "html.parser")

            for a in soup.find_all("a", href=True):
                href = a["href"]

                if href.startswith("https://www.cnbc.com") and href.endswith(".html"):
                    links.add(href.split("?")[0])

            print(f"Page {page} → {len(links)} links")
            sleep()

    return links

def parse_sitemap(url):
    res = request(url)
    if not res:
        return []

    soup = BeautifulSoup(res.text, "xml")

    sitemaps = soup.find_all("sitemap")
    if sitemaps:
        return [tag.loc.text.strip() for tag in sitemaps]

    urls = soup.find_all("url")
    return [tag.loc.text.strip() for tag in urls]

def scrape_sitemaps():
    all_links = set()

    print("\n[SITEMAP] Fetching index...")
    sitemap_list = parse_sitemap(SITEMAP_INDEX)

    print(f"Found {len(sitemap_list)} sitemap files")

    for sm in sitemap_list:
        print("Processing:", sm)

        urls = parse_sitemap(sm)

        for link in urls:
            if link.endswith(".html"):
                all_links.add(link)

        print(f"Collected {len(all_links)} links so far")
        sleep()

    return all_links

if __name__ == "__main__":
    print("Starting CNBC scraper...\n")

    section_links = scrape_sections()
    sitemap_links = scrape_sitemaps()

    all_links = section_links.union(sitemap_links)

    print(f"\nTotal unique links: {len(all_links)}")

    with open("cnbc_links.txt", "w", encoding="utf-8") as f:
        for link in sorted(all_links):
            f.write(link + "\n")

    print("Saved to cnbc_links.txt")