from flask import Flask
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect("./database.db")
curr = sqlite3.Cursor(conn)

curr.execute("CREATE TABLE IF NOT EXISTS clicks (name text primary key, num integer);")
curr.execute("INSERT OR IGNORE INTO clicks VALUES ('visits', 0);")
curr.execute("INSERT OR IGNORE INTO clicks VALUES ('clicks', 0);")
conn.commit()

@app.route("/")
def home():
    conn = sqlite3.connect("./database.db")
    curr = sqlite3.Cursor(conn)
    curr.execute("UPDATE clicks SET num = num + 1 WHERE name = 'visits';")
    conn.commit()
    return """<meta http-equiv="refresh" content="0; URL=/update">"""

@app.route("/update")
def update():
    conn = sqlite3.connect("./database.db")
    curr = sqlite3.Cursor(conn)
    html = "".join(open("./index.html").readlines());
    curr.execute("SELECT num FROM clicks WHERE name = 'visits';")
    view_counter = curr.fetchone()[0]
    curr.execute("SELECT num FROM clicks WHERE name = 'clicks';")
    click_counter = curr.fetchone()[0]
    return html.replace("{{visits}}", f"{view_counter}").replace("{{clicks}}", f"{click_counter}")


@app.route("/click")
def click():
    conn = sqlite3.connect("./database.db")
    curr = sqlite3.Cursor(conn)
    curr.execute("UPDATE clicks SET num = num + 1 WHERE name = 'clicks';")
    conn.commit()
    return """<meta http-equiv="refresh" content="0; URL=/update">"""

app.run(host="127.0.0.1", port=5000, use_reloader=True)
