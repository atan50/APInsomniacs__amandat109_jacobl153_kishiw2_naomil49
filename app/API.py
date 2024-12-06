# import requests
import urllib.request
from urllib.request import Request
from urllib.request import urlopen
import json
import random


def getBrews(): # Doesn't work now because forbidden from url???
    url = "https://api.openbrewerydb.org/v1/breweries"
    API = urllib.request.urlopen(url)
    python_ify = json.loads(API.read())
    #return [python_ify['id'], python_ify['advice']]
    return(python_ify)
getLoc()
