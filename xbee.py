import serial
import check_authorisation as check
import threading
import time


def nbPers():
    port = serial.Serial('/dev/tty.usbserial-A506QTYE', 9600)

    #port.open()

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

        #print(splitLine)

        while splitLine[0] == "ISO15693":
            try:
                tmp = splitLine[2]
            except IndexError:
                continue
            tmp = tmp.replace('[', '')
            tmp = tmp.replace(']', '')
            tmp = tmp.replace('\n', '')
            tmp = tmp.replace('\r', '')
            #print(tmp)  

            nb_personnes = check.nbPersonnes(tmp)
            #print('Nombres de personnes autorisees : ' + str(nb_personnes))

            line = port.readline()
            if not line:
                break
            try:
                splitLine = line.decode().split(' ')
            except UnicodeDecodeError:
                continue
            #time.sleep(5)

            port.close()
            print("*****************************")
            print("Port fermé")
            port.open()
            print("Port {} ouvert".format(port.name))
            print("*****************************")

            return nb_personnes

    #return nb_personnes

    port.close()
    print("*****************************")
    print("Port fermé")

#while(True):
#var = nbPers()
#print("fonction : " + str(var))