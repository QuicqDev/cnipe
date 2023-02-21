"""
Take beautiful screenshots from CNIPE
@author : Ashutosh | created on : 01-02-2023
"""
import os
import tempfile
from tkinter import filedialog, messagebox

import customtkinter

from PyQt5 import QtWidgets
from PIL import Image, ImageOps

from src.screenshot_taker import MyWidget
from src.html_to_image import make_gradient_image
from src.image_shaper import ImgModifier
from src.scroll_action import ScrollableLabelButtonFrame

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Theme
UI_PATH = "ui"
tempdir = tempfile.TemporaryDirectory()
# save gradient and captured images in temp file which gets deleted after the execution is done
IMAGE_DIR_PATH = tempdir.name


class App(customtkinter.CTk):
    """
    Tkinter Class
    """

    def __init__(self):
        super().__init__()
        # set full screen for better view, full screen is different in different OS
        if os.name == "nt":
            self.state('zoomed')
        elif os.name == "posix":
            self.attributes('-fullscreen', True)

        self.wm_iconbitmap(os.path.join("ui", "gnapper.ico"))
        self.iconbitmap(default=r'ui\\gnapper.ico')
        self.title("Cnipe - Take Beautiful Screenshot")
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(UI_PATH, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(UI_PATH, "home_light.png")),
                                                 size=(20, 20))
        self.use_same_colors = None
        self.colors = [(247, 253, 166, 1), (128, 255, 221, 1), (255, 128, 249, 1)]  # initialise with set of colors

        self.logo_image = customtkinter.CTkImage(
            Image.open(os.path.join(UI_PATH, "gnapper.png")), size=(30, 30))
        self.main_image = None
        self.modified_image = None
        self.padding = 25

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

    def capture_screenshot(self, use_old=False, padding=25):
        """
        capture screenshot
        """
        capture_name = "capture.png"
        gradient_name = "gradient.png"

        if not use_old:
            # minimise the app after clicking screenshot button
            self.wm_state('iconic')
            self.clear_frame(name="home")
            qt_app = QtWidgets.QApplication([])
            window = MyWidget(capture_path=os.path.join(IMAGE_DIR_PATH, capture_name))
            window.show()
            qt_app.aboutToQuit.connect(qt_app.deleteLater)
            qt_app.exec_()
            window.destroy()

        color_grad = None
        if self.use_same_colors is not None and self.use_same_colors.get() == 1:
            color_grad = self.colors

        # create gradient
        gradient_path, self.colors = make_gradient_image(
            store_dir=IMAGE_DIR_PATH,
            gradient_name=gradient_name,
            colors=color_grad
        )

        image_modify_object = ImgModifier(
            outer_img=Image.open(os.path.join(gradient_path)),
            inner_img=Image.open(os.path.join(IMAGE_DIR_PATH, capture_name)),
            padding=padding
        )

        self.modified_image = image_modify_object.paste_img(rounded_corners=16)
        self.modified_image.save(os.path.join(IMAGE_DIR_PATH, "modified.png"))

        pad_x, pad_y = 60, 40
        x, y = self.home_frame._current_width, self.home_frame._current_height # noqa
        x -= (8 * pad_x)
        y -= (10 * pad_y)

        bg_image = ImageOps.contain(self.modified_image, (int(x), int(y)))

        # show image in home frame
        bg_image = customtkinter.CTkImage(bg_image, size=(bg_image.size[0], bg_image.size[1]))

        if self.main_image is not None:
            try:
                self.main_image.destroy()
            except ValueError:
                pass

        self.main_image = customtkinter.CTkLabel(self.home_frame, text="", image=bg_image)
        self.main_image.grid(row=0, column=0, padx=pad_x, pady=pad_y)

        # refresh gradient, generate random gradient
        button_frame = customtkinter.CTkFrame(self.home_frame)
        regen_grad = customtkinter.CTkButton(
            button_frame,
            text="Refresh Gradient", command=self.generate_gradient, border_spacing=10)
        regen_grad.grid(row=0, column=0)
        button_frame.grid(row=2, column=0)

        # save modified image
        save_button = customtkinter.CTkButton(
            button_frame, text="Save Image", command=self.save_image, border_spacing=10)
        save_button.grid(row=0, column=1, padx=20)

        # checkbox for same color
        if self.use_same_colors is None:
            self.use_same_colors = customtkinter.CTkCheckBox(
                self.home_frame, text="Keep Same Colors"
            )
            self.use_same_colors.grid(row=3, column=0, padx=10, pady=10)
        else:
            current_val = self.use_same_colors.get()
            self.use_same_colors = customtkinter.CTkCheckBox(
                self.home_frame, text="Keep Same Colors"
            )
            self.use_same_colors.grid(row=3, column=0, padx=10, pady=10)
            if current_val == 1:
                self.use_same_colors.select()

        # slider frame
        sl_frame = customtkinter.CTkFrame(self.home_frame)
        slider = customtkinter.CTkSlider(
            sl_frame, from_=5, to=100, command=self.slider_event,
            number_of_steps=15
        )
        self.padding = padding
        slider.set(self.padding)
        slider_label = customtkinter.CTkLabel(sl_frame, text=f"Padding : {padding}x")
        slider_label.grid(row=0, column=0)
        slider.grid(row=0, column=1, padx=10)

        sl_frame.grid(row=4, column=0)

        # scrolls gradients
        scrolls = ScrollableLabelButtonFrame(
            master=self.home_frame, width=200, height=150,
            command=self.action_taken, corner_radius=10, orientation="horizontal"
        )
        scrolls.grid(row=5, column=0, padx=100, pady=10, sticky="nsew")

        grad_images_dir = r"ui/premade_gradients"
        gradients = [grad_images_dir + "/" + i for i in os.listdir(grad_images_dir)]

        for i in range(len(gradients)):
            scrolls.add_item(
                "x", image=customtkinter.CTkImage(
                    Image.open(gradients[i]), size=(200, 100)
                )
            )

        self.deiconify()

    def select_frame_by_name(self, name):
        """
        Select frame on main window by name
        """
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()

    def home_button_event(self):
        """Select home frame"""
        self.select_frame_by_name("home")

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

    def generate_gradient(self):
        """Generate random gradient"""
        self.capture_screenshot(use_old=True, padding=self.padding)

    def slider_event(self, slide):
        """
        Slider padding
        """
        self.capture_screenshot(use_old=True, padding=int(slide))

    def save_image(self):
        """save image to selected file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png", filetypes=[("PNG", "*.png")]
        )
        if file_path:
            self.modified_image.save(file_path)

    def on_closing(self):
        """On close"""
        if messagebox.askokcancel("Quit", "Do you want to quit, have you saved the image?"):
            tempdir.cleanup()
            self.destroy()

    @staticmethod
    def action_taken(image):
        """Action after click"""
        print("action")


if __name__ == "__main__":
    app = App()
    app.after(0, lambda: app.state('zoomed'))
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
