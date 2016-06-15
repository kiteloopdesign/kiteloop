#!/usr/bin/env python
# import numpy as np
import sys
sys.path.append("/home/pmora/bin/python_libs/beautifulsoup4-4.3.2/build/lib")
import bs4
from bs4 import BeautifulSoup
import subprocess
import matplotlib.pyplot as plt
from time import strftime

# TODO: specify name in wget command rather than here, as the default name might change
filename = 'VAL.html'
#filename = 'TOR.html'

dates   = []
number  = []
alert   = []
wind    = []
dir     = []
hours   = []

# date and time 
today_str = strftime("%d_%m_%Y@%Hh_%Mm")

# Mapa viento. HIRLAM-AEMET 0.05
# url = 'http://www.aemet.es/es/eltiempo/prediccion/modelosnumericos/hirlam005?opc2=val&opc3=vi'

# url = 'http://static.puertos.es/pred_simplificada/Predolas/Tablas/Med/TOR.html'
# url = 'http://static.puertos.es/pred_simplificada/Predolas/Tablas/Med/VAL.html'
url = 'http://static.puertos.es/pred_simplificada/Predolas/Tablas/?p=622028053&name=Valencia'

cmd = ['wget',url]
process = subprocess.Popen(cmd,True,stdout=subprocess.PIPE)
process.wait()
status = process.returncode

if status != 0:
  print('*E, ERROR: Data not downloaded. Wrong URL?')
  sys.exit()


f = open(filename,'r')
parsed_html = BeautifulSoup(f)
table_body = parsed_html.findAll('table')[2] #TODO: There are two tables on the page ... This might change in the future and script will break
rows = table_body.find_all('tr')

location = rows[0].find('th').text.strip().lower()

# Scrape the brains out of this MOFO! :D
for row in rows:
  cols = row.find_all('td')
  if cols: # avoid empty rows
    dates.append ( cols[0].text.strip() )
    number.append( cols[1].text.strip() )
    alert.append ( cols[2].text.strip() )
    wind.append  ( cols[3].text.strip() )
    dir.append   ( cols[4].text.strip() )

#yyyymmddhh
days = []
days.append(dates[0][6:8])
#hour = time[0][8:10]

# how many days are there so we can plot per day
for index,date in enumerate(dates):
  if days[-1] not in date[6:8]:
    days.append(date[6:8])


wind = [int(round(float(i)*1.94384,0)) for i in wind ]

line, = plt.plot(number, wind, label='wind',color='green',linewidth=2)

plt.grid()
plt.hold(True)

plt.legend(loc='best')
plt.title('{0}, {1}'.format(location, today_str))
plt.ylabel('Knots')
plt.xlabel('Time(hours)')
plt.savefig('{0}_{1}.png'.format(location,today_str),bbox_inches='tight') # TODO: save inside db ?
plt.show()


