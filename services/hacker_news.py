import requests
import json

from services.postgres import Source, Story


def request_top_story():
    response = requests.get(
        "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
    )

    top_stories = eval(response.text)
    response = requests.get(
        "https://hacker-news.firebaseio.com/v0/item/% s.json?print=pretty"
        % top_stories[0]
    )

    return response


def sql_template_from_top_story(
    session,
):
    top_story_response = request_top_story()
    top_story_content = json.dumps(top_story_response.text)
    top_story_id = json.loads(top_story_response.text)["id"]

    try:
        # handle when the story is an external website
        top_story_uri = json.loads(top_story_response.text)["url"]
    except:
        # handle when the story internal to hacker news
        top_story_uri = "https://news.ycombinator.com/item?id=" + str(top_story_id)

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
