import ssl
import urllib2
import json
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import psycopg2

context = ssl._create_unverified_context()
quote_page = 'https://opendata.epa.gov.tw/ws/Data/AQI/?$format=json'
page = urllib2.urlopen(quote_page,context=context)
soup = BeautifulSoup(page,'html.parser')
JsonData = json.loads(str(soup))
geolocator = Nominatim()

conn = psycopg2.connect(database="monitoringdata", user="postgres", password="password", host="127.0.0.1", port="5432")
print "Opened database successfully"
cur = conn.cursor()

for item in JsonData:

    if item['Longitude']!="":
      cur.execute("INSERT INTO data (SiteName,County,AQI,PublishTime,Longitude,Latitude) VALUES ('"+item['SiteName'].encode('utf-8')+"','"+item['County'].encode('utf-8')+"','"+item['AQI'].encode('utf-8')+"','"+item['PublishTime'].encode('utf-8')+"','"+item['Longitude'].encode('utf-8')+"','"+item['Latitude'].encode('utf-8')+"')")
    else:
      location = geolocator.geocode(item['County'])
      cur.execute("INSERT INTO data (SiteName,County,AQI,PublishTime,Longitude,Latitude) VALUES ('"+item['SiteName'].encode('utf-8')+"','"+item['County'].encode('utf-8')+"','"+item['AQI'].encode('utf-8')+"','"+item['PublishTime'].encode('utf-8')+"','"+str(location.longitude)+"','"+str(location.latitude)+"')")


conn.commit()
print "Records created successfully";
conn.close()

