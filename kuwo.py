# -*- coding:UTF-8 -*-

from selenium import webdriver
from bs4 import BeautifulSoup
import requests,os

#    class song():
#        def __init__(self,song_id,song_name,song_url=None):
#            self.id = song_id
#            self.name = song_name
#            self.url = '' if song_url is None else song_url

def download(name,url,path):
    headers = {"user-sgent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
    response = requests.get(url,headers = headers)
    with open('./'+path+'/'+name+'.aac','wb') as f:
        f.write(response.content)

def isnext(browser):
    try:
        browser.find_element_by_link_text('尾页')
        Flag = True
    except:
        Flag = False
    return Flag

def main(html):

    bf1 = BeautifulSoup(html,'lxml')
    folder = bf1.h1['title']
    if not os.path.exists(folder):
        os.mkdir(folder)
    bf2 = bf1.form.find_all('li')
    for i in range(0,len(bf2)):
        song_id = BeautifulSoup(str(bf2[i]),'lxml').input['mid']
        song_name = BeautifulSoup(str(bf2[i]),'lxml').a.text
#       song_url = BeautifulSoup(str(bf2[i]),'lxml').a['href']
        r_url = 'http://antiserver.kuwo.cn/anti.s?format=aac|mp3&rid=MUSIC_'+song_id+'&type=convert_url&response=res'
        song_url = requests.get(r_url,allow_redirects=False).headers['Location']
        print('正在下载歌曲：',song_name)
        download(song_name,song_url,folder)

main_url = input('输入歌单网址：')
options = webdriver.ChromeOptions()
options.add_argument('user-sgent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"')
browser = webdriver.Chrome(chrome_options=options)
browser.get(main_url)
page_num = 1
while isnext(browser):
        page = browser.page_source
        main(page)
        page_num += 1
        browser.find_element_by_link_text(str(page_num)).click()
page = browser.page_source
main(page)
