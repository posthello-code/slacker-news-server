from time import sleep
import requests
import json

from services.postgres import Source, Story

url_base = "https://hacker-news.firebaseio.com/v0"


def request_top_story():
    response = requests.get(f"{url_base}/topstories.json?print=pretty")

    top_stories = eval(response.text)
    response = requests.get(f"{url_base}/item/{top_stories[0]}.json?print=pretty")

    return response


def request_top_story_comments(id):
    response = requests.get(f"{url_base}/item/{id}.json?print=pretty")

    comment_ids = json.loads(response.text)["kids"]
    comments = []
    for item in comment_ids:
        comment = requests.get(f"{url_base}/item/{item}.json?print=pretty")
        print(f"processing comment {item}")

        comments.append(json.loads(comment.text))
        sleep(0.2)

    return comments


# Fetches the story,
def commit_source_data_to_db(
    session,
):
    top_story_response = request_top_story()
    top_story_content = top_story_response.text
    top_story_id = json.loads(top_story_response.text)["id"]
    top_story_uri = "https://news.ycombinator.com/item?id=" + str(top_story_id)
    top_story_comments = json.dumps(request_top_story_comments(top_story_id))

    try:
        # handle when the story is an external website
        top_story_uri = json.loads(top_story_response.text)["url"]
    except:
        # handle when the story internal to hacker news
        pass

    print(top_story_uri)

    top_story_title = json.loads(top_story_response.text)["title"]
    # model for story to insert into db
    top_story_source_sql = Source(
        source="hacker-news-story",
        sourceMethod="http",
        sourceUri=top_story_response.url,
        dataFormat="json",
        content=top_story_content,
        externalId=top_story_id,
    )

    # save to postgres
    session.add(top_story_source_sql)
    session.commit()

    print(top_story_comments)

    top_story_comments_sql = Source(
        source="hacker-news-comment",
        sourceMethod="http",
        sourceUri=top_story_response.url,
        dataFormat="json",
        content=top_story_comments,
        externalId=top_story_id,
    )

    # save to postgres
    session.add(top_story_comments_sql)
    session.commit()

    # get the page content
    top_story_site_html = requests.get(top_story_uri)

    # model for story to insert into db
    linked_site_source_sql = Source(
        source="hacker-news-story-linked-site",
        sourceMethod="http",
        sourceUri=top_story_uri,
        dataFormat="html",
        content=top_story_site_html.text,
        externalId=top_story_id,
    )

    # save to postgres
    session.add(linked_site_source_sql)

    try:
        session.commit()
    except ValueError:
        print("There was a problem with the source")
        exit(0)

    return Story(
        sourceId=top_story_source_sql.id,
        title=top_story_title,
        summary=linked_site_source_sql.content,
        sourceUri=top_story_uri,
    )
