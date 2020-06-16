from flask import Flask,render_template,request,url_for,redirect,session,flash,g
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'user'
mysql = MySQL(app)
bcrypt = Bcrypt()

@app.before_request
def before_request():
    g.username = None

    if 'username' in session:
        g.username = session['username']

@app.route('/')
def root():
    return render_template('login.html')

@app.route('/authentication',methods=['POST','GET'])
def authenticate():
    if request.method == 'POST':
        uname = request.form['username']
        passwrd = request.form['password']    

        cur = mysql.connection.cursor()
        cur.execute("SELECT username,password FROM user WHERE username=%s",[uname])
        user = cur.fetchone()
        temp = user[1]

        if len(user) > 0:
            session.pop('username',None)

            if (bcrypt.check_password_hash(temp,passwrd)) == True:   
                session['username'] = request.form['username']
                return render_template('home.html',uname=uname)
            else:
                flash('Invalid Username or Password !!')
                return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/home')
def home():
    if g.username:
        return render_template('home.html')
    else:
        return render_template('login.html')
 
@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')

if __name__ == '__main__':
  app.secret_key = os.urandom(24)
  app.run(host='127.0.0.1', port=8000, debug=True)
 