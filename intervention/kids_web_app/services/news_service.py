"""Tech news fetcher with 15-minute TTL cache.

Sources (in order, optimised for kids 8-18):
  1. The Verge RSS          — mainstream tech, gaming, AI; great thumbnails
  2. Popular Science RSS    — science + tech, accessible writing
  3. BBC Technology RSS     — reliable, global, kid-friendly
  4. Engadget RSS           — gadgets & consumer tech
  5. Static Dream Space placeholder cards
"""

import time
import requests
import feedparser
from cachetools import TTLCache
from config import NEWSAPI_KEY

_cache = TTLCache(maxsize=1, ttl=900)  # 15-minute TTL

_STATIC_FALLBACK = [
    {
        "title": "Girls Are Changing the World of Coding",
        "url": "#",
        "image": "https://images.unsplash.com/photo-1573164713714-d95e436ab8d6?w=400&q=80",
        "source": "Dream Space",
        "time": "now",
    },
    {
        "title": "How AI Is Helping Scientists Discover New Medicines",
        "url": "#",
        "image": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=400&q=80",
        "source": "Dream Space",
        "time": "now",
    },
    {
        "title": "Young Coder, Age 12, Builds App to Help Her Community",
        "url": "#",
        "image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&q=80",
        "source": "Dream Space",
        "time": "now",
    },
    {
        "title": "Robots Are Learning to Cook — What Happens Next?",
        "url": "#",
        "image": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=400&q=80",
        "source": "Dream Space",
        "time": "now",
    },
]


def _relative_time(published_parsed):
    """Convert time.struct_time → relative string."""
    if not published_parsed:
        return "recently"
    now = time.time()
    then = time.mktime(published_parsed)
    diff = int(now - then)
    if diff < 3600:
        return f"{diff // 60}m ago"
    if diff < 86400:
        return f"{diff // 3600}h ago"
    return f"{diff // 86400}d ago"


def _extract_image(entry):
    """Try multiple RSS image fields."""
    # media:thumbnail (BBC, many feeds)
    if hasattr(entry, "media_thumbnail") and entry.media_thumbnail:
        return entry.media_thumbnail[0].get("url")
    # media:content (The Verge, Engadget)
    if hasattr(entry, "media_content") and entry.media_content:
        url = entry.media_content[0].get("url", "")
        if url and not url.endswith((".mp4", ".webm")):
            return url
    # enclosure (podcast-style RSS)
    if hasattr(entry, "enclosures") and entry.enclosures:
        enc = entry.enclosures[0]
        if "image" in enc.get("type", ""):
            return enc.get("href") or enc.get("url")
    # Try to find an <img> inside the summary/content HTML
    summary = entry.get("summary", "") or ""
    if '<img' in summary:
        start = summary.find('src="', summary.find('<img'))
        if start != -1:
            start += 5
            end = summary.find('"', start)
            if end != -1:
                url = summary[start:end]
                if url.startswith("http"):
                    return url
    return None


def _fetch_verge():
    feed = feedparser.parse("https://www.theverge.com/rss/index.xml")
    items = []
    for entry in feed.entries[:10]:
        image = _extract_image(entry)
        title = entry.get("title", "")
        # Skip video-only articles
        if not title:
            continue
        items.append({
            "title": title,
            "url": entry.get("link", "#"),
            "image": image,
            "source": "The Verge",
            "time": _relative_time(entry.get("published_parsed")),
        })
        if len(items) >= 8:
            break
    return items


def _fetch_popsci():
    feed = feedparser.parse("https://www.popsci.com/feed/")
    items = []
    for entry in feed.entries[:10]:
        image = _extract_image(entry)
        title = entry.get("title", "")
        if not title:
            continue
        items.append({
            "title": title,
            "url": entry.get("link", "#"),
            "image": image,
            "source": "Popular Science",
            "time": _relative_time(entry.get("published_parsed")),
        })
        if len(items) >= 8:
            break
    return items


def _fetch_bbc_tech():
    feed = feedparser.parse("http://feeds.bbci.co.uk/news/technology/rss.xml")
    items = []
    for entry in feed.entries[:10]:
        image = _extract_image(entry)
        title = entry.get("title", "")
        if not title:
            continue
        items.append({
            "title": title,
            "url": entry.get("link", "#"),
            "image": image,
            "source": "BBC Technology",
            "time": _relative_time(entry.get("published_parsed")),
        })
        if len(items) >= 8:
            break
    return items


def _fetch_engadget():
    feed = feedparser.parse("https://www.engadget.com/rss.xml")
    items = []
    for entry in feed.entries[:10]:
        image = _extract_image(entry)
        title = entry.get("title", "")
        if not title:
            continue
        items.append({
            "title": title,
            "url": entry.get("link", "#"),
            "image": image,
            "source": "Engadget",
            "time": _relative_time(entry.get("published_parsed")),
        })
        if len(items) >= 8:
            break
    return items


def _fetch_newsapi():
    if not NEWSAPI_KEY:
        return []
    resp = requests.get(
        "https://newsapi.org/v2/top-headlines",
        params={"category": "technology", "pageSize": 8, "language": "en"},
        headers={"X-Api-Key": NEWSAPI_KEY},
        timeout=5,
    )
    articles = resp.json().get("articles", [])
    return [
        {
            "title": a.get("title", ""),
            "url": a.get("url", "#"),
            "image": a.get("urlToImage"),
            "source": a.get("source", {}).get("name", "NewsAPI"),
            "time": "today",
        }
        for a in articles
        if a.get("title")
    ]


def get_news():
    """Return up to 8 news items, cached for 15 minutes."""
    if "news" in _cache:
        return _cache["news"]

    items = []
    for fetcher in [_fetch_verge, _fetch_bbc_tech, _fetch_popsci, _fetch_engadget, _fetch_newsapi]:
        try:
            result = fetcher()
            if result:
                items = result
                break
        except Exception:
            continue

    if not items:
        items = _STATIC_FALLBACK

    _cache["news"] = items
    return items
