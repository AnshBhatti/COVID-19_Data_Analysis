import pandas as pd
import numpy as np
from tkinter import *
from datetime import date, timedelta, datetime
import os.path
from generate_excel import generate, update
from ghs import acquire_ghs
from time import sleep
import matplotlib.pyplot as plt
import tkinter.font as tkFont
from PIL import ImageTk,Image
from time import sleep
from life_exp import get_exp
global letters
global lis
global opts
global colors
global m
global b
colors=["red","green","blue","brown","yellow"]
letters=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S1","S2","T","U","V","W","X","Y","Z"]
lis=[-1,-1,-1,-1,-1]
tk=Tk()
helv36 = tkFont.Font(family="Comfortaa",size=14)
tk.title("COVID-19 Analysis")
canvas=Canvas(bg="#fce8b1",width=1000,height=750)
canvas.pack()
def call(event):
    print(str(event.x)+' '+str(event.y))
canvas.bind("<Button-1>",call)

BASE_URL="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"
def updates_by_country(event,r=1):
    canvas.delete('all')
    canvas.create_rectangle(20,20,980,730,fill="white",outline="white")
    btn=Button(text='Return',command=setup_GUI,relief=FLAT,bg="cyan")
    canvas.create_window(930,120,window=btn)
    canvas.create_text(500,50,font="Courier 20",text="Covid-19 Cases and Response Factors",justify=CENTER)
    writ=canvas.create_rectangle(50,100,150,140,fill="#dbddff",outline="#dbddff")
    writ1=canvas.create_text(100,120,text="Written",font=helv36)
    grph=canvas.create_rectangle(150,100,250,140,fill="#ffe3cf",outline="#ffe3cf")
    grph1=canvas.create_text(200,120,text="Graph",font=helv36)
    canvas.tag_bind(writ,"<Button-1>",wri)
    canvas.tag_bind(writ1,"<Button-1>",wri)
    canvas.tag_bind(grph,"<Button-1>",gr)
    canvas.tag_bind(grph1,"<Button-1>",gr)
    if r==1:
        written('A')
    else:
        graph()
def wri(event):
    updates_by_country(event,r=1)
def written(let):
    canvas.create_rectangle(50,140,950,710,fill="#dbddff",outline="#dbddff")
    canvas.create_text(70,160,text="Country",font="Times 14",anchor=W)
    canvas.create_text(200,160,text="Confirmed",font="Times 14",anchor=W)
    canvas.create_text(300,160,text="Recovered",font="Times 14",anchor=W)
    canvas.create_text(400,160,text="Deaths",font="Times 14",anchor=W)
    canvas.create_text(500,160,text="Active",font="Times 14",anchor=W)
    canvas.create_text(600,160,text="Response Factor",font="Times 14",anchor=W)
    canvas.create_text(860,180,text="Browse countries by letter:",font="Times 14",width=150)
    act=active.tail(1)
    con=confirmed.tail(1)
    dea=deaths.tail(1)
    rec=recovered.tail(1)
    y=190
    for a in range(len(countries)):
        if countries[a][0].upper()==let or let=="S1" and countries[a][0].upper()=='S' and countries[a][1].lower()<'o' or let=="S2" and countries[a][0].upper()=='S' and countries[a][1].lower()>='o':
            canvas.create_text(70,y,text=countries[a],font="Times 12",anchor=W,width=130)
            canvas.create_text(200,y,text=int(con[countries[a]]),font="Times 12",anchor=W)
            canvas.create_text(300,y,text=int(rec[countries[a]]),font="Times 12",anchor=W)
            canvas.create_text(400,y,text=int(dea[countries[a]]),font="Times 12",anchor=W)
            canvas.create_text(500,y,text=int(act[countries[a]]),font="Times 12",anchor=W)
            if countries[a] in list(country_rf.index):
                canvas.create_text(600,y,text=country_rf["rf"][countries[a]],font="Times 12",anchor=W)
            else:
                canvas.create_text(600,y,text="N/A",font="Times 12",anchor=W)
            y+=30
    var=StringVar(tk)
    var.set(let)
    w=OptionMenu(tk,var,*letters,command=written)
    canvas.create_window(900,200,window=w)
def gr(event):
    updates_by_country(0,r=0)
def graph():
    canvas.create_rectangle(50,140,950,710,fill="#ffe3cf",outline="#ffe3cf")
    canvas.create_text(500,160,text="Select at most 5 countries you want to compare (leave dropdowns empty as needed):",font="Times 14")
    q=StringVar(tk)
    q1=StringVar(tk)
    q2=StringVar(tk)
    q3=StringVar(tk)
    q4=StringVar(tk)
    q.set("Select a letter:")
    q1.set("Select a letter:")
    q2.set("Select a letter:")
    q3.set("Select a letter:")
    q4.set("Select a letter:")
    p1=OptionMenu(tk,q,*letters,command=p11)
    p2=OptionMenu(tk,q1,*letters,command=p22)
    p3=OptionMenu(tk,q2,*letters,command=p33)
    p4=OptionMenu(tk,q3,*letters,command=p44)
    p5=OptionMenu(tk,q4,*letters,command=p55)
    canvas.create_window(140,195,window=p1)
    canvas.create_window(320,195,window=p2)
    canvas.create_window(500,195,window=p3)
    canvas.create_window(680,195,window=p4)
    canvas.create_window(860,195,window=p5)
    global v
    global v1
    global v2
    global v3
    global v4
    v=StringVar(tk)
    v1=StringVar(tk)
    v2=StringVar(tk)
    v3=StringVar(tk)
    v4=StringVar(tk)
    v.set("Select a country:")
    v1.set("Select a country:")
    v2.set("Select a country:")
    v3.set("Select a country:")
    v4.set("Select a country:")
def p11(val):
    cont=[]
    for a in range(len(countries)):
        if countries[a][0].upper()==val or val=="S1" and countries[a][0].upper()=='S' and countries[a][1].lower()<'o' or val=="S2" and countries[a][0].upper()=='S' and countries[a][1].lower()>='o':
            cont.append(countries[a])
    o1=OptionMenu(tk,v,*cont,command=add)
    canvas.create_window(140,240,window=o1)
def p22(val):
    cont=[]
    for a in range(len(countries)):
        if countries[a][0].upper()==val or val=="S1" and countries[a][0].upper()=='S' and countries[a][1].lower()<'o' or val=="S2" and countries[a][0].upper()=='S' and countries[a][1].lower()>='o':
            cont.append(countries[a])
    o2=OptionMenu(tk,v1,*cont,command=add)
    canvas.create_window(320,240,window=o2)
def p33(val):
    cont=[]
    for a in range(len(countries)):
        if countries[a][0].upper()==val or val=="S1" and countries[a][0].upper()=='S' and countries[a][1].lower()<'o' or val=="S2" and countries[a][0].upper()=='S' and countries[a][1].lower()>='o':
            cont.append(countries[a])
    o3=OptionMenu(tk,v2,*cont,command=add)
    canvas.create_window(500,240,window=o3)
def p44(val):
    cont=[]
    for a in range(len(countries)):
        if countries[a][0].upper()==val or val=="S1" and countries[a][0].upper()=='S' and countries[a][1].lower()<'o' or val=="S2" and countries[a][0].upper()=='S' and countries[a][1].lower()>='o':
            cont.append(countries[a])
    o4=OptionMenu(tk,v3,*cont,command=add)
    canvas.create_window(680,240,window=o4)
def p55(val):
    cont=[]
    for a in range(len(countries)):
        if countries[a][0].upper()==val or val=="S1" and countries[a][0].upper()=='S' and countries[a][1].lower()<'o' or val=="S2" and countries[a][0].upper()=='S' and countries[a][1].lower()>='o':
            cont.append(countries[a])
    o5=OptionMenu(tk,v4,*cont,command=add)
    canvas.create_window(860,240,window=o5)
def add(val):
    global li
    l1=[v.get(),v1.get(),v2.get(),v3.get(),v4.get()]
    li=[]
    for each in l1:
        if each!="Select a country:":
            li.append(each)
    if len(li)==1:
        canvas.create_text(70,320,width=200,anchor=W,justify=LEFT,text="Click on any of the following after you select at most 5 countries:",font="Times 14")
        bt1=Button(text="Confirmed",width=10,relief=FLAT,font="Times 14",bg="#31007a",fg="white",command=confirm)
        bt2=Button(text="Active",width=10,relief=FLAT,font="Times 14",bg="#31007a",fg="white",command=activ)
        bt3=Button(text="Recovered",width=10,relief=FLAT,font="Times 14",bg="#31007a",fg="white",command=recover)
        bt4=Button(text="Deaths",width=10,relief=FLAT,font="Times 14",bg="#31007a",fg="white",command=show_death)
        canvas.create_window(150,400,window=bt1)
        canvas.create_window(150,470,window=bt2)
        canvas.create_window(150,540,window=bt3)
        canvas.create_window(150,610,window=bt4)
    print(li)
def confirm():
    z=plt.cla()
    z=plt.xlabel("Date")
    z=plt.ylabel("Confirmed cases")
    va=max(list(confirmed.index))+1
    #z=plt.yticks(np.arange(0,6000000,50000))
    z=plt.xticks(np.arange(0,va,int(va/4)))
    confi=[list(confirmed[each]) for each in li]
    dates=active["Date"]
    for e in range(len(li)):
        z=plt.plot(dates,confi[e],color=colors[e],label=li[e])
    plt.legend()
    plt.savefig('plot.png',bbox_inches='tight')
    put_img('plot.png',620,485)
def put_img(fil,x,y):
    img=PhotoImage(file=fil)
    label=Label(image=img)
    label.image=img
    label.pack()
    canvas.create_window(x,y,window=label)
def activ():
    z=plt.cla()
    z=plt.xlabel("Date")
    z=plt.ylabel("Active cases")
    va=max(list(active.index))+1
    #z=plt.yticks(np.arange(0,6000000,50000))
    z=plt.xticks(np.arange(0,va,int(va/4)))
    confi=[list(active[each]) for each in li]
    dates=active["Date"]
    for e in range(len(li)):
        z=plt.plot(dates,confi[e],color=colors[e],label=li[e])
    plt.legend()
    plt.savefig('plot.png',bbox_inches='tight')
    put_img('plot.png',620,485)
def recover():
    z=plt.cla()
    z=plt.xlabel("Date")
    z=plt.ylabel("# of people recovered")
    va=max(list(recovered.index))+1
    #z=plt.yticks(np.arange(0,6000000,50000))
    z=plt.xticks(np.arange(0,va,int(va/4)))
    confi=[list(recovered[each]) for each in li]
    dates=active["Date"]
    for e in range(len(li)):
        z=plt.plot(dates,confi[e],color=colors[e],label=li[e])
    plt.legend()
    plt.savefig('plot.png',bbox_inches='tight')
    put_img('plot.png',620,485)
def show_death():
    z=plt.cla()
    z=plt.xlabel("Date")
    z=plt.ylabel("Confirmed cases")
    va=max(list(deaths.index))+1
    #z=plt.yticks(np.arange(0,6000000,50000))
    z=plt.xticks(np.arange(0,va,int(va/4)))
    confi=[list(deaths[each]) for each in li]
    dates=active["Date"]
    for e in range(len(li)):
        z=plt.plot(dates,confi[e],color=colors[e],label=li[e])
    plt.legend()
    plt.savefig('plot.png',bbox_inches='tight')
    put_img('plot.png',620,485)
def rf_by_country(event):
    canvas.create_rectangle(20,20,980,730,fill="white",outline="white")
    btn=Button(text='Return',command=setup_GUI,relief=FLAT,bg="cyan")
    canvas.create_window(950,120,window=btn)
    canvas.create_text(500,50,font="Courier 20",text="Covid-19 Response Factor v. Confirmed Cases")
    canvas.create_rectangle(50,140,950,710,fill="#ffe3cf",outline="#ffe3cf")
    canvas.create_text(60,160,text="Analysis:",font="Times 20",anchor=W,justify=LEFT)
    con=confirmed.tail(1)
    z=plt.cla()
    z=plt.xlabel("# of confirmed cases to date")
    z=plt.ylabel("Response factor")
    x_data=np.array([int(con[each]) for each in countries])
    y_data=np.array(list(country_rf["rf"]))
    m,b=np.polyfit(x_data,y_data,1)
    print(y_data)
    z=plt.title("Response Factor vs. Cases")
    plt.scatter(x_data,y_data,color="black")
    plt.plot(x_data,m*x_data+b,color="black")
    plt.savefig("plot1.png",bbox_inches='tight')
    put_img('plot1.png',650,380)
    canvas.create_text(60,190,width=300,justify=LEFT,anchor=NW,font="Times 14",text='''Analyzing the dependance of the Response Factor of each country over its current # of confirmed cases is important in order to understand how much the # of confirmed cases affected the time it will take for a country to reach its peak in the number of active cases. This relationship is all but obvious. Even though in general, there is a positive correlation as expected, there are a lot of outliers, i.e. a lot of countries that either have a huge response factor and low number of confirmed cases or a low response factor and a high number of confirmed cases. As of now, issues with this analysis include the fact that the number of active cases in some countries are still increasing, so the response factor of many countries is''')
    canvas.create_text(60,610,width=900,justify=LEFT,anchor=NW,font="Times 14",text='''still increasing. Another issue is squeezed visualization of countries' # of confirmed cases in the scatter plot due to outliers in the # of confirmed cases. The correlation value tells us that, in general, for a +1 increase in response factor, nearly '''+str(int(1/m))+''' additional cases are needed.''')
def rf_ghs(event):
    canvas.create_rectangle(20,20,980,730,fill="white",outline="white")
    btn=Button(text='Return',command=setup_GUI,relief=FLAT,bg="cyan")
    canvas.create_window(950,120,window=btn)
    canvas.create_text(500,50,font="Courier 20",text="Response Factor v. Global Health Security Index")
    canvas.create_rectangle(50,140,950,720,fill="#ffe3cf",outline="#ffe3cf")
    canvas.create_text(60,160,text="Analysis:",font="Times 20",anchor=W,justify=LEFT)
    x_data=[]
    y_data=[]
    for each in list(ghs.index):
        if each in countries:
            x_data.append(ghs[ghs.columns[0]][each])
            y_data.append(country_rf["rf"][each])
    x_data=np.array(x_data)
    y_data=np.array(y_data)
    plt.cla()
    plt.xlabel("Global Health Security Index")
    plt.ylabel("Response Factor")
    plt.title("Response Factor v. GHS Index")
    m,b=np.polyfit(x_data,y_data,1)
    plt.scatter(x_data,y_data,color="black")
    plt.plot(x_data,m*x_data+b,color="black")
    plt.savefig("plot2.png",bbox_inches='tight')
    put_img("plot2.png",650,380)
    canvas.create_text(60,190,width=300,justify=LEFT,anchor=NW,font="Times 14",text='''Many consider Global Health Security Index to be an important factor that determined the fate of a country infected with the coronavirus. It is a score of how prepared a country is to face a pandemic such as the coronavirus. For this reason, it is important to compare GHS index with what we define as response factor, which is the number of days it took for a country to reach its peak in the number of active cases. Thus, one would expect a negative correlation between response factor and the GHS index, as they would expect a better (lower) response factor with a better (higher) GHS index. However, the scatter plot and linear regression indicate a slightly positive correlation, showing that an increase in the GHS''')
    canvas.create_text(60,610,width=900,justify=LEFT,anchor=NW,font="Times 14",text='''index will result in an increase in the response factor. The low magnitude of correlation also indicates that response factor and the GHS index are largely unrelated to each other. Both developed and developing countries suffered different fates, which mostly did not depend on how developed they were as indicated by this correlation. Many developed countries rank near the top in the number of cases due to other factors such as tourism and mass transportation. Thus, the GHS index is a good measure of preparedness, but not the reality.''')
    #plt.show()
def acr_rf(event):
    canvas.create_rectangle(20,20,980,730,fill="white",outline="white")
    btn=Button(text='Return',command=setup_GUI,relief=FLAT,bg="cyan")
    canvas.create_window(950,120,window=btn)
    canvas.create_text(500,50,font="Courier 20",text="Response Factor v. Life Expectancy")
    canvas.create_rectangle(50,140,950,720,fill="#ffe3cf",outline="#ffe3cf")
    canvas.create_text(60,160,text="Analysis:",font="Times 20",anchor=W,justify=LEFT)
    x_data=[]
    y_data=[]
    for each in countries:
        if each in list(life.index):
            x_data.append(life[life.columns[0]][each])
            y_data.append(country_rf["rf"][each])
    x_data=np.array(x_data)
    y_data=np.array(y_data)
    m,b=np.polyfit(x_data,y_data,1)
    plt.cla()
    plt.ylabel("Response Factor")
    plt.xlabel("Life Expectancy (in years)")
    plt.title("Response Factor v. Life Expectancy")
    plt.scatter(x_data,y_data,color="black")
    plt.plot(x_data,m*x_data+b,color="black")
    plt.savefig("plot3.png",bbox_inches="tight")
    put_img("plot3.png",650,380)
    canvas.create_text(60,190,width=300,justify=LEFT,anchor=NW,font="Times 14",text='''The life expectancy of a country is an average number of years that a person is expected to live for in that country. Higher life expectancy is generally associated with nations more on the developed side due to better health infrastructures and promotion of well-being in those countries. For this reason it is essential to analyze whether life expectancy has any impact the response factor of a country (the number of days it took for a country to reach its peak in active cases). Many would assume a negative correlation, in which a better life expectancy (higher) will resulted in a better response factor (lower). It turns out that the correlation is indeed negative. However, the magnitude of the correlation is low enough for the deduction that life''')
    canvas.create_text(60,610,width=900,justify=LEFT,anchor=NW,font="Times 14",text='''expectancy and response factor are barely or not correlated. The regression plot indicates that a significant difference in life expectancy will lead to a minor change. Therefore, the myth that life expectancy means better conditions for a country that faces a pandemic is not necessarily true as it depends on case to case. A pandemic's effects and every country's response factor vary on many different factors, including tourism, mass transportation, government action, public action, and political/social situation.''')
def setup_GUI():
    canvas.delete('all')
    canvas.create_text(500,50,text="COVID-19 Data Analysis",font="Courier 25")
    canvas.create_text(500,100,text="By: Ansh Bhatti",font="Courier 16")
    c1=canvas.create_rectangle(100,150,450,400,activefill="#d4bf96",fill="#fce8b1")
    c2=canvas.create_rectangle(550,150,900,400,activefill="#d4bf96",fill="#fce8b1")
    c3=canvas.create_rectangle(100,450,450,700,activefill="#d4bf96",fill="#fce8b1")
    c4=canvas.create_rectangle(550,450,900,700,activefill="#d4bf96",fill="#fce8b1")
    c11=canvas.create_text(275,270,text="COVID-19 Updates and Response\n Factor by Country",justify=CENTER,font="Times 16")
    c22=canvas.create_text(725,270,text="Response Factor vs Cases",font="Times 16")
    c33=canvas.create_text(275,570,text="Response Factor v. Global Health\nSecurity Index",justify=CENTER,font="Times 16")
    c44=canvas.create_text(725,570,text="Response Factor v. Life Expectancy",font="Times 16",justify=CENTER)
    canvas.tag_bind(c1,"<Button-1>",updates_by_country)
    canvas.tag_bind(c11,"<Button-1>",updates_by_country)
    canvas.tag_bind(c2,"<Button-1>",rf_by_country)
    canvas.tag_bind(c22,"<Button-1>",rf_by_country)
    canvas.tag_bind(c3,"<Button-1>",rf_ghs)
    canvas.tag_bind(c33,"<Button-1>",rf_ghs)
    canvas.tag_bind(c4,"<Button-1>",acr_rf)
    canvas.tag_bind(c44,"<Button-1>",acr_rf)
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
ghs_c=list(ghs["Country"])
for a in range(len(ghs_c)):
    if ghs_c[a]=="Czech Republic":
        ghs_c[a]="Czechia"
    elif ghs_c[a]=="Congo Democratic Republic":
        ghs_c[a]="Congo (Kinshasa)"
    elif ghs_c[a]=="Congo Brazzaville":
        ghs_c[a]="Congo (Brazzaville)"
    elif ghs_c[a]=="Myanmar":
        ghs_c[a]="Burma"
    elif ghs_c[a]=="Côte d’Ivoire":
        ghs_c[a]="Cote d'Ivoire"
    elif ghs_c[a]=="Eswatini (Swaziland)":
        ghs_c[a]="Swaziland"
    elif ghs_c[a]=="Guinea Bissau":
        ghs_c[a]="Guinea-Bissau"
    elif ghs_c[a]=="Kyrgyz Republic":
        ghs_c[a]="Kyrgyzstan"
    elif ghs_c[a]=="São Tomé and Príncipe":
        ghs_c[a]="Sao Tome and Principe"
    elif ghs_c[a]=="St Kitts and Nevis":
        ghs_c[a]="Saint Kitts and Nevis"
    elif ghs_c[a]=="St Lucia":
        ghs_c[a]="Saint Lucia"
    elif ghs_c[a]=="St Vincent and The Grenadines":
        ghs_c[a]="Saint Vincent and the Grenadines"
    elif ghs_c[a]=="Timor Leste":
        ghs_c[a]="Timor-Leste"
ghs.index=ghs_c
del ghs["Country"]
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
active.drop(["Diamond Princess","MS Zaandam","Holy See","Western Sahara","West Bank and Gaza"],axis=1)
confirmed.drop(["Diamond Princess","MS Zaandam","Holy See","Western Sahara","West Bank and Gaza"],axis=1)
recovered.drop(["Diamond Princess","MS Zaandam","Holy See","Western Sahara","West Bank and Gaza"],axis=1)
deaths.drop(["Diamond Princess","MS Zaandam","Holy See","Western Sahara","West Bank and Gaza"],axis=1)
active.rename(columns={"Korea, South":"South Korea","Eswatini":"Swaziland","US":"United States"},inplace=True)
recovered.rename(columns={"Korea, South":"South Korea","Eswatini":"Swaziland","US":"United States"},inplace=True)
confirmed.rename(columns={"Korea, South":"South Korea","Eswatini":"Swaziland","US":"United States"},inplace=True)
deaths.rename(columns={"Korea, South":"South Korea","Eswatini":"Swaziland","US":"United States"},inplace=True)
countries=list(active.columns)[1:]
country_rf=pd.DataFrame(index=countries,columns=["rf"])
if not os.path.exists("life_exp.csv"):
    get_exp()
life=pd.read_csv("life_exp.csv")
life_c=list(life["Country"])
del life["Country"]
for a in range(len(life_c)):
    if life_c[a]=="Côte d'Ivoire":
        life_c[a]="Cote d'Ivoire"
    elif life_c[a]=="DR Congo":
        life_c[a]="Congo (Kinshasa)"
    elif life_c[a]=="Czech Republic (Czechia)":
        life_c[a]="Czechia"
    elif life_c[a]=="Congo":
        life_c[a]="Congo (Brazzaville)"
    elif life_c[a]=="St. Vincent & Grenadines":
        life_c[a]="Saint Vincent and the Grenadines"
    elif life_c[a]=="Sao Tome & Principe":
        life_c[a]="Sao Tome and Principe"
    elif life_c[a]=="Myanmar":
        life_c[a]="Burma"
    elif life_c[a]=="Eswatini":
        life_c[a]="Swaziland"
life.index=life_c
for country in countries:
    cases=list(active[country])
    start=0
    while start<len(cases) and cases[start]==0:
        start+=1
    end=cases.index(max(cases))-start
    start=max(1,start)
    end=max(end,0)
    country_rf.at[country,"rf"]=end
