import requests
from flask import Flask, render_template, request

app = Flask(__name__) 

headers = {'Authorization': 'ec6e95b6efb1413f8546562ae41d0b34'}
api = "ec6e95b6efb1413f8546562ae41d0b34"
everything = "https://newsapi.org/v2/everything?"
top_headlines = "https://newsapi.org/v2/top-headlines?"
sources = "https://newsapi.org/v2/sources?"
src = "abc-news, associated-press, bloomberg, crypto-coins-news, medical-news-today, national-geographic, nbc-news, newsweek, new-york-magazine, politico, reuters, the-hill, the-wall-street-journal, the-washington-post, time, wired"


#get webapp input from flask app and return API response
@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        keyword = request.form["keyword"]
        params= {
            'q': keyword,
            "sources": src,
            'apiKey': api,
            'sortBy': "relevancy",
            'language': 'en',
        }
        response = requests.get(url = everything, headers = headers, params = params)

        articles = response.json()['articles']
        return render_template("home.html", all_articles = articles, keyword=keyword)
    else:
        params= {
            "sources": src,
            'apiKey': api,
            'sortBy': "relevancy",
            'language': 'en',
            }
        response = requests.get(url = top_headlines, headers = headers, params = params)
        headlines = response.json()['articles']
        return render_template("home.html", all_headlines = headlines)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
