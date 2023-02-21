"""
Scroll action
"""
import customtkinter
import os
from PIL import Image


class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
    """Scroll class"""

    def __init__(self, master, command=None, **kwargs):
        customtkinter.ThemeManager.theme["CTkScrollableFrame"] = {'label_fg_color': ['gray78', 'gray23']}
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=0)

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.label_list = []
        self.button_list = []

    def add_item(self, item, image=None):
        """Add items to scroll"""
        label = customtkinter.CTkLabel(self, text="", image=image)
        button = customtkinter.CTkButton(self, text="Select Gradient", width=100, height=24)
        if self.command is not None:
            button.configure(command=lambda: self.command(item))
        label.grid(row=0, column=len(self.label_list), padx=20)
        button.grid(row=1, column=len(self.button_list), padx=20, pady=10)
        self.label_list.append(label)
        self.button_list.append(button)

    @staticmethod
    def action_taken(image):
        """Action after click"""
        print("action")
