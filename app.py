"""
Project Edu-Meeting
Done By Sameer Shaik (Backend Only)
deployed on:  https://ruraledusystem.azurewebsites.net
github link: https://github.com/Sameer7878/Rural_online_education_system
Tech Stack:
Python Flask FrameWork
MongoDB database
gunicorn server
html,css,bootstarp,javascript
"""
#==========================
from flask import *
import pymongo
import certifi
#==========================
ca = certifi.where()
client = pymongo.MongoClient(
    "mongodb+srv://nikhila:nikhila7878@outsourcing.fl6cohl.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
db=client['edu_meet']
users=db['logins']

# ==========================
"""
App Configurations
"""
app=Flask(__name__)
app.secret_key = '27009e15fbad776cfb3cf6fe174790e42574c8af5be4eb884f76acc874b4c0a9'
# ==========================
"""
Routes of the application
"""

# ==========================
@app.route('/')
def index():
    if 'auth' in session:
        return render_template('index.html',login=True,name=session['name'])
    return render_template('index.html',login=False)
@app.route('/login/',methods=["POST","GET"])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        user=users.find_one({"email":username.lower()})
        if user:
            if user['password']==password:
                session [ 'name' ] = user['name']
                session [ 'auth' ] = True
                session [ 'id' ] = user['id']
                if 'next' in request.args:
                    return redirect(request.args.get('next'))
                return redirect('/')
            return render_template('login.html',errormsg="Incorrect Password")
        return render_template('login.html',errormsg="User Not Found. Please Register First")
    if 'next' in request.args:
        errormsg='Please Login First'
        return render_template('login.html', errormsg=errormsg)
    return render_template('login.html')
@app.route('/stu_register/',methods=["POST","GET"])
def stu_register():
    if request.method == "POST":
        name = request.form['fullname']
        mobile = request.form['mobilenum']
        email = request.form['email']
        password = request.form['password']

        # Check if the user already exists in the database
        user_status = users.find_one({"email": email.lower()})
        if not user_status:
            # Get the highest existing user ID or set to 1 if no users exist
            if users.find_one(sort=[("id", -1)]) is None:
                id = 1
            else:
                id = users.find_one(sort=[("id", -1)])['id'] + 1

            # Insert the user with an initial score of 0
            users.insert_one({"id": id, "name": name.upper(), "mobile": mobile, "email": email.lower(),
                              "password": password, "score": 0})

            # Set user information in the session
            session['name'] = name
            session['auth'] = True
            session['id'] = id
            session['score'] = 0  # Added to session for future use
            return redirect('/')
        return render_template('signup.html', errormsg="User Already Exists")
    return render_template('signup.html')

@app.route('/village/<village_id>/')
def village(village_id):
    return render_template(f'village{village_id}.html')
@app.route('/video_tutorial/<video_id>/')
def video_tutorial(video_id):
    return render_template(f'video{video_id}.html')
@app.route('/meeting_details/')
def meeting_details():
    if 'auth' in session:
        return render_template('meeting-details.html')
    return redirect(url_for('login',next="/meeting_details/"))
@app.route('/meetings/')
def meetings():
    if 'auth' in session:
        return render_template('meetings.html')
    return redirect(url_for('login',next="/meetings/"))
@app.route('/progress_test/')
def progess_test():
    return render_template('progress.html')
@app.route('/game/<game_id>')
def game(game_id):
    return render_template(f'game{game_id}.html')
@app.route('/signout/')
def signout():
    session.pop('auth')
    return redirect('/')
#===========================



if "__main__"==__name__:
    app.run()




