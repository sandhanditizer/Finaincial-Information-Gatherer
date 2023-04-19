# from tkinter import PhotoImage, Label
# from customtkinter import CTkFrame, CTkProgressBar

# class LoadingPage(CTkFrame):
#     def __init__(self, parent):
#         super().__init__(parent)
        
#         # For correctly sizing the loading screen
#         self.grid_rowconfigure(0, weight=1)
#         self.grid_columnconfigure(0, weight=1)
        
#         # Background image label for light and dark versions
#         if self._get_appearance_mode() == 'light':
#             self.image = PhotoImage(file='LSImages/lightbackground.png')
#         else:
#             self.image = PhotoImage(file='LSImages/darkbackground.png')
            
#         bg_label = Label(self, image=self.image, text='')
#         bg_label.grid(row=0, column=0, sticky="nsew")      
    
#         # Progress bar
#         self.progress_bar = CTkProgressBar(self, mode='indeterminate')
#         self.progress_bar.grid(row=0, column=0)
#         self.progress_bar.start()

from PIL import Image
from customtkinter import CTkFrame, CTkProgressBar, CTkImage, CTkLabel

class LoadingPage(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # For correctly sizing the loading screen
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
            
        light_image = Image.open('LoadingImages/lightbackground.png')
        dark_image = Image.open('LoadingImages/darkbackground.png')
        CTk_image = CTkImage(light_image=light_image, dark_image=dark_image, size=(1390, 930))
        bg_label = CTkLabel(self, image=CTk_image, text='')
        bg_label.grid(row=0, column=0, sticky="nsew")      
    
        # Progress bar
        self.progress_bar = CTkProgressBar(self, mode='indeterminate')
        self.progress_bar.grid(row=0, column=0)
        self.progress_bar.start()