from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request as urllib
import requests
import re
import pathlib
import os
import tkinter as tk
from tkinter import simpledialog
import subprocess
from collections import Counter
import _thread as thread


root= tk.Tk()

root.withdraw()
keyword = ""
file_n = open('main.tmp', 'w')
headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4147.135'
}


def getLinks(url, count):
    certificate = pathlib.Path().absolute().__str__() + "/cacert-2020-10-14.pem" #certifikati za SSL
    html_page = requests.get(url, headers=headers, verify=certificate).content
    soup = BeautifulSoup(html_page, features="html.parser")
    links = []
    links2 = []

    i = 0
    thread.start_new_thread(text_from_html,(soup,))

    for link in soup.findAll("a",{"href": [re.compile("^http://"), re.compile("^https://")]}):
            links.append(link.get("href"))
            file_n.write(link.get("href"))
            file_n.write("\n")



    for _ in range(count):
        for link2 in links:
            try:
                html_page = requests.get(link2, headers=headers, verify=certificate).content
                soup = BeautifulSoup(html_page, features="html.parser")
                thread.start_new_thread(text_from_html,(soup,))
                for link3 in soup.findAll("a", {"href": [re.compile("^http://"), re.compile("^https://")]}):
                    if not links2:
                        for pitanje in links:
                            if link3.get("href") in pitanje:
                                break
                        else:
                            links2.append(link3.get("href"))
                            file_n.write(link3.get("href"))
                            file_n.write("\n")
                    else:
                        for pitanje in links2:
                            if link3.get("href") in pitanje:
                                break
                        else:
                            links2.append(link3.get("href"))
                            file_n.write(link3.get("href"))
                            file_n.write("\n")
            except:
                    print("greska, preskacem")
        links = links2
    file_n.close()
    lines_seen = set()
    with open("out.txt", "w", encoding="utf-8", errors='ignore') as output_file:
        for each_line in open("main.tmp", "r", encoding="utf-8", errors='ignore'):
            if each_line not in lines_seen:
                output_file.write(each_line)
                lines_seen.add(each_line)
    #os.remove("main.tmp")
    output_file.close()
    sorter(keyword)
    print("done!")

  #  os.startfile(pathlib.Path().absolute().__str__() + "\\out.txt")

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(soup):
    global keyword
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    keyword += " ".join(t.strip() for t in visible_texts)



def sorter(list):
    list = list.split(" ")
    lista = [elem for elem in list if elem.strip()]
    list = [elem for elem in lista if "\"" not in elem and "}" not in elem and "\\" not in elem] #ovo je dodano jer je povlacilo i neke html tagove
    counts = Counter(list)
    with open("counter.txt", "w", encoding="utf-8", errors='ignore') as counter_file:
        for k,v in counts.most_common():
            counter_file.write( "{}\t{}\n".format(k,v) )
    counter_file.close()
    #print(counts)


unos1 = simpledialog.askstring(title="LinkFolower", prompt="Enter starting web address")
unos2 = int(simpledialog.askstring(title="LinkFolower", prompt="How many hops?"))

if unos1.startswith("http"):
    getLinks(unos1, unos2)
else:
    unos1 = "http://" + unos1
    getLinks(unos1, unos2)


