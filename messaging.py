
class message():
    def __init__(self, sender_id, sender_name, receiver_id, receiver_name, text):
        self.sender_id = sender_id
        self.sender_name = sender_name
        self.receiver_id = receiver_id
        self.receiver_name = receiver_name
        self.text = text
    def get_text(self):
        return self.text
    def get_sender_id(self):
        return self.sender_id
    def get_receiver_id(self):
        return self.receiver_id
    def __str__(self):
        return f"message sent from {self.get_receiver_id()}" + self.text

class user():
    def __init__(self, username, password, id):
        self.username = username
        self.password = password
        self.messages = []
        self.messages_by_sender = {} # messages you recieved ordered by sender
        self.sent_messages = []
        self.sent_messages_by_receiver = {} # messages you sent
        self.id = id

    def get_username(self):
        return self.username
    
    def get_id(self):
        return self.id
    
    def get_password(self):
        return self.password
    
    def get_messages(self):
        return self.messages
    
    def get_sent_messages(self):
        return self.sent_messages
    
    def receive_message(self, msg):
        self.messages.append(msg)
        sender_id = msg.get_sender_id()
        if self.messages_by_sender.get(sender_id) == None:
            self.messages_by_sender[sender_id] = [msg]
        else:
            self.messages_by_sender[sender_id].append(msg)
    
    def sent_message(self, msg):
        self.sent_messages.append(msg)
        receiver_id = msg.get_receiver_id()
        if self.sent_messages_by_receiver.get(receiver_id) == None:
            self.sent_messages_by_receiver[receiver_id] = [msg]
        else:
            self.sent_messages_by_receiver[receiver_id].append(msg)
    
    def print_messages(self):
        print(self.messages)

    def message_dict(self, msg):
        d = {}
        senderId = msg.get_sender_id()
        receiverId = msg.get_receiver_id()
        d["senderId"] = senderId
        d["senderName"] = msg.sender_name
        d["receiverId"] = receiverId
        d["receiverName"] = msg.receiver_name
        d["text"] = msg.get_text()
        return d
    
    def messages_dict(self):
        j = []
        for msg in self.get_messages():
            j.append(self.message_dict(msg))
        return j[::-1] # returns in order from newest to oldest
    
    def sent_messages_dict(self):
        j = []
        for msg in self.get_sent_messages():
            j.append(self.message_dict(msg))
        return j[::-1]
    
    def messages_by_sender_id_dict(self, id):
        j = []
        for msg in self.messages_by_sender.get(id, []):
            j.append(self.message_dict(msg))
        return j[::-1]
    
    def sent_messages_by_receiver_id_dict(self, id):
        j = []
        for msg in self.sent_messages_by_receiver.get(id, []):
            j.append(self.message_dict(msg))
        return j[::-1]

    def __str__(self):
        current = ""
        current += f"Username: {self.username}\n"
        current += f"Password: {self.password}\n"
        current += str(self.messages)
        return current


class messenger():
    def __init__(self):
        self.users = {}
        self.names = {}

    # O(1) time
    def add_user(self, username, password):
        total = len(self.users)
        id = total + 1
        person = user(username, password, id)
        self.users[id] = person
        self.names[username] = person
        return person
    
    # O(1) time
    def get_id(self, username):
        u = self.names.get(username)
        if u != None:
            return u.get_id()
        else:
            return None
    
    # O(1) time
    def get_user(self, id):
        return self.users.get(id)
    
    # O(1) time
    def deliver_message(self, sender_id, receiver_id, text):
        sender = self.get_user(sender_id)
        receiver = self.get_user(receiver_id)
        msg = message(sender_id, sender.get_username(), receiver_id, receiver.get_username(), text)
        self.users[receiver_id].receive_message(msg)
        self.users[sender_id].sent_message(msg)

    def user_dict(self):
        lst = []
        for id,usr in self.users.items():
            username = usr.get_username()
            lst.append({"id": id, "username": username})
        return lst

# m = messenger()

# m.add_user("philza", "123")
# m.add_user("jerk", "pass")

# u1 = m.users[1]
# u2 = m.users[2]


# # u1.print_messages()
# print(u2)

# m.deliver_message(2, 1, "Hello jerk!")
# m.deliver_message(2, 1, "PHILZA")

# print(u1.messages_by_sender)
# print(u1.sent_messages_by_receiver)

# print(u2)
# print(m.get_id("jerk"))
