"""
take screenshots
@author : Ashutosh | created on : 29-01-2023
"""
import os

from PyQt5 import QtWidgets
import sys
from PIL import Image

from screenshot_taker import MyWidget
from html_to_image import make_gradient_image
from image_shaper import ImgModifier


dir_path = os.path.join("temp")
capture_name = "capture.png"
gradient_name = "gradient.png"


def sc_taker():
    """
    Take Screenshot
    """
    # take screenshot
    app = QtWidgets.QApplication(sys.argv)
    window = MyWidget(capture_path=os.path.join(dir_path, capture_name))
    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    app.exec_()

    # create gradient
    gradient_path = make_gradient_image(store_dir=dir_path, gradient_name=gradient_name)

    image_modify_object = ImgModifier(
        outer_img=Image.open(os.path.join(gradient_path)),
        inner_img=Image.open(os.path.join(dir_path, capture_name)),
        padding=25
    )

    modified_image = image_modify_object.paste_img(rounded_corners=16)
    modified_image.save(os.path.join(dir_path, "modified.png"))
