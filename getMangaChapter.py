import requests

from parseJsonMangaPage import idMangaJSON


def getUrlChapter(id):
    url = f"https://api.mangadex.org/manga/{id}/aggregate?translatedLanguage%5B%5D=vi"
    r = requests.get(url)
    j = r.json()
    return j

def getChapter():
    for key,value in idMangaJSON().items():
        a = getUrlChapter(value)
        print(a)


getChapter()