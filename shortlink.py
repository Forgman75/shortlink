import requests
import sys
from account import token
from urllib.parse import urljoin, urlparse

base_url = 'https://api-ssl.bitly.com/v4/'

def is_bitlink(token, input_url):
    link = urlparse(input_url)
    bitlink_path = "bitlinks/{lh}{lp}".format(lh=link.hostname, lp=link.path)
    url = urljoin(base_url, bitlink_path)
    bearer = "Bearer {t}".format(t=token)
    headers = {
        "Authorization": bearer 
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.ok


def shorten_link(token, link):
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

def count_clicks(token, input_url):
    link = urlparse(input_url)
    clicks_path = "bitlinks/{lh}{lp}/clicks".format(lh=link.hostname, lp=link.path)
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
 user_input = input("Введите ссылку:")
 if is_bitlink(token, user_input):
    try:
        c_count = count_clicks(token, user_input)
        print("По вашей ссылке прошли {c} раз(а)".format(c=c_count))
    except requests.exceptions.HTTPError:
        print("Вы ввели не корректную ссылку")
        sys.exit()
 else:
    try:  
        bitlink = shorten_link(token, user_input)
        print('Битлинк', bitlink)
    except requests.exceptions.HTTPError:
        print("Вы ввели не корректную ссылку")
        sys.exit()
