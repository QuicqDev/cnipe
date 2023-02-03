"""
(FILE DESCRIPTION)
@author : Ashutosh | created on : 29-01-2023
"""
import sys

import screeninfo
from PyQt5 import QtWidgets, QtCore, QtGui
import tkinter as tk
from PIL import ImageGrab


class MyWidget(QtWidgets.QWidget):
    """
    Widget to capture screenshots
    """

    def __init__(self, capture_path):
        super().__init__()
        root = tk.Tk()
        screen_count = QtWidgets.QDesktopWidget().screenCount()
        print(screen_count)
        all_screens = []
        for screen_number in range(screen_count):
            screen = QtWidgets.QDesktopWidget().screenGeometry(screen_number)
            all_screens.append(screen)
        print(all_screens)
        total_width = sum(screen.width() for screen in all_screens)
        max_height = max(screen.height() for screen in all_screens)
        self.setGeometry(0, 0, total_width, max_height)
        self.setWindowTitle(' ')
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowOpacity(0.3)
        self.capture_path = capture_path
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.show()

    @staticmethod
    def get_monitor_from_coord(x, y):
        monitors = screeninfo.get_monitors()

        for m in reversed(monitors):
            if m.x <= x <= m.width + m.x and m.y <= y <= m.height + m.y:
                return m
        return monitors[0]

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), 3))
        qp.setBrush(QtGui.QColor(128, 128, 255, 128))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.close()
        print(self.begin, self.end)
        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())
        print((x1, y1, x2, y2))
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2), all_screens=True)
        img.save(self.capture_path)
