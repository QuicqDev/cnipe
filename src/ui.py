"""
(FILE DESCRIPTION)
@author : Ashutosh | created on : 01-02-2023
"""
import os
import customtkinter

from PyQt5 import QtWidgets
from PIL import Image, ImageOps

from screenshot_taker import MyWidget
from html_to_image import make_gradient_image
from image_shaper import ImgModifier

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green
UI_PATH = "../ui"
IMAGE_DIR_PATH = os.path.join("..", "temp")


class App(customtkinter.CTk):
    """
    Tkinter Class
    """

    def __init__(self):
        super().__init__()
        self.geometry("900x700")
        self.wm_iconbitmap("../ui/gnapper.ico")
        self.iconbitmap(default='../ui/gnapper.ico')
        self.title("Cnipe - Take Beautiful Screenshot")
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(UI_PATH, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(UI_PATH, "home_light.png")),
                                                 size=(20, 20))
        # self.home_frame_large_image_label = None

        self.logo_image = customtkinter.CTkImage(
            Image.open(os.path.join(UI_PATH, "gnapper.png")), size=(30, 30))

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)
        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  CNIPE  ",
                                                             image=self.logo_image,
                                                             compound="left",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=40, pady=40)

        # place button
        self.sc_button = customtkinter.CTkButton(
            self.navigation_frame,
            text="Capture Screenshot", command=self.capture_screenshot, border_spacing=10)
        self.sc_button.grid(row=1, column=0, sticky="ew", padx=20, pady=20)

        # frames
        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                                   text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=2, column=0, sticky="ew")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_button_event()

    def capture_screenshot(self):
        """
        capture screenshot
        """
        capture_name = "capture.png"
        gradient_name = "gradient.png"

        # minimise the app after taking screenshot
        self.wm_state('iconic')
        self.clear_frame(name="home")
        qt_app = QtWidgets.QApplication([])
        window = MyWidget(capture_path=os.path.join(IMAGE_DIR_PATH, capture_name))
        window.show()
        qt_app.aboutToQuit.connect(qt_app.deleteLater)
        qt_app.exec_()
        window.destroy()

        # create gradient
        gradient_path = make_gradient_image(store_dir=IMAGE_DIR_PATH, gradient_name=gradient_name)

        image_modify_object = ImgModifier(
            outer_img=Image.open(os.path.join(gradient_path)),
            inner_img=Image.open(os.path.join(IMAGE_DIR_PATH, capture_name)),
            padding=25
        )

        modified_image = image_modify_object.paste_img(rounded_corners=16)
        modified_image.save(os.path.join(IMAGE_DIR_PATH, "modified.png"))

        im_width, im_height = modified_image.size
        pad_x, pad_y = 20, 10
        print(">> ", im_width, im_height, self.home_frame.current_width, self.home_frame._current_height) # noqa
        x, y = self.home_frame.current_width, self.home_frame._current_height # noqa
        x -= (2 * pad_x)
        y -= (2 * pad_y)
        # if x > 0 and y > 0:
        #     print("here")
        bg_image = ImageOps.contain(modified_image, (int(x), int(y)))

        # show image in home frame
        # bg_image = customtkinter.CTkImage(Image.open(os.path.join(IMAGE_DIR_PATH, "modified.png")), size=(500, 150))
        bg_image = customtkinter.CTkImage(bg_image, size=(bg_image.size[0], bg_image.size[1]))
        # bg_image_label.grid(row=0, column=1)

        home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=bg_image)
        home_frame_large_image_label.grid(row=0, column=0, padx=pad_x, pady=pad_y)

        # self.home_frame_large_image_label.bind('<Configure>', self.resize_image)
        # self.home_frame_large_image_label.pack(expand=tkinter.YES)

        # open the app after taking screenshot
        # APP.wm_state("zoomed")
        self.deiconify()

    def select_frame_by_name(self, name):
        """
        Select frame on main window
        """
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        # self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        # self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        # if name == "frame_2":
        #     self.second_frame.grid(row=0, column=1, sticky="nsew")
        # else:
        #     self.second_frame.grid_forget()
        # if name == "frame_3":
        #     self.third_frame.grid(row=0, column=1, sticky="nsew")
        # else:
        #     self.third_frame.grid_forget()

    def home_button_event(self):
        """Select home frame"""
        self.select_frame_by_name("home")

    # def resize_image(self, event):
    #     """auto resize image"""
    #     new_width = event.width
    #     new_height = event.height
    #     print(f"resizing : {new_width, new_height}")
    #     image = self.sc_image.resize((new_width, new_height))
    #     photo = ImageTk.PhotoImage(image)
    #     self.home_frame_large_image_label.configure(image=photo)
    #     self.home_frame_large_image_label.image = photo  # avoid garbage collection

    # @staticmethod
    # def resize_image(self, image_width, image_height, frame_width, frame_height, pad_x=0, pad_y=0):
    #     """
    #     Resize image
    #     """
    #     net_width = frame_width - (2 * pad_x)
    #     net_height = frame_height - (2 * pad_y)
    #
    #     aspect_ratio = image_width / image_height
    #     net_height = net_height * aspect_ratio
    #
    #     return net_width, net_height

    def clear_frame(self, name):
        """
        name
        """
        if name == "home":
            # destroy all widgets from frame
            for widget in self.home_frame.winfo_children():
                widget.destroy()

        # this will clear frame and frame will be empty
        # if you want to hide the empty panel then
        # frame.pack_forget()


if __name__ == "__main__":
    app = App()
    app.mainloop()
