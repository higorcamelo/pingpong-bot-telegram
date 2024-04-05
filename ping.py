#import schedule
#import time
import requests

# Testar conexão com site via requisição HTTP
def pingURL(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        return False
    