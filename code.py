from tkinter import *
from tkinter import filedialog
import pandas as pd
import csv
import json
import os
import ntpath
import sqlite3
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure


conn = sqlite3.connect('chinyere.db')

def make_json(csvFilePath, jsonFilePath):
     
    # create a dictionary
    data = {}

# code for airports.csv
    names=os.path.basename(csvFilePath)
   
    if names=="airports.csv":
        # code to cleaning data
        df = pd.read_csv(csvFilePath)
        new_df = df.dropna()    
       
        new_df.to_csv (r'C:\Users\sa\Desktop\Vandna Pyhton\airportss.csv', index=None)
 
        listOfTables =conn.execute(''' SELECT name  FROM sqlite_master WHERE type='table' AND name='Airports' ''')
        if listOfTables == []:
            conn.execute("""CREATE TABLE Airports(id INTEGER  , ident varchar[20] , type varchar[20], name varchar[20], latitude_deg INTEGER,longitude_deg INTEGER, elevation_ft INTEGER, continent varchar[20],iso_country varchar[30],iso_region varchar[30],municipality varchar[30],scheduled_service varchar[30],gps_code varchar[30],iata_code varchar[20],local_code varchar[30],home_link varchar[50],wikipedia_link varchar[50],keywords varchar[30] );""")
            conn.commit()

        else:
            
            air_details = pd.read_csv('airportss.csv') # load to DataFrame
            air_details.to_sql('Airports',conn, if_exists='append', index = False) # write to sqlite table
        #Open a csv reader called DictReader
        with open("airportss.csv", encoding='utf-8') as csvf:
            csvReader = csv.DictReader(csvf)

            for rows in csvReader:
                        key = rows['id']
                        data[key] = rows
            
        # code to create json file after cleaning data
        with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
            jsonf.write(json.dumps(data, indent=4))
            
    # code for airport-frequencies.csv
    if names=="airport-frequencies.csv":
        # code to cleaning data
        df = pd.read_csv(csvFilePath)
        new_df = df.dropna()    
        new_df.to_csv (r'C:\Users\sa\Desktop\Vandna Pyhton\airport-frequencies.csv', index=None)
        listOfTables =conn.execute(''' SELECT name  FROM sqlite_master WHERE type='table' AND name='Airport_frequency' ''')
        if listOfTables == []:
            conn.execute("""CREATE TABLE Airport_frequency(id INTEGER  , airport_ref varchar[20] ,airport_ident varchar[20], type varchar[20], description varchar[100],frequency_mhz INTEGER);""")
            conn.commit()
            air_details = pd.read_csv('airport-frequencies.csv') # load to DataFrame
            air_details.to_sql('Airport_frequency',conn, if_exists='append', index = False) # write to sqlite table

        else:
            
            print('Table found!')
            air_details = pd.read_csv('airport-frequencies.csv') # load to DataFrame
            air_details.to_sql('Airport_frequency',conn, if_exists='append', index = False) # write to sqlite table
        #Open a csv reader called DictReader
        with open("airport-frequencies.csv", encoding='utf-8') as csvf:
            csvReader = csv.DictReader(csvf)

            for rows in csvReader:
                        key = rows['id']
                        data[key] = rows
            
        # code to create json file after cleaning data
        with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
            jsonf.write(json.dumps(data, indent=4))
        
#  code to calculate mean ,median and mode for large airport's frequencies
        data = pd.read_sql_query('''SELECT frequency_mhz,Airports.type
            FROM Airport_frequency 
            INNER JOIN Airports
            ON Airport_frequency.airport_ident = Airports.ident where Airports.type!='closed' and Airports.type=='large_airport';''', conn)

        # mode, median and mean of the airports.
        air_mode = data.mode()
        
        air_median = data.median()
        
        air_mean = data.mean()
        
        
#  code to  calculate mean, mode and median of frequency more than 100 mhz 
        data = pd.read_sql_query('''SELECT frequency_mhz,Airports.type
            FROM Airport_frequency 
            INNER JOIN Airports
            ON Airport_frequency.airport_ident = Airports.ident where Airports.type!='closed' and Airport_frequency.frequency_mhz>100;''', conn)

        # mode,median and mean
        freq_mode = data.mode()
        freq_median = data.median()
        freq_mean = data.mean()

    # code for runways.csv
    if names=="runways.csv":
        # code to cleaning data
        df = pd.read_csv(csvFilePath)
        new_df = df.dropna()    

        new_df.to_csv (r'C:\Users\sa\Desktop\Vandna Pyhton\runwayss.csv', index=None)
        listOfTables =conn.execute(''' SELECT name  FROM sqlite_master WHERE type='table' AND name='Airport_runway' ''')
        if listOfTables == []:
            conn.execute("""CREATE TABLE Airport_runway(id INTEGER  , airport_ref varchar[20] ,airport_ident varchar[20], width_ft varchar[20], surface varchar[100],lighted INTEGER, closed integer,le_ident varchar[30],le_latitude_deg integer, le_longitude_deg integer,le_elevation_ft integer,le_heading_degT integer, le_displaced_threshold_ft integer,he_ident varchar[30],he_latitude_deg integer,he_longitude_deg intger, he_elevation_ft integer, he_heading_degT integer, he_displaced_threshold_ft integer, );""")
            conn.commit()
            air_details = pd.read_csv('runwayss.csv') # load to DataFrame
            air_details.to_sql('Airport_runway',conn, if_exists='append', index = False) # write to sqlite table

        else:
            
            print('Table found!')
            air_details = pd.read_csv('runwayss.csv') # load to DataFrame
            air_details.to_sql('Airport_runway',conn, if_exists='append', index = False) # write to sqlite table
        #Open a csv reader called DictReader
        with open("runwayss.csv", encoding='utf-8') as csvf:
            csvReader = csv.DictReader(csvf)

            for rows in csvReader:
                        key = rows['id']
                        data[key] = rows
            
        # code to create json file after cleaning data
        with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
            jsonf.write(json.dumps(data, indent=4))

    

def openFile():
    tf = filedialog.askopenfilename(
        initialdir="C:/Users/MainFrame/Desktop/", 
        title="Open Text file", 
        filetypes=(("CSV Files", "*.csv"),)
        )
    pathh.insert(END, tf)
    df = pd.read_table(tf, sep="[;,]", on_bad_lines='skip',engine='python')
   
    name=os.path.basename(tf)
    x = name.replace(".csv",".json")

    
    make_json(tf,x)



#  method to open new window  
def Visualisation():

# code to show visualization  frequencies used my "small-airports"
    mydb = sqlite3.connect('chinyere.db')
    mycursor = mydb.cursor()

    # Fecthing Data from sqlite to my python progame
    sql = '''SELECT frequency_mhz,Airports.type
    FROM Airport_frequency 
    INNER JOIN Airports
    ON Airport_frequency.airport_ident = Airports.ident where Airports.type!='closed' and Airports.type=='small_airport';''' 
    mycursor.execute(sql)
    mycursor.fetchall
    freq = []
    tdata = []

    for i in mycursor:
        freq.append(i[0])
        tdata.append(i[1])

    plt.bar(freq,tdata, color='green', edgecolor='blue', 
            linewidth=2)
    # Visulizing Data using Matplotlib

    plt.ylim(0, 5)
    plt.xlabel("frequency")
    plt.ylabel("type of airport")
    plt.title("Visualisation")
    plt.show()
    f = Figure(figsize=(5,5), dpi=100)
    a = f.add_subplot(111)
    a.plot(freq,tdata)

    canvas = FigureCanvasTkAgg(f,self)
    canvas.show()
    canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    toolbar = NavigationToolbar2TkAgg(canvas,self)
    toolbar.update()
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
def airport_frequecy_graph():

    data1 = pd.read_sql_query('''SELECT frequency_mhz,Airports.type
        FROM Airport_frequency 
        INNER JOIN Airports
        ON Airport_frequency.airport_ident = Airports.ident where Airports.type!='closed' and  Airports.type ='small_airport' GROUP BY frequency_mhz ;''', conn)

    data2 = pd.read_sql_query('''SELECT frequency_mhz,Airports.type
        FROM Airport_frequency 
        INNER JOIN Airports
        ON Airport_frequency.airport_ident = Airports.ident where Airports.type!='closed' and  Airports.type ='large_airport' GROUP BY frequency_mhz ;''', conn)


    data3 = pd.read_sql_query('''SELECT frequency_mhz,Airports.type
        FROM Airport_frequency 
        INNER JOIN Airports
        ON Airport_frequency.airport_ident = Airports.ident where Airports.type!='closed' and  Airports.type ='medium_airport' GROUP BY frequency_mhz ;''', conn)

    # correlation between column 1 and column2 
    dt=data1['frequency_mhz'].corr(data2['frequency_mhz'])

    # correlation between column 2 and column3
    dtt=data2['frequency_mhz'].corr(data3['frequency_mhz'])

    # correlation between column 1 and column3
    dts=data1['frequency_mhz'].corr(data3['frequency_mhz'])

    plt.bar(dt,dtt,dts, color='green', edgecolor='blue', 
            linewidth=2)

    # Visulizing Data using Matplotlib

    plt.ylim(0, 5)
    plt.xlabel("frequency")
    plt.ylabel("Airports")
    plt.title("visualisation")
    plt.show()
    f = Figure(figsize=(5,5), dpi=100)
    a = f.add_subplot(111)
    a.plot(dt,dtt,dts)

    canvas = FigureCanvasTkAgg(f,self)
    canvas.show()
    canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    toolbar = NavigationToolbar2TkAgg(canvas,self)
    toolbar.update()
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


# code to display frequencies used more than once
def RepeatedFrequency():
    
    conn = sqlite3.connect('chinyere.db')
    # create cursor object
    cursor =conn.cursor()
    cursor.execute('''SELECT frequency_mhz,Airports.type
        FROM Airport_frequency 
        INNER JOIN Airports
        ON Airport_frequency.airport_ident = Airports.ident GROUP BY Airports.type HAVING COUNT(*) > 1;''')

    # fetch duplicate Frequencies and display them
    freq=[]
    datas=[]
    print('Duplicate Frequencies:')               
    for row in cursor.fetchall(): 
        freq.append(row[0])
        datas.append(row[1])
    plt.bar(freq,datas ,color='green', edgecolor='blue', 
            linewidth=2)
    # Visulizing Data using Matplotlib

    plt.ylim(0, 5)
    plt.xlabel("frequency")
    plt.ylabel("type of airport")
    plt.title("visualisation")
    plt.show()
    f = Figure(figsize=(5,5), dpi=100)
    a = f.add_subplot(111)
    a.plot(dt,dtt,dts)
    canvas = FigureCanvasTkAgg(f,self)
    canvas.show()
    canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    toolbar = NavigationToolbar2TkAgg(canvas,self)
    toolbar.update()
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    conn.close()

def openNewWindow():
     
    newWindow = Toplevel(ws)
    # Toplevel widget
    newWindow.title("Visualisation")
    newWindow.minsize(600,550)
    newWindow.maxsize(600,550)
    newWindow['bg']='#fb0'
    # sets the geometry of toplevel
    newWindow.geometry("600x550")
    visual_label = Label(newWindow, 
                  text = "Visualisation For Small Airport",bg='#fb0',  font=("Arial", 25)).place(x='70px',y='50px')
    Button(
    newWindow, 
    text="Plot Graph", 
    command=Visualisation
    ).place(x='200px',y='80px')
    
    visual_label1 = Label(newWindow, 
                  text = "Frequencies Corelation Visualisation",bg='#fb0',  font=("Arial", 25)).place(x='50px',y='150px')
    Button(
    newWindow, 
    text="Plot Graph", 
    command=airport_frequecy_graph
    ).place(x='200px',y='190px')
    
    visual_label2 = Label(newWindow, 
                  text = "Frequencies Reused",bg='#fb0',  font=("Arial", 25)).place(x='50px',y='240px')
    Button(
    newWindow, 
    text="Plot Graph", 
    command=RepeatedFrequency
    ).place(x='200px',y='290px')
    
ws = Tk()
ws.title("Upload Files")
ws.geometry("600x550")
ws.minsize(600,550)
 
# set maximum window size value
ws.maxsize(600,550)
ws['bg']='#fb0'

upload_label = Label(ws, 
                  text = "Upload Your File",bg='#fb0',  font=("Arial", 25)).place(x='130px',y='100px')


pathh = Entry(ws)
pathh.pack(side=LEFT, expand=True, fill=X, padx=10)



Button(
    ws, 
    text="Upload File", 
    command=openFile
    ).pack(side=LEFT, expand=True, fill=X, padx=10)
Button(
    
    ws, 
    text="Show Graph", 
    command=openNewWindow
    ).pack(side=RIGHT, expand=True, fill=X, padx=10)


ws.mainloop()