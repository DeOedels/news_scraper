import requests
from bs4 import BeautifulSoup
import feedparser
import csv
from datetime import datetime, timedelta, timezone

# list of RSS feed URLs
rss_feeds = [
    "https://news.stanford.edu/feed/",
    "https://news.mit.edu/rss",
    "https://www.caltech.edu/about/news/feed",
    "https://www.berkeley.edu/news/rss",
    "https://news.harvard.edu/gazette/feed/"
]

def get_rss_articles(feed_url):
    """Fetches article links from an RSS feed and filters them."""
    feed = feedparser.parse(feed_url)
    articles = []
    two_weeks_ago = datetime.now(timezone.utc) - timedelta(days=14)  # Make timezone-aware

    for entry in feed.entries:
        if "news" in entry.link:
            title = entry.title if "title" in entry else "No Title"
            pub_date = entry.published if "published" in entry else None
            
            # Convert date string to datetime object
            if pub_date:
                try:
                    pub_date_dt = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %z")
                    if pub_date_dt < two_weeks_ago:
                        continue  # Skip old articles
                except ValueError:
                    pass  # If date can't be parsed, keep the article

            articles.append((title, entry.link, pub_date or "No Date"))

    return articles



def save_to_csv(articles, filename="articles.csv"):
    """Saves the articles list to a CSV file."""
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Link", "Publication Date"])
        writer.writerows(articles)


def scrape_multiple_rss(feeds):
    """Scrapes multiple RSS feeds and stores the articles."""
    all_articles = []

    for feed_url in feeds:
        print(f"Scraping: {feed_url}")
        articles = get_rss_articles(feed_url)
        all_articles.extend(articles)  # Combine results

    save_to_csv(all_articles, "all_universities_articles.csv")
    print("Saved all articles to all_universities_articles.csv!")

if __name__ == "__main__":
    scrape_multiple_rss(rss_feeds)