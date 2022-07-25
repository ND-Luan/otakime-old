import json
import requests



def parseJsonMangadex():
    with open('database.json',encoding="utf8") as f:
        data = json.loads(f.read())
    return data

def idMangaJSON():
    idMangaList = {}
    for key,value in parseJsonMangadex().items():
        idMangaList.update({key:value})
    return idMangaList



def parseJsonIMG():
    with open('dbManga.json',encoding="utf8") as f:
        data = json.loads(f.read())
    return data


#def checkImgIndex(keyID):
    listcheckImgIndex = ""
    for keyImg,valueIMG in parseJsonIMG().items():
        if keyID == keyImg:
            listcheckImgIndex = valueIMG['cardImgUrlIndex']
            break
    return listcheckImgIndex

def imgMangaJSON():
    imgMangaList = {}

    for keyID, valueID in idMangaJSON().items():
        for keyImg,valueIMG in parseJsonIMG().items():
            if keyID == keyImg:
                 imgMangaList.update(
                    {
                        keyID:{
                            "imgIndex":valueIMG['cardImgUrlIndex'],
                            "imgBanner":valueIMG['cardImgUrl'],
                            "imgCover":valueIMG['cardSingleImgUrl'],
                        }
                    }
                )
    return imgMangaList

print(imgMangaJSON())