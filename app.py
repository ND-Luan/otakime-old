import json
from flask import Flask, render_template, request
from flask_mail import Mail,Message

app = Flask(__name__)
mail = Mail(app)

mail_username='mail.otakime@gmail.com'
mail_password='smwacblnqgibazdd'

app.debug=True

app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = mail_username
app.config['MAIL_PASSWORD'] = mail_password




def parseJson():
    with open('dbManga.json',encoding="utf8") as f:
        data = json.loads(f.read())
    return data

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
    

def getallManga():
    index_list = 0
    dictMangaIndex ={}
    for key , value in parseJson()[index_list].items():
        dictMangaIndex.update({key:value})
    return dictMangaIndex.items()



@app.route("/")
def home():
    dictMangaIndex ={}
    temp= 0
    for key,value in getallManga():
        dictMangaIndex.update({key:value})
        temp = temp +1
        if temp == 4:
            break

    return render_template('manga/index.html', data = dictMangaIndex.items()) 


@app.route("/about")
def about():
    return render_template('manga/page/about.html')

@app.route("/contact", methods = ['GET','POST'])
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

@app.route("/manga")
def manga():
    return render_template('manga/page/mangaList.html', data = getallManga())


@app.route("/<urlnameManga>")
def mangaPage(urlnameManga):
    dict_mangaPage ={}
    for key, value in getallManga():
        if urlnameManga == value['nameManga'].lower().replace(' ','-'):
            dict_mangaPage.update({key:value})  
            break
        #else:
            #return render_template('manga/404Page.html')
 
    return render_template('manga/page/mangaPage.html', data = dict_mangaPage.items()) 

        

@app.route("/blog")
def blog():
    return render_template('page/blog.html')

@app.route("/admin", methods=['GET','POST'])
def admin():
    if request.method == "POST":
        name = request.form.get('name')
        password = request.form.get('password')

        NAME = 'potato'
        PASSWORD = 'potato'

        if name == NAME and password == PASSWORD:
            return render_template('admin/adminMan.html')

    return render_template('admin/admin.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('manga/404Page.html'), 404