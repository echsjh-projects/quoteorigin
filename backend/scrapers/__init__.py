from scrapers.wikiquote import search_wikiquote
from scrapers.wikipedia import search_wikipedia
from scrapers.newsapi import search_news
from scrapers.tavily import search_web
from scrapers.quotable import search_quotable

__all__ = [
    "search_wikiquote",
    "search_wikipedia",
    "search_news",
    "search_web",
    "search_quotable",
]
