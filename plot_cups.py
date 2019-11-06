#!/usr/bin/python3

import matplotlib.pyplot as plt
import matplotlib
import urllib.request
from datetime import datetime, timedelta
from dateutil import tz

#open the txt, return two lists:
# t: time as datetime
# c: cups as float from 0 to 10
def openfile():
    dictionary = {}
    filepath = "https://coffeestats.eero.tech/coffee.txt"
    data = urllib.request.urlopen(filepath)
    i = 0
    times = [] #time
    cups = [] #cups
    #return data after a certain time
    idx = 0
    datastart = datetime.strptime("2019-10-28 00:00:01", "%Y-%m-%d %H:%M:%S")

    for line in data:
        line = (line.decode('utf-8').strip("\n").split(" "))
        time = int(line[0])
        cup = float(line[1])
        time = datetime.fromtimestamp(time)
        times.append(time)
        cups.append(cup)
        if idx == 0:
            if time > datastart:
                idx = i
        i += 1
    return [times[idx:],cups[idx:]]

# coffee is brewing if cups increasing for more than 20 measurements
# coffee is ready when it is brewed and then cups decreases
# log the time when coffee is ready, and how many cups were made
def listbrewing(times, cups):
    brewing = False
    brewtimes = []
    brewcups = []
    starttime = 0
    duration = 0
    brewing = False
    for i in range(len(times) - 1):
        #check if brewing started
        if brewing == False:
            if cups[i+1] > cups[i]:
                duration += 1
                if starttime == 0:
                    starttime = times[i]
                    startidx = i
                #check if brewing for more than 20 meas
                if duration > 20:
                    brewing = True
            else:
                duration = 0
        #check if brewing done
        else:
            if cups[i] > cups[i+1]:
                brewtimes.append(times[i])
                brewcups.append(cups[i])
                brewing = False
                starttime = 0
                duration = 0
    if 1:
        plt.cla()
        plt.clf()
        plt.plot(brewtimes,brewcups,"rx")#,"gx")
        bottom, top = plt.ylim()
        plt.ylim(0, top)
        #plt.xlabel("Aika")
        plt.ylabel("Kuppeja")
        plt.grid(which='major')
        plt.xticks(rotation=15)
        plt.tight_layout()
        plt.savefig("pannut.png")
        #plotcombined(times, cups)

    return [brewtimes, brewcups]

#plot how many pots (and cups) brewed per day
# cups = (brewed cups)/(max of brewed cups)
# return three lists: dates, cups, pots
def plotPotsPerDay(brewtimes, brewcups):
    cups = {}
    pots = {}
    startdate = brewtimes[0].date()
    maxcups = 10 #max(brewcups)
    for i in range(len(brewtimes)):
        d = brewtimes[i].date()
        if d not in cups.keys():
            cups[d] = 0
            pots[d] = 0
        cups[d] += brewcups[i]/maxcups
        pots[d] += 1
    dlist = cups.keys()
    datelist = []
    cuplist = []
    potlist = []
    for k in dlist:
        datelist.append(k)
        cuplist.append(cups[k])
        potlist.append(pots[k])
    plt.cla()
    plt.clf()
    plt.plot(datelist, cuplist, ".")
    plt.plot(datelist, potlist, ".")
    plt.legend(["Pannullisia","Pannuja"])
    plt.grid(which='major')
    plt.xticks(rotation=10)
    plt.tight_layout()
    plt.savefig("pannutperpva.png")
    return [datelist, cuplist, potlist]

def plotPotsPerWeekday(datelist, cuplist, potlist):
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",\
               "Saturday", "Sunday"]
    weekdaysFi = ["Ma", "Ti", "Ke", "To", "Pe", "La", "Su"]
    weekdaysEn = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    wd = {}
    for d in weekdays:
        wd[d] = 0
    for i in range(len(datelist)):
        d = (datelist[i].strftime("%A"))
        wd[d] += cuplist[i]
    plotlist = []
    for d in weekdays:
        plotlist.append(wd[d])
    plt.cla()
    plt.clf()
    plt.bar(weekdaysEn, plotlist)
    plt.tight_layout()
    plt.savefig("pannutpervkpva.png")
    return 0

def plotPotsPerHour(brewtime, brewcups):
    hlist = range(0,24)
    hd = {}
    maxcups = 10#max(brewcups)
    for h in hlist:
        hd[h] = 0
    for i in range(len(brewtime)):
        h = (brewtime[i].hour)
        hd[h] += brewcups[i]/maxcups
    plotlist = []
    for h in hlist:
        plotlist.append(hd[h])
    plt.cla()
    plt.clf()
    plt.bar(hlist, plotlist)
    plt.title("Pannullista per kellonaika, n={:.0f}".format(sum(brewcups)/maxcups))
    plt.tight_layout()
    plt.savefig("pannutpertunti.png")
    #plt.show()
    return 0

#plot all of the data
def plotcombined(times, cups):
    plt.plot(times,cups,"k.")
    bottom, top = plt.ylim()
    plt.ylim(0, top)
    plt.grid(which='major')
    plt.xlabel("Aika")
    plt.ylabel("Kuppeja")
    plt.savefig("kuva.png")
    #plt.show()
    return 0

#plot last 24h or 3d
def plotTimeperiod(times, cups, period):
    time = datetime.now()
    if period == "24h":
        timeperiod = 24
        time = time - timedelta(hours = timeperiod)
    elif period == "3d":
        timeperiod = 3 
        time = time - timedelta(days = timeperiod)
    ptimes = []
    pcups = []
    for i in range(len(times)):
        if times[i] > time:
            idx = i
            break
    plt.cla()
    plt.clf()
    plt.plot(times[idx:],cups[idx:],".")
    bottom, top = plt.ylim()
    plt.ylim(0, top)
    plt.grid(which='major')
    plt.xlabel("Aika")
    plt.ylabel("Kuppeja")
    plt.xticks(rotation=10)
    plt.tight_layout()
    plt.savefig("kupit{}.png".format(period))
    #plt.show()
    return 0

[t, c] = openfile()
#plotcombined(t, c)
[bt, bc] = listbrewing(t, c)
[dl, cl, pl] = plotPotsPerDay(bt, bc)
plotPotsPerWeekday(dl, cl, pl)
plotPotsPerHour(bt, bc)
plotTimeperiod(t, c, "24h")
plotTimeperiod(t, c, "3d")

