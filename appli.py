import sys
from itertools import product
from PyQt5.QtWidgets import QMainWindow, QApplication,QHBoxLayout, QFrame,QPushButton,QTableWidgetItem, QWidget, QAction, QTabWidget,QVBoxLayout,QLabel,QTableWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from pylab import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from gmplot import gmplot
import os


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
     #map.__setup__()
     
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
        
        # Create first tab Map
        layout = QVBoxLayout() 
        layout.addWidget(self.tabs) 
        self.setLayout(layout) 
        fichierweb = "file:///" + os.path.abspath("my_map.html").replace("\\", "/") + "#partiecommune"
        self.page = QWebEnginePage()
        self.page.setUrl(QUrl(fichierweb))
        self.tab1.setPage(self.page)
        self.tab1.show()

        # Create second tab Cardio
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
     
class Map(QWidget):

    def __init__(self):
        super().__init__()
        self.__setup__(49.373659, 1.0752621, 16)
        
    def __setup__(self, x, y, z):
        gmap = gmplot.GoogleMapPlotter(x, y, z)
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

