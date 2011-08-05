#!/usr/bin/python

import sys
from PyQt4 import QtGui
from interface import window

app = QtGui.QApplication(sys.argv)
main_w = window.Window()
main_w.show()
sys.exit(app.exec_())

