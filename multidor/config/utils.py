import requests
import hashlib
from urllib.parse import urlparse

def send_index_now_request(url):

    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    domain_hash = compute_hash(domain)
    index_now_url = f'https://yandex.com/indexnow?key={domain_hash}&url={url}'

    try:
        response = requests.get(index_now_url)
        response.raise_for_status()
        return response.json()  # если ответ в формате JSON
    except requests.RequestException as e:

        print(f"Failed to send index now request: {e}")
        return None

def compute_hash(text):
    hash_object = hashlib.md5()
    hash_object.update(text.encode('utf-8'))
    hash_hex = hash_object.hexdigest()
    return hash_hex