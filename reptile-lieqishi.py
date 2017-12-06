# -*- coding: UTF-8 -*-
import requests
from urllib import request
from urllib import parse
from bs4 import BeautifulSoup
import urllib.parse
import os
import random
import time

download_path='D:/Media/Pictures/MMPic/'#你的图片保存路径
urls=['https://lieqishi.com/index.php/fuli/show/id/{}'.format(str(i))for i in range(1,3364,1)] #目前共3363张， [1,100) 。46、53
login_url='https://lieqishi.com/index.php/api/ulog/login?username=UserName&userpass=123456'

#Ctrl+Shift+J , document.cookie ,查看cookie
user_agent_list = [\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"\
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",\
        'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.1 (KHTML, like Gecko) Maxthon/3.0.8.2 Safari/533.1'
       ]
#这里是user-agent和cookie，代码展示的只是样式，并非真实的user-agent和cookie，你要换成你自己的

requests.adapters.DEFAULT_RETRIES = 5

#url,网页地址; cookies,登录后获取的cookies;num_retries,重试次数，默认为3次
def openurl(url, cookies='', num_retries=3):
    try:
        html = requests.get(url,cookies=cookies)
    except requests.RequestException as e:
        print('Open error:', e)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                print('Try again')
                return openurl(url, cookies,num_retries-1)
    return html

#url,网页地址; cookies,登录后获取的cookies; index，实际网页编号，否则分页的目录就错了
def get_info(url, cookies, index):
    print('Downloading:', url)
    wb_data=openurl(url,cookies,3)#发起网页请求
    if 'pay' in url :
        html=urllib.parse.unquote(wb_data.text.split("\'")[1])
        soup=BeautifulSoup(html,'html.parser')
        img=soup.select('img')#定位元素
    else :
        soup=BeautifulSoup(wb_data.text,'html.parser')#解析网页
        img=soup.select('#content > img')#定位元素

    next_page_url=url
    for i in soup.find_all('a',attrs={'class':'layui-laypage-next'}):
        next_page_url=i.get('href')
    
    #print(img)
    imgs_url=[]					#清空imgs数组
    for i in img:               #判断是否为GIF，是就pass，不是就添加到下载列表
        z=i.get('src')
        if str('gif') in str(z):
           pass
        else:
            imgs_url.append(z)
            
    print()
    
    #print(imgs_url)      #输出下载列表
    dir_name=download_path+index
    if not os.path.exists(dir_name) and imgs_url:
        os.makedirs(dir_name)
    download(imgs_url,dir_name)  #下载图片组

    if 'pay' not in url :
        get_info(url.replace('id','pay'),cookies,index)
    
    if next_page_url!=url :
        get_info(next_page_url,cookies,index)

#下载图片组
def download(imgs_url,dir_name):   
    for i in imgs_url:            #下载模块
        try:
        	r=requests.get(i,headers=get_headers())
        except:
	        print("Let me sleep for 5 seconds.ZZZzzz......")  
        	time.sleep(10)
        	r=requests.get(i,headers=get_headers(),timeout=30)
        
        file_name=dir_name+'/'+i.split('/')[-1]
        if not os.path.isfile(file_name) :	#文件不存在才会下载文件
            with open(file_name,'wb')as pic:
                pic.write(r.content)

            print(i)
        else:
            print(file_name+' : 此文件已存在，不再下载。')

    print()                  
    
#模拟登录，获取cookies
def login(url):
    login_Wdata=requests.get(url)
    return login_Wdata.cookies

#取header，随机agent
def get_headers():
	ua = random.choice(user_agent_list)
	headers={'User-Agent': random.choice(user_agent_list),'Connection': 'close'}
	return headers

#程序开始
def start():           
    cookies=login(login_url)
    for i in urls:
        index=i.split('/')[-1]
        get_info(i,cookies,index)


start()       
