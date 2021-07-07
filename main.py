from flask import Flask, jsonify, render_template, url_for, request, redirect

import filmrec

app = Flask(__name__)

# App homepage
@app.route("/")
def home():
    # Fetches film data
    films = filmrec.get_data()
    titles = films["primaryTitle"]
    return render_template("index.html", titles = titles)

# Recommendations page
@app.route("/recommendations", methods=["GET", "POST"])
def recommendations():
    # Gets film selection from form
    selection = str(request.form.get("films"))
    # Gets recommedations based on selection
    results = filmrec.get_recs(selection)
    imdb_ids = results["imdb_id"]
    titles = results["title"]
    return render_template("recommendations.html", imdb_ids = imdb_ids, titles = titles, selection = selection)

app.jinja_env.filters["zip"] = zip

if __name__ == "__main__":
    app.run()