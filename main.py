from tkinter import *
import requests
import json
from PIL import ImageTk, Image

url = requests.get("https://api.mcsrvstat.us/2/2b2t.org").text
y = json.loads(url)
bad_chars = ['[', ']', '{', '}']

def getQueue():
    queueurl = requests.get("https://2b2t.io/api/queue?last=true")
    data = queueurl.json()
    queue = int(data[0][1])
    return queue

def getPrioQ():
    pqueueurl = requests.get("https://2b2t.io/api/prioqueue?last=true")
    data = pqueueurl.json()
    pqueue = int(data[0][1])
    return pqueue

def getMotd():
    global y
    global bad_chars
    motd = y['motd']['clean']
    motd = ''.join(i for i in motd if not i in bad_chars)
    motd = motd.replace('2T', ' 2T')
    return motd

def getOnline(tm):
    global y
    playersmax = y['players']['max']
    playersonline = y['players']['online']
    if tm == 1:
        return playersonline
    else:
        return playersmax


window = Tk()

window.wm_iconbitmap('icon.ico')

window.title("2b2t utils")

window.geometry('580x250')

lblone = Label(window, text="2b2t queue: " + str(getQueue()), font=("Arial Bold", 15))
lblone.grid(column=1, row=1)

lbltwo = Label(window, text="| 2b2t prio queue: " + str(getPrioQ()), font=("Arial Bold", 15))
lbltwo.grid(column=2, row=1)

lblthree = Label(window, text="| 2b2t online: " + str(getOnline(1)) + "/" + str(getOnline(0)), font=("Arial Bold", 15))
lblthree.grid(column=3, row=1) 

lblmotd = Label(window, text="2b2t motd: " + str(getMotd()), font=("Roboto", 15))
lblmotd.place(x=0, y=25)

def clicked():
    res = "Info about: {}".format(txt.get())  
    lbl.configure(text=res)  
    player = str(txt.get())
    txt.delete(0, END)
    info = requests.get(f"https://api.2b2t.dev/stats?username=" + str(player))
    seen = requests.get(f"https://api.2b2t.dev/seen?username=" + str(player))
    info = info.json()[0]
    seen = seen.json()[0]
    kills = {info['kills']}
    kills = ''.join(i for i in str(kills) if not i in bad_chars)
    deaths = {info['deaths']}
    deaths = ''.join(i for i in str(deaths) if not i in bad_chars)
    joins = {info['joins']}
    joins = ''.join(i for i in str(joins) if not i in bad_chars)
    leaves = {info['leaves']}
    leaves = ''.join(i for i in str(leaves) if not i in bad_chars)
    lastseen = {seen['seen']}
    seen = ''.join(i for i in str(seen) if not i in bad_chars)
    seen = seen.replace('seen', '')
    infolabel.config(text="Kills: " + str(kills) + "\nDeaths: " + str(deaths) + "\nJoins: " + str(joins) + "\nLeaves: " + str(leaves),font=("Roboto", 10))
    infoseen.config(text="lastseen: " + str(seen))
infolabel = Label(window, text="Kills: none\nDeaths: none\nJoins: none\nLeaves: none", font=("Roboto", 10))
infolabel.place(x=257,y=145)
infoseen = Label(window, text="Last seen: none", font=("Roboto", 10))
infoseen.place(x=257, y=210)
lbl = Label(window, text="Info about: ", font=("Roboto", 10))  
lbl.place(x=250,y=100)  
txt = Entry(window,width=15)  
txt.place(x=250,y=125)
btn = Button(window, text="Click!", command=clicked)
btn.place(x=200,y=120)   

window.mainloop()
