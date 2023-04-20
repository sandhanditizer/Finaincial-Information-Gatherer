from customtkinter import CTkFrame, CTkToplevel, CTkButton, CTkLabel, CTkEntry
from interface import getCredentials, setCredentials
from GUI_popup import Popup


class Settings(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.top_level = CTkToplevel(parent)
        self.top_level.title('Credential Settings')
        self.top_level.geometry(f'+670+400') # Shift
                
        self.top_level.grid_rowconfigure(0, minsize=10)
        
        current_username, current_password = getCredentials()
        self.new_username = ''
        self.new_password = ''
        
        # Shows current username
        username_label1 = CTkLabel(self.top_level, text=f'Current username: ', font=('', 16, 'bold'), text_color=('black', 'white'))
        username_label1.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        
        username_label2 = CTkLabel(self.top_level, text=current_username, font=('', 16), text_color=('black', 'white'))
        username_label2.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky='w')
        
        username_label3 = CTkLabel(self.top_level, text=f'Edit username: ', font=('', 16, 'bold'), text_color=('black', 'white'))
        username_label3.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='w')
        
        # Entry box that allows to change username
        self.entry1 = CTkEntry(self.top_level, placeholder_text=f'Type here', justify='center', font=('', 14), width=250, fg_color='gray50')
        self.entry1.bind('<KeyRelease>', self.changeUsername)
        self.entry1.grid(row=2, column=1, columnspan=2,  padx=10, pady=10, sticky='nsew')
        
        # Shows current password
        password_label1 = CTkLabel(self.top_level, text=f'Current password: ', font=('', 16, 'bold'), text_color=('black', 'white'))
        password_label1.grid(row=3, column=0, padx=10, pady=10, sticky='w')
        
        password_label2 = CTkLabel(self.top_level, text=current_password, font=('', 16,), text_color=('black', 'white'))
        password_label2.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky='w')
        
        password_label3 = CTkLabel(self.top_level, text=f'Edit password: ', font=('', 16, 'bold'), text_color=('black', 'white'))
        password_label3.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky='w')
        
        # Entry box that allows to change password
        self.entry2 = CTkEntry(self.top_level, placeholder_text=f'Type here', justify='center', font=('', 14), width=250, fg_color='gray50')
        self.entry2.bind('<KeyRelease>', self.changePassword)
        self.entry2.grid(row=4, column=1, columnspan=2, padx=10, pady=10, sticky='nsew')
        
        # Button that forces the changes
        button1 = CTkButton(self.top_level, text='Make Change(s)', command=self.makeChange, font=('', 16), width=100)
        button1.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

    
    def changeUsername(self, _):
        """Gets what the user is typing into the box and save it the class global.\n"""
        
        self.new_username = self.entry1.get()
        
        
    def changePassword(self, _):
        """Gets what the user is typing into the box and save it the class global.\n"""

        self.new_password = self.entry2.get()

    
    def makeChange(self):
        """Write any changes that were made to config.json.\n"""
        
        popup = Popup(self)
        if self.new_username != '' and self.new_password != '':
            ans = popup.showQuestioning('Are you sure you want to change your username and password?')
            if ans == True:
                setCredentials(self.new_username, self.new_password)
                self.top_level.destroy()
            
        elif self.new_username != '' and self.new_password == '':
            ans = popup.showQuestioning('Are you sure you want to change your username?')
            if ans == True:
                setCredentials(self.new_username)
                self.top_level.destroy()
            
        elif self.new_username == '' and self.new_password != '':
            ans = popup.showQuestioning('Are you sure you want to change your password?')
            if ans == True:
                setCredentials(self.new_password)
                self.top_level.destroy()
                
        else:
            popup.showInfo('No changes were made! To make a credential change, edit the text box, then press `Make Change(s)`.')