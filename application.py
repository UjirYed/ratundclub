import os
import requests
import eventlet
eventlet.monkey_patch()
from flask import Flask, session, render_template, request, redirect, url_for
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from collections import deque

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")
#All users online
CurrentUsers = []
#All Channels online
CurrentChannels = []

channelsMessages = dict()


#users will sign in through here.
@app.route("/")
def index():
    if "username" in session:
        return redirect('/chat')
    return render_template("index.html")

@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect("/")

#Main Page for accessing everything
@app.route("/chat", methods = ["GET", "POST"])
def chat():
    if request.method == "POST":
        username = request.form.get("username")
        if not username: #Check if username variable exists and the user actually entered a name
            return render_template("error.html", message="No username entered")
        if username in CurrentUsers:
            return render_template("error.html", message="Someone is already using that username.")
        session["username"] = username

    if not session.get("username"):
        return redirect('/')
    return render_template('chat.html', CurrentChannels=CurrentChannels)
#Creating Channels
@app.route("/addchannel", methods = ["POST", "GET"])
def addchannel():
    if request.method == "POST":
        Channelrequest = request.form.get("channelrequest")
        if Channelrequest is None or Channelrequest == "":
            return render_template("error.html", message="No Channel name entered")
        if Channelrequest in CurrentChannels:
            return render_template("error.html", message="This channel already exists! Try again.")
        CurrentChannels.append(Channelrequest)

        # Add channel to global dict of channels with messages
        # Every channel is a deque to use popleft() method
        # https://stackoverflow.com/questions/1024847/add-new-keys-to-a-dictionary
        channelsMessages[Channelrequest] = deque()

        return redirect("/channel/" + Channelrequest)

    return render_template("addchannel.html")
#Going to a specific channel

@app.route("/channel/<channelname>")
def channels(channelname):
    if channelname not in CurrentChannels:
        return render_template("error.html", message="This channel does not exist.")
    session["UserChannel"] = channelname
    return render_template("channel.html", CurrentChannels=CurrentChannels, channel=channelname, messages=channelsMessages[channelname])

@app.route("/checkvariables")
def checkvariables():
    username = session.get("username")
    return render_template("checkeverything.html", username=username, CurrentUsers=CurrentUsers, CurrentChannels=CurrentChannels)

@socketio.on("submit message")
def submitMessage(message, timestamp):
    username = session.get("username")
    room = session.get('UserChannel')
    if len(channelsMessages[room]) > 100:
        # Delete old messages
        channelsMessages[room].popleft()

    channelsMessages[room].append([timestamp, session.get('username'), message])

    emit('display message', {
        'user': session.get('username'),
        'timestamp': timestamp,
        'message': message},
        room=room)

@socketio.on("joined")
def joined():
    room = session.get("UserChannel")
    join_room(room)

    emit("status", {
    "username": session.get("username"),
     "channel": room,
     "message": str(session.get("username")) + " has joined!"},
     room=room)

if __name__ == "__main__":
    socketio.run(app)
