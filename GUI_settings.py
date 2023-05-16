import customtkinter as ctk
from GUI_popup import Popup
from interface import setCredentials, getCredentials


class Settings(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry(f'+670+470')
        self.title('Settings')
        
        self.button1 = ctk.CTkButton(self, text='Change Username', command=self.changeUsername)
        self.button1.grid(row=0, column=0, padx=10, pady=(20, 10), sticky='ew')
        
        self.button2 = ctk.CTkButton(self, text='Change Password', command=self.changePassword)
        self.button2.grid(row=0, column=1, padx=10, pady=(20, 10), sticky='ew')
    
        self.button3 = ctk.CTkButton(self, text='App Info', command=self.showInfo, width=70)
        self.button3.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        
        
        
    def changeCredentials(self, username=None, password=None):
        """Write any changes that were made to config.json."""
        popup = Popup(self)  
        if username != None and password == None:
            ans = popup.showQuestioning('Are you sure you want to change your username?')
            if ans == True:
                setCredentials(username=username)
            
        elif username == None and password != None:
            ans = popup.showQuestioning('Are you sure you want to change your password?')
            if ans == True:
                setCredentials(password=password)
        else:
            popup.showInfo('No changes were made.')
    
    
    def changeUsername(self):
        current_username = getCredentials()[0]
        username_dialog = ctk.CTkInputDialog(text=f'Your current username is:\n{current_username}\nEnter a new username:', title='Change Username')
        new_username = username_dialog.get_input()
        if new_username:
            self.changeCredentials(username=new_username)
        
        
    def changePassword(self):
        current_password = getCredentials()[1]
        password_dialog = ctk.CTkInputDialog(text=f'Your current password is:\n{current_password}\nEnter a new password:', title='Change Password')
        new_password = password_dialog.get_input()
        if new_password:
            self.changeCredentials(password=new_password)
        
        
    def showInfo(self):
        self.button1.destroy()
        self.button2.destroy()
        self.button3.destroy()
        
        self.title('App Information')
        self.geometry('700x400')
        self.geometry(f'+470+370')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        textbox = ctk.CTkTextbox(self, wrap='word')
        textbox.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        
        with open('app_info.txt', 'r') as file:
            message = file.read()
        textbox.insert('0.0', message)
        textbox.configure(state='disabled')