import requests
import json
import feedparser
from uuid import uuid5, NAMESPACE_URL
from models.data_models import Source, Story

RSS_FEED_URL = "https://feeds.arstechnica.com/arstechnica/index"


def fetch_top_story():
    """Fetch the top story from Ars Technica RSS feed"""
    feed = feedparser.parse(RSS_FEED_URL)

    if not feed.entries:
        raise Exception("No entries found in RSS feed")

    # Get the first (most recent) entry
    top_entry = feed.entries[0]

    return {
        "title": top_entry.title,
        "link": top_entry.link,
        "published": top_entry.published,
        "summary": top_entry.summary,
        "id": top_entry.id,
    }


def commit_source_data_to_db(session):
    """Fetch Ars Technica story and commit to database"""

    # Fetch top story from RSS feed
    story_data = fetch_top_story()

    story_uri = story_data["link"]
    story_title = story_data["title"]
    story_id = story_data["id"]

    # Generate unique UUIDs for different source types using the story ID
    rss_uuid = str(uuid5(NAMESPACE_URL, f"rss:{story_id}"))
    article_uuid = str(uuid5(NAMESPACE_URL, f"article:{story_id}"))
    story_uuid = str(uuid5(NAMESPACE_URL, f"story:{story_id}"))

    print(f"Fetching: {story_title}")
    print(f"URI: {story_uri}")
    print(f"Story ID: {story_id}")
    print(f"RSS UUID: {rss_uuid}")
    print(f"Article UUID: {article_uuid}")
    print(f"Story UUID: {story_uuid}")

    # Store RSS feed data
    rss_source_sql = Source(
        source="ars-technica-rss",
        sourceMethod="rss",
        sourceUri=RSS_FEED_URL,
        dataFormat="json",
        content=json.dumps(story_data),
        externalUuid=rss_uuid,
    )

    if session.query(Story).where(Story.title == story_title).all():
        print("already saved")
        return Story

    session.add(rss_source_sql)
    session.commit()

    # Fetch the actual article HTML
    article_response = requests.get(story_uri)

    article_source_sql = Source(
        source="ars-technica-article",
        sourceMethod="http",
        sourceUri=story_uri,
        dataFormat="html",
        content=article_response.text,
        externalUuid=article_uuid,
    )

    session.add(article_source_sql)

    try:
        session.commit()
    except ValueError:
        print("There was a problem with the source")
        exit(0)

    return Story(
        sourceId=article_source_sql.id,
        title=story_title,
        summary=story_data["summary"],
        sourceUri=story_uri,
        externalUuid=story_uuid,
    )
