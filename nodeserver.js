//Python sends the URLS to Node 
//Node sends the full article back to Python

const axios = require('axios');
const { JSDOM } = require('jsdom');
const { Readability } = require('@mozilla/readability');

var express = require('express');
var bodyParser = require('body-parser');

var app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
const urlOrder = [];
const articleTextList = [];

app.post("/fulltext", (req, res) => {
    const urls = req.body.urls;  
    console.log(urls)

    urls.forEach(url => {
        axios.get(url)
          .then(response => {
            const data = response.data;
            let dom = new JSDOM(data, {
            url: url
            })
            let article = new Readability(dom.window.document).parse()
            let text = article.textContent
            urlOrder.push(url)
            articleTextList.push(text)
            });
          })
    Promise.allSettled(urls.map(url => axios.get(url)))
        .then(() => {
            console.log(articleTextList);
            console.log(urlOrder)
            res.json({ result: articleTextList, all_urls: urlOrder});
        })        
})
app.listen(3000);