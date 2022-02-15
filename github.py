from requests import get
from bs4 import BeautifulSoup as BS
import time
from json import loads


def get_gh(username):
    link = f'https://api.github.com/users/{username}'
    resp = get(link)

    if resp.status_code == 200:
        begin = time.time()

        soup = BS(resp.text, 'html.parser')


        all_data = loads(str(soup))

        end = time.time()

        slice1 = all_data['created_at'].replace('T', ' ')
        final_sclice = slice1.replace('Z', ' ')

        all_data['resp_time'] = str(round(end - begin, 5)) + 's'
        all_data['created_at'] = final_sclice[0:len(final_sclice)-1]
        

        return all_data