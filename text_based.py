import pandas as pd
import requests
import sqlite3
import openai
import os

openai.api_key = ""

#START NODE SERVER TO RUN
#"node nodeserver.js"


keywordFlag = True
headers = {'Authorization': ''}
api = ""
everything = "https://newsapi.org/v2/everything?"
top_headlines = "https://newsapi.org/v2/top-headlines?"
sources = "https://newsapi.org/v2/sources?"
src = "abc-news, associated-press, bloomberg, crypto-coins-news, medical-news-today, national-geographic, nbc-news, newsweek, new-york-magazine, politico, reuters, the-hill, the-wall-street-journal, the-washington-post, time, wired"

#text based, asks user questions and returns API response
def user_input():
    yes_no_symbols = input("""Hello! Are you looking for top headlines or searching for something specific? Input "top" for top headlines and "keyword" to search by keyword. """)
    if yes_no_symbols == "keyword":
        symbols = input("Input a keyword to search for: ")
        keywordFlag = True
    if yes_no_symbols == "top":
        keywordFlag = False

    yes_no_sort = input("""Would you like to sort by relevancy, popularity, or published date? Input "r" for relevancy, "p" for popularity, "d" for published date. """)
    if yes_no_sort == "r":
        sort = "relevancy"
    if yes_no_sort == "p":
        sort = "popularity"
    if yes_no_sort == "d":
        sort = "publishedAt"

    if keywordFlag == True:
        params= {
            'q': symbols,
            "sources": src,
            'apiKey': api,
            'sortBy': sort,
            'language': 'en',
            }
        response = requests.get(url = everything, headers = headers, params = params)

    if keywordFlag == False:
        params= {
            "sources": src,
            'apiKey': api,
            'sortBy': sort,
            'language': 'en',
            }
        response = requests.get(url = top_headlines, headers = headers, params = params)

    return response

#utilizing API response generated by user input
def use_API(response):
    output = response.json()
    lines2 = output['articles']

    df2 = pd.DataFrame(lines2)
    df2.dropna(subset=['content'], inplace=True)
    url = df2['url'].to_list()
  
    # Data that we will send in post request.
    data = {'urls':url}
  
    # The POST request to our node server
    res = requests.post('http://127.0.0.1:3000/fulltext', json=data) 
  
    # Convert response data to json
    returned_data = res.json() 
    result = returned_data['result']  
    result_urls = returned_data['all_urls']  
    content_urls = dict(zip(result_urls, result))

    by_url = []
    for i in lines2:
        for j in result_urls:
            if i["url"] == j:
                url = j
                author = i["author"]
                date = i['publishedAt']
                title = i['title']
                urlToImage = i['urlToImage']
                source = i['source']['name']
                content = content_urls[j]
                row = [url, author, date, title, urlToImage, source, content]
                by_url.append(row)

    return result, by_url

#for each result in final request, create chunks and clean text using chatGPT API
def clean_text(result):
    for i in result:
        split_val = i.split()
        if len(split_val) >= 3000:
            chunk = split_val[:3000]
            i = ' '.join(chunk)

        prompt = (f"Clean and return this text:\n{i}")
 
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=1047,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=1
    )
    cleaned_text = response.choices[0].text
    return cleaned_text

#add to SQLite3 database
def sql_connection(by_url):
    connection = sqlite3.connect('articles_list.db')
    cur = connection.cursor()
    cur.execute('''CREATE TABLE articles(url TEXT, author TEXT, date TEXT, title TEXT, urlToImage TEXT, source TEXT, content TEXT)''')
    cur.executemany('INSERT INTO articles VALUES (?,?,?,?,?,?,?)', by_url)
    connection.commit()


#AT THE MOMENT: adds info to database, prints text from node server
def main_text_based():
    response = user_input()
    result = use_API(response)[0]
    print(result)
    by_url = use_API(response)[1]
    sql_connection(by_url)

main_text_based()
