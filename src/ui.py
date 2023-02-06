"""
(FILE DESCRIPTION)
@author : Ashutosh | created on : 01-02-2023
"""
import os
import tkinter
import customtkinter

from PyQt5 import QtWidgets
from PIL import Image

from screenshot_taker import MyWidget
from html_to_image import make_gradient_image
from image_shaper import ImgModifier


customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green


class App(customtkinter.CTk):
    """
    Tkinter Class
    """

    def __init__(self):
        super().__init__()
        self.geometry("800x500")
        self.wm_iconbitmap("../ui/gnapper.ico")
        self.iconbitmap(default='../ui/gnapper.ico')
        self.title("Cnipe - Take Beautiful Screenshot")

        # place button
        button = customtkinter.CTkButton(self, text="Capture Screenshot", command=self.capture_screenshot)
        button.place(relx=0.7, rely=0.5, anchor=tkinter.W)

    def capture_screenshot(self):
        """
        capture screenshot
        """
        dir_path = os.path.join("..", "temp")
        capture_name = "capture.png"
        gradient_name = "gradient.png"

        # minimise the app after taking screenshot
        self.wm_state('iconic')
        qt_app = QtWidgets.QApplication([])
        window = MyWidget(capture_path=os.path.join(dir_path, capture_name))
        window.show()
        qt_app.aboutToQuit.connect(qt_app.deleteLater)
        qt_app.exec_()
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
        bg_image_label = customtkinter.CTkLabel(self, image=bg_image)
        bg_image_label.grid(row=0, column=0)

        # open the app after taking screenshot
        # APP.wm_state("zoomed")
        self.deiconify()


if __name__ == "__main__":
    app = App()
    app.mainloop()
