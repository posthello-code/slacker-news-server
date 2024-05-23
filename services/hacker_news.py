import requests
import json

from services.postgres import sources, stories


def request_top_story():
    response = requests.get(
        "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
    )

    topStories = eval(response.text)
    response = requests.get(
        "https://hacker-news.firebaseio.com/v0/item/% s.json?print=pretty"
        % topStories[3]
    )

    return response


def sqlTemplateFromTopStory(
    session,
):
    topStoryResponse = request_top_story()
    topStoryContent = json.dumps(topStoryResponse.text)
    topStoryId = json.loads(topStoryResponse.text)["id"]

    try:
        # handle when the story is an external website
        topStoryUri = json.loads(topStoryResponse.text)["url"]
    except:
        # handle when the story internal to hacker news
        topStoryUri = "https://news.ycombinator.com/item?id=" + str(topStoryId)

    print(topStoryUri)

    topStoryTitle = json.loads(topStoryResponse.text)["title"]
    # model for story to insert into db
    topStorySourceSql = sources(
        source="hacker-news-story",
        sourceMethod="http",
        sourceUri=topStoryResponse.url,
        dataFormat="json",
        content=topStoryContent,
        externalId=topStoryId,
    )

    # save to postgres
    session.add(topStorySourceSql)
    session.commit()

    # get the page content
    topStorySiteHtml = requests.get(topStoryUri)

    # model for story to insert into db
    linkedSiteSourceSql = sources(
        source="hacker-news-story-linked-site",
        sourceMethod="http",
        sourceUri=topStoryUri,
        dataFormat="html",
        content=topStorySiteHtml.text,
        externalId=topStoryId,
    )

    # save to postgres
    session.add(linkedSiteSourceSql)
    session.commit()

    return stories(
        sourceId=topStorySourceSql.id,
        title=topStoryTitle,
        summary=linkedSiteSourceSql.content,
        sourceUri=topStoryUri,
    )
