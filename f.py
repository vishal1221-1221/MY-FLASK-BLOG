from flask import Flask,render_template,request,session,redirect
#from flask_mail import Mail
#from flask_mail import Message
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'This is your database uri'
db = SQLAlchemy(app)
app.secret_key = 'the random string'
#THIS IS MAIL CONFIG
#app.config.update(
#    MAIL_SERVER = 'smtp.gmail.com',
#    MAIL_PORT ='465',
#    MAIL_USE_SSL = True,
#    MAIL_USERNAME = '',
#    MAIL_PASSWORD= ''
    
#    )
#mail=Mail(app)
class Mytable(db.Model):
    Sno=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    pnum = db.Column(db.String(12), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    
class Mypost(db.Model):
    SNo = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    subhead = db.Column(db.String(21), nullable=False)
    content = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(12), nullable=True)
   
    

@app.route("/")
def front():
    po=Mypost.query.filter_by().all()
    return render_template("index.html",po=po)
@app.route("/about.html")
def about():
    return render_template("about.html")
@app.route("/contact.html",methods=['GET','POST'])
def contact():
    if(request.method=='POST'):
        name=request.form.get('name')
        email=request.form.get('email')
        phnum=request.form.get('pnum')
        msg=request.form.get('message')
        entry = Mytable(name=name, pnum =phnum, message = msg,email = email )
        db.session.add(entry)
        db.session.commit()
        #THIS IS FOR SEND MAIL TO YOUR GMAIL ACCOUNT BUT YOU NEED TO CONFIGURE SOME SETTING IN GMAIL ACCOUNT LIKE -ON LESS SECURE APP
        #mail.send_message('New message from ' + name,
        #                  sender=email,
        #                recipients = ['your email'],
        #                  body = msg + "\n" + phnum
        #                  )
    return render_template("contact.html")
@app.route("/")
def home():
    
    return render_template("/index.html")  
@app.route("/post.html/<string:post_slug>",methods=['GET'])
def postroute(post_slug):
    post=Mypost.query.filter_by(slug=post_slug).first()
    return  render_template("post.html",post=post)
@app.route("/dash", methods=['GET','POST'])
def dash():
    posts=Mypost.query.all()
    uname='Any mail'
    passw='any password'
    u=request.form.get('uname')
    p=request.form.get('pass')
    print(u,p)
    if ('user' in session and session['user']==uname):
        return render_template("dash.html",posts=posts)
    if request.method=='POST':
        if(u==uname and p==passw):
            session['user']=uname
            return render_template("dash.html")
    else:
        return render_template("login.html")
@app.route("/new/<string:SNo>",methods=['GET','POST'])
def new(SNo):
    if ('user' in session and session['user']==uname):
        print(request.method)
        if request.method=='POST':
            print("in if")
            slug=request.form.get('SLUG')
            
            title=request.form.get('TITLE')
            content=request.form.get('CONTENT')
            subheading=request.form.get('SUBHEADING')
            date=datetime.now()
            print(slug,title,content)
            if SNo=='0':
                
                print("you are in o")
            
                posts=Mypost(title=title,content=content,subhead=subheading,slug=slug,date=date)
                db.session.add(posts)
                db.session.commit()
             
        return  render_template("new.html",SNo=SNo)
@app.route("/edit/<string:SNo>",methods=['GET','POST'])
def edit(SNo):
    if ('user' in session and session['user']=='v@gmail.com'):
        print(request.method)
        if request.method=='POST':
            
            slug=request.form.get('SLUG')
            
            title=request.form.get('TITLE')
            content=request.form.get('CONTENT')
            subheading=request.form.get('SUBHEADING')
            date=datetime.now()
            print(slug,title,content)
            posts=Mypost.query.filter_by(SNo=SNo).first()
            posts.title=title
            posts.content=content
            posts.subhead=subheading
            posts.date=date
            posts.slug=slug
            db.session.commit()
            return redirect("/edit/"+SNo)
          
        posts=Mypost.query.filter_by(SNo=SNo).first()     
        return  render_template("edit.html",SNo=SNo,posts=posts)
@app.route("/delete/<string:SNo>",methods=['GET','POST'])
def delete(SNo):
    if ('user' in session and session['user']=='v@gmail.com'):
        posts=Mypost.query.filter_by(SNo=SNo).first()
        db.session.delete(posts)
        db.session.commit()
    return redirect("/dash")
@app.route("/logout")
def logout():
    if ('user' in session and session['user']==uname):
        session.pop('user')
        return redirect("/dash")
      
app.run(debug=True)