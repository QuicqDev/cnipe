"""
(FILE DESCRIPTION)
@author : Ashutosh | created on : 23-12-2022
"""
import sys
from PyQt6 import QtWidgets, uic

app = QtWidgets.QApplication(sys.argv)

window = uic.loadUi("temp/untitled.ui")
window.show()
app.exec()
