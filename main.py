import pandas as pd
from tkinter import *
from datetime import date, timedelta, datetime
import os.path
from generate_excel import generate, update
from ghs import acquire_ghs
from time import sleep
import matplotlib.pyplot as plt
tk=Tk()
tk.title("COVID-19 Analysis")
canvas=Canvas(bg="#fce8b1",width=1000,height=750)
canvas.pack()
BASE_URL="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"
def event_click(event):
    if event.x>=100 and event.x<=450 and event.y>=150 and event.y<=400:
        updates_by_country()
    elif event.x>=550 and event.x<=900 and event.y>=150 and event.y<=400:
        rf_by_country()
    elif event.x>=100 and event.x<=450 and event.y>=450 and event.x<=700:
        rf_ghs()
    elif event.x>=550 and event.x<=900 and event.y>=450 and event.x<=700:
        acr_rf()
def updates_by_country():
    canvas.create_rectangle(20,20,980,730,fill="white",outline="white")
    canvas.create_text(500,50,font="Courier 20",text="Covid-19 Cases by Country")
def rf_by_country():
    canvas.create_rectangle(20,20,980,730,fill="white",outline="white")
    canvas.create_text(500,50,font="Courier 20",text="Covid-19 Response Factor by Country")
def rf_ghs():
    canvas.create_rectangle(20,20,980,730,fill="white",outline="white")
    canvas.create_text(500,50,font="Courier 20",text="Response Factor v. Global Health Security Index")
def acr_rf():
    canvas.create_rectangle(20,20,980,730,fill="white",outline="white")
    canvas.create_text(500,50,font="Courier 20",text="Active-Confirmed Ratio v. \nResponse Factor")
def setup_GUI():
    canvas.delete('all')
    canvas.create_text(500,50,text="COVID-19 Data Analysis",font="Courier 25")
    canvas.create_text(500,100,text="By: Ansh Bhatti",font="Courier 16")
    canvas.create_rectangle(100,150,450,400,activefill="#d4bf96")
    canvas.create_rectangle(550,150,900,400,activefill="#d4bf96")
    canvas.create_rectangle(100,450,450,700,activefill="#d4bf96")
    canvas.create_rectangle(550,450,900,700,activefill="#d4bf96")
    canvas.create_text(275,270,text="COVID-19 Updates and Response\n Factor by Country",justify=CENTER,font="Times 16")
    canvas.create_text(725,270,text="Response Factor vs Cases",font="Times 16")
    canvas.create_text(275,570,text="Response Factor v. Global Health\nSecurity Index",justify=CENTER,font="Times 16")
    canvas.create_text(725,570,text="Active-Confirmed Ratio v. \nResponse Factor",font="Times 16",justify=CENTER)
    canvas.bind("<Button-1>",event_click)
    #pending_work
if os.path.exists("data.xlsx"):
    f=open("STATUS.txt",'r')
    r=f.readline().split()
    f.close()
    d=str(datetime.today()).split()[0]
    if d[5:8]+d[8:]+'-'+d[:4]!=r[0]:
        print("Please wait for updates: Last update took place on "+r[0])
        update()
else:
    print("Please wait for the COVID cases data to be acquired...")
    generate()
if os.path.exists("ghs.csv"):
    ghs=pd.read_csv("ghs.csv")
else:
    print("Please wait for the Global Health Security Index data to be acquired")
    acquire_ghs()
    ghs=pd.read_csv("ghs.csv")
print("Loading graphical interface")
setup_GUI()
global active
global confirmed
global recovered
global deaths
active=pd.read_excel("data.xlsx",sheet_name="Active")
confirmed=pd.read_excel("data.xlsx",sheet_name="Confirmed")
recovered=pd.read_excel("data.xlsx",sheet_name="Recovered")
deaths=pd.read_excel("data.xlsx",sheet_name="Deaths")
countries=list(active.columns)[1:]
country_rf=pd.DataFrame(index=countries,columns=["rf"])
for country in countries:
    cases=list(active[country])
    start=0
    while start<len(cases) and cases[start]==0:
        start+=1
    end=cases.index(max(cases))-start
    start=max(1,start)
    rf=end/start
    country_rf.at[country,"rf"]=end
