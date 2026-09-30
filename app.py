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
    
    author_id = request.args.get('author_id')
    
    if author_id:
        posts = conn.execute('SELECT * FROM posts WHERE author_id = ?', (author_id,)).fetchall()
    else:
        posts = conn.execute('SELECT * FROM posts').fetchall()
        
    conn.close()
    
    return jsonify([dict(post) for post in posts])

@app.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    conn = get_db_connection()
    
    conn.execute(
        "UPDATE posts SET views = views + 1 WHERE id = ?",(id,)
    )
    
    conn.commit()
    
    post = conn.execute(
        """
        SELECT
            posts.id,
            posts.title,
            posts.content,
            posts.views,
            authors.id AS author_id,
            authors.name AS author_name,
            authors.bio AS author_bio
        FROM posts
        JOIN authors ON posts.author_id = authors.id
        WHERE posts.id = ?
        """, (id,)
    ).fetchone()
    
    if post is None:
        conn.close()
        return jsonify({"error": "Post not found"}), 404
    
    conn.close()
    
    return jsonify({
        "id": post["id"],
        "title": post["title"],
        "content": post["content"],
        "views": post["views"],
        "author": {
            "id": post["author_id"],
            "name": post["author_name"],
            "bio": post["author_bio"]
        }
    })
    
    

    
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

@app.route("/authors/<int:id>/posts", methods=["GET"])
def get_author_posts(id):
    conn = get_db_connection()

    author = conn.execute(
        "SELECT * FROM authors WHERE id = ?",
        (id,)
    ).fetchone()

    if author is None:
        conn.close()
        return jsonify({"error": "Author not found"}), 404

    posts = conn.execute(
        "SELECT * FROM posts WHERE author_id = ?",
        (id,)
    ).fetchall()

    conn.close()

    return jsonify([dict(post) for post in posts])


@app.route("/posts/<int:id>", methods=["DELETE"])
def delete_post(id):
    conn = get_db_connection()

    cursor = conn.execute(
        "DELETE FROM posts WHERE id = ?",
        (id,)
    )

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "Post not found"}), 404

    conn.commit()
    conn.close()

    return jsonify({"message": "Post deleted"})
    

@app.route("/authors/<int:id>", methods=["GET"])
def get_author(id):
    conn = get_db_connection()

    author = conn.execute(
        "SELECT * FROM authors WHERE id = ?",
        (id,)
    ).fetchone()

    if author is None:
        conn.close()
        return jsonify({"error": "Author not found"}), 404

    posts = conn.execute(
        "SELECT id, title FROM posts WHERE author_id = ?",
        (id,)
    ).fetchall()

    conn.close()

    author_data = dict(author)
    author_data["posts"] = [dict(post) for post in posts]

    return jsonify(author_data)


@app.route("/posts/popular", methods=["GET"])
def get_popular_posts():
    conn = get_db_connection()

    posts = conn.execute(
        """
        SELECT * FROM posts
        ORDER BY views DESC
        LIMIT 3
        """
    ).fetchall()

    conn.close()

    return jsonify([dict(post) for post in posts])
    
    
if __name__ == '__main__':
    app.run(debug=True)