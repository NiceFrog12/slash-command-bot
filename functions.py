import random
import os
import requests



def foxpic():
    url = "https://randomfox.ca/floof/"
    res = requests.get(url)
    data = res.json()
    return data['image']