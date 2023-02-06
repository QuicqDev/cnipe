"""
(FILE DESCRIPTION)
@author : Ashutosh | created on : 01-02-2023
"""
import os
import tkinter
import customtkinter

from napper import sc_taker

from PyQt5 import QtWidgets
from PIL import Image

from screenshot_taker import MyWidget
from html_to_image import make_gradient_image
from image_shaper import ImgModifier


dir_path = os.path.join("..", "temp")
capture_name = "capture.png"
gradient_name = "gradient.png"


dir_path = os.path.join("..", "temp")
capture_name = "capture.png"
gradient_name = "gradient.png"

# customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

APP = customtkinter.CTk()  # create CTk window like you do with the Tk window
APP.geometry("600x600")
APP.wm_iconbitmap("../ui/icon.ico")
APP.title("GNapper - Take Beautiful Screenshots")


def button_function():
    """
    nope
    """
    app = QtWidgets.QApplication([])
    window = MyWidget(capture_path=os.path.join(dir_path, capture_name))
    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    app.exec_()
    window.destroy()

    # create gradient
    gradient_path = make_gradient_image(store_dir=dir_path, gradient_name=gradient_name)

    image_modify_object = ImgModifier(
        outer_img=Image.open(os.path.join(gradient_path)),
        inner_img=Image.open(os.path.join(dir_path, capture_name)),
        padding=25
    )

    modified_image = image_modify_object.paste_img(rounded_corners=16)
    modified_image.save(os.path.join(dir_path, "modified.png"))

    bg_image = customtkinter.CTkImage(Image.open(os.path.join(dir_path, "modified.png")), size=(300, 400))
    bg_image_label = customtkinter.CTkLabel(master=APP, image=bg_image)
    bg_image_label.grid(row=0, column=0)


# Use CTkButton
button = customtkinter.CTkButton(master=APP, text="Capture Screenshot", command=button_function)
button.place(relx=0.7, rely=0.5, anchor=tkinter.W)


if __name__ == "__main__":
    APP.mainloop()
