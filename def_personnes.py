import serial
import check_authorisation as check

port = serial.Serial('/dev/ttyUSB0', 9600)

print("Port {} ouvert".format(port.name))
print("*****************************")


while True:
    line = port.readline()
    if not line:
        continue

    try:
        splitLine = line.decode().split(' ')
    except UnicodeDecodeError:
        continue

    dataString = ""

    if splitLine[0] == 'Temperature':
        temperature = splitLine[2]
        temperature = temperature.replace('\r', '')
        temperature = temperature.replace('\n', '')
        temperature = temperature.replace(' ', '')

        print('Température : ' + temperature)

    while splitLine[0] == "Block":
        try:
            tmp = splitLine[3]
        except IndexError:
            continue
        tmp = tmp.replace('[', '')
        tmp = tmp.replace(']', '')
        tmp = tmp.replace('\n', '')
        tmp = tmp.replace('\r', '')

        dataString += tmp

        print(dataString)

        #On s'assure qu'il y a assez de data pour qu'un ID soit identifiable (ou non)
        if len(dataString) >= 46:
            check.idRFID = dataString[26 : 46]
            check.temperature = temperature
            #print('---------- ' + str(temperature))
            #print('__________' + str(check.temperature))
            nb_personnes = check.nbPersonnes()
            print('Nombres de personnes autorisees : ' + str(nb_personnes))

            """if authorisation is True:
                port.write('1'.encode())
            else:"""
            port.write('0'.encode())


        line = port.readline()
        if not line:
            break
        try:
            splitLine = line.decode().split(' ')
        except UnicodeDecodeError:
            continue

port.close()
print("*****************************")
print("Port fermé")
