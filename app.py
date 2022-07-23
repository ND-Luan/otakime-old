
import json
import os
from flask import Flask, redirect, render_template, request, session, url_for
from flask_mail import Mail,Message
from datetime import timedelta
app = Flask(__name__)

app.debug=True

mail_username='mail.otakime@gmail.com'
mail_password='lpavozmbebtxdhbb'

app.config["SECRET_KEY"] = "POTATO"
app.permanent_session_lifetime = timedelta(seconds=10)

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

def parseJson():
    with open('dbManga.json',encoding="utf8") as f:
        data = json.loads(f.read())
    return data
def getallManga():
    index_list = 0
    dictMangaIndex ={}
    for key , value in parseJson()[index_list].items():
        dictMangaIndex.update({key:value})
    return dictMangaIndex.items()
def getallMangaIndex(nameManga):
    dictMangaIndex ={}
    temp= 0
    for key,value in getallManga():
        if nameManga == value['nameManga']:
            dictMangaIndex.update({key:value})
            temp = temp +1
            if temp == 4:
                break
    return dictMangaIndex.items()
    
def home():
    title= 'Otakime - Nha tu ban'
    description = 'Trang web chính thức của nhóm dịch Otakime, Việt hóa những dự án manga nhằm giới thiệu độc giả. Truy cập ngay để đọc những tựa truyện được yêu thích.'
    dictMangaIndex ={}
    temp= 0
    for key,value in getallManga():
        dictMangaIndex.update({key:value})
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
            body= f'Name: {name}\nEmail: {email}\nMessage: {message}' 

        )
        mail.send(msg)

        return render_template('manga/page/contact.html', success = True, title= title,description=description)

    return render_template('manga/page/contact.html', title= title, description=description)

def manga():
    title = 'Otakime - Manga'
    description = 'Đọc ngay những tựa truyện được Việt hóa chất lượng bởi Otakime.'
    return render_template('manga/page/mangaList.html', data = getallManga(),title= title,description = description)

def mangaPage(urlnameManga):
    dict_mangaPage ={}
    for key, value in getallManga():
        if urlnameManga == value['nameManga'].lower().replace(' ','-'):
            title = f"Otakime - {value['nameManga']}"
            dict_mangaPage.update({key:value})  
            return render_template('manga/page/mangaPage.html', data = dict_mangaPage.items(), title= title) 
        #=else:
            #return render_template('manga/404Page.html')
    return render_template('manga/page/mangaPage.html', data = dict_mangaPage.items()) 
    

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
        return render_template('admin/adminPage.html', title= title)

def logout():
    session.pop("admin", None)
    return render_template('admin/adminPage.html')

def adminPostManga():

    if "admin" in session:
        name = session['admin']
        return render_template('admin/page/adminPost.html', nameAdmin = name)
    else:
        return render_template('admin/adminPage.html')
    
def adminUpdateManga():
    if "admin" in session:
        name = session['admin']
        return render_template('admin/page/adminUpdate.html', nameAdmin = name)
    else:
        return render_template('admin/adminPage.html')

def adminDeleteManga():
    if "admin" in session:
        name = session['admin']
        return render_template('admin/page/adminDelete.html', nameAdmin = name)
    else:
        return render_template('admin/adminPage.html')

def sitemap():
    pass

app.add_url_rule('/','home', home )

app.add_url_rule('/about','about', about )

app.add_url_rule('/contact','contact', contact , methods =['GET','POST'])

app.add_url_rule('/manga','manga', manga )

app.add_url_rule('/blog','blog', blog )

app.add_url_rule('/<urlnameManga>','mangaPage', mangaPage )

app.add_url_rule('/admin','admin', admin, methods=['GET','POST'])
app.add_url_rule('/admin','logout', logout, methods=['GET','POST'])

app.add_url_rule('/admin/postmanga','adminPostManga', adminPostManga, methods=['GET','POST'])
app.add_url_rule('/admin/updatemanga','adminUpdateManga', adminUpdateManga, methods=['GET','POST'])
app.add_url_rule('/admin/deletemanga','adminDeleteManga', adminDeleteManga, methods=['GET','POST'])


@app.errorhandler(404)
def page_not_found(e):
    return render_template('manga/404Page.html'), 404


