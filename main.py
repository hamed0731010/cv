from operator import imod
from flask import Flask, render_template, request, session, redirect
import json

app = Flask(__name__,static_url_path='/static')
app.secret_key = 'Salam'


@app.route('/')
def home():
    user = None
    if 'username' not in session:
        return redirect('/login')
    with open('db.json','r') as file:
        data=json.load(file)     
    for usr in data:
        if usr['id'] == session['username']:
            user = usr
            break
    if user == None:
        return redirect('/login')
    return render_template('cv.html', user=user)

@app.route('/logout')

def logout():
    session.pop('username')
    return redirect('/login')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login-post', methods =['POST'])
def login_post():
    username = request.form.get('username', None)
    password = request.form.get('password', None)
    with open('db.json','r') as file:
        data=json.load(file)
    for user in data:
        if user['username'] == username and user['password']== password:
            session['username'] = user['id']
            return redirect('/')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup-post', methods =['POST'])
def signup_post():
    li=[]
    id = request.form.get('id', None)
    full_name = request.form.get('fullname', None)
    username = request.form.get('username', None)
    password = request.form.get('password', None)
    user_dict = {'id':id, 'username':username, 'password':password, 'full_name':full_name}
    with open('db.json') as fp:
         li=json.load(fp)
    li.append(user_dict)   
    with open('db.json', 'w') as json_file:
        json.dump(li, json_file, 
                        indent=4,  
                        separators=(',',': '))
 
    return redirect('/login')
app.run()
