import os
import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class Screenshot(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Create a label and set its background color to white
        self.label = QtWidgets.QLabel(self)
        self.label.setStyleSheet("background-color: white")

        # Create a push button and set its text
        self.button = QtWidgets.QPushButton('Take Screenshot', self)

        # Create a vertical layout and add the label and button
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        # Connect the button's clicked signal to the start_rectangle_screenshot method
        self.button.clicked.connect(self.start_rectangle_screenshot)

    def start_rectangle_screenshot(self):
        # Hide the button and show the cursor
        self.button.hide()
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))

        # Create a blank pixmap and a painter to draw on it
        self.pixmap = QtGui.QPixmap()
        self.painter = QtGui.QPainter(self.pixmap)
        self.painter.setRenderHint(QtGui.QPainter.Antialiasing)
        self.painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)

        # Set the painter's pen to a red dashed line
        self.painter.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0), 2, QtCore.Qt.DashLine))

        # Connect the mouse press, move, and release events to the corresponding methods
        self.label.mousePressEvent = self.on_mouse_press
        self.label.mouseMoveEvent = self.on_mouse_move
        self.label.mouseReleaseEvent = self.on_mouse_release

    def on_mouse_press(self, event):
        # Start drawing the rectangle from the mouse press position
        self.start_point = event.pos()
        self.end_point = self.start_point

    def on_mouse_move(self, event):
        # Update the end point of the rectangle and redraw it
        self.end_point = event.pos()
        self.update_screenshot()

    def on_mouse_release(self, event):
        # Update the end point of the rectangle and redraw it
        self.end_point = event.pos()
        self.update_screenshot()

        # Save the screenshot to a file
        self.pixmap.save("screenshot.png")

        # Show the button and reset the cursor
        self.button.show()
        QtWidgets.QApplication.restoreOverrideCursor()

    def update_screenshot(self):
        # Clear the pixmap and draw the desktop screenshot on it
        self.pixmap.fill(QtCore.Qt.transparent)
        self.painter.drawPixmap(QtCore.QRect(0, 0, QtWidgets.QApplication.primaryScreen().size().width(), QtWidgets.QApplication.primaryScreen().size().height()), QtWidgets.QApplication.primaryScreen().grabWindow(0))

        # Draw the rectangle on the pixmap
        self.painter.drawRect(QtCore.QRect(self.start_point, self.end_point))

        # Set the label's pixmap to the updated screenshot
        self.label.setPixmap(self.pixmap)

    

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Screenshot()
    window.show()
    sys.exit(app.exec_())