import json

def parseJsonMangadex():
    with open('dbManga.json',encoding="utf8") as f:
        data = json.loads(f.read())
    return data

def idMangaJSON():
    idMangaList = {}
    for key,value in parseJsonMangadex().items():
        idMangaList.update({key:value['id']})
    return idMangaList


def imgMangaJSON():
    imgMangaList = {}

    for keyID, valueID in parseJsonMangadex().items():
        imgMangaList.update(
        {
            keyID:{
                "imgIndex":valueID['cardImgUrlIndex'],
                "imgBanner":valueID['cardImgUrl'],
                "imgCover":valueID['cardSingleImgUrl'],
            }
        }
        )
    return imgMangaList
