
import json
from flask import Flask, render_template, request
from flask_mail import Mail,Message

app = Flask(__name__)

app.debug=True

mail_username='mail.otakime@gmail.com'
mail_password='lpavozmbebtxdhbb'

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
    dictMangaIndex ={}
    temp= 0
    for key,value in getallManga():
        dictMangaIndex.update({key:value})
        temp = temp +1
        if temp == 4:
            break

    return render_template('manga/index.html', data = dictMangaIndex.items()) 

def about():
    return render_template('manga/page/about.html')

def contact():
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

        return render_template('manga/page/contact.html', success = True)

    return render_template('manga/page/contact.html')

def manga():
    return render_template('manga/page/mangaList.html', data = getallManga())

def mangaPage(urlnameManga):
    dict_mangaPage ={}
    for key, value in getallManga():
        if urlnameManga == value['nameManga'].lower().replace(' ','-'):
            dict_mangaPage.update({key:value})  
            return render_template('manga/page/mangaPage.html', data = dict_mangaPage.items()) 
        #=else:
            #return render_template('manga/404Page.html')
    return render_template('manga/page/mangaPage.html', data = dict_mangaPage.items()) 
    

def blog():
    return render_template('page/blog.html')

def admin():
    if request.method == "POST":
        name = request.form.get('name')
        password = request.form.get('password')

        NAME = 'potato'
        PASSWORD = 'potato'

        if name == NAME and password == PASSWORD:
            return render_template('admin/adminMan.html')

    return render_template('admin/admin.html')

def sitemap():
    pass

app.add_url_rule('/','home', home )

app.add_url_rule('/about','about', about )

app.add_url_rule('/contact','contact', contact , methods =['GET','POST'])

app.add_url_rule('/manga','manga', manga )

app.add_url_rule('/blog','blog', blog )

app.add_url_rule('/<urlnameManga>','mangaPage', mangaPage )

app.add_url_rule('/admin','admin', admin, methods=['GET','POST'])




@app.errorhandler(404)
def page_not_found(e):
    return render_template('manga/404Page.html'), 404


