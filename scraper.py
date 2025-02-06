import requests
from bs4 import BeautifulSoup
import feedparser
import csv
from datetime import datetime, timedelta, timezone

# List of RSS feed URLs
rss_feeds = [
    "https://news.harvard.edu/gazette/feed/",
    "https://news.iu.edu/live/rss/news",
    "https://hub.jhu.edu/topics/university-news/articles/feed/",
    "https://news.mit.edu/rss/feed",
    "https://www.mayoclinic.org/rss/all-news",
    "https://www.newswise.com/legacy/feed/institution.php?inst=200",
    "https://www.nist.gov/news-events/news/rss.xml",
    "https://ifp.nyu.edu/category/news/feed/",
    "https://news.northeastern.edu/feed/",
    "https://news.feinberg.northwestern.edu/feed/",
    "https://www.ornl.gov/rssfeeds/ornl_news_releases.xml",
    "https://news.ohsu.edu/rss.xml",
    "https://www.princeton.edu/feed",
    "https://www.rcac.purdue.edu/news/rss/Science%20Highlights",
    "https://news.siu.edu/index.xml"
    "https://news.stanford.edu/feed/",
    #"https://original-ufdc.uflib.ufl.edu/rss/all_rss.xml",
    "https://news.temple.edu/rss/news/topics/research/",
    "https://news.tamus.edu/feed/",
    "https://www.tsus.edu/news.rss/",
    "https://smhs.gwu.edu/news/rss.xml/",
    "https://www.psu.edu/news/rss/latest-news/rss.xml/",
    "https://www.uab.edu/news/component/k2/itemlist/search?searchword=news&format=feed/",
    "https://feeds.feedburner.com/UChicago/",
    "https://www.k-state.edu/today/rss/news_and_research.xml?cache=1738865861/",
    "https://news.unm.edu/rss.xml/",
    "https://scholar.utc.edu/recent.rss/",
    "https://news.uthsc.edu/feed/",
    "https://news.tennessee.edu/feed/",
    "https://unews.utah.edu/feed/",
    "https://now.tufts.edu/rss.xml/",
    "https://www.epa.ie/resources/rss/index-90474.xml/",
    "https://www.epa.gov/rss.xml/",
    "https://www.navy.mil/DesktopModules/ArticleCS/RSS.ashx?ContentType=1&Site=1067&max=10/",
    "https://www.universityofcalifornia.edu/rss.xml/",
    "https://news.ucr.edu/rss.xml/",
    "https://www.colorado.edu/rss.xml/",
    "https://www.cu.edu/rss.xml/",
    "https://news.uillinois.edu/xml/7815/rss.xml/",
    "https://news.miami.edu/feeds/latest-25.xml/",
    "https://news.umich.edu/feed/",
    "https://showme.missouri.edu/feed/",
    "https://news.unl.edu/feed/",
    "https://news.nd.edu/news.atom/",
    "https://penntoday.upenn.edu/rss.xml/",
    "https://pittnews.com/feed/",
    "https://www.medschool.pitt.edu/rss.xml/",
    "https://www.rochester.edu/newscenter/feed/",
    "https://today.usc.edu/feed/",
    "https://news.virginia.edu/rss.xml/",
    "https://www.washington.edu/news/feed/",
    "https://www.wisconsin.edu/news/feed/",
    "https://www.usg.edu/news/newsreleases/",
    #"https://www.usda.gov/rss/home.xml/",
    "https://www.commerce.gov/feeds/news/",
    "https://www.hhs.gov/rss/news.xml/",
    "https://www.af.mil/DesktopModules/ArticleCS/RSS.ashx?ContentType=1&Site=1&isdashboardselected=0&max=20&Category=22750/"

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