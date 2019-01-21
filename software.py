# -*- coding: utf-8 -*-
# Author : Rodolphe Latour


import sys

from xbee import XBee, ZigBee
import serial

from PyQt5 import QtWidgets, QtGui, QtCore
import pyqtgraph as pg

#from utils import TimeAxisItem, timestamp

import numpy as np


class Window(QtWidgets.QWidget):

    def __init__(self):

        super().__init__()
        self.init_ui()

		
    def init_ui(self):

        """
        # Define window geometry
        """
        self.setWindowTitle("Projet OC 4")
        self.setGeometry(150,150,1000,600)
        self.setFixedSize(1200,600)

        """
        # Define layout and frame
        """
        self.vBox = QtWidgets.QVBoxLayout()
        self.setLayout(self.vBox)
        self.frame = QtWidgets.QFrame()
        self.vBox.addWidget(self.frame)

        """
        # Define table
        """
        self.tableLabel = QtWidgets.QLabel(self.frame)
        self.tableLabel.setText("Data: ")
        self.tableLabel.move(20,0)
        
        self.table = QtWidgets.QTableWidget(self.frame)
        self.table.setMinimumWidth(516)
        self.table.setMinimumHeight(475)
        self.table.move(20,20)
        self.table.setRowCount(150)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("HEX"))
        self.table.setColumnWidth(0,150)
        self.table.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("°C"))
        self.table.setColumnWidth(1,150)
        self.table.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem("Time"))
        self.table.setColumnWidth(2,200)
        self.table.verticalHeader().setVisible(False)
        # Unset the possibility to edit cells
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        """
        # Define temperature graph
        """
        self.tempLabel = QtWidgets.QLabel(self.frame)
        self.tempLabel.setText("Temperature: ")
        self.tempLabel.move(580,0)

        pg.setConfigOption('background', (240,240, 240))
        pg.setConfigOption('foreground', 'k')


        self.view = pg.PlotWidget(self.frame)
        #self.view = pg.PlotWidget(self.frame, axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.view.resize(550,475)
        self.view.move(580,20)
        self.view.setYRange(0, 30)
        #self.view.setXRange(timestamp(), timestamp() + 100)

        self.view.showGrid(x=True,y=True)
        
        #self.plotData = {'x': [], 'y': []}
        #self.plotCurve = self.view.plot(pen='y')
        
        #self.plotData['y'].append(testList)
        #self.plotData['x'].append(timestamp())

        #self.plotCurve.setData(self.plotData['x'], self.plotData['y'])

        """
        # Define buttons
        """
        self.resetButton = QtWidgets.QPushButton("Reset", self.frame)
        self.resetButton.move(50,530)
        #self.resetButton.clicked.connect(self.reset)

        self.updateButton = QtWidgets.QPushButton("Update", self.frame)
        self.updateButton.move(200,530)
        #self.updateButton.clicked.connect(self.update)

        self.updateClearButton = QtWidgets.QPushButton("Clear", self.frame)
        self.updateClearButton.move(800,530)
        #self.updateClearButton.clicked.connect(self.clearPlot)

        self.show()


    def fileSelector(self):
	
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,
								"QtWidgets.getOpenFileName()",
								"",
								"Log Files (*.log);;All Files (*)",
								options=options)
        if fileName:
        	return str(fileName)
		

    def xBee_init(self):
	
        self.ser = serial.Serial('/dev/ttyUSB0', 9600)

        # Use an XBee 802.15.4 device
        self.xbee = XBee(ser)



app = QtWidgets.QApplication(sys.argv)
win = Window()
quit(app.exec_())
