from sigfoxapi import Sigfox
import datetime

login = '5c4846efe833d917aff289ee'
pwd = 'e4a403da12cadcd0d81140176b75a5c8'
device = '1C684'

s = Sigfox(login, pwd)
out  = s.device_info(device)
mes = s.device_messages(device)


print("####################################################################")
print(mes[0])
print("####################################################################")
for k,v in mes[0].items():
    #print(k)
    if k == 'data':
        data = v
    if k == 'time':
        time_s = v
    if k == 'rinfos':
        for ki, vi in v[0].items():
            if ki == 'lat':
                lat = vi
            if ki == 'lng':
                lng = vi

print('data : ' + str(data))
print('time(s) : ' + str(time_s))
print('longitude : ' + str(lng))
print('latitude : ' + str(lat))

#print(time.time()) 
heure = str(datetime.datetime.fromtimestamp(time_s))
print(heure)

print("####################################################################")
#print(out)
#print(mes)
#print(type_mes)