import sys
from services import hacker_news, ars
from models.data_models import Story
from services.openai import doCompletionWithSystemMessage
from services.postgres import init_postgres, close_session
from services.utils import clean_html
from dotenv import load_dotenv

load_dotenv(override=True)

# Parse command line argument
source_type = sys.argv[1] if len(sys.argv) > 1 else "all"

if source_type not in ["hn", "ars", "all"]:
    print(f"Invalid source type: {source_type}")
    print("Usage: python stories.py [hn|ars|all]")
    sys.exit(1)

session = init_postgres()

# Fetch stories based on source type
stories = []
if source_type in ["hn", "all"]:
    stories.append(hacker_news.commit_source_data_to_db(session))
if source_type in ["ars", "all"]:
    stories.append(ars.commit_source_data_to_db(session))
print(stories)
# Process each story
for story in stories:
    print(story)
    checkDuplicates = session.query(Story).where(Story.title == story.title).all()
    if len(checkDuplicates) == 0:
        story.summary = clean_html(story.summary)
        storySummary = doCompletionWithSystemMessage(
            story.summary,
            """Summarize this webpage content for tech news readers. Use simple language.

            FOR GITHUB REPOS: State what the repo does in one sentence.

            RESPOND WITH ONLY "." (a single period character) IF:
            - Text is CSS or JavaScript code
            - Content is about website styling, themes, formatting, or hosting
            - Page shows a 403 error
            - Text is empty or contains only whitespace
            - Text is a single character or meaningless fragment

            Keep summaries under 250 characters. Be concise and factual.""",
        )

        if len(storySummary) == 0:
            print("no summary")
            continue

        if storySummary[0] == ".":
            storySummary = storySummary[1:]

        print(storySummary)

        if len(storySummary) > 0:
            storyStmt = Story(
                sourceId=story.sourceId,
                title=story.title,
                summary=storySummary,
                sourceUri=story.sourceUri,
                externalId=getattr(story, "externalId", None),
                externalUuid=getattr(story, "externalUuid", None),
            )

            session.add(storyStmt)
            session.commit()
    else:
        print("duplicate story")

close_session(session)
