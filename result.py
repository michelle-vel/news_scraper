#returns properties of an individual search result, whether it comes from text input or web input

class Result:
    def __init__(self, url, author, date, title, urlToImage, source, content):
        self.url = url
        self.author = author
        self.date = date
        self.title = title
        self.urlToImage = urlToImage
        self.source = source
        self.content = content