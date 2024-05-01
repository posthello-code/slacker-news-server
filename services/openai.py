import os
from time import sleep
from openai import OpenAI

aiClient = OpenAI()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def optimizeTextForCompletion(text):
    # trim long text and split into parts
    completionText = []
    completionTextMaxParts = 12
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
            + " completion progress"
        )
        completion = aiClient.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are a tech You are a tech news and blog 
                    summarizer. You simplify technical jargon 
                    so that the average technologist will 
                    understand. Given an html doc, summarize 
                    only the article text, ignore the code and 
                    tags. If you can't provide a summary 
                    respond with the character '.'""",
                },
                {"role": "user", "content": item},
            ],
        )
        result += completion.choices[0].message.content
        sleep(1)
    return result
