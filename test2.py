#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python 3.5, PyQt5 v5.9.2
 
import sys
import os
from PyQt5 import QtWidgets, QtCore, QtWebEngineWidgets
 
#############################################################################
class Aide(QtWidgets.QWidget):
 
    #========================================================================
    def __init__(self, parent=None):
        super().__init__(parent)
 
        self.setWindowTitle("Aide")
        self.resize(800, 600)
 
        self.view = QtWebEngineWidgets.QWebEngineView()
 
        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.view, 0, 0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
 
        self.page = QtWebEngineWidgets.QWebEnginePage()
 
    #========================================================================
    def affiche(self, fichierweb):
        """affiche le fichier web donné
        """
        self.page.setUrl(QtCore.QUrl(fichierweb))
        self.view.setPage(self.page)
        self.view.show()
 
#############################################################################
if __name__ == '__main__':
 
    app = QtWidgets.QApplication(sys.argv)
 
    aide = Aide()
    aide.show()
 
    fichierweb = "file:///" + os.path.abspath("my_map.html").replace("\\", "/") + "#partiecommune"
 
    aide.affiche(fichierweb)
 
    sys.exit(app.exec_())