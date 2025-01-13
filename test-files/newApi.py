import reqs
from pprint import pprint


url = ('https://newsapi.org/v2/top-headlines?'
       'sources=bbc-news&'
       'apiKey=2bf69752e89045b6a4ace9ab036c4b85')
response = reqs.get(url)
pprint (response.json())