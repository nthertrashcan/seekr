from prettytable import PrettyTable
import requests 
from bs4 import BeautifulSoup 
import os
import sys
import subprocess as sp
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import youtube_dl 
from moviepy.editor import *
import time
from tqdm import tqdm      



_options=Options()

def initiate_pdl(links,flag):
    ch=""
    name=""
    if len(links)!=0:
        links=set(links)
        t={}
        for l,i in enumerate(links):
            t[l]=i
        tp = PrettyTable(['S.no', 'Source'])
        for key, val in t.items():
           tp.add_row([key+1, val])
        if flag==1:
            ch==""
        else:
            print(tp)
            ch=input("Press 'Enter' to skip\nor\nSelect :- ")
        if ch=="":
            name=down_pdf(t)
            return (True,name)
        else:
            name=down_pdf(t,ch)
            return (True,name)
    return (False,name)


def down_pdf(t,ch='1'):
    name=""
    r = requests.get(t[int(ch)-1], stream = True)
    size=len(r.content)
    if r!="":
        flag=0
        name=t[int(ch)-1].split("/")[-1]
        if name.endswith(".pdf"):
            flag=1
        if flag==1:
            with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),os.path.join("downloaded/temp",name)),"wb") as pdf: 
                for chunk in tqdm(iterable=r.iter_content(chunk_size=1024),total=size/1024,unit='KB'):
                    if chunk:
                        pdf.write(chunk)
                        time.sleep(0.001)
            print("Finished")
            
    else:
        print("Invalid format!!!")
    return name

def ggl_check(q,links):
    url="https://www.google.com/search?q=download+"+q+"+pdf"
    driver=webdriver.Chrome(executable_path="C:\\chromedriver.exe", options=_options)
    driver.get(url)
    table=driver.find_elements_by_tag_name('a')
    
    sour=[]
    ddg=0
    avoid=["https://policies.google.com","https://www.google.com","https://accounts.google.com","https://maps.google.com","https://www.quora.com"]
    for i in table:
        if i.get_attribute('href')!=None:
            if "http" in i.get_attribute('href'):
                if ".pdf" in i.get_attribute('href'):
                    if i.get_attribute('href').split("&sa=U")[0].endswith(".pdf"):
                        links.append(i.get_attribute('href').split("&sa=U")[0].strip("/url?q="))
                else:
                    if i.get_attribute('href').strip("/url?q=").split(".com")[0]+".com" not in avoid:
                        sour.append(i.get_attribute('href').strip("/url?q="))
    return links


def ddg_check(q,links):
    url="https://www.duckduckgo.com?q=download+"+q+"+pdf"
    driver.get(url)
    table=driver.find_elements_by_tag_name('a')
    sour=[]
    avoid=["https://www.quora.com"]
    for i in table:
        if i.get_attribute('href')!=None:
            if "http" in i.get_attribute('href'):
                if ".pdf" in i.get_attribute('href'):
                    if i.get_attribute('href').split("&sa=U")[0].endswith(".pdf"):
                        links.append(i.get_attribute('href').split("&sa=U")[0].strip("/url?q="))
                else:
                    if i.get_attribute('href').strip("/url?q=").split(".com")[0]+".com" not in avoid:
                        sour.append(i.get_attribute('href').strip("/url?q="))
    driver.quit()
    return links,sour


def bsoup(temp):
    links=[]
    for k in temp:
        r = requests.get(k) 
        soup = BeautifulSoup(r.content, 'html5lib')
        table = soup.findAll("a")
        for i in table:
            try:
                if "pdf" in i.get('href'):
                    if i.get('href').endswith(".pdf"):
                        if "http" not in i.get('href'):
                            try:
                                links.append(k.split(".org")[0]+".org"+i.get('href'))
                            except:
                                try:
                                    links.append(k.split(".edu")[0]+".edu"+i.get('href'))
                                except: 
                                    links.append(k.split(".com")[0]+".com"+i.get('href'))
                        else:
                            links.append(i.get('href'))
            except:
                pass
    return links



def pdl(arg,flag=1):
    _options.add_argument("--headless")
    
    ddg=0
    links=[]
    sour=[]
    if len(arg.split(" "))>1:
        arg=arg.replace(" ","+")
    
    links=ggl_check(arg,links)
    if len(links)==0:
        ddg=1
        links,sour=ddg_check(arg,links)
    
    check=initiate_pdl(links,flag)
    if check[0]:
        return check[1]
    
    temp=[]
    for i in arg.split("+"):
        for j in sour:
            if i.lower() in j.lower():
                temp.append(j)

    temp=set(temp)
    links=bsoup(temp)
    return initiate_pdl(links,flag)[1]


def mp3(name,extn):
    video = VideoFileClip(os.path.join(os.path.dirname(os.path.realpath(__file__)),os.path.join("downloaded/temp",name+extn)))
    video.audio.write_audiofile(os.path.join(os.path.dirname(os.path.realpath(__file__)),os.path.join("downloaded/temp",name.split(extn)[0].strip()+".mp3")))
    video.close()
    os.remove(os.path.join(os.path.dirname(os.path.realpath(__file__)),os.path.join("downloaded/temp",name+extn)))



def search(url):
    link={}
    _options.add_argument("--headless")
    driver=webdriver.Chrome(options=_options)
    driver.get(url)
    s=driver.find_elements_by_id("video-title")
    for i in s:
        if i.get_attribute('href')!=None:
            link[i.text]=i.get_attribute("href")
    driver.quit()
    return link

def ydl(arg,mp3flag=0,flag=1):
    
    ch=""
    link={}
    url="https://www.youtube.com/results?search_query="+arg.replace(".mp3","")
    ydl_opts = {'outtmpl': '{}.%(ext)s'.format(os.path.join(os.path.dirname(os.path.realpath(__file__)),os.path.join("downloaded/temp",arg.replace(".mp3",""))))}

    
    def dwl_vid(url): 
        with youtube_dl.YoutubeDL(ydl_opts) as ydl: 
            ydl.download([url])

    link=search(url)
    if len(link)>0:
        dr={}
        for l,i in enumerate(link):
            dr[l]=i
        tp = PrettyTable(['S.no', 'Name'])
        for key, val in dr.items():
           tp.add_row([key+1, val])
        if flag:
            ch==""
        else:
            print(tp)
            ch=input("Select or Press 'Enter' to Skip -: ")
        if ch=="":
            url=link[dr[0]]
        else:
            ch=ch.strip()
            ch=int(ch.strip())
            url=link[dr[ch-1]]
    else:
        url=input("Enter URL-: ")

    link_of_the_video = url
    dwl_vid(link_of_the_video.strip() )

    
    extns=[".mp4",".mkv",".webm"]
    extn=""

    file=next(os.walk(os.path.join(os.path.dirname(os.path.realpath(__file__)),"downloaded/temp")))[2][0]
    
    extn=[x for x in extns if file.endswith(x)][0]

    if mp3flag:
        mp3(arg.split(".mp3")[0],extn)
        return arg

    return file


