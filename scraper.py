import requests
from bs4 import BeautifulSoup
import feedparser
import csv
from datetime import datetime, timedelta, timezone

# List of RSS feed URLs
rss_feeds = [
    "https://news.stanford.edu/feed/",
    "https://news.harvard.edu/gazette/feed/"
]

def get_rss_articles(feed_url):
    """Fetches article links from an RSS feed and filters them."""
    # Parse the RSS feed
    feed = feedparser.parse(feed_url)
    articles = []
    # Calculate the date two weeks ago from now
    two_weeks_ago = datetime.now(timezone.utc) - timedelta(days=14)  # Make timezone-aware

    # Iterate over each entry in the feed
    for entry in feed.entries:
        # Check if the entry link contains "news"
        if "news" in entry.link:
            # Get the title of the entry, or use "No Title" if not available
            title = entry.title if "title" in entry else "No Title"
            # Get the publication date of the entry, or None if not available
            pub_date = entry.published if "published" in entry else None
            
            # Convert date string to datetime object
            if pub_date:
                try:
                    # Parse the publication date
                    pub_date_dt = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %z")
                    # Skip articles older than two weeks
                    if pub_date_dt < two_weeks_ago:
                        continue  # Skip old articles
                except ValueError:
                    pass  # If date can't be parsed, keep the article

            # Append the article details to the list
            articles.append((title, entry.link, pub_date or "No Date"))

    return articles

def save_to_csv(articles, filename="articles.csv"):
    """Saves the articles list to a CSV file."""
    # Open the CSV file for writing
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(["Title", "Link", "Publication Date"])
        # Write the article rows
        writer.writerows(articles)

def scrape_multiple_rss(feeds):
    """Scrapes multiple RSS feeds and stores the articles."""
    all_articles = []

    # Iterate over each feed URL
    for feed_url in feeds:
        print(f"Scraping: {feed_url}")
        # Get articles from the RSS feed
        articles = get_rss_articles(feed_url)
        # Combine results
        all_articles.extend(articles)

    # Save all articles to a CSV file
    save_to_csv(all_articles, "all_universities_articles.csv")
    print("Saved all articles to all_universities_articles.csv!")

if __name__ == "__main__":
    # Start scraping multiple RSS feeds
    scrape_multiple_rss(rss_feeds)