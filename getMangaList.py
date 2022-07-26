import requests

from parseJsonMangaPage import imgMangaJSON


def getUrlServer(id):
    url = f"https://api.mangadex.org/manga/{id}"
    r = requests.get(url)
    j = r.json()
    return j


def getAuthor(id):
    j = getUrlServer(id)
    idAuthor = j['data']['relationships'][0]['id']
    url = f"https://api.mangadex.org/author/{idAuthor}" 
    r = requests.get(url)
    j = r.json()
    return j

def titleMangaList(id):
    j = getUrlServer(id)
    title = j['data']['attributes']['altTitles'][-1].get('vi')
    return title
def tagsMangaList(id):
    j = getUrlServer(id)
    tagsJSON = j['data']['attributes']['tags']
    tags = []
    for item in tagsJSON:
        tags.append(item['attributes']['name'].get('en')) #print tags with list
    return tags
def desciptionMangaList(id):
        j = getUrlServer(id)
        desciptionJSON = j['data']['attributes']['description']
        desciption = dict(reversed(list(desciptionJSON.items())))
        for key,value in desciption.items():
            if key =="en":
                desciption = value
                break
            elif key =="vi":
                desciption = value
                break
        return desciption


def authorMangaList(id):
    j = getAuthor(id)
    author = j['data']['attributes']['name']
    return author

def updateAt(id):
    j = getUrlServer(id)
    updateAtJSON = j['data']['attributes']['updatedAt']
    updateAt = updateAtJSON[0:10]
    updateAtYear = updateAt[0:4]
    updateAtMonth = updateAt[5:7]
    updateAtDay = updateAt[8:10]
    updateAt = f"{updateAtDay}/{updateAtMonth}/{updateAtYear}"
    return updateAt


def otherName(id):
    j = getUrlServer(id)
    otherNameJSON = j['data']['attributes']['altTitles']
    #otherName = list(reversed(otherNameJSON))
    for item in otherNameJSON:
        for keyOtherName,valueOtherName in item.items():
            if keyOtherName == "ja":
                return valueOtherName
            elif keyOtherName == "en":
                return valueOtherName
           


def imgBannerMangaList(keyID):
    img = imgMangaJSON()
    return img[keyID]['imgBanner']

def imgIndexMangaList(keyID):
    img = imgMangaJSON()
    return img[keyID]['imgIndex']

def imgCoverMangaList(keyID):
    img = imgMangaJSON()
    return img[keyID]['imgCover']
