# CNBC Article Extraction and SQL Analysis

This project is an end-to-end news data pipeline built using Python, BeautifulSoup, JSON, and MySQL. The system automatically scrapes CNBC news articles, cleans and structures the extracted content, stores the data in JSON format, and inserts it into a MySQL database for further analysis and NLP applications.

## Features

- CNBC article web scraping
- Headline and body content extraction
- Article URL extraction
- Published date and time extraction
- Image URL and caption extraction
- JSON dataset generation
- MySQL database integration
- CSV export of final SQL table
- Secure database configuration using `.env`

## Technologies Used

- Python
- BeautifulSoup
- Requests
- MySQL
- JSON
- dotenv
- Git & GitHub

## Database Columns

- article_no
- hash_id
- url
- headline
- body_content
- published_at_date
- published_at_time
- scraped_at_date
- scraped_at_time
- image_url
- image_caption

## Workflow

```text
CNBC URLs
   ↓
Web Scraping
   ↓
JSON Dataset
   ↓
MySQL Database
   ↓
CSV Export
