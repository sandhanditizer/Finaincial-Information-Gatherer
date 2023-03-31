from customtkinter import CTkFrame
from tkinter import messagebox


class Popup(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
    def showWarning(self, message):
        """Displays the warning popup with whatever message you include.\n"""
        
        messagebox.showwarning("Warning", message)
        
    def showInfo(self, message):
        """Displays the information popup with whatever message you include.\n"""
        
        messagebox.showinfo("Info", message)
        
    def showError(self, message):
        """Displays the error popup with whatever message you include.\n"""
        
        messagebox.showerror("Error", message)
        
    def showQuestioning(self, message):
        """Displays `YES` or `NO` prompt with whatever message you include.\n"""
        
        return messagebox.askyesno('Change Credentialing', message)