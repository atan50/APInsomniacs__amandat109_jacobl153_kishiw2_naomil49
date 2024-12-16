# import requests
import json, random, requests, urllib.request
from urllib.request import Request, urlopen


def getBrews(): # Doesn't work now because forbidden from url???
    try:
        url = "https://api.openbrewerydb.org/v1/breweries"
        headers={"User-Agent" : "Mozilla/5.0"} # Authorizes request. Tells API that you're not a bot???
        request = urllib.request.Request(url, headers=headers)
        API = urllib.request.urlopen(request)
        data = json.loads(API.read()) # List of dictionaries. 50 brewery locations.
        names = [article['name'] for article in data]
        longs = [article['longitude'] for article in data]
        lats = [article['latitude'] for article in data]
        info_list =[]
        for (name, long, lat) in zip(names, longs, lats):
            info_list.append([name, long, lat])
        return(info_list)
    except Exception as e:
        print(e)


def getArticles():
    try:
        file = open('keys/NYT_API_key.txt', 'r')
        content = file.read().strip()
        file.close()
        url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q=food&q=dining&api-key={content}" # Food and DIning Articles as query
        API = urllib.request.urlopen(url)
        data = json.loads(API.read())
        articles = data['response']['docs']
        urls = [article['web_url'] for article in articles] # url's of articles in past month
        lead_pars = [article['lead_paragraph'] for article in articles]
        headlines = [article['headline']['print_headline'] for article in articles]
        info_list =[]
        for (url, lead_par, headline) in zip(urls, lead_pars, headlines):
            print("\n\n",lead_par,headline, '.' in lead_par)
            par_len = (len(lead_par))
            if(par_len > 0 and '.' not in lead_par):
                continue
            info_list.append([url, lead_par, headline])
        return (info_list)
    except Exception as e:
        print(e)

def getRecipes():
    try:
        file = open('keys/Spoonacular_API_key.txt', 'r')
        content = file.read().strip()
        file.close()
        url = f"https://api.spoonacular.com/recipes/random?apiKey={content}"
        response = requests.get(url)# Get Request of URL. API Key is required at end.
        data = response.json()# random recipe and all its info

        title = data['recipes'][0]['title']

        instructions = data['recipes'][0]['instructions']

        ingredients = data['recipes'][0]['extendedIngredients']

        image = data['recipes'][0]['image']
        name_ingredients = [ingredient['original'] for ingredient in ingredients] # List of ingredients and amounts required for each.
        list_ingredients = ""
        for ingredient in name_ingredients:
            list_ingredients += ingredient + " + "
        list_ingredients = list_ingredients[:-2] + "."
        return([title, list_ingredients, instructions, image])
    except Exception as e:
        print(e)

getBrews()
