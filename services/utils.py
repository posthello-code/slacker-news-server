import re


def clean_html(text):
    clean = re.compile("<.*?>")
    tagsRemovedText = re.sub(clean, "", text)
    clean = re.compile("{.*?}", re.DOTALL)
    cssRemovedText = re.sub(clean, "", tagsRemovedText)
    clean = re.compile(r"\s{2,}")
    return re.sub(clean, "", cssRemovedText)
