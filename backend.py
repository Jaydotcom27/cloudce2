from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('todolist.db')  
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/api/items")
def get_items():
    conn = get_db_connection()
    cur = conn.execute('SELECT what_to_do, due_date, status FROM entries')
    entries = cur.fetchall()
    conn.close()
    tdlist = [dict(what_to_do=row['what_to_do'], due_date=row['due_date'], status=row['status']) for row in entries]
    return jsonify(tdlist)

@app.route("/api/items", methods=['POST'])
def add_item():
    data = request.get_json()
    what_to_do = data['what_to_do']
    due_date = data['due_date']
    status = data['status']

    conn = get_db_connection()
    conn.execute('INSERT INTO entries (what_to_do, due_date, status) VALUES (?, ?, ?)', (what_to_do, due_date, status))
    conn.commit()
    conn.close()
    return jsonify({"message": "Item added successfully"})

@app.route("/api/mark/<item>", methods=['PUT'])
def mark_as_done(item):
    conn = get_db_connection()
    conn.execute("UPDATE entries SET status='done' WHERE what_to_do=?", (item,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Item marked as done successfully"})

@app.route("/api/delete/<item>", methods=['DELETE'])
def delete_item(item):
    conn = get_db_connection()
    conn.execute("DELETE FROM entries WHERE what_to_do=?", (item,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Item deleted successfully"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)