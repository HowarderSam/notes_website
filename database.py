import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn



def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

# init_db()


# create new functions to 
# add username,
# add note,
# get user from db by username



def add_user(username,password):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""INSERT INTO users (username, password) VALUES (?, ?)""",
                (username, password)
                )
    conn.commit()
    conn.close()


def add_note(user_id,content):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute(
        """INSERT INTO notes (user_id, content) VALUES (?, ?)""",
        (user_id, content)
    )
    conn.commit()
    conn.close()




def get_user(username):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """SELECT * FROM users WHERE username = ?""",
        (username,)
    )
    user = cur.fetchone()
    conn.close()
    return user
              

                                                   
def get_notes(user_id):            
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """SELECT * FROM notes WHERE user_id = ?""",
        (user_id,)
    )
    notes = cur.fetchall()
    conn.close()
    return notes



def delete_note(note_id,user_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """ DELETE FROM notes WHERE id = ? AND user_id = ?""" ,
        (note_id,user_id)     
)
    conn.commit()
    conn.close()


def upd_note(note_id,user_id,content):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """UPDATE notes SET content = ? WHERE id = ? AND user_id = ?""",
        (content,note_id,user_id)
)
    conn.commit()
    conn.close()



def get_note(note_id, user_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """SELECT * FROM notes WHERE id = ? AND user_id = ?""",
        (note_id, user_id)
    )

    note = cur.fetchone()
    conn.close()
    return note


def user_by_id(user_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """SELECT * FROM users WHERE id = ?""",
        (user_id,)
    )
    user = cur.fetchone()
    conn.close()
    return user



def upd_password(user_id,new_hashp):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """UPDATE users SET password = ? WHERE id = ?""",
        (new_hashp,user_id)
)
    conn.commit()
    conn.close()