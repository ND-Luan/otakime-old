from ast import parse
from dataclasses import replace
import json
from pkgutil import iter_modules

from sqlalchemy import values




def parseJson():
    with open('dbManga.json',encoding="utf8")  as f:
        data = json.load(f)
    return data
   

class Manga:
    def __init__(self,nameManga,author,description,isUpdate,otherName,dateUpdate,category,chapter,cardImgUrl):
        self.nameManga = nameManga
        self.author = author
        self.description = description
        self.isUpdate = False
        self.otherName = otherName
        self.dateUpdate = dateUpdate
        self.category = category
        self.cardImgUrl = cardImgUrl
        self.chapter = chapter['chap1']
    

mangaList = []
def test():
    with open('dbManga.json',encoding="utf8")  as f:
        data = json.loads(f.read())
        for item in data:
            mangaList.append(Manga(**item))


#index = 0
#for index in range(len(parseJson())):
#    for key, value in parseJson()[index].items():
#        print(key," : ",value)
#    print()



def getallManga():
    index_list = 0
    dictMangaIndex ={}
    for key , value in parseJson()[index_list].items():
        dictMangaIndex.update({key:value})
    return dictMangaIndex



def mangaPage(id=3):
    dict_mangaPage ={}
    for key, value in getallManga():
        if id == value['id']:
            dict_mangaPage.update({key:value})
            break
    return dict_mangaPage.items()




def mangaPageIndex(url):
    temp= 0
    dictMangaIndex ={}
    for key,value in getallManga().items():
        if url == value['url']:
            dictMangaIndex.update({key:value})
            temp = temp +1
            if temp == 4:
                break
    return dictMangaIndex



def parseChapter():
    data = getallManga()
    dict_chapter={}
    value_data = {}
    for key,value in data:
        dict_chapter.update({key : value['chapter']})
        value_data = values['id']
    print(value_data)
    return dict_chapter

def mangaPageImg(nameManga,chap):
    dictImg ={}
    for key, value in getallManga().items():
        if nameManga == value['nameManga']:
            dictImg.update({key:value['chapter'][chap]})
            break
    return dictImg


def chapter():

    list_chapter =[]
    for key,value in getallManga().items():
        for item in value['chapter'].keys():
            if url == value['url']:
                list_chapter.append({key:item})
    return list_chapter




def mangaPage(urlnameManga):
    dict_mangaPage ={}
    for key, value in getallManga().items():
        if urlnameManga == value['nameManga'].lower().replace(' ','-'):
            dict_mangaPage.update({key:value})  
            return dict_mangaPage
        else:
            print('abc')
urlnameManga =['r15-ja-dame-desuka','kawaii-kanojo-chan']

print(mangaPage(urlnameManga[0]))

#nameManga = 'Kawaii Kanojo-chan'
#chap = "chap-1"
#list_chap = []
#for item in mangaPageImg(nameManga,chap).values():
#    for chap in item["imgUrl"].values():
#        print(chap)

#url ='kawaii-kanojo-chan'
#print(mangaPageIndex(url))
    

def dictMangaIndex2():
    dictMangaIndex2 ={}
    temp= 0
    for key,value in getallManga().items():
        dictMangaIndex2.update({key:value})
        temp = temp +1
        if temp == 7:
            break
    print(reversed(dictMangaIndex2))


def test(url):
    dict_mangaPage ={}
    for key, value in getallManga().items():
        if url ==value['nameManga'].lower().replace(" ","-"):
            dict_mangaPage.update({key:value})
            return dict_mangaPage
            




 nameFile = request.form.get('nameFile')
        nameMangaKey = request.form.get('nameMangaKey')
        nameMangaUrl = request.form.get('nameMangaUrl')
        author = request.form.get('author')
        description = request.form.get('description')
        otherName = request.form.get('otherName')
        dateUpdate = request.form.get('dateUpdate')
        category = request.form.get('category')
        cardImgUrlIndex = request.form.get('cardImgUrlIndex')
        cardImgUrl = request.form.get('cardImgUrl')
        cardSingleImgUrl = request.form.get('cardSingleImgUrl')
        urlChapter = request.form.get('urlChapter')

        tempList = [nameFile,nameMangaKey,nameMangaUrl,author,description,otherName,dateUpdate,category, cardImgUrlIndex,cardImgUrl, cardSingleImgUrl, urlChapter]