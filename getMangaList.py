import requests

from parseJsonMangaPage import idMangaJSON, imgMangaJSON


def getUrlServer(id):
    url = f"https://api.mangadex.org/manga/{id}"
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
def imgBannerMangaList(keyID):
    img = imgMangaJSON()
    return img[keyID]['imgBanner']

def imgIndexMangaList(keyID):
    img = imgMangaJSON()
    return img[keyID]['imgIndex']

def imgCoverMangaList(keyID):
    img = imgMangaJSON()
    return img[keyID]['imgCover']

