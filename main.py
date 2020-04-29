import pandas as pd
from tkinter import *
from datetime import date, timedelta, datetime
import os.path
from generate_excel import generate, update
from time import sleep
tk=Tk()
tk.title("COVID-19 Analysis")
canvas=Canvas(bg="#fce8b1",width=1000,height=750)
canvas.pack()
BASE_URL="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"
def setup_GUI():
    canvas.delete('all')
    canvas.create_text(500,50,text="COVID-19 Data Analysis",font="Courier 25")
    canvas.create_text(500,100,text="By: Ansh Bhatti",font="Courier 16")
    canvas.create_rectangle(100,150,450,400)
    canvas.create_rectangle(550,150,900,400)
    canvas.create_rectangle(100,450,450,700)
    canvas.create_rectangle(550,450,900,700)
    canvas.create_text(275,270,text="COVID-19 Updates by Country",font="Times 16")
    canvas.create_text(725,270,text="COVID-19 Response Factor by Country",font="Times 16")
    canvas.create_text(275,570,text="Response Factor v. Global Health\nSecurity Index",justify=CENTER,font="Times 16")
    canvas.create_text(725,570,text="Economic Drop (%) v. Response Factor",font="Times 16")
    #pending_work
if os.path.exists("data.xlsx"):
    f=open("STATUS.txt",'r')
    r=f.readline().split()
    f.close()
    d=str(datetime.today()).split()[0]
    if d[5:8]+d[8:]+'-'+d[:4]!=r[0]:
        print("Please wait for updates: Last update took place on "+d[5:8]+d[8:]+'-'+d[:4])
        update()
else:
    print("Please wait for data to be acquired...")
    generate()
setup_GUI()
active=pd.read_excel("data.xlsx",sheet_name="Active")
confirmed=pd.read_excel("data.xlsx",sheet_name="Confirmed")
recovered=pd.read_excel("data.xlsx",sheet_name="Recovered")
deaths=pd.read_excel("data.xlsx",sheet_name="Deaths")
