# News Scraper

This is a personal project utilizing the NewsAPI to create a custom news page. There are two ways to use this project:

1. Text based input:
   To run: 
   "node nodeserver.js"
   "python text_based.py"
   - this will ask the user some questions about what articles they want to see, then send the
     request to NewsAPI
   - the json response of this request is sent to the NodeJS server to get the full text content of      the article, since this is not provided by NewsAPI
   - the full text of each article is sent back to the python side 
   - if necessary, the text is cleaned by using the chatGPT API 
   - all the information from the article and the full, cleaned text is put into SQLite database


2. Web app:
   - accesses NewsAPI headlines endpoint and displays it on front page of web app
   - web app created using Flask and run in a dockerized container
   - users can also use the search bar at the top and find articles relevant to their search term
