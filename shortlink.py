import requests
import sys
from account import token
from urllib.parse import urljoin

base_url = 'https://api-ssl.bitly.com/v4/'


def shorten_link(link):
    url = "{b}shorten".format(b=base_url)
    bearer = "Bearer {t}".format(t=token)
    headers = {
        "Authorization": bearer 
    }
    payload = {
        "long_url": link 
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['link']

def count_clicks(token, link):
    clicks_path = "bitlinks/{l}/clicks".format(l=link)
    url = urljoin(base_url, clicks_path)
    bearer = "Bearer {t}".format(t=token)
    headers = {
        "Authorization": bearer 
    }
    params = {
        "unit": "day",
        "units": -1
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    clicks_json = response.json()['link_clicks']
    clicks_count = clicks_json[0].get('clicks')
    return clicks_count

if __name__ == "__main__":
 link = input("Введите ссылку, которую нужно сократить:")
 try:  
    bitlink = shorten_link(link)
 except requests.exceptions.HTTPError:
    print("Вы ввели не корректную ссылку")
    sys.exit()   
 print('Битлинк', bitlink)
