import os
from time import sleep
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)
aiClient = OpenAI()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL") or "gpt-4o"

print("Selected GPT model: " + OPENAI_MODEL)


def optimizeTextForCompletion(text):
    # function will split text into an array strings
    # and trunactes text that exceeds completionTextMaxParts * partLength
    completionText = []
    completionTextMaxParts = 3
    partLength = 16000
    partText = ""
    for index, item in enumerate(text):
        partText += item
        if len(text) < partLength and index == len(text) - 1:
            # exit on the last part
            completionText.append(partText)
            break
        if (index % partLength) == 0:
            completionText.append(partText)
            partText = ""
        if index == partLength * completionTextMaxParts:
            # leave the loop if the text is too long
            break
    return completionText


def doCompletionWithSystemMessage(completionTextList: list[str], systemMessage: str):
    completionTextList = optimizeTextForCompletion(completionTextList)
    result = ""
    for index, item in enumerate(completionTextList):
        print(
            "awaiting completions from openai..."
            + str(round((index / len(completionTextList)) * 100))
            + "%"
            + " completion progress"
        )
        completion = aiClient.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": systemMessage,
                },
                {"role": "user", "content": item},
            ],
        )
        try:
            if completion.choices[0].message.content != ".":
                result += completion.choices[0].message.content
            # sleep to avoid rate limiting
            sleep(0.02)
        except:
            print("no summary")
    return result
