from PyQt5 import QtWidgets, QtCore, QtWebEngineWidgets 

from gmplot import gmplot

import os


class MainWindow(QtWidgets.QMainWindow): 
    def __init__(self, parent = None): 
     super(MainWindow, self).__init__() 
     self.__setup__() 

    def __setup__(self): 
     self.resize(600, 600) 
     tabWidget = TabWidget(self) 
     self.setCentralWidget(tabWidget) 

    """ options = Options(self) 
     optionsDock = QtWidgets.QDockWidget() 
     optionsDock.setWidget(options) 
     optionsDock.setWindowTitle("Options") 
     self.addDockWidget(QtCore.Qt.TopDockWidgetArea, optionsDock) 

     options.spinBox_columns.valueChanged.connect(lambda: tabWidget.tabWidget.currentWidget(). 
                setColumnCount(options.spinBox_columns.value())) """
"""
class Options(QtWidgets.QWidget): 
    def __init__(self, parent): 
     super(Options, self).__init__(parent) 
     self.__setup__() 

    def __setup__(self): 
     self.spinBox_columns = QtWidgets.QSpinBox() 
     self.spinBox_columns.setValue(1) 
     self.spinBox_columns.setMinimum(1) 

     layout = QtWidgets.QVBoxLayout() 
     layout.addWidget(self.spinBox_columns) 
     self.setLayout(layout) """

class TabWidget(QtWidgets.QWidget): 
    def __init__(self, parent): 
     super(TabWidget, self).__init__(parent) 
     self.__setup__() 
     map = Map()
     #map.__setup__()
     
    def __setup__(self): 
        self.tabWidget = QtWidgets.QTabWidget() 
        
        self.view = QtWebEngineWidgets.QWebEngineView()
        self.tabWidget.addTab(self.view, "Map") 

        widget_2 = QtWidgets.QTableWidget() 
        self.tabWidget.addTab(widget_2, "Sys2") 
        
        widget_3 = QtWidgets.QTableWidget() 
        self.tabWidget.addTab(widget_3, "Sys3") 
        
        layout = QtWidgets.QVBoxLayout() 
        layout.addWidget(self.tabWidget) 
        self.setLayout(layout) 
        fichierweb = "file:///" + os.path.abspath("my_map.html").replace("\\", "/") + "#partiecommune"
        self.page = QtWebEngineWidgets.QWebEnginePage()
        self.page.setUrl(QtCore.QUrl(fichierweb))
        self.view.setPage(self.page)
        self.view.show()
     
class Map(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.__setup__(49.373659, 1.0752621, 16)
        
    def __setup__(self, x, y, z):
        gmap = gmplot.GoogleMapPlotter(x, y, z)
        gmap.draw("my_map.html")
        print("done")

def main(): 
    import sys 
    app = QtWidgets.QApplication(sys.argv) 
    window = MainWindow() 
    window.show() 
    app.exec_()

if __name__ == "__main__": 
    main() 

