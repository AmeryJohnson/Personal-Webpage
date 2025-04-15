# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request, session, url_for, copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from .utils.database.database  import database
from werkzeug.datastructures   import ImmutableMultiDict
from pprint import pprint
import json
import random
import functools
from . import socketio
db = database()

app.debug = True
#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        # Check if encrypted 'email' is in session
        if "email" not in session:
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)
    return secure_function

def getUser():
    encrypted_email = session.get('email')
    if encrypted_email:
        try:
            decrypted_email = db.reversibleEncrypt('decrypt', encrypted_email)
            return decrypted_email
        except Exception as e:
            print("Error decrypting email:", e)  # For debugging; can be removed in production
    return 'Unknown'

@app.route('/login')
def login():
    return render_template('login.html', user=getUser())

@app.route('/logout')
def logout():
    session.pop('email', default=None)
    return redirect('/home')

@app.route('/processlogin', methods=["POST"])
def processlogin():
    form_fields = dict(request.form)
    email = form_fields.get('email')
    password = form_fields.get('password')

    result = db.authenticate(email=email, password=password)

    if result['success'] == 1:
        # Encrypt the email and store it in session under 'email'
        session['email'] = db.reversibleEncrypt('encrypt', email)
        session.modified = True  # Ensure session update is registered
        return json.dumps({'success': 1, 'redirect': '/home'})
    else:
        attempts = session.get('login_attempts', 0) + 1
        session['login_attempts'] = attempts
        return json.dumps({'success': 0, 'attempts': attempts})

#######################################################################################
# CHATROOM RELATED
#######################################################################################
@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html', user=getUser())

@socketio.on('joined', namespace='/chat')
def joined(message):
    join_room('main')
    if getUser() == 'owner@email.com':
        emit('status', {'msg': getUser() + ' has entered the room.', 'style': 'width: 100%;color:blue;text-align: right'}, room='main')
    else:
        emit('status', {'msg': getUser() + ' has entered the room.', 'style': 'width: 100%;color:grey;text-align: left'},
             room='main')

@socketio.on('text', namespace='/chat')
def text(message):
    if getUser() == 'owner@email.com':
        emit('message', {'msg': getUser() + ': ' + message['msg'], 'style': 'width: 100%;color:blue;text-align: right'}, room='main')
    else:
        emit('message', {'msg': getUser() + ': ' + message['msg'], 'style': 'width: 100%;color:grey;text-align: left'}, room='main')

@socketio.on('left', namespace='/chat')
def left(message):
    leave_room('main')

    if getUser() == 'owner@email.com':
        emit('status', {'msg': getUser() + ' has left the room.', 'style': 'width: 100%;color:blue;text-align: right'}, room='main')
    else:
        emit('status', {'msg': getUser() + ' has left the room.', 'style': 'width: 100%;color:grey;text-align: left'}, room='main')



#######################################################################################
# OTHER
#######################################################################################

@app.route('/processfeedback', methods=['POST'])
def processfeedback():
    # Collect feedback form data
    feedback = {
        'name': request.form['name'],
        'email': request.form['email'],
        'comment': request.form['comment']
    }

    # Insert feedback into the feedback table
    db.insertRows(table='feedback', columns=['name', 'email', 'comment'], parameters=[list(feedback.values())])

    # Retrieve all feedback for display
    all_feedback = db.query("SELECT * FROM feedback")

    # Render feedback page
    return render_template('processfeedback.html', feedback_list=all_feedback)

@app.route('/')
def root():
	return redirect('/home', user=getUser())

@app.route('/home')
def home():
	x     = random.choice(['I started university when I was a wee lad of 15 years.','I have a pet sparrow.','I write poetry.'])
	return render_template('home.html', user=getUser())

@app.route('/resume')
def resume():
	resume_data = db.getResumeData()
	print(resume_data)
	return render_template('resume.html', resume_data = resume_data, is_resume_page = True, user=getUser())

@app.route('/projects')
def projects():
	return render_template('projects.html', user=getUser())

@app.route('/piano')
def piano():
	return render_template('piano.html', user=getUser())

@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r
