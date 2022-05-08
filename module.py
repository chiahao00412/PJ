import tkinter as tk
import subprocess as sp
from bs4 import BeautifulSoup
import requests
import threading


def yget_info(url):
    process = sp.Popen('you-get -i'+ url,
                       shell=True,
                       stdout=sp.PIPE, stderr=sp.PIPE)
    r = process.communicate()
    s = str(r[0],'utf-8')
    print(s)
    if s.find('title:') < 0:
        return '',''
    title = s[s.find('title:')+6: s.find('streams')].strip()
    itag =  s[s.find('itag:')+6: s.find('container')].strip()
    if len(itag)>8:
        itag = itag[4:-4]
    return title, itag


def yget_dl(url, itag = None):
    cmd = 'you-get'
    if itag:
        cmd = cmd + '--itag=' + 'itag' + ''
    process=sp.Popen(cmd+url)
    process.wait()
    return process.returncode

#爬蟲函數
def get_urls(url):
    urls=[]
    if '&list=' not in url: return urls
    response = requests.get(url)
    if response.status_code != 200:
        print('fail')
        return
    bs=BeautifulSoup(response.text,'lxml')
    a_list = bs.find_all('a')
    base = 'https://www.youtube.com/'
    for a in a_list:
        href=a.get('href')
        url = base + href
        if('&index=' in url) and (url not in urls):
            urls.append(url)
    return urls

lock = threading.Lock()   

def set_listbox(listbox, pos,msg):
 
    lock.acquire()
    if pos < 0:
        pos = listbox.size()
        listbox.insert(tk.END,f'{pos+1:02d}:'+msg)
    else:
        listbox.delete(pos)
        listbox.insert(pos,f'{pos+1:02d}:'+msg)
    lock.release()
    return pos


def build_windows(windows,click_func):
    windows.geometry('640x580')
    windows.title('youtube filminstaller')
    fm=tk.Frame(windows,bg='red',width=640,height=180)
    fm.pack()
    lb=tk.Label(fm,text='please input the url from youtube',
                padx=100,pady=100,fg='white',bg='red')
    lb.place(relx=0.5,rely=0.3,anchor='center')
    yt_url=tk.StringVar()
    user_input=tk.Entry(fm,textvariable=yt_url,width=47)
    user_input.place(relx=0.5,rely=0.5,anchor='center')
    btn=tk.Button(fm,text='download',command=click_func,height=0,width=8)
    btn.place(relx=0.9,rely=0.5,anchor='e')
    d_fm = tk.Frame(windows, width=640, height=480)
    d_fm.pack()
    lb2=tk.Label(d_fm,text='State',
                 fg='black')
    lb2.place(relx=0.5,rely=0.1,anchor='center')
    listbox= tk.Listbox(d_fm,width=65,height=15)
    listbox.place(relx=0.5,rely=0.5,anchor='center')
    sbar = tk.Scrollbar(d_fm)
    sbar.place(relx=0.86,rely=0.2,relheight=0.61)
    sbar.config(command=listbox.yview)
    listbox.config(yscrollcommand = sbar.set)
    sbar.config(command=listbox.yview)
    return listbox, yt_url

def start_dload(url,listbox):
    no = set_listbox(listbox,-1,f'read{url}')
    title, best = yget_info(url)
    if title == '':
        name ='error'
    else:
        name = f'{title}downloading'
    set_listbox(listbox, no, name)
    if title=='':
        return
    if best:
        yget_dl(url)
    else:
        pass
    set_listbox(list, no,f'{title}complete')    
    

    








    

    
    
    
    
    
    
    
    
    
    
    
    

