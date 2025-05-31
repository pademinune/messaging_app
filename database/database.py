
import sqlite3

# ====================================== MESSAGES ======================================

def get_all_sent_messages(user_id):
    with sqlite3.connect("chat.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM messages WHERE sender_id = ?", (user_id,))
        return c.fetchall()

# returns a list of tuples where each tuple stores (id, sender_id, receiver_id, message_text, timestamp)
def get_all_received_messages(user_id):
    with sqlite3.connect("chat.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM messages WHERE receiver_id = ?", (user_id,))
        return c.fetchall()

def get_messages_between_users(sender_id, receiver_id):
    if sender_id is None:
        return get_all_received_messages(receiver_id)
    elif receiver_id is None:
        return get_all_sent_messages(sender_id)
    
    with sqlite3.connect("chat.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM messages WHERE sender_id = ? AND receiver_id = ?", (sender_id, receiver_id))
        return c.fetchall()

def get_all_related_messages(user_id, other_id):
    with sqlite3.connect("chat.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM messages WHERE (sender_id = ? AND receiver_id = ?) OR (receiver_id = ? AND sender_id = ?) ORDER BY id DESC", (user_id, other_id, user_id, other_id))
        return c.fetchall()

def get_all_messages():
    with sqlite3.connect("chat.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM messages")
        return c.fetchall()
    

def add_message(sender_id, receiver_id, message_text):
    with sqlite3.connect("chat.db") as conn:
        c = conn.cursor()
        c.execute("INSERT INTO messages (sender_id, receiver_id, message_text) VALUES (?, ?, ?)", (sender_id, receiver_id, message_text))
        conn.commit()
        return True

# ====================================== USERS ======================================

# returns tuples of (id, username, password)

def user_exists(id=None, username=None):
    with sqlite3.connect("chat.db") as conn:
        c = conn.cursor()
        if id is not None:
            c.execute("SELECT * FROM users WHERE id = ?", (id,))
            return len(c.fetchall()) != 0
        else:
            c.execute("SELECT * FROM users WHERE username = ?", (username,))
            return len(c.fetchall()) != 0

def get_user_by_id(id):
    with sqlite3.connect("chat.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE id = ?", (id,))
        return c.fetchone()

def get_user_by_username(username):
    with sqlite3.connect("chat.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        return c.fetchone()

def get_id_by_username(username):
    return get_user_by_username(username)[0]

def get_username_by_id(id):
    return get_user_by_id(id)[1]

def get_all_users():
    with sqlite3.connect("chat.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        return c.fetchall()

def add_user(username, password):
    with sqlite3.connect("chat.db") as conn:
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True

if __name__ == "__main__":
    # add_user("admin3", "123")

    # print(get_user_by_username("admin3"))

    # print(get_all_users())
    # with sqlite3.connect("chat.db") as conn:
    #     c = conn.cursor()
    #     c.execute("SELECT * FROM users")
    #     print(c.fetchall())

    print(get_all_related_messages(1, 4))

    pass

