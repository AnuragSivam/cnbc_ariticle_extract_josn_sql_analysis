import json
import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "Anurag@1729",
    "database": "article_db3",
    "port": 3306,
    "auth_plugin": "mysql_native_password"
}

JSON_FILE = r"C:\Users\Asus\Desktop\sentiment_analysis1\cnbc_articles_clean.json"

try:

    conn = mysql.connector.connect(**DB_CONFIG)

    cursor = conn.cursor()

    print("Connected to MySQL")

    cursor.execute("""

        CREATE DATABASE IF NOT EXISTS article_db3

    """)

    cursor.execute("""

        USE article_db3

    """)

    cursor.execute("""

        DROP TABLE IF EXISTS articles_news1

    """)

    cursor.execute("""

        CREATE TABLE articles_news1 (

            article_no VARCHAR(20) PRIMARY KEY,

            hash_id VARCHAR(100),

            url TEXT,

            headline TEXT,

            body_content LONGTEXT,

            published_at_date DATE,

            published_at_time TIME,

            scraped_at_date DATE,

            scraped_at_time TIME,

            image_url LONGTEXT,

            image_caption TEXT

        )

    """)

    print("Table created successfully")

    with open(JSON_FILE, "r", encoding="utf-8") as f:

        data = json.load(f)

    inserted = 0
    failed = 0

    for item in data:

        try:

            image_urls = []

            image_data = item.get("image_url", [])

            if isinstance(image_data, list):

                for img in image_data:

                    if isinstance(img, dict):

                        image_urls.append(img.get("url"))

            image_urls_json = json.dumps(
                image_urls,
                ensure_ascii=False
            )

            cursor.execute("""

                INSERT INTO articles_news1 (

                    article_no,
                    hash_id,
                    url,
                    headline,
                    body_content,
                    published_at_date,
                    published_at_time,
                    scraped_at_date,
                    scraped_at_time,
                    image_url,
                    image_caption

                )

                VALUES (

                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s

                )

            """, (

                item.get("article_no"),
                item.get("hash_id"),
                item.get("url"),
                item.get("headline"),
                item.get("body_content"),
                item.get("published_at_date"),
                item.get("published_at_time"),
                item.get("scraped_at_date"),
                item.get("scraped_at_time"),
                image_urls_json,
                item.get("image_caption")

            ))

            inserted += 1

            print(f"Inserted: {item.get('article_no')}")

        except Exception as e:

            failed += 1

            print("Insert Error:", e)

    conn.commit()

    print("\nFINAL REPORT")
    print("Inserted :", inserted)
    print("Failed   :", failed)

    print("\nSTORED DATA\n")

    cursor.execute("""

        SELECT
            article_no,
            hash_id,
            url,
            headline,
            published_at_date,
            published_at_time
        FROM articles_news1
        LIMIT 20

    """)

    rows = cursor.fetchall()

    for row in rows:

        print(row)

except Error as e:

    print("MYSQL ERROR:", e)

except Exception as e:

    print("GENERAL ERROR:", e)

finally:

    try:

        if conn.is_connected():

            cursor.close()
            conn.close()

            print("\nMySQL connection closed")

    except:
        pass 