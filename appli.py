import sys, os
from itertools import product

import serial
import check_persons as check
from sigfoxapi import Sigfox
import datetime

from PyQt5.QtWidgets import QMainWindow, QApplication,QHBoxLayout, QFrame,QPushButton,QTableWidgetItem, QWidget, QAction, QTabWidget,QVBoxLayout,QLabel,QTableWidget, QMessageBox, QAbstractItemView
from PyQt5.QtGui import QIcon, QPixmap, QFont, QImage
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from pylab import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

import json
from gmplot import gmplot
import cv2
import pyqtgraph as pg


class MainWindow(QMainWindow): 
    def __init__(self, parent = None): 
     super(MainWindow, self).__init__() 
     self.__setup__() 

    def __setup__(self): 
     self.resize(1000, 600) 
     self.setFixedSize(1000,600)
     tabs = TabWidget(self) 
     self.setCentralWidget(tabs) 

class TabWidget(QWidget): 
    def __init__(self, parent): 
        super(TabWidget, self).__init__(parent) 
        self.__setup__() 
        self.map = Map()
        
    def __setup__(self): 
    
        # Initialize geotag position value
        self.x = "0.0"
        self.y = "0.0"
        
        # Initialize graph coordinates of heartbeat
        self.bufferX = []
        self.bufferY = []
        
        # Initialize tab screen
        self.tabs = QTabWidget() 
        self.tab1 = QTableWidget()
        self.tab2 = QTableWidget() 
        self.tab3 = QTableWidget()

        # Add tabs
        self.tabs.addTab(self.tab1, "Map") 
        self.tabs.addTab(self.tab2, "Cardio")
        self.tabs.addTab(self.tab3, "Domotique") 
        
        layout = QVBoxLayout() 
        layout.addWidget(self.tabs) 
        self.setLayout(layout) 
        
        ###################################################################
        # TAB 1                                                           #
        ###################################################################
        
        # Create first tab Map
        self.latLab=QLabel(self.tab1)
        self.lonLab=QLabel(self.tab1)
        self.latValue=QLabel(self.tab1)
        self.lonValue=QLabel(self.tab1)
        
        self.latLab.setText("Latitude : ")
        self.lonLab.setText("Longitude :")
        self.latLab.move(5,0)
        self.lonLab.move(205,0)
        
        self.latValue.setText(self.x)
        self.lonValue.setText(self.y)
        self.latValue.move(85,0)
        self.lonValue.move(285,0)
        
        self.webWidget = QWebEngineView(self.tab1)
        self.webWidget.move(0,20)
        self.webWidget.resize(1000,580)
        self.fichierweb = "file:///" + os.path.abspath("my_map.html").replace("\\", "/")
        self.page = QWebEnginePage()
        self.page.setUrl(QUrl(self.fichierweb))
        self.webWidget.setPage(self.page)
        self.webWidget.show()
        
        ###################################################################
        # TAB 2                                                           #
        ###################################################################
        
        # Create second tab Cardio
        """
        # Define table
        """
        self.tableLabel = QLabel(self.tab2)
        self.tableLabel.setText("Data: ")
        self.tableLabel.move(20,0)
        
        self.table = QTableWidget(self.tab2)
        self.table.setMinimumWidth(304)
        self.table.setMinimumHeight(475)
        self.table.move(20,20)
        self.table.setRowCount(150)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderItem(0, QTableWidgetItem("Heure"))
        self.table.setColumnWidth(0,150)
        self.table.resizeRowsToContents()
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem("Rythme cardiaque"))
        self.table.setColumnWidth(1,150)
        self.table.verticalHeader().setVisible(False)
        # Unset the possibility to edit cells
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        """
        # Define graph
        """
        self.tempLabel = QLabel(self.tab2)
        self.tempLabel.setText("Rythme cardiaque: ")
        self.tempLabel.move(380,0)
        pg.setConfigOption('background', (240,240, 240))
        pg.setConfigOption('foreground', 'k')
        self.view = pg.PlotWidget(self.tab2)
        self.view.resize(550,475)
        self.view.move(380,20)
        self.view.setYRange(0, 30)

        self.view.showGrid(x=True,y=True)
        
        # Extract data from Sigfox device's message
        self.th3 = Thread3(self)
        self.th3.start()
        dicDevice, dicCardio = self.th3.sigfox()
        self.x = dicDevice['lat']
        self.y = dicDevice['lng']
        self.time = dicCardio['time_s']
        self.bpm = dicCardio['data']

        ###################################################################
        # TAB 3                                                           #
        ###################################################################
        
        # Create third tab
        self.tab3.principalLayout = QHBoxLayout(self.tab3)
        self.tab3.rightFrame = QFrame(self.tab3)
        self.tab3.verticalLayout = QVBoxLayout(self.tab3.rightFrame)
        self.label1 = QLabel(self)
        self.label1.setText("Nombre de personnes autorisées à entrer : ")
        self.label2 = QLabel(self)
        self.label2.setText("Nombre de personnes qui entrent : ")

        # Define label showing the number of person seen by the camera
        self.labelNbPerson = QLabel(self)
        self.nbPerson = self.catchNbPerson()
        self.labelNbPerson.setText(self.nbPerson)
        font = QFont("Times", 20, QFont.Bold)
        self.labelNbPerson.setFont(font)
        
        # Define serial port
        self.th2 = Thread2(self)
        self.th2.start()

        # Define label showing the number of person get from the RFID receptor
        self.labelNbPersonRFID = QLabel(self)
        self.nbPersonRFID = "0"
        self.labelNbPersonRFID.setText(self.nbPersonRFID)
        self.labelNbPersonRFID.setFont(font)
        
        # Define refresh button
        self.refreshButton = QPushButton("Refresh",self)
        self.refreshButton.clicked.connect(self.refresh)
        
        # Define video
        self.video = QLabel(self.tab3)
        self.video.move(280, 20)
        self.video.resize(640, 480)
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()
		
        # Set labels to tab3
        self.tab3.verticalLayout.addWidget(self.label1)
        self.tab3.verticalLayout.addWidget(self.labelNbPersonRFID)
        self.tab3.verticalLayout.addWidget(self.label2)
        self.tab3.verticalLayout.addWidget(self.labelNbPerson)
        self.tab3.verticalLayout.addWidget(self.refreshButton)
        self.tab3.principalLayout.addWidget(self.tab3.rightFrame)

        self.tab3.verticalLayoutR = QVBoxLayout()
        self.tab3.verticalLayoutR.setSpacing(0)
        self.tab3.exitFrame = QFrame(self.tab3)
        self.label3 = QLabel(self)
        pixmap = QPixmap("logo.png")
        self.resize(1000, 600)
        self.label3.setPixmap(pixmap)
        self.tab3.verticalLayoutR.addWidget(self.label3)
        self.tab3.principalLayout.addLayout(self.tab3.verticalLayoutR)
        
        ###################################################################
		
    def catchNbPerson(self):
	
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        rel_path = "dl/persons.txt"
        abs_file_path = os.path.join(script_dir, rel_path)

        try:
            fd = open(abs_file_path, mode='r')
        except FileNotFoundError:
            print("ERROR Cannot find file named: %s"%abs_file_path)
            #sys.exit()

        content = fd.read()
        fd.close()
        return content
        
    def refresh(self):
        
        self.nbPersonRFID = self.th2.nbPers() # Prendra la donnée transmise depuis le récepteur RFID
        self.labelNbPersonRFID.setText(str(self.nbPersonRFID))
        self.catchNbPerson()
        self.nbPerson = self.catchNbPerson()
        self.labelNbPerson.setText(self.nbPerson)
        self.alarm()
        self.extractToJson()
        
        self.latValue.setText(self.x)
        self.lonValue.setText(self.y)
        self.map.__setup__(float(self.x), float(self.y), 9)
        self.page.setUrl(QUrl(self.fichierweb))
        self.webWidget.setPage(self.page)
        self.webWidget.show()
        
        dicDevice, dicCardio = self.th3.sigfox()
        self.x = dicDevice['lat']
        self.y = dicDevice['lng']
        self.time = dicCardio['time_s']
        self.bpm = dicCardio['data']
        
        self.table_constructor(int(self.time),int(self.bpm))
        self.bufferX.append(int(self.time))
        self.bufferY.append(int(self.bpm))
        self.view.clear()
        self.view.plot(x = self.bufferX, y = self.bufferY, name='Rythme Cardiaque', pen='r', symbol='o')
        self.table.resizeRowsToContents()
        QApplication.processEvents()

    def alarm(self):
        if int(self.nbPersonRFID) != int(self.nbPerson):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Number of persons doesn't tie on!")
            msg.setWindowTitle("Alarm")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return True
        else:
            return False
            
    def setImage(self, image):
        self.video.setPixmap(QPixmap.fromImage(image))
        
    def extractToJson(self):
        dicOut = {"latitude":self.x,"longitude":self.y,"nbPerson":str(self.nbPersonRFID),"nbPersonCam":self.nbPerson,"cardiaque":self.bpm}

        filename = "data.json" 
        try: 
            with open(filename, "w") as fd: 
                json.dump(dicOut, fd) 
        except IOError:
            print("Problems opening file "+filename)

    def table_constructor(self, time, data):
        """
        # Construct info in the table
        """
        heure = datetime.datetime.fromtimestamp(time)
        for row in range(self.table.rowCount()):
            # Check for a free row
            """heures = [0]
            if heures[row-1] == heure:
                print("Data already received.")
                break
            
            heures.append(heure)
            print(heures)"""
            
            if self.table.cellWidget(row,0) is None:
                HBox1 = QHBoxLayout()
                HBox2 = QHBoxLayout()
                
                
                # Will take the value of time and beat per minute into the table
                HBox1.addWidget(QLabel(str(heure)))
                HBox2.addWidget(QLabel(str(data)))
                w1 = QWidget()
                w2 = QWidget()
                w1.setLayout(HBox1)
                w2.setLayout(HBox2)
                self.table.setCellWidget(row, 0, w1)
                self.table.setCellWidget(row, 1, w2)
                break

            elif row==149:
                popUp = QMessageBox()
                popUp.setText("The list is full. Reset it to show new values.")
                popUp.exec()
                break
            
class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        cap = cv2.VideoCapture("http://192.168.43.84:8080/?action=stream")
        while True:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

class Thread2(QThread):
    def nbPers(self):
        try:
            port = serial.Serial('/dev/tty.usbserial-A506QTYE', 9600) # MAC/OS
        except:
            try:                                                      # Windows
                port = serial.Serial()
                port.baudrate=9600
                port.port='COM32'                                     # Specify the good port
                port.open()
            except:
                print("ERROR Cannot open serial port.")
                return 0
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

class Thread3(QThread):
    def sigfox(self):
        login = '5c4846efe833d917aff289ee'
        pwd = 'e4a403da12cadcd0d81140176b75a5c8'
        device = '1C684'
        cardio = '736E5'

        s = Sigfox(login, pwd)
        mes = s.device_messages(device)

        for k,v in mes[0].items():
            #print(k)
            if k == 'rinfos':
                for ki, vi in v[0].items():
                    if ki == 'lat':
                        self.lat = vi
                    if ki == 'lng':
                        self.lng = vi
        self.dicDevice = {'lat' : self.lat, 'lng' : self.lng}

        mes = s.device_messages(cardio)

        for k,v in mes[0].items():
            #print(k)
            if k == 'data':
                self.data = v
            if k == 'time':
                self.time_s = v
        self.dicCardio = {'data' : self.data, 'time_s' : self.time_s}
        return self.dicDevice, self.dicCardio
         
class Map(QWidget):

    def __init__(self):
        super().__init__()
        self.__setup__(49.373659, 1.0752621, 12)
        
    def __setup__(self, x, y, z):
        gmap = gmplot.GoogleMapPlotter(x, y, z)
        gmap.marker(x, y, 'red')
        gmap.draw("my_map.html")
        print("done")

def main(): 
    import sys 
    app = QApplication(sys.argv) 
    window = MainWindow() 
    window.show() 
    app.exec_()

if __name__ == "__main__": 
    main()