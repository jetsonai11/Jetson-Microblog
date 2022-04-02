import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient

def create_app():
    app = Flask(__name__)
    client = MongoClient("mongodb+srv://jetsonearth:110611..@cluster0.0n4yu.mongodb.net/test")
    app.db = client["microblog"]
    mycol = app.db["entries"]
    entries = []

    @app.route("/", methods = ["GET", "POST"])
    # link the form here so we could receive data when adding entires
    # Recent posts section would then display past entries
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            entries.append((entry_content, formatted_date))
            mycol.insert_one({"content": entry_content, "date": formatted_date}) 

        entries_with_date = [
            (
                entry["content"], 
                entry["date"], 
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
            )
            for entry in mycol.find({})
        ]
        return render_template("home.html", entries = entries_with_date)

    return app