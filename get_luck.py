# -*- coding: UTF-8 -*-
# Author@HuKe
# Time@2022/8/20 20:41
import requests
from bs4 import BeautifulSoup
import re

def get_html(url):
    User_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
    headers = {'User_agent': User_agent}
    html = requests.get(url, headers=headers).text
    return html

def get_luck():
    url = 'https://www.xzw.com/fortune/sagittarius/'
    html = get_html(url)
    soup = BeautifulSoup(html)
    html2 = soup.find('div', class_='c_cont')
    html2 = str(html2)
    soup = BeautifulSoup(html2)
    luck_title = [str(x)[-13:-9] for x in soup.find_all('strong')]
    luck_content = []
    for x in soup.find_all('span'):
        index = re.search(r'>.*?<', str(x)).span()
        luck_content.append(str(x)[index[0]+1:index[1]-1])
    return luck_title, luck_content

if __name__ == '__main__':
    luck_t, luck_c = get_luck()
    print(luck_t)
    print(luck_c)
