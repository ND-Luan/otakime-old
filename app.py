import shutil
from flask import Flask, redirect, render_template, request, send_file, session, url_for
from flask_mail import Mail,Message

from datetime import timedelta

from getMangaChapter import ChapterMangaPage, imgChapter
from getMangaList import authorMangaList, desciptionMangaList, imgBannerMangaList, imgCoverMangaList, imgIndexMangaList, otherName, tagsMangaList, titleMangaList, updateAt

from parseJsonMangaPage import idMangaJSON


from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField,IntegerField,MultipleFileField,SelectField
from wtforms.validators import DataRequired,InputRequired

import os
import json
app = Flask(__name__)


app.config['IMAGE_UPLOADS'] = 'static/img/imgManga'

mail_username='mail.otakime@gmail.com'
mail_password='lpavozmbebtxdhbb'

app.config["SECRET_KEY"] = "POTATO"
app.permanent_session_lifetime = timedelta(seconds=300)

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = mail_username,
    MAIL_PASSWORD = mail_password,
))

mail = Mail(app)

def home():
    title= 'Otakime - Nha tu ban'
    description = 'Trang web chính thức của nhóm dịch Otakime, Việt hóa những dự án manga nhằm giới thiệu độc giả. Truy cập ngay để đọc những tựa truyện được yêu thích.'
    dictMangaIndex ={}
    temp= 0
    for key,value in idMangaJSON().items():
        dictMangaIndex.update({
            key:{
                "nameManga": key.lower().replace(' ','-'),
                "title":titleMangaList(value),
                "description":desciptionMangaList(value),
                "tags":', '.join(tagsMangaList(value)),
                "imgIndex":imgIndexMangaList(key),
                "imgBanner":imgBannerMangaList(key),
                "imgCover":imgCoverMangaList(key)
            }
        })
        temp = temp +1
        if temp == 4:
            break

    return render_template('manga/index.html', data = dictMangaIndex.items(), title= title, description= description) 

def about():
    title = 'Otakime - About'
    return render_template('manga/page/about.html', title= title)

def contact():
    title = 'Otakime - Contact'
    description = 'Bạn có ý kiến, đề xuất đến nhóm? Hay bạn muốn hợp tác quảng cáo? Đừng ngại gửi liên hệ đến nhóm, bạn sẽ nhận câu trả lời trong 4 ngày làm việc.'
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        msg = Message(
            subject=f'Mail from {subject}',
            sender=email,
            recipients=[mail_username],
            html= render_template('manga/mail.html',name=name, email = email,message=message)
            #body= f'Name: {name}\nEmail: {email}\nMessage: {message}' 
        )
        mail.send(msg)

        return render_template('manga/page/contact.html', success = True, title= title,description=description)

    return render_template('manga/page/contact.html', title= title, description=description)

def manga():
    title = 'Otakime - Manga'
    description = 'Đọc ngay những tựa truyện được Việt hóa chất lượng bởi Otakime.'

    dictManga={}

    for key,value in idMangaJSON().items():
        dictManga.update({
            key:
            {
                "nameManga": key.lower().replace(' ','-'),
                "title":titleMangaList(value),
                "author":authorMangaList(value),
                "updateAt": updateAt(value),
                "otherName":otherName(value),
                "description":desciptionMangaList(value),
                "tags":', '.join(tagsMangaList(value)),
                "imgIndex":imgIndexMangaList(key),
                "imgBanner":imgBannerMangaList(key),
                "imgCover":imgCoverMangaList(key)
            }
            })
  
    return render_template('manga/page/mangaList.html', data = dictManga.items(),title= title,description = description)


def mangaChapter (urlnameManga,chapter):
    dict_mangaPage ={}
    for keyID, valueID in idMangaJSON().items():
        if urlnameManga == keyID.lower().replace(' ','-'):
            title = f"Otakime - {keyID}"
            dict_mangaPage.update({
                keyID: {
                "nameManga": keyID.lower().replace(' ','-'),
                "title":titleMangaList(valueID),
                "author":authorMangaList(valueID),
                "updateAt": updateAt(valueID),
                "otherName":otherName(valueID),
                "description":desciptionMangaList(valueID),
                "tags":', '.join(tagsMangaList(valueID)),
                "imgIndex":imgIndexMangaList(keyID),
                "imgBanner":imgBannerMangaList(keyID),
                "imgCover":imgCoverMangaList(keyID),
                "chapter":[item['chapter'] for item in ChapterMangaPage(valueID)]
            }
            })
            idchapter = imgChapter(valueID)
            for key,value in idchapter.items():
                if key == chapter:
                #print(keyID)
                    return render_template('manga/page/mangaChapter.html', CHAPTER = chapter, previousChapter = idchapter,  dataIMG= value, title = title, description =dict_mangaPage[keyID]['description'],data = dict_mangaPage.items())  
            else:
                return render_template("manga/404Chapter.html")

def mangaPage(urlnameManga):
    dict_mangaPage ={}
    for keyID, valueID in idMangaJSON().items():
        if urlnameManga == keyID.lower().replace(' ','-'):
            title = f"Otakime - {keyID}"
                    
            """
            for keyChapter, valueChapter in idchapter.items():
                if keyChapter == chapter:
                    url = f"https://api.mangadex.org/at-home/server/{valueChapter}"
                    r = requests.get(url)
                    j = r.json()
                    hashChapter = j['chapter']['hash']
                    imgUrlChapter = j['chapter']['dataSaver']
                    for imgUrl in imgUrlChapter:
                        urlUpload = f"https://uploads.mangadex.org/data-saver/{hashChapter}/{imgUrl}"
                        listurlUpload.append(urlUpload)
                    return render_template('manga/page/mangaChapter.html', dataIMG= listurlUpload)
                #else:
                #    return render_template('manga/404Page.html')
            """        
            dict_mangaPage.update({
                keyID: {
                "nameManga": keyID.lower().replace(' ','-'),
                "title":titleMangaList(valueID),
                "author":authorMangaList(valueID),
                "updateAt": updateAt(valueID),
                "otherName":otherName(valueID),
                "description":desciptionMangaList(valueID),
                "tags":', '.join(tagsMangaList(valueID)),
                "imgIndex":imgIndexMangaList(keyID),
                "imgBanner":imgBannerMangaList(keyID),
                "imgCover":imgCoverMangaList(keyID),
                "chapter":[item['chapter'] for item in ChapterMangaPage(valueID)]
            }
            })
            
            
                          
            return render_template('manga/page/mangaPage.html', data = dict_mangaPage.items(), title= title, description=dict_mangaPage[keyID]['description']) 
    else:   
        return render_template("manga/404Page.html")
    

def blog():
    title = 'Otakime - Blog'
    return render_template('page/blog.html', title = title)

def admin():
    title = 'Otakime - Admin'
    if request.method == "POST":
        name = request.form.get('name')
        password = request.form.get('password')
        
        username= 'potato'
        password='potato'

        if name == username and password == password:
            session['admin'] = name
            session.permanent = True
            return redirect(url_for('adminPostManga'))
    else:
        return render_template('admin/adminLogin.html', title= title)

def logout():
    session.pop("admin", None)
    return render_template('admin/adminLogin.html')

def adminPostManga():
    class ValidateCreateManga(FlaskForm):
        nameManga = StringField("nameManga", validators=[InputRequired()])
        idManga = StringField("idManga", validators=[InputRequired()])
        cardImgUrlIndex = FileField("cardImgUrlIndex",validators=[DataRequired()])
        cardImgUrlBanner = FileField("cardImgUrlBanner",validators=[DataRequired()])
        cardImgUrlCover = FileField("cardImgUrlCover",validators=[DataRequired()])
        chapter = IntegerField("chapter", validators=[InputRequired()])
        imgChapter = MultipleFileField('imgChapter',validators=[DataRequired()])
    if "admin" in session:
        name = session['admin']
        form = ValidateCreateManga()
        if request.method == 'POST':
            nameManga = form.nameManga.data
            idManga = form.nameManga.data
            cardImgUrlIndex = form.cardImgUrlIndex.data
            cardImgUrlBanner = form.cardImgUrlBanner.data
            cardImgUrlCover = form.cardImgUrlCover.data
            chapter = form.chapter.data
            imgChapter = form.imgChapter.data


            if os.path.exists(f"{app.config['IMAGE_UPLOADS']}/{nameManga}"):
                return render_template("post.html", checkFolderExist = True, nameManga= nameManga) #Check thu muc co ton tai ko
            else:    
                os.mkdir(f"{app.config['IMAGE_UPLOADS'] }/{nameManga}")
                os.mkdir(f"{app.config['IMAGE_UPLOADS']}/{nameManga}/chapter")
                os.mkdir(f"{app.config['IMAGE_UPLOADS']}/{nameManga}/logo")

                cardImgUrlIndex.save(os.path.join(f"{app.config['IMAGE_UPLOADS']}/{nameManga}/logo",cardImgUrlIndex.filename))     
                cardImgUrlBanner.save(os.path.join(f"{app.config['IMAGE_UPLOADS']}/{nameManga}/logo",cardImgUrlBanner.filename))
                cardImgUrlCover.save(os.path.join(f"{app.config['IMAGE_UPLOADS']}/{nameManga}/logo",cardImgUrlCover.filename))           

                os.mkdir(f"{app.config['IMAGE_UPLOADS']}/{nameManga}/chapter/{chapter}")

                for item in imgChapter:
                    item.save(os.path.join(f"{app.config['IMAGE_UPLOADS']}/{nameManga}/chapter/{chapter}",item.filename))

            with open('dbManga.json','r') as f:
                data = json.load(f)
            data.update({
                nameManga:{
                    "id" : idManga,
                    "cardImgUrlIndex":f"img/imgManga/{nameManga}/logo/index/{cardImgUrlIndex.filename}",
                    "cardImgUrlBanner":f"img/imgManga/{nameManga}/logo/banner/{cardImgUrlBanner.filename}",
                    "cardImgUrlCover":f"img/imgManga/{nameManga}/logo/cover/{cardImgUrlCover.filename}",
                    "chapter":{
                        chapter:[f'img/imgManga/{nameManga}/chapter/{chapter}/{item.filename}' for item in imgChapter]
                    }
                }
            })
            with open("dbManga.json",'w') as f:
                    f.write(json.dumps(data, indent=4))

                    
            return render_template("admin/page/adminPost.html", form = form)
        return render_template("admin/page/adminPost.html", form = form)
    else:
        return render_template('admin/adminLogin.html')
    
def adminUpdateChapter():
    class ValidateUpdateManga(FlaskForm):
        listFolderImg2= os.listdir(app.config['IMAGE_UPLOADS'])
        chapter = StringField("chapter", validators=[InputRequired()])
        imgChapter = MultipleFileField('imgChapter',validators=[DataRequired()])
        selectedManga = SelectField('selectedManga', choices=listFolderImg2)
    if "admin" in session:
        name = session['admin']
        form = ValidateUpdateManga()
        if request.method == 'POST':
            selectedManga = form.selectedManga.data
            chapter = form.chapter.data
            imgChapter = form.imgChapter.data
            
            if ".gitkeep" == selectedManga:
                return render_template('update.html', success = True,form=form)    

            os.mkdir(f"{app.config['IMAGE_UPLOADS']}/{selectedManga}/chapter/{chapter}")
            for itemIMG in imgChapter:
                itemIMG.save(os.path.join(f"{app.config['IMAGE_UPLOADS']}/{selectedManga}/chapter/{chapter}",itemIMG.filename))

            with open('dbManga.json','r') as f:
                data = json.load(f)
            data[selectedManga]['chapter'][chapter] = [f'img/imgManga/{selectedManga}/chapter/{chapter}/{itemIMG.filename}' for itemIMG in imgChapter]
            with open("dbManga.json",'w') as f:
                f.write(json.dumps(data, indent=4, sort_keys=True))
            return render_template('admin/page/adminUpdateChapter.html',form=form)

        return render_template('admin/page/adminUpdateChapter.html', form=form)
    else:
        return render_template('admin/adminLogin.html')

def adminDeleteManga():
    class ValidateDeleteManga(FlaskForm):
        listFolderImg = os.listdir(app.config['IMAGE_UPLOADS'])
        nameManga = SelectField("nameManga", choices=listFolderImg)
    if "admin" in session:
        name = session['admin']

        form = ValidateDeleteManga()
        if request.method == 'POST':
            nameManga = form.nameManga.data

            with open('dbManga.json','r') as f:
                data = json.load(f)

            shutil.rmtree(f'static/img/imgManga/{nameManga}')

            del data[nameManga]

            with open("dbManga.json",'w') as f:
                f.write(json.dumps(data, indent=4))
            return render_template('admin/page/adminDeleteManga.html',form = form)
        return render_template('admin/page/adminDeleteManga.html', form = form)
    else:
        return render_template('admin/adminPage.html')

def adminDeleteChapter():
    class ValidateDeleteChapter(FlaskForm):
        listFolderImg = os.listdir(app.config['IMAGE_UPLOADS'])
        selectedManga = SelectField('selectedManga', choices=listFolderImg)
        chapter = IntegerField("chapter", validators=[InputRequired()])
    if "admin" in session:
       
        form = ValidateDeleteChapter()
        if request.method == 'POST':
            selectedManga = form.selectedManga.data
            chapter = form.chapter.data

            with open('dbManga.json','r') as f:
                data = json.load(f)

            shutil.rmtree(f'static/img/imgManga/{selectedManga}/chapter/{chapter}')

            del data[selectedManga]['chapter'][chapter]

            with open("dbManga.json",'w') as f:
                f.write(json.dumps(data, indent=4))
            return render_template('admin/page/adminDeleteChapter.html',form = form)

        return render_template('admin/page/adminDeleteChapter.html',form = form)
    else:
        return render_template('admin/adminPage.html')
def adminEmailHire():
    if "admin" in session:
        if request.method == "POST":
            #emailTaker = request.form.get('emailTaker')
            name = request.form.get('name')
            email = request.form.get('email')
            subject = request.form.get('subject')

            msg = Message(
                subject=f'{subject}',
                sender= mail_username,
                recipients=[email],
                html = render_template('admin/page/mailLayout.html', name = name)
                #body= f'Name: {name}\nEmail: {email}\nMessage: {message}' 
            )
            mail.send(msg)
            return render_template('admin/page/mail.html', success = True)
        return render_template('admin/page/mail.html')
    else:
        return render_template('admin/adminPage.html')

    
def sitemap():
    pass

def dieukhoangsudung():
    return send_file('static/dieukhoangsudung.txt')
app.add_url_rule('/','home', home )

app.add_url_rule('/about','about', about )

app.add_url_rule('/contact','contact', contact , methods =['GET','POST'])

app.add_url_rule('/manga','manga', manga )

app.add_url_rule('/blog','blog', blog )

app.add_url_rule('/<urlnameManga>','mangaPage', mangaPage,)
app.add_url_rule('/<urlnameManga>/<chapter>','mangaChapter', mangaChapter)

app.add_url_rule('/admin','admin', admin, methods=['GET','POST'])
app.add_url_rule('/admin','logout', logout, methods=['GET','POST'])

app.add_url_rule('/admin/postmanga','adminPostManga', adminPostManga, methods=['GET','POST'])
app.add_url_rule('/admin/updatemanga','adminUpdateChapter', adminUpdateChapter, methods=['GET','POST'])
app.add_url_rule('/admin/deletemanga','adminDeleteManga', adminDeleteManga, methods=['GET','POST'])
app.add_url_rule('/admin/deletechapter','adminDeleteChapter', adminDeleteChapter, methods=['GET','POST'])

app.add_url_rule('/admin/email','adminEmailHire', adminEmailHire, methods=['GET','POST'])

app.add_url_rule('/dieukhoangsudung','dieukhoangsudung', dieukhoangsudung )

@app.errorhandler(404)
def page_not_found(e):
    return render_template('manga/404Page.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
