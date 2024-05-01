import json
import os
from time import sleep
from services.hacker_news import *
from services.postgres import *
from openai import OpenAI

print("getting story from hacker news")

aiClient = OpenAI()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
session = init_postgres()


def sqlTemplateFromTopStory():
    topStoryResponse = request_top_story()
    topStoryContent = json.dumps(topStoryResponse.text)
    topStoryUri = json.loads(topStoryResponse.text)["url"]
    topStoryTitle = json.loads(topStoryResponse.text)["title"]
    # model for story to insert into db
    topStorySourceSql = sources(
        source="hacker-news-story",
        sourceMethod="http",
        sourceUri=topStoryResponse.url,
        dataFormat="json",
        content=topStoryContent,
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
    )

    # save to postgres
    session.add(linkedSiteSourceSql)
    session.commit()

    return stories(
        sourceId=topStorySourceSql.id,
        title=topStoryTitle,
        summary=linkedSiteSourceSql.content,
    )


def optimizeTextForCompletion(text):
    # trim long text and split into parts
    completionText = []
    completionTextMaxParts = 2
    partText = ""
    partLength = 16000
    for index, item in enumerate(text):
        partText += item
        if len(text) < partLength and index == len(text) - 1:
            completionText.append(partText)
            break
        if (index % partLength) == 0:
            completionText.append(partText)
            partText = ""
        if index == partLength * completionTextMaxParts:
            # leave the loop if the text is too long
            break
    return completionText


def doCompletionWithList(completionTextList):
    result = ""
    for index, item in enumerate(completionTextList):
        print(
            "awaiting completions from openai..."
            + str(round((index / len(completionTextList)) * 100))
            + "%"
        )
        completion = aiClient.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a tech news and blog summarizer. You simplify technical "
                    + "jargon so that the average technologist will understand. Given an html doc,"
                    + "summarize only the article text, ignore the code and tags."
                    + "If you can't provide a summary respond with the string '.'",
                },
                {"role": "user", "content": item},
            ],
        )
        result += completion.choices[0].message.content
        sleep(1)
    return result


storySql = sqlTemplateFromTopStory()
completionTextList = optimizeTextForCompletion(storySql.summary)
storySummary = doCompletionWithList(
    completionTextList,
)

print(storySummary)

storySummary = doCompletionWithList(
    completionTextList,
)

print(storySummary)

storyStmt = stories(
    sourceId=storySql.sourceId, title=storySql.title, summary=storySummary
)
session.add(storyStmt)
session.commit()

try:
    session.close()
except:
    print("already closed")
