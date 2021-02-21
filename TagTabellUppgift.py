# Först måste du installera biblioteket requests. Skriv i terminalen: pip install requests
# Vid Fel:
# Canceled, Deleted, Deviation[].Description
# ToLocation
# ViaFromLocation
# LastUpdateDateTime
# TrackAtLocation
# ReasonCode[].Description
# Ta bort AdvertisedTrainIdent
import datetime
import requests
import tkinter as tk
from tkinter import ttk
import json

stations_dict = {'Karlstad':'Ks', 'Arvika': 'Ar', 'Kristinehamn':'Khn', 'Säffle':'Sfl', 'Sunne':'Sun'}

api_key = '6a7ca0019c5e4645bbb02acd60527ee9'

def getDepartures():
    request = f"""<REQUEST>
<LOGIN authenticationkey="{api_key}" />
<QUERY objecttype="TrainAnnouncement" schemaversion="1.3" orderby="AdvertisedTimeAtLocation">
<FILTER>
<AND>
<EQ name="ActivityType" value="Avgang" />
<EQ name="LocationSignature" value="{stations_dict[stationer.get()]}" />
<OR>
<AND>
<GT name="AdvertisedTimeAtLocation" value="$dateadd(07:00:00)" />
<LT name="AdvertisedTimeAtLocation" value="$dateadd(10:00:00)" />
</AND>
<AND>
<LT name="AdvertisedTimeAtLocation" value="$dateadd(00:30:00)" />
<LT name="EstimatedTimeAtLocation" value="$dateadd(10:00:00)" />
</AND>
</OR>
</AND>
</FILTER>
<INCLUDE>ViaFromLocation</INCLUDE>
<INCLUDE>Deleted</INCLUDE>
<INCLUDE>Cancelled</INCLUDE>
<INCLUDE>LastUpdateDateTime</INCLUDE>
<INCLUDE>Deviation[].Description</INCLUDE>
<INCLUDE>ReasonCode[].Description</INCLUDE>
<INCLUDE>AdvertisedTimeAtLocation</INCLUDE>
<INCLUDE>TrackAtLocation</INCLUDE>
<INCLUDE>ToLocation</INCLUDE>
</QUERY>
</REQUEST>"""

    url = 'https://api.trafikinfo.trafikverket.se/v1.3/data.json'
    response = requests.post(url, data = request, headers = {'Content-Type': 'text/xml'}, )

    response_json = json.loads(response.text)
    departures = response_json["RESPONSE"]['RESULT'][0]['TrainAnnouncement']

    senasteStation.delete(0,"end")

    senasteStationText.delete(1.0, "end")

    for dep in departures:
        stationer_text.insert(1., dep)
        stationer_text.insert(1., '\n')

    station = stationer.get()
    senasteStation.insert(0,station)
    

def sparaStation():
    stationen = stationer.get()

    with open(f'sparadstation.json', "w") as station:
        json.dump(stationen, station)
          
def uppdatering():
    time = datetime.datetime.now

     # box5.insert()


#----------------------
root = tk.Tk()
canvas = tk.Canvas(root, height=800, width=1200)
canvas.pack()

button=tk.Button(root, text='Hämta avgångar', fg='red', command= getDepartures)
button.place(relwidth=0.1, height=50)

stationer = ttk.Combobox(canvas, state='readonly')
stationer['values'] = list(stations_dict.keys())
stationer.set("")
stationer.place(relx=0, rely=0.1)

#Spara Station
sparaStationbox = tk.Button(canvas, text='Spara station', fg='red', command= sparaStation)
sparaStationbox.place(relx=0.12, rely=0)
#, """ # """

#Uppdatera informationen för att se ifall det är något nytt
box2 = tk.Button(canvas, text='Uppdatera', fg='red')
box2.place(relx=0.12, rely=0.03)
#, """ #command= uppdateraStats """

#Label för senast använda station
box3 = tk.Label(canvas, text='Senast Använda Station', fg='red')
box3.place(relwidth=0.2, height=30, relx=0, rely=0.3)

#Texten som säger senaste uppdatering
#, """ #command senastValdaStation"""
senasteUppdateringText = tk.Text(canvas)
senasteUppdateringText.place(relx=0.9, rely=0, relwidth=0.3, relheight=0.2)
#, text='Senaste Uppdateringen'

#Senast Använda station
senasteStation = tk.Listbox(canvas, fg='red')
#box5['values'] = list(stationer)
senasteStation.place(relwidth=0.2, height=60, relx=0, rely=0.35)

#Informations text
stationer_text = tk.Text(canvas)
stationer_text.place(relx=0.3, rely=0, relwidth=0.7, relheight=1)

root.mainloop()