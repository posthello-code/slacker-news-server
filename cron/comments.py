import json

from sqlalchemy import desc
from services.postgres import init_postgres, close_session
from models.data_models import Source, Comment
from services.openai import doCompletionWithSystemMessage, optimizeTextForCompletion

session = init_postgres()

comment_sources = (
    session.query(Source)
    .order_by(desc("createdDate"))
    .where(Source.source == "hacker-news-comment")
    .all()
)

comments_from_latest_source = comment_sources[0]
latest_comments_text = json.dumps(comments_from_latest_source.content)
text_list = optimizeTextForCompletion(
    "Any quotes in your output should be verbatim, use the following data: "
    + latest_comments_text
)
summary = doCompletionWithSystemMessage(
    text_list,
    """
    You are a comment summarizer.
    Describe the general sentiment of the conversation and
    Provide a few interesting quotes from the provided comments verbatim.
    Limit the length to 250 characters.
    Don't repeat yourself.
    If there is nothing to summarize respond with the character '.'
    """,
)

print(summary)

existing_comments = session.query(Comment).where(
    Comment.externalId == comments_from_latest_source.externalId
)
if len(existing_comments.all()) == 0:
    session.add(
        Comment(
            summary=summary,
            sourceId=comments_from_latest_source.id,
            externalId=comments_from_latest_source.externalId,
        )
    )
    session.commit()
else:
    print("update existing")
    session.query(Comment).where(
        Comment.externalId == comments_from_latest_source.externalId
    ).update({Comment.summary: summary}, synchronize_session="auto")
    session.commit()

close_session(session)
