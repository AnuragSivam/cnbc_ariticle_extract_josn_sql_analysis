import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import re
import os

def clean_text(text):

    text = re.sub(r'\s+', ' ', text)

    text = re.sub(
        r'[^A-Za-z0-9.,!?\'"()\-:/ ]+',
        '',
        text
    )

    return text.strip()

file_path = "cnbc_balanced_links1.txt"

with open(file_path, "r", encoding="utf-8") as f:

    urls = [
        line.strip()
        for line in f.readlines()
        if line.strip()
    ]

print(f"Total URLs Loaded: {len(urls)}")

headers = {
    "User-Agent": "Mozilla/5.0"
}

all_articles = []

def fetch_page(url, retries=3):

    for attempt in range(retries):

        try:

            response = requests.get(
                url,
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                return response

            else:
                print(
                    f"Status Code {response.status_code}: {url}"
                )

        except Exception as e:

            print(f"Retry {attempt + 1} Failed: {e}")

            time.sleep(2)

    return None

for idx, url in enumerate(urls, start=1):

    try:

        response = fetch_page(url)

        if not response:

            print(f"Failed: {url}")

            continue

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        headline = None
        published_date = None
        published_time = None
        image_url = None
        image_caption = None
        body_content = ""

        dt = None

        json_ld_tags = soup.find_all(
            "script",
            type="application/ld+json"
        )

        for tag in json_ld_tags:

            try:

                if not tag.string:
                    continue

                data = json.loads(tag.string)

                if isinstance(data, list):

                    for item in data:

                        if isinstance(item, dict):

                            if item.get("@type") == "NewsArticle":

                                headline = item.get("headline")

                                raw_datetime = item.get(
                                    "datePublished"
                                )

                                if raw_datetime:

                                    dt = datetime.fromisoformat(
                                        raw_datetime.replace(
                                            "Z",
                                            "+00:00"
                                        )
                                    )

                                    published_date = dt.strftime(
                                        "%Y-%m-%d"
                                    )

                                    published_time = dt.strftime(
                                        "%H:%M:%S"
                                    )

                                image_url = item.get("image")

                                break

                elif isinstance(data, dict):

                    if data.get("@type") == "NewsArticle":

                        headline = data.get("headline")

                        raw_datetime = data.get(
                            "datePublished"
                        )

                        if raw_datetime:

                            dt = datetime.fromisoformat(
                                raw_datetime.replace(
                                    "Z",
                                    "+00:00"
                                )
                            )

                            published_date = dt.strftime(
                                "%Y-%m-%d"
                            )

                            published_time = dt.strftime(
                                "%H:%M:%S"
                            )

                        image_url = data.get("image")

            except Exception as e:

                print("JSON-LD Error:", e)

        if not headline:

            h1 = soup.find("h1")

            if h1:

                headline = h1.get_text(strip=True)

        content_div = soup.find(
            "div",
            {"class": "ArticleBody-articleBody"}
        )

        if content_div:

            paragraphs = content_div.find_all("p")

        else:

            paragraphs = soup.find_all("p")

        body_content = " ".join([
            p.get_text(strip=True)
            for p in paragraphs
        ])

        body_content = clean_text(body_content)

        figure = soup.find("figure")

        if figure:

            img_tag = figure.find("img")

            if img_tag:

                if img_tag.has_attr("src"):

                    image_url = img_tag["src"]

                elif img_tag.has_attr("data-src"):

                    image_url = img_tag["data-src"]

            cap = figure.find("figcaption")

            if cap:

                image_caption = clean_text(
                    cap.get_text(strip=True)
                )

        scraped_now = datetime.now()

        scraped_date = scraped_now.strftime("%Y-%m-%d")

        scraped_time = scraped_now.strftime("%H:%M:%S")

        article_no = str(idx).zfill(3)

        if dt:

            hash_id = (
                f"cnbc-"
                f"{dt.strftime('%d%m%Y')}-"
                f"{dt.strftime('%H%M')}-"
                f"{article_no}"
            )

        else:

            hash_id = f"cnbc-unknown-{article_no}"

        article_data = {

            "article_no": article_no,

            "hash_id": hash_id,

            "url": url,

            "headline": headline,

            "body_content": body_content,

            "published_at_date": published_date,

            "published_at_time": published_time,

            "scraped_at_date": scraped_date,

            "scraped_at_time": scraped_time,

            "image_url": image_url,

            "image_caption": image_caption

        }

        all_articles.append(article_data)

        print(
            f"Done {idx}/{len(urls)}"
        )

        time.sleep(1)

    except Exception as e:

        print(f"Error at {url}: {e}")

output_file = "cnbc_articles_clean.json"

with open(
    output_file,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        all_articles,
        f,
        indent=4,
        ensure_ascii=False
    )

print("\nJSON Saved Successfully")

print(
    "Saved At:",
    os.path.abspath(output_file)
)