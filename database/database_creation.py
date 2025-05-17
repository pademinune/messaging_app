
import sqlite3


conn = sqlite3.connect("chat.db")

c = conn.cursor()


def add_message(sender_id, receiver_id, text):
    c.execute("INSERT INTO messages (sender_id, receiver_id, message_text) VALUES (?, ?, ?)", (sender_id, receiver_id, text))
    conn.commit()

def get_messages(receiver_id):
    c.execute("SELECT * FROM messages WHERE receiver_id = ?", (receiver_id,))
    return c.fetchall()

# c.execute("""CREATE TABLE messages (
#           id INTEGER PRIMARY KEY AUTOINCREMENT,
#           sender_id INTEGER NOT NULL,
#           receiver_id INTEGER NOT NULL,
#           message_text TEXT,
#           timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
#         )""")

# c.execute("""CREATE TABLE users (
#           id INTEGER PRIMARY KEY AUTOINCREMENT,
#           username TEXT NOT NULL,
#           password TEXT NOT NULL
#           )""")

# conn.commit()

# c.execute("CREATE INDEX idx_username ON users(username)")
# conn.commit()
# c.execute("SELECT * FROM messages")
# print(c.fetchall())

# # Index for sender_id
# c.execute("CREATE INDEX idx_sender_id ON messages(sender_id)")

# # Index for receiver_id
# c.execute("CREATE INDEX idx_receiver_id ON messages(receiver_id)")

# conn.commit()

# c.execute("INSERT INTO messages (sender_id, receiver_id, message_text) VALUES (?, ?, ?)", (1000, 1034, "Hi guy im a massive jerk..."))

# conn.commit()

# add_message(1034, 1000, "You are a fat person and I already knew you were a jerk.")

# c.execute("SELECT message_text, timestamp, sender_id FROM messages WHERE (receiver_id=1000 AND sender_id=1034) OR (receiver_id=1034 AND sender_id=1000)")

# print(c.fetchall())

# print(get_messages(1000))

conn.close()
