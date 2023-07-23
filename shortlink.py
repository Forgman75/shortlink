import requests
import sys
from account import token
from urllib.parse import urljoin, urlparse

base_url = 'https://api-ssl.bitly.com/v4/'

def make_url_for_api(input_url):
    link = urlparse(input_url)
    bitlink_path = "bitlinks/{lh}{lp}".format(lh=link.hostname, lp=link.path)
    url = urljoin(base_url, bitlink_path)
    return url

def bearer_auth(token):
    bearer = "Bearer {t}".format(t=token)
    headers = {
        "Authorization": bearer 
    }
    return headers

def is_bitlink(headers, input_url):

    response = requests.get(input_url, headers=headers)
    return response.ok


def shorten_link(headers, link):
    url = "{b}shorten".format(b=base_url)
    payload = {
        "long_url": link 
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['link']

def count_clicks(headers, input_url):
    url = "{i}/clicks".format(i=input_url)
    params = {
        "unit": "day",
        "units": -1
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    clicks_json = response.json()['link_clicks']
    clicks_count = clicks_json[0].get('clicks')
    return clicks_count



def main():
    user_input = input("Введите ссылку:")
    api_url = make_url_for_api(user_input)
    auth_headers = bearer_auth(token)
    if is_bitlink(auth_headers, api_url):
      try:
        c_count = count_clicks(auth_headers, api_url)
        print("По вашей ссылке прошли {c} раз(а)".format(c=c_count))
      except requests.exceptions.HTTPError as error:
        sys.exit("Can't get data from server:\n{0}".format(error))
    else:
      try:  
        bitlink = shorten_link(auth_headers, user_input)
        print('Битлинк', bitlink)
      except requests.exceptions.HTTPError as error:
        sys.exit("Can't get data from server:\n{0}".format(error))


if __name__ == "__main__":
    main()
