"""
Scroll action
"""
import customtkinter


class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
    """Scroll class"""

    def __init__(self, master, command=None, **kwargs):
        customtkinter.ThemeManager.theme["CTkScrollableFrame"] = {'label_fg_color': ['#242424', "#242424"]}
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=0)

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.label_list = []
        self.button_list = []
        self.grad_count = 0
        self._grad_row = 0
        self._grad_column = -1

    def add_item(self, item, image=None):
        """Add items to scroll"""
        if image is not None:
            self.grad_count += 1
            self._grad_column += 1
        if self.grad_count > 10:
            self._grad_row += 1
            self._grad_column = 0
            self.grad_count = 0

        button = customtkinter.CTkButton(
            self, text="", width=40, height=40, image=image, border_spacing=0, border_width=0,
            fg_color="#242424"
        )
        if self.command is not None:
            button.configure(command=lambda: self.command(item))
        button.grid(row=self._grad_row, column=self._grad_column, padx=5, pady=5)
        self.button_list.append(button)
