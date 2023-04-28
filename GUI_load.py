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
        bg_label.grid(row=0, column=0, sticky='nsew')
    
        # Progress bar
        self.progress_bar = CTkProgressBar(self, mode='indeterminate', indeterminate_speed=0.7, width=250)
        self.progress_bar.grid(row=0, column=0)
        self.progress_bar.start()
        
        self.after(200, func=lambda: self.welcome('Hello Father'))
        self.after(3000, func=lambda: self.welcome('One moment while I work some magic...'))
        self.after(13000, func=lambda: self.welcome('                                                     '))
        
        
    def welcome(self, message):
        welcome_label = CTkLabel(self, fg_color=('#9cc9d3', '#111b1f'), text_color='white', font=('Comic Sans MS', 20, 'bold'), text=message)
        welcome_label.grid(row=0, column=0, pady=(750, 0))