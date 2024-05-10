from services.hacker_news import sqlTemplateFromTopStory, stories
from services.openai import doCompletionWithSystemMessage
from services.postgres import init_postgres
from services.utils import clean_html

session = init_postgres()

print("getting story from hacker news")
storySql = sqlTemplateFromTopStory(session)

checkDuplicates = session.query(stories).where(stories.title == storySql.title).all()
if len(checkDuplicates) == 0:
    storySql.summary = clean_html(storySql.summary)
    print(storySql.summary)
    storySummary = doCompletionWithSystemMessage(
        storySql.summary,
        """You are a tech news and blog 
        summarizer. You will simplify technical jargon 
        so that the average technologist will 
        understand. 
        
        You will be proided text from a website, you 
        need to explain what it contains.
        
        If the page appears to be a github repo, state
        simply what the repo appears to be for.
    
        If the text appears to be CSS, or javascript code, 
        respond with the character '.'.
        
        If the text appears to be related to the style or
        theme, format or hosting of the website respond 
        with the character '.'.
        
        Keep the length under 250 characters.
        If the provided text is empty respond with the
        character '.'""",
    )

if len(checkDuplicates) == 0:
    if storySummary[0] == ".":
        storySummary = storySummary[1:]

    print(storySummary)

    storyStmt = stories(
        sourceId=storySql.sourceId,
        title=storySql.title,
        summary=storySummary,
        sourceUri=storySql.sourceUri,
    )

    session.add(storyStmt)
    session.commit()
else:
    print("duplicate story")

try:
    session.close()
except:
    print("already closed")
