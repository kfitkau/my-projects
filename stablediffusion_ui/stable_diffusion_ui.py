import tkinter
import tkinter.messagebox
import customtkinter
import threading
import logging
import sys
import json
import ctypes
import locale

from tkinter_widgets.text2image import Text2ImageFrame
from utils.utils import get_translations

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"
    
#READ USER UI/OS LANGUAGE
windll = ctypes.windll.kernel32
locale_lang = locale.windows_locale[windll.GetUserDefaultUILanguage()]
if locale_lang[:2] == "de":
    data = get_translations("de")
    list_of_languages = ["DE", "EN"]
else:
    data = get_translations("en")
    list_of_languages = ["EN", "DE"]

#GLOBAL VARIABLES
MAXWIDTH = 1200
MINHEIGHT = 580
MAINWINDOW_TITLE = data['PROGRAMTITLE']

class App(customtkinter.CTk):
    """A class for handling the Main frame."""
    def __init__(self):
        """
        Constructor of the main window.

        """
        super().__init__()

        # configure window
        self.title(MAINWINDOW_TITLE)
        self.geometry(f"{MAXWIDTH}x{MINHEIGHT}")
        self.resizable(False,False)

        self.frame_sidebar = customtkinter.CTkFrame(self)
        self.frame_content = customtkinter.CTkFrame(self)

        # Place frames in the grid
        self.frame_sidebar.grid(row=0, column=0, rowspan=1, sticky="nsew")
        self.frame_content.grid(row=0, column=1, rowspan=2, sticky="nsew")

        # Configure row and column weights so that they expand proportionally
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.frame_sidebar, text=MAINWINDOW_TITLE, font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(padx=20, pady=(20, 10), anchor="nw")
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.frame_sidebar, text_color="white", values=["System", "Light Mode", "Dark Mode"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.pack(side="bottom", padx=20, pady=(0, 20), anchor="sw")
        self.appearance_mode_label = customtkinter.CTkLabel(self.frame_sidebar, text=data['LABEL_APPEARANCE_MODE'])
        self.appearance_mode_label.pack(side="bottom", padx=20, pady=(10, 0), anchor="sw")
        self.language_menu = customtkinter.CTkOptionMenu(self.frame_sidebar, text_color="white", values=list_of_languages, command=self.change_translation)
        self.language_menu.pack(side="bottom", padx=20, anchor="sw")
        self.language_menu_label = customtkinter.CTkLabel(self.frame_sidebar, text=data['LABEL_LANGUAGE_MENU'])
        self.language_menu_label.pack(side="bottom", padx=20, anchor="sw")

        self.list_of_widgets = [self.appearance_mode_optionemenu, self.language_menu]
        #Main Content 1
        self.text2image_frame = Text2ImageFrame(self.frame_content, self.list_of_widgets, data, locale_lang[:2])
        

    def change_appearance_mode_event(self, new_appearance_mode: str) -> None:
        """
        Change the appearance mode of the application.

        This method sets the appearance mode based on the selected option:
        - "System": Follow the system's appearance mode.
        - "Light Mode": Set the appearance mode to light.
        - "Dark Mode": Set the appearance mode to dark.

        Args:
            new_appearance_mode: The selected appearance mode.

        """
        try:        
            # select Appearance Mode
            if new_appearance_mode == "System":
                customtkinter.set_appearance_mode("system")
            elif new_appearance_mode == "Light Mode":
                customtkinter.set_appearance_mode("light")
            elif new_appearance_mode == "Dark Mode":
                customtkinter.set_appearance_mode("dark")
        except ValueError as e:
            # Log the error
            print(f"Error: {e}")

    #TODO: Change translation behavior
    def change_translation(self, language: str) -> None:
        """
        Change the translation of UI elements based on the selected language.

        This method updates various UI components, including labels, buttons, and error messages,
        with translations retrieved from the `get_translations` function.

        Args:
            language: The selected language code.

        """
        try:
            data = get_translations(language)
            #Sidebar
            self.title(data['PROGRAMTITLE'])
            self.logo_label.configure(text=data['PROGRAMTITLE'])
            self.appearance_mode_label.configure(text=data['LABEL_APPEARANCE_MODE'])
            self.language_menu_label.configure(text=data['LABEL_LANGUAGE_MENU'])
            #FRAME TEXT2IMAGE
            self.text2image_frame.label_menu.configure(text=data['LABEL_TEXT2IMAGE_1'])
            self.text2image_frame.label_sampling_menu.configure(text=data['LABEL_SAMPLING_MENU'])
            self.text2image_frame.label_seed.configure(text=data['LABEL_SEED'])
            self.text2image_frame.label_sampling_steps.configure(text=data['LABEL_SAMPLING_STEPS'])
            self.text2image_frame.label_cfg_scale.configure(text=data['LABEL_CFG_SCALE'])
            self.text2image_frame.label_picture_height.configure(text=data['LABEL_PICTURE_HEIGHT'])
            self.text2image_frame.label_picture_width.configure(text=data['LABEL_PICTURE_WIDTH'])
            self.text2image_frame.btn_text2image.configure(text=data['BUTTON_TEXT2IMAGE'])
            self.text2image_frame.entry_positive.configure(placeholder_text=data['ENTRY_POSITIVE_TEXT2IMAGE'])
            self.text2image_frame.entry_negative.configure(placeholder_text=data['ENTRY_NEGATIVE_TEXT2IMAGE'])
            self.text2image_frame.error_label_seed.configure(text=data['ERROR_LABEL_SEED'])
            
            self.text2image_frame.error_label_height.configure(text=data['ERROR_LABEL_VALUE'])
            self.text2image_frame.error_label_height_64.configure(text=data['ERROR_LABEL_HEIGHT_WIDTH_64'])
            self.text2image_frame.error_label_height_2048.configure(text=data['ERROR_LABEL_HEIGHT_WIDTH_2048'])
            self.text2image_frame.error_label_height_DIVIDED8.configure(text=data['ERROR_LABEL_HEIGHT_WIDTH_DIVIDED8'])
            self.text2image_frame.error_label_width.configure(text=data['ERROR_LABEL_VALUE'])
            self.text2image_frame.error_label_width_64.configure(text=data['ERROR_LABEL_HEIGHT_WIDTH_64'])
            self.text2image_frame.error_label_width_2048.configure(text=data['ERROR_LABEL_HEIGHT_WIDTH_2048'])
            self.text2image_frame.error_label_width_DIVIDED8.configure(text=data['ERROR_LABEL_HEIGHT_WIDTH_DIVIDED8'])
            if self.text2image_frame.second_window is not None:
                self.text2image_frame.finished_label.configure(text=data['FINISHED_LABEL'])
                self.text2image_frame.second_window.button.configure(text=data['SAVE_PICTURE'])
                self.text2image_frame.second_window.close_button.configure(text=data['CLOSE_BUTTON'])
            #FRAME TEXT2IMAGE - PLACE
            self.text2image_frame.model_menu.place_forget()
            if language.lower() == "de":
                self.text2image_frame.model_menu.place(x=200, y=20)
                self.text2image_frame.sampling_menu.place(x=480, y=20)
                self.text2image_frame.label_sampling_steps_value.place(x=770, y=70)
                self.text2image_frame.slider_sampling_steps.place(x=570, y=75)
            else:
                self.text2image_frame.model_menu.place(x=130, y=20)
                self.text2image_frame.sampling_menu.place(x=460, y=20)
                self.text2image_frame.label_sampling_steps_value.place(x=700, y=70)
                self.text2image_frame.slider_sampling_steps.place(x=500, y=75)
        except ValueError as e:
            print(f"Error: {e}")