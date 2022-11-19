from flask import Flask, render_template, session, url_for, redirect, flash, request
import ibm_db;
con=ibm_db.connect("DATABASE=bludb;HOSTNAME=2d46b6b4-cbf6-40eb-bbce-6251e6ba0300.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32328;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=bkj82229;PWD=KCwhio0Cb0XQmB5H",'','')

app = Flask(__name__);

app.secret_key="Secret";

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard/", methods=['GET', 'POST'])
def dashboard():
    if session:
        return render_template("dashboard.html")
    flash("You're not logged in. Please login to enter into dashboard", "danger")
    return redirect(url_for('login'))
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login')) 

@app.route("/login/", methods=['GET','POST'])
def login():
    if request.method=="GET":
        return render_template("login.html")
    
    elif request.method=="POST":
        User_mailid=request.form['mailid']
        User_pswd=request.form['pswd']
        
        sql="SELECT * FROM user_login WHERE User_mailid=? and User_pswd=?" 
        stmt=ibm_db.prepare(con,sql)
        ibm_db.bind_param(stmt,1,User_mailid)
        ibm_db.bind_param(stmt,2,User_pswd)
        ibm_db.execute(stmt)
        data=ibm_db.fetch_assoc(stmt)

        if data:
            session["mailid"]= User_mailid
            return redirect(url_for("dashboard"))
            
        else:
            flash("E-mail & Password Mismatch","danger")
        
        return redirect(url_for("login"))


@app.route("/registration/")
def registration():
    return render_template("registration.html")         

@app.route("/addrec/", methods=['GET', 'POST'])
def addrec():
    
    if request.method == 'POST':
        # try:
            User_fname=request.form['User_fname'];
            User_lname=request.form['User_lname'];
            User_mailid=request.form['User_mailid'];
            User_pswd=request.form['User_pswd'];
            User_repswd=request.form['User_repswd'];
            User_phoneno=request.form['User_phoneno'];
            
            if(User_pswd==User_repswd):                

                sql="SELECT * FROM user_login WHERE User_mailid=?"
                stmt=ibm_db.prepare(con,sql)
                ibm_db.bind_param(stmt,1,User_mailid)
                ibm_db.execute(stmt)
                account=ibm_db.fetch_assoc(stmt)

                if account:
                    flash("User already exists with the same email-id, Try another one", "danger")
                    return redirect(url_for("registration"))        
                
                
                stmt2="INSERT INTO user_login VALUES(?,?,?,?,?)"
                prep_stmt=ibm_db.prepare(con,stmt2)                
                ibm_db.bind_param(prep_stmt,1,User_fname)    
                ibm_db.bind_param(prep_stmt,2,User_lname)    
                ibm_db.bind_param(prep_stmt,3,User_mailid)
                ibm_db.bind_param(prep_stmt,4,User_pswd)
                ibm_db.bind_param(prep_stmt,5,User_phoneno)
                
                ibm_db.execute(prep_stmt)  
                
                flash("Record added successfully", "success")
            else:
                flash("Password & Retype password mismatches","danger")
                return redirect(url_for("registration"))
            
        # except:                
        #     flash("Error in Registration", "danger")
            
       
    return redirect(url_for("login"))