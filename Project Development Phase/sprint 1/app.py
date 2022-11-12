from flask import Flask, render_template,request,redirect,url_for,session,flash
import ibm_db

app=Flask(__name__)
app.secret_key='a'
try:
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=125f9f61-9715-46f9-9399-c8177b21803b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30426;SECURITY=SSL;SSLServerCertificat=DigiCertGlobalRootCA.crt;UID=wfq61013;PWD=mlp4pZJpldWruPNU",'','')
except:
    print("Unable to connect: ",ibm_db.conn_error())
    
@app.route("/")
def dash():
    return render_template('welcome.html',msg=" ")
    
@app.route("/register",methods=['GET','POST'])
def register():
    error = None 
    if request.method=='POST':
           username=request.form['username']
           email=request.form['email']
           phone_number=request.form['phonenumber']
           password=request.form['password']
           pin=request.form['pin']
           sql="SELECT * FROM user WHERE phone_number=?"
           prep_stmt=ibm_db.prepare(conn,sql)
           ibm_db.bind_param(prep_stmt,1,phone_number)
           ibm_db.execute(prep_stmt)
           account=ibm_db.fetch_assoc(prep_stmt)
           print(account)
           if account:
               error="Account already exists! Log in to continue !"
           else:
               insert_sql="INSERT INTO user values(?,?,?,?,?)"
               prep_stmt=ibm_db.prepare(conn,insert_sql)
               ibm_db.bind_param(prep_stmt,1,email)
               ibm_db.bind_param(prep_stmt,2,username)
               ibm_db.bind_param(prep_stmt,3,phone_number)
               ibm_db.bind_param(prep_stmt,4,password)
               ibm_db.bind_param(prep_stmt,5,pin)
               ibm_db.execute(prep_stmt)
               flash(" Registration successfull. Log in to continue !")
    else:
        pass
    return render_template('register.html',error=error)

@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        sql="SELECT * FROM user WHERE username=? AND password=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['Loggedin']=True
            session['id']=account['USERNAME']
            session["username"]=account["USERNAME"]
            flash("Logged in successfully!")
            return redirect(url_for("home"))
        else:
            error="Incorrect username / password"
            return render_template('login.html',error=error)
    return render_template('login.html',error=error)

@app.route('/forget',methods=['GET','POST'])
def forget():
    error = None
    if request.method=='POST':
        username=request.form['username']
        pin=request.form['pin']
        sql="SELECT * FROM user WHERE username=? AND pin=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,pin)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['Loggedin']=True
            session['id']=account['USERNAME']
            session["username"]=account["USERNAME"]
            flash("Logged in successfully!")
            return redirect(url_for("home"))
        else:
            error="Incorrect username / pin"
            return render_template('login.html',error=error)
    return render_template('forget.html',error=error)
@app.route('/welcome')
def welcome_page():
    return render_template("welcome.html",msg=" ")
@app.route('/home')
def home():
    return render_template("home.html",msg=" ")
if __name__=='__main__':
    app.run(debug=True)
