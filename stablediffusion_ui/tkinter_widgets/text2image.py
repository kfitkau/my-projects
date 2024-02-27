import customtkinter
import tkinter
import torch
import sys
from threading import Thread
from modules.stable_diffusion import StableDiffusion
from tkinter_widgets.text2image_display import Text2ImageDisplay
from utils.utils import load_scheduler_options_from_file

class Text2ImageFrame(customtkinter.CTkFrame):
    """A class for handling the Text2Image frame."""
    def __init__(self, framecontent, list_of_widgets: list, data: dict, local_language: str):
        """Constructor for the Text2ImageFrame class.

        Args:
            framecontent: The parent frame.
            list_of_widgets: List of widgets.
            data: Data for internationalization.
            local_language: The local language.
        """
        super().__init__(master=framecontent)
        self.language = local_language
        self.framecontent = framecontent
        self.list_of_widgets = list_of_widgets
        self.data = data
        self.setup_ui()

    def setup_ui(self):
        """Initialize UI components."""
        #MODEL MENU
        self.label_menu = customtkinter.CTkLabel(self.framecontent, text=self.data['LABEL_TEXT2IMAGE_1'])
        self.label_menu.place(x=30, y=20)
        self.modelmenu_var = customtkinter.StringVar(value="")
        self.model_menu = customtkinter.CTkOptionMenu(self.framecontent, values=['SD 1.5', 'SD 2.1', 'SDXL'], variable=self.modelmenu_var)
        self.model_menu.place(x=200, y=20) if self.language == "de" else self.model_menu.place(x=130, y=20)

        #SAMPLING METHOD
        self.label_sampling_menu = customtkinter.CTkLabel(self.framecontent, text=self.data['LABEL_SAMPLING_MENU'])
        self.label_sampling_menu.place(x=350, y=20)
        self.sampling_menu_var = customtkinter.StringVar(value="")
        scheduler_options = load_scheduler_options_from_file('./assets/lists/scheduler.txt')
        self.sampling_menu = customtkinter.CTkOptionMenu(self.framecontent, values=scheduler_options, variable=self.sampling_menu_var)
        self.sampling_menu.place(x=480, y=20) if self.language == "de" else self.sampling_menu.place(x=460, y=20)

        #SEED
        self.random_seed = torch.randint(0, 1000000, (1,)).item()
        self.label_seed = customtkinter.CTkLabel(self.framecontent, text=self.data['LABEL_SEED'])
        self.label_seed.place(x=30, y=70)
        self.label_seed_entry = customtkinter.CTkEntry(self.framecontent, height=30, placeholder_text=self.random_seed, width=160, justify="left")
        self.label_seed_entry.place(x=210, y=70)

        #SAMPLING STEPS
        self.label_sampling_steps = customtkinter.CTkLabel(self.framecontent, text=self.data['LABEL_SAMPLING_STEPS'])
        self.label_sampling_steps.place(x=390, y=70)
        self.slider_sampling_steps = customtkinter.CTkSlider(self.framecontent, from_=1, to=100, number_of_steps=99, command=self.slider_event_sampling_steps)
        self.slider_sampling_steps.set(25)
        self.label_sampling_steps_value = customtkinter.CTkLabel(self.framecontent, text="25")
        self.label_sampling_steps_value.place(x=770, y=70) if self.language == "de" else self.label_sampling_steps_value.place(x=700, y=70)
        self.slider_sampling_steps.place(x=570, y=75) if self.language == "de" else self.slider_sampling_steps.place(x=500, y=75)
            
        #CFG SCALE
        self.label_cfg_scale = customtkinter.CTkLabel(self.framecontent, text=self.data['LABEL_CFG_SCALE'])
        self.label_cfg_scale.place(x=30, y=120)
        self.slider_cfg_scale = customtkinter.CTkSlider(self.framecontent, from_=1, to=30, number_of_steps=29, command=self.slider_event_cfgscale)
        self.slider_cfg_scale.set(7)
        self.slider_cfg_scale.place(x=100, y=125)
        self.label_cfg_scale_value = customtkinter.CTkLabel(self.framecontent, text="7")
        self.label_cfg_scale_value.place(x=300, y=120)
   
        #PICTURE HEIGHT
        self.label_picture_height = customtkinter.CTkLabel(self.framecontent, text=self.data['LABEL_PICTURE_HEIGHT'])
        self.label_picture_height.place(x=30, y=170)
        self.slider_height = customtkinter.CTkSlider(self.framecontent, from_=64, to=2048, number_of_steps=2048, command=self.slider_event_height)
        self.slider_height.set(256)
        self.slider_height.place(x=120, y=175)
        self.entry_picture_height = customtkinter.CTkEntry(self.framecontent, height=30, placeholder_text="256")
        self.entry_picture_height.place(x=330, y=170)

        #PICTURE WIDTH
        self.label_picture_width = customtkinter.CTkLabel(self.framecontent, text=self.data['LABEL_PICTURE_WIDTH'])
        self.label_picture_width.place(x=30, y=210)
        self.slider_width = customtkinter.CTkSlider(self.framecontent, from_=64, to=2048, number_of_steps=2048, command=self.slider_event_width)
        self.slider_width.set(256)
        self.slider_width.place(x=120, y=215)
        self.entry_picture_width = customtkinter.CTkEntry(self.framecontent, height=30, placeholder_text="256")
        self.entry_picture_width.place(x=330, y=210)

        #ENTRY
        self.entry_positive = customtkinter.CTkEntry(self.framecontent, height=100, placeholder_text=self.data['ENTRY_POSITIVE_TEXT2IMAGE'], width=820)
        self.entry_positive.place(x=30, y=260)
        self.entry_negative = customtkinter.CTkEntry(self.framecontent, height=100, placeholder_text=self.data['ENTRY_NEGATIVE_TEXT2IMAGE'], width=820)
        self.entry_negative.place(x=30, y=380)
        self.word_count_label_positive = customtkinter.CTkLabel(self.framecontent, text="0/75", fg_color=("#F9F9FA", "#343638"))
        self.word_count_label_positive.place(x=805, y=262)
        self.word_count_label_negative = customtkinter.CTkLabel(self.framecontent, text="0/75", fg_color=("#F9F9FA", "#343638"))
        self.word_count_label_negative.place(x=805, y=382)

        #LABEL NEXT TO BUTTON
        self.status_label = customtkinter.CTkLabel(self.framecontent, text="Status:", font=("Arial", 18))
        self.status_label.place(x=30, y=510)
        self.finished_label = customtkinter.CTkLabel(self.framecontent, text="", text_color="green", font=("Arial", 18))
        #self.finished_label.place(x=90, y=510)

        #BUTTON GENERATE IMAGE
        self.btn_text2image = customtkinter.CTkButton(self.framecontent, text=self.data['BUTTON_TEXT2IMAGE'], text_color="white", height=40, width=250, command=self.generate_text2image)
        self.btn_text2image.place(x=600, y=510)

        #BINDS
        self.entry_positive.bind("<KeyRelease>", lambda entry: self.count_words(entry='positive'))
        self.entry_negative.bind("<KeyRelease>", lambda entry: self.count_words(entry='negative'))
        self.entry_picture_height.bind("<KeyRelease>", lambda entry: self.connect_entry_to_slider(entry='height'))
        self.entry_picture_width.bind("<KeyRelease>", lambda entry: self.connect_entry_width_to_slider(entry='width'))
        self.label_seed_entry.bind("<KeyRelease>", lambda entry: self.checkNumber())
        
        #ERROR
        self.error_label_height = customtkinter.CTkLabel(self.framecontent, text=self.data['ERROR_LABEL_VALUE'], text_color="red")
        self.error_label_height_64 = customtkinter.CTkLabel(self.framecontent, text=self.data['ERROR_LABEL_HEIGHT_WIDTH_64'], text_color="red")
        self.error_label_height_2048 = customtkinter.CTkLabel(self.framecontent, text=self.data['ERROR_LABEL_HEIGHT_WIDTH_2048'], text_color="red")
        self.error_label_height_DIVIDED8 = customtkinter.CTkLabel(self.framecontent, text=self.data['ERROR_LABEL_HEIGHT_WIDTH_DIVIDED8'], text_color="red")
        self.error_label_width = customtkinter.CTkLabel(self.framecontent, text=self.data['ERROR_LABEL_VALUE'], text_color="red")
        self.error_label_width_64 = customtkinter.CTkLabel(self.framecontent, text=self.data['ERROR_LABEL_HEIGHT_WIDTH_64'], text_color="red")
        self.error_label_width_2048 = customtkinter.CTkLabel(self.framecontent, text=self.data['ERROR_LABEL_HEIGHT_WIDTH_2048'], text_color="red")
        self.error_label_width_DIVIDED8 = customtkinter.CTkLabel(self.framecontent, text=self.data['ERROR_LABEL_HEIGHT_WIDTH_DIVIDED8'], text_color="red")
        self.error_label_seed = customtkinter.CTkLabel(self.framecontent, text=self.data['ERROR_LABEL_SEED'], text_color="red")
        self.error_status = customtkinter.CTkLabel(self.framecontent, text=self.data['ERROR_LABEL_STATUS'], text_color="red")

        self.second_window = None

    def count_words(self, entry: str) -> None:
        """
        Count the number of words in the positive or negative entry and update the corresponding label.

        Args:
            entry: A string specifying which entry to count ("positive" or "negative").
        """
        text = self.entry_positive.get() if entry == "positive" else self.entry_negative.get()
        word_count = len(text)
        self.word_count_label_positive.configure(text=f"{word_count}/75") if entry == "positive" \
            else self.word_count_label_negative.configure(text=f"{word_count}/75")
        
    def slider_event_sampling_steps(self, value: float) -> None:
        """
        Update the label displaying the sampling steps value based on the slider value.

        Args:
            value: The current value of the sampling steps slider.
        """
        self.label_sampling_steps_value.configure(text=int(value))
    
    def slider_event_cfgscale(self, value: float) -> None:
        """
        Update the label displaying the configuration scale value based on the slider value.

        Args:
            value: The current value of the configuration scale slider.
        """
        self.label_cfg_scale_value.configure(text=int(value))

    def slider_event_height(self, value: float) -> None:
        """
        Handle the event when the height slider is moved, updating the entry field accordingly.

        Args:
            value: The current value of the height slider.
        """
        self.error_label_height.place_forget()
        self.entry_picture_height.delete(0, tkinter.END)
        self.entry_picture_height.insert(0, int(value))

    def slider_event_width(self, value: float) -> None:
        """
        Handle the event when the width slider is moved, updating the entry field accordingly.

        Args:
            value: The current value of the width slider.
        """
        self.error_label_width.place_forget()
        self.entry_picture_width.delete(0, tkinter.END)
        self.entry_picture_width.insert(0, int(value))
    
    def connect_entry_to_slider(self, entry: str) -> None:
        """
        Connect the entry field for picture height to the corresponding slider, updating both.

        Args:
            entry: Placeholder parameter, not used in the method.
        """
        try:
            self.error_label_height_64.place_forget()
            self.error_label_height_2048.place_forget()
            self.error_label_height_DIVIDED8.place_forget()
            self.error_label_height.place_forget()
            number = int(self.entry_picture_height.get())
            if number < 64:
                self.error_label_height_64.place(x=480, y=170)
            if number > 2048:
                self.error_label_height_2048.place(x=480, y=170)
            if number % 8 != 0:
                self.error_label_height_DIVIDED8.place(x=480, y=170)
            self.slider_height.set(number)
            self.entry_picture_height.delete(0, tkinter.END)
            self.entry_picture_height.insert(0, number)
        except ValueError:
            self.error_label_height.place(x=480, y=170)

    def connect_entry_width_to_slider(self, entry: str) -> None:
        """
        Connect the entry field for picture width to the corresponding slider, updating both.

        Args:
            entry: Placeholder parameter, not used in the method.
        """
        try:
            self.error_label_width_64.place_forget()
            self.error_label_width_2048.place_forget()
            self.error_label_width_DIVIDED8.place_forget()
            self.error_label_width.place_forget()
            number = int(self.entry_picture_width.get())
            if number < 64:
                self.error_label_width_64.place(x=480, y=210)
            if number > 2048:
                self.error_label_width_2048.place(x=480, y=210)
            if number % 8 != 0:
                self.error_label_width_DIVIDED8.place(x=480, y=210)
            self.slider_width.set(number)
            self.entry_picture_width.delete(0, tkinter.END)
            self.entry_picture_width.insert(0, number)
        except ValueError:
            self.error_label_width.place(x=480, y=210)

    def checkNumber(self) -> None:
        """
        Validate and handle the input in the seed entry field.

        This method checks if the entered value is a valid integer. If it is less than 0, it resets
        the entry field to the randomly generated seed value. If a non-integer value is entered,
        it displays an error label.

        """
        try:
            self.error_label_seed.place_forget()
            number = int(self.label_seed_entry.get())
            if number < 0:
                self.label_seed_entry.delete(0, tkinter.END)
                self.label_seed_entry.insert(0, self.random_seed)
        except ValueError:
            if self.label_seed_entry.get() != "":
                if self.language == "de":
                    self.error_label_seed.place(x=390, y=70)
                else:
                    self.error_label_seed.place(x=370, y=70)
            else:
                self.label_seed_entry.delete(0, tkinter.END)
                self.label_seed_entry.insert(0, self.random_seed)

    def time_consuming_task(self) -> None:
        """
        Perform the time-consuming task of generating an image using the provided parameters.

        This method retrieves various parameters from UI components, validates them, and then uses
        these parameters to create an image using the StableDiffusion class. The resulting image is
        displayed in a new window, and a finished label is updated.

        """
        modelmenu_var = self.modelmenu_var.get(), self.label_menu.configure(text_color=("#000000", "#FFFFFF")) if self.modelmenu_var.get() else self.label_menu.configure(text_color='red')
        sampling_menu_var = self.sampling_menu_var.get(), self.label_sampling_menu.configure(text_color=("#000000", "#FFFFFF")) if self.sampling_menu_var.get() else self.label_sampling_menu.configure(text_color='red')
        seed_entry = self.label_seed_entry.get() if self.label_seed_entry.get() else self.random_seed
        slider_sampling_steps = int(self.slider_sampling_steps.get())
        slider_cfg_scale = int(self.slider_cfg_scale.get())
        entry_picture_height = int(self.entry_picture_height.get())
        entry_picture_width = int(self.entry_picture_width.get())
        entry_positive = str(self.entry_positive.get()) if self.entry_positive.get() else self.entry_positive.configure(placeholder_text_color='red')
        entry_negative = str(self.entry_negative.get())

        if not self.modelmenu_var.get() or not self.sampling_menu_var.get() or not self.entry_positive.get():
            self.error_status.configure(text=self.data['ERROR_LABEL_STATUS'])
            self.error_status.place(x=100, y=510)
            return
        
        if entry_picture_height < 64 or entry_picture_height > 2048 or entry_picture_height % 8 != 0:
            return
        
        if entry_picture_width < 64 or entry_picture_width > 2048 or entry_picture_width % 8 != 0:
            return
        
        if len(entry_positive) >= 75:
            self.error_status.configure(text=self.data['ERROR_LABEL_PROMPT'])
            self.error_status.place(x=100, y=510)
            return

        sd = StableDiffusion(modelmenu_var[0], sampling_menu_var[0], seed_entry, slider_sampling_steps, slider_cfg_scale, entry_picture_height, entry_picture_width, entry_positive, entry_negative)
        image = sd.start()
        self.finished_label.configure(text=self.data['FINISHED_LABEL'])
        self.finished_label.place(x=90, y=510)
        tk_image = customtkinter.CTkImage(image, size=(entry_picture_height, entry_picture_width))
        self.second_window = Text2ImageDisplay(self.data, tk_image, image)
        self.second_window.focus()

    def check_thread_status(self, fg_color, thread) -> None:
        """
        Check the status of the given thread and update UI elements accordingly.

        Args:
            fg_color: The foreground color to set for UI elements once the task is completed.
            thread: The thread whose status needs to be checked.

        """
        if thread.is_alive():
            # If the thread is still running, check again after 100 milliseconds
            self.after(100, lambda: self.check_thread_status(fg_color, thread))
        else:
            # Enable the button once the task is completed
            self.btn_text2image.configure(state=customtkinter.NORMAL)
            self.btn_text2image.configure(text=self.data['BUTTON_TEXT2IMAGE'])
            self.list_of_widgets[0].configure(fg_color=fg_color)
            for widget in self.list_of_widgets:
                widget.configure(state=customtkinter.NORMAL)

    def generate_text2image(self) -> None:
        """
        Initiate the process of generating a text-to-image using the parameters provided.

        This method sets up the UI for the generation process by updating button states,
        disabling widgets, and initiating a separate thread for the time-consuming task.

        """
        self.finished_label.place_forget()
        self.error_status.place_forget()
        fg_color = self.list_of_widgets[0].cget("fg_color")
        self.btn_text2image.configure(state=customtkinter.DISABLED)
        for widget in self.list_of_widgets:
            widget.configure(state=customtkinter.DISABLED)
        self.list_of_widgets[0].configure(fg_color="gray")
        self.btn_text2image.configure(text=self.data['BUTTON_TEXT2IMAGE_LOADING'], text_color_disabled="white")
        
        try:
            thread = Thread(target=self.time_consuming_task)
            thread.start()
            self.check_thread_status(fg_color, thread)
        except (KeyboardInterrupt, SystemExit):
            sys.exit()