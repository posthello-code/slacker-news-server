from time import sleep
from services.hacker_news import *
from services.openai import doCompletionWithList, optimizeTextForCompletion
from services.postgres import *

session = init_postgres()

print("getting story from hacker news")
storySql = sqlTemplateFromTopStory(session)
completionTextList = optimizeTextForCompletion(storySql.summary)
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
