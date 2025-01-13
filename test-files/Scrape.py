from newspaper import Article

url = 'https://www.bbc.co.uk/news/articles/cdekew421dgo'
article = Article(url)
article.download()
article.parse()
s =article.text
print(s)