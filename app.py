from main import retrieve_section,call_db
import json
from flask import Flask,render_template,request,jsonify,url_for,redirect,flash
from flask_pymongo import pymongo
from audio import record,audio_to_text
import speech_recognition as sr


import os

app = Flask(__name__)
app.secret_key = 'random string'


CONNECTION_STRING = "Your-connection-string"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('ipc_insight')


@app.route("/", methods=["GET","POST"])
def index():
    return render_template('about.html')

@app.route("/sign.html",methods=["GET","POST"])
def sign():
    return render_template('sign.html')

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == 'POST':
        name=request.form['name']
        email = request.form['email']
        password = request.form['password']
        check = db.ipc_insight.find_one({"email": email})

        if check:
            print("Same USer NAme Already Exists!!")
            msg="Username Already Exists"
            # return redirect('/signup')
            flash("Same User Already exist")
            return redirect(url_for('signup'))

        else:
            db.ipc_insight.insert_one({"name": name,"email":email,"password":password})
            print(name,email,password)
            print("data added")
            return render_template('sign.html')
        
    return render_template('sign.html')


@app.route("/login", methods=["GET","POST"])
def menu():
    if request.method =='POST':
        email=request.form['email']
        password = request.form['password']

        user = db.ipc_insight.find_one({"$and": [{"email": email}, {"password": password}]})

        if user:
            print(user['name'])
            return render_template('menu.html',name=user['name']) 
          
            
        else:
            print(user)
            print("Login Failed")
            flash('Incorrect Credentials')
            return redirect(url_for('menu'))
           
        
    return render_template('sign.html')


@app.route("/chat.html/", methods=["GET","POST"])
def chat():
    return render_template('index.html')

@app.route("/get", methods=["GET","POST"])
def get():
    input_data = request.form['text']

    if input_data == "":
        print("No Input")
        input_data=""
        print(input_data)
        return render_template('index.html')
    
    else:
        result = call_db(input_data)
        print(input_data)
        print(result)
        return jsonify({"message": result})


@app.route('/upload', methods=["GET","POST"])
def upload_audio():
    if 'audio_data' not in request.files['audio_data']:
        print("No Audio")

    # if request.method == "POST":
        file = request.files['audio_data']
        print(request.files)
        data = file.read()
        print(type(data))
        file.seek(0)

        name = request.files['audio_data'].filename
        print(name)
        name = name.replace(":", "-")
        name = name.replace(".", "-") + '.wav'
        with open(name, 'wb') as audio:
            file.save(audio)
        print(name)
        print("File Uploaded Succesfuly")

                
        result = audio_to_text(name)
        print(result)

        if result == "":
            print("No output")
            os.remove("./" + name)
            return render_template('index.html')
        
        else:
            os.remove("./" + name)
            return jsonify({"message": result})

    

@app.route('/logout', methods=["GET","POST"])
def logout():
    return redirect(url_for('index'))
    # return render_template('about.html')


@app.route("/about.html" , methods=["GET","POST"])
def about():
    return render_template('about.html')


@app.route('/try.html',methods=["GET","POST"])
def back():
    return render_template('try.html')
        
    

if __name__ == "__main__":
    app.run()
    # debug=True



