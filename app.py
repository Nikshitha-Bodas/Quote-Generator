from flask import Flask, render_template, redirect
import sqlite3
import requests

app = Flask(__name__)

# Create Database
def init_db():

    conn = sqlite3.connect("quotes.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote TEXT,
            author TEXT
        )
    """)

    conn.commit()
    conn.close()


# Home Page
@app.route("/")
def home():

    conn = sqlite3.connect("quotes.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM quotes ORDER BY id DESC")

    quotes = cursor.fetchall()

    conn.close()

    return render_template("index.html", quotes=quotes)


# Fetch Quote
@app.route("/get_quote")
def get_quote():

    url =  "https://zenquotes.io/api/random"

    response = requests.get(url)

    data = response.json()
    quote = data[0]["q"]
    author = data[0]["a"]

    conn = sqlite3.connect("quotes.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO quotes (quote, author) VALUES (?, ?)",
        (quote, author)
    )

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":

    init_db()

    app.run(debug=True)