import customtkinter
from tkinter import filedialog
from PIL import Image, ImageTk

class Text2ImageDisplay(customtkinter.CTkToplevel):
    def __init__(self, data: dict, tk_image: ImageTk.PhotoImage, image: Image.Image, *args, **kwargs):
        """
        Constructor for the Text2ImageDisplay class.

        Args:
            data (dict): Dictionary containing program-related data.
            tk_image: Tkinter image to be displayed.
            image: Pillow image to be saved.
            *args, **kwargs: Additional arguments and keyword arguments for the parent class.
        """
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.title(data['PROGRAMTITLE'] + " - Text2Image")
        self.__label = customtkinter.CTkLabel(self, text="", image=tk_image)
        self.button = customtkinter.CTkButton(self, text=data['SAVE_PICTURE'], command=self.save_image, sticky="nsew")
        self.close_button = customtkinter.CTkButton(self, text=data['CLOSE_BUTTON'], command=self.close_window, sticky="nsew")
        self.__label.grid(row=0, column=0, columnspan=2, pady=(10, 0), sticky="nsew")
        self.button.grid(row=1, column=0, padx=(10, 5), pady=10)
        self.close_button.grid(row=1, column=1, padx=(5, 10), pady=10)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.__image = image

    def save_image(self) -> None:
        """
        Method to save the displayed Pillow image to a user-selected file.

        Returns:
            None
        """
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            self.__image.save(file_path)
            self.destroy()

    def close_window(self) -> None:
        """
        Method to close the window.

        Returns:
            None
        """
        self.destroy()