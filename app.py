from flask import Flask, redirect, render_template, request, send_file, session, url_for,jsonify,make_response
from flask_mail import Mail,Message

from datetime import timedelta
from dbFireBase import getManga


from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField,IntegerField,MultipleFileField,SelectField,DateField,SelectField
from wtforms.validators import DataRequired,InputRequired,Optional

from firebase import db,storage,user
from werkzeug.utils import secure_filename
app = Flask(__name__)

app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.config['IMAGE_UPLOADS'] = 'static/img/imgManga'

mail_username='mail.otakime@gmail.com'
mail_password='lpavozmbebtxdhbb'

app.config["SECRET_KEY"] = "POTATO"
#app.permanent_session_lifetime = timedelta(seconds=1000)

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
    dictMangaKawai ={}
    dictMangaR15  ={}
    dictMangaToaru ={}
    dictMangaMizore ={}

    nameMangaKawaii = "Kawaii Kanojo-chan"
    nameMangaR15 = "R15 Ja Dame Desuka"
    nameMangaToaru = "Toaru Meoto no Nichijou"
    nameMangaMizore = "Tokedase Mizore-chan"

    for key,value in getManga().items():
        if key == nameMangaKawaii:
            dictMangaKawai.update({
                key:{
                    "url" : key.lower().replace(' ','-'),
                    "nameManga": value['nameManga'],
                    "description": value['description'],
                    "tags":', '.join(value['tags']),
                    "imgIndex":value['imgIndex'],
                    "imgBanner":value['imgBanner'],
                    "imgCover":value['imgCover']
                }
            })

            break
    for key,value in getManga().items():
        if key == nameMangaR15:
            dictMangaR15.update({
                key:{
                    "url" : key.lower().replace(' ','-'),
                    "nameManga": value['nameManga'],
                    "description": value['description'],
                    "tags":', '.join(value['tags']),
                    "imgIndex":value['imgIndex'],
                    "imgBanner":value['imgBanner'],
                    "imgCover":value['imgCover']
                }
            })

            break
    for key,value in getManga().items():
        if key == nameMangaToaru:
            dictMangaToaru.update({
                key:{
                    "url" : key.lower().replace(' ','-'),
                    "nameManga": value['nameManga'],
                    "description": value['description'],
                    "tags":', '.join(value['tags']),
                    "imgIndex":value['imgIndex'],
                    "imgBanner":value['imgBanner'],
                    "imgCover":value['imgCover']
                }
            })

            break
    for key,value in getManga().items():
        if key == nameMangaMizore:
            dictMangaMizore.update({
                key:{
                    "url" : key.lower().replace(' ','-'),
                    "nameManga": value['nameManga'],
                    "description": value['description'],
                    "tags":', '.join(value['tags']),
                    "imgIndex":value['imgIndex'],
                    "imgBanner":value['imgBanner'],
                    "imgCover":value['imgCover']
                }
            })

            break

    return render_template(
        'manga/index.html', 
        dataKawaii = dictMangaKawai.items(),
        dataR15 = dictMangaR15.items(),
        dataToaru = dictMangaToaru.items(),
        dataMizore = dictMangaMizore.items(),
        title= title, 
        description= description) 

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

    for key,value in getManga().items():
        dictManga.update({
            key:
            {
                "url": key.lower().replace(' ','-'),
                "nameManga":value['nameManga'],
                "author":value['author'],
                "updateAt": value['updateAt'],
                "otherName":value['otherName'],
                "description":value['description'],
                "tags":', '.join(value['tags']),
                "imgIndex":value['imgIndex'],
                "imgBanner":value['imgBanner'],
                "imgCover":value['imgCover']
            }
            })
  
    return render_template('manga/page/mangaList.html', data = dictManga.items(),title= title,description = description)


def mangaChapter (urlnameManga,chapter):
    dict_mangaPage ={}
    for keyID, valueID in getManga().items():
        if urlnameManga == keyID.lower().replace(' ','-'):
            title = f"Otakime - {keyID}"
            dict_mangaPage.update({
                keyID: {
                "url": keyID.lower().replace(' ','-'),
                "nameManga":valueID['nameManga'],
                "author":valueID['author'],
                "updateAt": valueID['updateAt'],
                "otherName":valueID['otherName'],
                "description":valueID['description'],
                "tags":', '.join(valueID['tags']),
                "imgIndex":valueID['imgIndex'],
                "imgBanner":valueID['imgBanner'],
                "imgCover": valueID['imgCover'],
                "chapter":[item for item in valueID['chapter']]
            }
            })
            
            for keychapterDB,vauleIMG in valueID['chapter'].items():
                
                if  keychapterDB.lower().replace('chap ','') == chapter:
                #print(keyID)
                    return render_template('manga/page/mangaChapter.html', CHAPTER = chapter, previousChapter = [item.lower().replace('chap ','') for item in dict_mangaPage[keyID]['chapter']],  dataIMG= vauleIMG, title = title, description =dict_mangaPage[keyID]['description'],data = dict_mangaPage.items())  
            else:
                return render_template("manga/404Chapter.html")

def mangaPage(urlnameManga):
    dict_mangaPage ={}
    for keyID, valueID in getManga().items():
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
                
                "url" : keyID.lower().replace(' ','-'),
                "nameManga":valueID['nameManga'],
                "author":valueID['author'],
                "updateAt": valueID['updateAt'],
                "otherName":valueID['otherName'],
                "description":valueID['description'],
                "tags":', '.join(valueID['tags']),
                "imgIndex":valueID['imgIndex'],
                "imgBanner":valueID['imgBanner'],
                "imgCover": valueID['imgCover'],
                "chapter":[item for item in valueID['chapter']]

            }
            })
            img = getManga()['Sonouchi kekkon made ikukedo ima wa mada']['imgDonate']
            
            
                          
            return render_template('manga/page/mangaPage.html',url=urlnameManga, img= img ,data = dict_mangaPage.items(), title= title, description=dict_mangaPage[keyID]['description']) 
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
        author = StringField("author", validators=[InputRequired()])
        otherName = StringField("otherName",validators=[InputRequired()])
        tags = StringField("tags",validators=[InputRequired()])
        tag = SelectField("tag",choices=['Romance','DarkHole','Book'])
        updateAt = DateField("updateAt",validators=[InputRequired()])
        description = StringField("description", validators=[InputRequired()])
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
            author = form.author.data
            otherName = form.otherName.data
            tags = form.tags.data
            updateAt = form.updateAt.data
            description = form.description.data
            cardImgUrlIndex = form.cardImgUrlIndex.data
            cardImgUrlBanner = form.cardImgUrlBanner.data
            cardImgUrlCover = form.cardImgUrlCover.data
            chapter = form.chapter.data
            imgChapter = form.imgChapter.data

            print(cardImgUrlIndex.filename)
            storage.child("manga").child(nameManga).child("logo").child(cardImgUrlIndex).put(secure_filename(cardImgUrlIndex.filename))
            storage.child("manga").child(nameManga).child("logo").child(cardImgUrlBanner).put(cardImgUrlBanner)
            storage.child("manga").child(nameManga).child("logo").child(cardImgUrlCover).put(cardImgUrlCover)


                    
            return render_template("admin/page/adminPost.html", form = form, success = True)
        return render_template("admin/page/adminPost.html", form = form)
    else:
        return render_template('admin/adminLogin.html')
    
def adminUpdateChapter():
    class ValidateUpdateManga(FlaskForm):

        chapter = StringField("chapter", validators=[InputRequired()])
        imgChapter = MultipleFileField('imgChapter',validators=[DataRequired()])
        selectedManga = SelectField('selectedManga', choices=[])
    if "admin" in session:
        name = session['admin']
        form = ValidateUpdateManga()
        if request.method == 'POST':
            selectedManga = form.selectedManga.data
            chapter = form.chapter.data
            imgChapter = form.imgChapter.data
            


        return render_template('admin/page/adminUpdateChapter.html', form=form)
    else:
        return render_template('admin/adminLogin.html')

def adminDeleteManga():
    class ValidateDeleteManga(FlaskForm):
        nameManga = SelectField("nameManga", choices=[])
    if "admin" in session:
        name = session['admin']

        form = ValidateDeleteManga()
        if request.method == 'POST':
            nameManga = form.nameManga.data

           
            return render_template('admin/page/adminDeleteManga.html',form = form)
        return render_template('admin/page/adminDeleteManga.html', form = form)
    else:
        return render_template('admin/adminPage.html')

def adminDeleteChapter():
    class ValidateDeleteChapter(FlaskForm):
      
        selectedManga = SelectField('selectedManga', choices=[])
        chapter = IntegerField("chapter", validators=[InputRequired()])
    if "admin" in session:
       
        form = ValidateDeleteChapter()
        if request.method == 'POST':
            selectedManga = form.selectedManga.data
            chapter = form.chapter.data



           
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

app.add_url_rule('/dieukhoan','dieukhoangsudung', dieukhoangsudung )

@app.errorhandler(404)
def page_not_found(e):
    return render_template('manga/404Page.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
