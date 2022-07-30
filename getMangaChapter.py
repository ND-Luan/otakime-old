import requests
from parseJsonMangaPage import parseJsonMangadex
def getVolumes(id):
    r = requests.get(f'https://api.mangadex.org/manga/{id}/aggregate?translatedLanguage%5B%5D=vi')
    j = r.json()

    temp = j['volumes']
    
    for key,value in temp.items():
        if key == "none":
            dictList = {}

            for key,value in temp.items():
                dictList.update({
                    key:{
                    "chapters":value['chapters']}})

            return dictList
        elif key =="2" or key == "1":
            dictList = {}
            for key,value in temp.items():
                dictList.update({
                    key:{
                    "chapters":value['chapters']}})
            return dictList

def getChapter(id):
    listChapter = []
    chapter = getVolumes(id)
    for keyVolumes,valueVolumes in chapter.items():
        for keyChapter,valueChapter in valueVolumes['chapters'].items():
            listChapter.append(valueChapter)
    return listChapter


def ChapterMangaPage(id):

    chapter = getChapter(id)
    listChapter = []
    for item in chapter:
        listChapter.append(item)
    return listChapter



def getIdChapter(id):
    idChapter = ChapterMangaPage(id)
    dictIdChapter = {}
    for itemList in idChapter:
        dictIdChapter.update({itemList['chapter']:itemList['id']})
        
    return dictIdChapter







def imgChapter(id):
    DICT = {}
    for keyID, valueID in parseJsonMangadex().items():
        if id == valueID['id']:
            #for itemChap in valueID['chapter']:
            for key,value in valueID['chapter'].items():
                DICT.update({key:value})
    return DICT