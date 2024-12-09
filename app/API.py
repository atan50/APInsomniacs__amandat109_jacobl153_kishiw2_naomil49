# import requests
import urllib.request
from urllib.request import Request
from urllib.request import urlopen
import json
import random
# import requests


def getBrews(): # Doesn't work now because forbidden from url???
    try:
        url = "https://api.openbrewerydb.org/v1/breweries"
        headers={"User-Agent" : "Mozilla/5.0"} # Authorizes request. Tells API that you're not a bot???
        request = urllib.request.Request(url, headers=headers)
        API = urllib.request.urlopen(request)
        data = json.loads(API.read()) # List of dictionaries. 50 brewery locations.
        print(data)
    except Exception as e:
        return e


def getArticles():
    try:
        file = open('keys/NYT_API_key.txt', 'r')
        content = file.read()
        file.close()
        url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q=food&q=dining&api-key={content}" # Food and DIning Articles as query
        API = urllib.request.urlopen(url)
        data = json.loads(API.read())
        articles = data['response']['docs']
        urls = [article['web_url'] for article in articles] # url's of articles in past month
        print(urls)
    except Exception as e:
        return e

def getRecipes():
    try:
        file = open('keys/Spoonacular_API_key.txt', 'r')
        content = file.read().strip()
        file.close()
        url = f"https://api.spoonacular.com/recipes/random?apiKey={content}"
        response = requests.get(url)# Get Request of URL. API Key is required at end.
        data = response.json()# random recipe and all its info
        print(data)
    except Exception as e:
        return e
