from services.hacker_news import commit_source_data_to_db
from models.data_models import Story
from services.openai import doCompletionWithSystemMessage
from services.postgres import init_postgres, close_session
from services.utils import clean_html

session = init_postgres()

print("getting story from hacker news")
story = commit_source_data_to_db(session)

checkDuplicates = session.query(Story).where(Story.title == story.title).all()
if len(checkDuplicates) == 0:
    story.summary = clean_html(story.summary)
    storySummary = doCompletionWithSystemMessage(
        story.summary,
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
        
        If the page is forbidden due to 403 error respond 
        with the character '.'
        
        Keep the length under 250 characters.
        If the provided text is empty respond with the
        character '.'""",
    )

    if len(storySummary) == 0:
        print("no summary")
        close_session(session)

    if storySummary[0] == ".":
        storySummary = storySummary[1:]

    print(storySummary)

    if len(storySummary) > 0:
        storyStmt = Story(
            sourceId=story.sourceId,
            title=story.title,
            summary=storySummary,
            sourceUri=story.sourceUri,
        )

        session.add(storyStmt)
        session.commit()
else:
    print("duplicate story")

close_session(session)
