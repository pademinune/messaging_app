from flask import Flask, request, render_template, session, redirect, url_for

from messaging import messenger, message, user


app = Flask(__name__)
app.secret_key = "your-secret-key-here"

m = messenger()

ip_storage = read_from_file("ips.j")

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




@app.route("/")
def start():
    # ip()
    return redirect("/home")


@app.route('/home')
def index():
    # return "<p>No</p>"
    return render_template('index.html', users=m.users.values())

@app.route("/user_page/user_list")
def user_list():
    return render_template("user_list.html", users=m.users.values())

# @app.route('/submit', methods=['POST'])
# def submit():
#     data = request.form # data is basically a dictionary of field names, and the input
#     name = data["userName"]
#     num = data["userAge"]
#     users[name] = num
#     # print(users)
#     return render_template("submitted.html", userName=name)

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
    id = m.get_id(username)
    if id == None:
        u = m.add_user(username, password)
        session["user_id"] = u.get_id()
        return redirect("/user_page")
    else:
        u = m.get_user(id)
        if password != u.get_password():
            return f"A user with a username of {username} (id is {id}) already exists!"
        else:
            session["user_id"] = u.get_id()
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
    id = m.get_id(username)
    if id == None:
        return "No such user..."
    else:
        m.deliver_message(session["user_id"], id, message)
        return redirect("/user_page")

@app.route("/json")
def json():
    return m.user_dict()

@app.route("/api/text")
def apitext():
    return "hello"

@app.route("/user_page")
def user_page():
    # ip()
    id = session.get("user_id")
    if id == None:
        return redirect("/home")
    u = m.get_user(id)
    if u == None:
        return redirect("/home")
    return render_template("logged_in.html", username=u.get_username(), password = u.get_password(), messages = process_messages(u.get_messages()), 
                           sent_messages = process_messages(u.get_sent_messages()))

@app.route("/chat")
def chat():
    to_id = request.args.get("to")
    if session.get("user_id") == None:
        return redirect("/home")
    return render_template("chat.html")

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
    usr = m.get_user(id)
    # print(id)
    # print(usr)
    # print(m.users)
    if usr == None:
        return {"userId": -1}
    else:
        return {"userId": id, "username": usr.get_username()}

@app.route("/api/received_messages")
def get_received_messages_json():
    usr = m.get_user(session["user_id"])
    return usr.messages_dict()

@app.route("/api/sent_messages")
def get_sent_messages_json():
    usr = m.get_user(session["user_id"])
    return usr.sent_messages_dict()

@app.route("/api/sent_messages/<toId>")
def get_sent_json(toId):
    usr = m.get_user(session["user_id"])
    # print(usr.sent_messages_by_receiver)
    # print(toId)
    return usr.sent_messages_by_receiver_id_dict(int(toId))

@app.route("/api/received_messages/<fromId>")
def get_received_json(fromId):
    usr = m.get_user(session["user_id"])
    return usr.messages_by_sender_id_dict(int(fromId))

@app.route("/user_json")
def user_json():
    return m.user_dict()

@app.route("/api/users")
def get_users_json():
    return m.user_dict()

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', debug=True)
