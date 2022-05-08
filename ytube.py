import tkinter as tk
from tkinter import messagebox
import module as m
import threading
import re

def multi_download(urls,listbox):
    max_thread = threading.activeCount()+20
    urls.sort(key = lambda s: int(re.search('index=\d+',s).
                                  group()[6:]))
    for url in urls:
        while threading.activeCount()>= max_thread:
            pass
        threading.Thread(target=m.start_dload,
                         args=(url, listbox)).start()
        

def click_func():
    url=yt_url.get()
    if url.strip() == '': return 0
    urls = m.get_urls(url)
    if urls:
        if messagebox.askyesno('confirmbox','download all ?'):
            threading.Thread(target=multi_download,args=(urls, listbox)).start()
        else:
            threading.Thread(target = m.start_dload,args=(url, listbox)).start()
    else:
        threading.Thread(target = m.start_dload,
                         args=(url, listbox)).start()    
                
windows = tk.Tk()
listbox, yt_url=m.build_windows(windows,click_func)
windows.mainloop()
    


