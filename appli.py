import sys, os
from itertools import product

import serial
import check_authorisation as check

from PyQt5.QtWidgets import QMainWindow, QApplication,QHBoxLayout, QFrame,QPushButton,QTableWidgetItem, QWidget, QAction, QTabWidget,QVBoxLayout,QLabel,QTableWidget, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QFont, QImage
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from pylab import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

import json
from gmplot import gmplot
import cv2


class MainWindow(QMainWindow): 
    def __init__(self, parent = None): 
     super(MainWindow, self).__init__() 
     self.__setup__() 

    def __setup__(self): 
     self.resize(1000, 600) 
     tabs = TabWidget(self) 
     self.setCentralWidget(tabs) 


class TabWidget(QWidget): 
    def __init__(self, parent): 
        super(TabWidget, self).__init__(parent) 
        self.__setup__() 
        map = Map()
        self.x = 0
        self.y = 0
        
    
    def __setup__(self): 
        # Initialize tab screen
        self.tabs = QTabWidget() 
        self.tab1 = QWebEngineView()
        self.tab2 = QTableWidget() 
        self.tab3 = QTableWidget()

        # Add tabs
        self.tabs.addTab(self.tab1, "Map") 
        self.tabs.addTab(self.tab2, "Cardio")
        self.tabs.addTab(self.tab3, "Domotique") 
        
        ###################################################################
        # TAB 1                                                           #
        ###################################################################
        
        # Create first tab Map
        layout = QVBoxLayout() 
        layout.addWidget(self.tabs) 
        self.setLayout(layout) 
        fichierweb = "file:///" + os.path.abspath("my_map.html").replace("\\", "/")
        self.page = QWebEnginePage()
        self.page.setUrl(QUrl(fichierweb))
        self.tab1.setPage(self.page)
        self.tab1.show()

        ###################################################################
        # TAB 2                                                           #
        ###################################################################
        
        # Create second tab Cardio
        self.cardio = 64
        
        self.tab2.principalLayout = QHBoxLayout(self.tab2)

        self.tab2.rightFrame = QFrame(self.tab2)
        self.tab2.verticalLayout = QVBoxLayout(self.tab2.rightFrame)
        self.table1 = QTableWidget()
        self.table1.setRowCount(150)
        self.table1.setColumnCount(2)
        self.table1.setHorizontalHeaderLabels(["Heure","Rythme Cardiaque"])
        self.tab2.verticalLayout.addWidget(self.table1)
        self.tab2.principalLayout.addWidget(self.tab2.rightFrame)


        self.tab2.verticalLayoutR = QVBoxLayout()
        self.tab2.verticalLayoutR.setSpacing(0)
        self.tab2.exitFrame = QFrame(self.tab2)

        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
 
        self.x = linspace(-pi, pi, 30)
        self.y = cos(self.x)
        self.line, = self.axes.plot(self.x, self.y)

        self.canvas = FigureCanvas(self.fig)
        self.tab2.verticalLayoutR.addWidget(self.canvas)

        self.tab2.principalLayout.addLayout(self.tab2.verticalLayoutR)

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
        self.nbPersonRFID = "0"#Thread2.run(self) # Prendra la donnée transmise depuis le récepteur RFID
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
        dic = {"latitude":self.x,"longitude":self.y,"nbPerson":self.nbPersonRFID,"nbPersonCam":self.nbPerson,"cardiaque":self.cardio}

        filename = "data.json" 
        try: 
            with open(filename, "w") as fd: 
                json.dump(dic, fd) 
        except IOError:
            print("Problems opening file "+filename)

            
            
class Map(QWidget):

    def __init__(self):
        super().__init__()
        self.__setup__(49.373659, 1.0752621, 12)
        
    def __setup__(self, x, y, z):
        gmap = gmplot.GoogleMapPlotter(x, y, z)
        gmap.marker(x, y, 'red')
        gmap.draw("my_map.html")
        print("done")


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
            port = serial.Serial('/dev/tty.usbserial-A506QTYE', 9600)
        except:
            try:
                port = serial.Serial()
                port.bitrate=9600
                port.port='COM29'
                port.open()
            except:
                print("ERROR Cannot open serial port.")
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
        

def main(): 
    import sys 
    app = QApplication(sys.argv) 
    window = MainWindow() 
    window.show() 
    app.exec_()


if __name__ == "__main__": 
    main()