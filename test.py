from dbFireBase import getManga


for key,value in getManga().items():
    for chapter,valueChapter in value['chapter'].items():
        print(key,chapter,valueChapter)