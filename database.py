import sqlite3

def init_db():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            bio TEXT
        )
    ''')
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            views INTEGER NOT NULL DEFAULT 0
        )
    """)
   
        
    conn.commit()
    conn.close()
    
def seed_db():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    cursor.execute('''INSERT INTO authors (name, bio) VALUES (?, ?)''', ('Jorik', 'Backend Developer.'))
    
    cursor.execute('''INSERT INTO authors (name, bio) VALUES (?, ?)''', ('Ymed', 'Python Developer.'))
    
    cursor.execute('''INSERT INTO authors (name, bio) VALUES (?, ?)''', ('Azam', 'Frontend Developer.'))
    
    cursor.execute("""INSERT INTO posts (title, content, author_id) VALUES (?, ?, ?)""",
                   ("Мой первый пост", "Привет, это мой блог!", 1))

    cursor.execute("""INSERT INTO posts (title, content, author_id) VALUES (?, ?, ?)""",
                   ("Изучаю Flask", "Сегодня изучаю Flask и SQLite.", 1))

    cursor.execute("""INSERT INTO posts (title, content, author_id) VALUES (?, ?, ?)""",
                   ("Что такое Python и с чем его едят?", "Python — популярный язык программирования.", 2))

    cursor.execute("""INSERT INTO posts (title, content, author_id) VALUES (?, ?, ?)""",
                   ("Работа с базами", "SQLite отлично подходит для небольших проектов.", 2))

    cursor.execute("""INSERT INTO posts (title, content, author_id) VALUES (?, ?, ?)""",
                   ("Мой опыт", "Сегодня я создала свой первый Blog API.", 3))

    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    init_db()
    seed_db()