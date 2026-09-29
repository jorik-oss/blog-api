from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/authors', methods=['GET'])
def get_authors():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM authors').fetchall()
    conn.close()
    
    return jsonify([dict(row) for row in rows])

@app.route('/posts', methods=['GET'])
def get_posts():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    
    return jsonify([dict(row) for row in rows])

@app.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()
    
    if post is None:
        conn.close()
        return jsonify({'error': 'Post not found'}), 404
    
    conn.execute('UPDATE posts SET views = views + 1 WHERE id = ?', (id,))
    conn.commit()
    
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    return jsonify(dict(post))

    
@app.route("/posts", methods=["POST"])
def create_post():
    data = request.get_json()

    required_fields = ["title", "content", "author_id"]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"Missing field: {field}"
            }), 400

    conn = get_db_connection()

    author = conn.execute(
        "SELECT id FROM authors WHERE id = ?",
        (data["author_id"],)
    ).fetchone()

    if author is None:
        conn.close()
        return jsonify({"error": "Author not found"}), 400

    cursor = conn.execute(
        """
        INSERT INTO posts (title, content, author_id)
        VALUES (?, ?, ?)
        """,
        (
            data["title"],
            data["content"],
            data["author_id"]
        )
    )

    conn.commit()

    post_id = cursor.lastrowid

    post = conn.execute(
        "SELECT * FROM posts WHERE id = ?",
        (post_id,)
    ).fetchone()

    conn.close()

    return jsonify(dict(post)), 201


if __name__ == '__main__':
    app.run(debug=True)