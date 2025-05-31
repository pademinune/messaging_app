from flask import Flask, request, render_template, session, redirect, url_for

# from messaging import messenger, message, user

import database.database as database

app = Flask(__name__)
app.secret_key = "your-secret-key-here"


def process_messages(messages):
    lst = []
    for msg in messages[::-1]:
        lst.append({
            "sender": m.get_user(msg.get_sender_id()).get_username(),
            "sender_id": msg.get_sender_id(),
            "receiver": m.get_user(msg.get_receiver_id()).get_username(),
            "receiver_id": msg.get_receiver_id(),
            "text": msg.get_text()
        })
    # print(lst)
    return lst

def message_dict(msg):
    d = {}
    d["senderId"] = msg[1]
    d["senderName"] = database.get_user_by_id(msg[1])[1]
    d["receiverId"] = msg[2]
    d["receiverName"] = database.get_user_by_id(msg[2])[1]
    d["text"] = msg[3]
    d["timestamp"] = msg[4]
    return d



@app.route("/")
def start():
    return redirect("/home")


@app.route('/home')
def index():
    return render_template('index.html')

@app.route("/user_page/user_list")
def user_list():
    return render_template("user_list.html")


@app.route('/about')
def about():
    return render_template("about.html")

@app.route("/fake")
def fake():
    return "You've discovered something cool"

@app.route("/login", methods=['POST'])
def login():
    data = request.form
    username = data["username"]
    password = data["password"]
    # id = database.get_user_by_username(username)
    if not database.user_exists(username=username):
        u = database.add_user(username, password)
        session["user_id"] = database.get_id_by_username(username)
        return redirect("/user_page")
    else:
        u = database.get_user_by_username(username)
        if password != u[2]:
            return f"A user with a username of {username} (id is {id}) already exists!"
        else:
            session["user_id"] = u[0]
            return redirect("/user_page")

@app.route("/logout")
def logout():
    session.pop("user_id")
    return redirect("/home")

@app.route("/send_message", methods=['POST'])
def send_message():
    data = request.form
    username = data["username"]
    message = data["message"]

    if not database.user_exists(username=username):
        return "No such user..."
    else:
        receiver_id = database.get_id_by_username(username)
        database.add_message(session["user_id"], receiver_id, message)
        return redirect("/user_page")

@app.route("/send_message/<to_id>", methods=['POST'])
def send_message_to(to_id):
    data = request.form
    message = data["message"]

    if not database.user_exists(id=to_id):
        return "No such user..."
    else:
        # receiver_id = database.get_id_by_username(username)
        database.add_message(session["user_id"], to_id, message)
        return redirect(f"/chat?to={to_id}")

# @app.route("/json")
# def json():
#     return m.user_dict()

# @app.route("/api/text")
# def apitext():
#     return "hello"

@app.route("/user_page")
def user_page():
    id = session.get("user_id")
    if id == None:
        return redirect("/home")
    
    if not database.user_exists(id=id):
        session.pop("user_id")
        return redirect("/home")
    usr = database.get_user_by_id(id)
    return render_template("logged_in.html", username=usr[1], password=usr[2])
    # return render_template("logged_in.html", username=u.get_username(), password = u.get_password(), messages = process_messages(u.get_messages()), 
    #                        sent_messages = process_messages(u.get_sent_messages()))

@app.route("/chat")
def chat():
    to_id = request.args.get("to")
    if session.get("user_id") == None:
        return redirect("/home")
    return render_template("chat.html", to_user = database.get_username_by_id(to_id))

@app.route("/api/self_id")
def self_id():
    id = session.get("user_id")
    if id == None:
        return {"user_id": -1}
    else:
        return {"user_id": id}

@app.route("/api/user_info/<id>")
def user_info(id):
    id = int(id)
    if not database.user_exists(id=id):
        return {"userId": -1}
    else:
        return {"userId": id, "username": database.get_username_by_id(id)}

@app.route("/api/received_messages")
def get_received_messages_json():
    usr_id = session.get("user_id")
    return [message_dict(msg) for msg in database.get_all_received_messages(usr_id)[::-1]]
    # usr = m.get_user(session["user_id"])
    # return usr.messages_dict()

@app.route("/api/sent_messages")
def get_sent_messages_json():
    usr_id = session.get("user_id")
    return [message_dict(msg) for msg in database.get_all_sent_messages(usr_id)[::-1]]
    # return usr.sent_messages_dict()

@app.route("/api/sent_messages/<toId>")
def get_sent_json(toId):
    usr_id = session.get("user_id")
    return [message_dict(msg) for msg in database.get_messages_between_users(usr_id, toId)[::-1]]
    # return usr.sent_messages_by_receiver_id_dict(int(toId))

@app.route("/api/received_messages/<fromId>")
def get_received_json(fromId):
    usr_id = session["user_id"]
    msgs = database.get_messages_between_users(fromId, usr_id)[::-1]
    message_dicts = []
    for msg in msgs:
        # d = {}
        # d["senderId"] = msg[1]
        # d["senderName"] = database.get_user_by_id(msg[1])[1]
        # d["receiverId"] = msg[2]
        # d["receiverName"] = database.get_user_by_id(msg[2])[1]
        # d["text"] = msg[3]
        message_dicts.append(message_dict(msg))
    return message_dicts
    # usr = m.get_user(session["user_id"])
    # return usr.messages_by_sender_id_dict(int(fromId))

@app.route("/api/related_messages/<toId>")
def get_related_messages(toId):
    usr_id = session.get("user_id")
    return [message_dict(msg) for msg in database.get_all_related_messages(usr_id, toId)]
    # return usr.sent_messages_by_receiver_id_dict(int(toId))

# @app.route("/user_json")
# def user_json():
#     return m.user_dict()

@app.route("/api/users")
def get_users_json():
    usrs = database.get_all_users()
    return [{"id": row[0], "username": row[1]} for row in usrs]

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', debug=True)
