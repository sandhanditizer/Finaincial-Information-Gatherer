from GUI_popup import Popup
from interface import summonNasdaqData
import customtkinter as ctk
from tkinter import ttk
from threading import Thread


# The file `GUI_nyse.py` is identical to this file. Comments on functionality will be located here.

class NASDAQPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Class global
        self.data = None
        self.progress_bar = ctk.CTkProgressBar(self, mode='indeterminate', indeterminate_speed=0.5)
        self.dates = summonNasdaqData(all_dates=True)
        self.dates.reverse()
        
        # Page specifier
        page_title = ctk.CTkLabel(self, text='Power Play Results', font=(None, 40, 'bold'))
        page_title.grid(row=0, column=0, columnspan=3, padx=10, pady=20,  sticky='w')
        
        # Reload data button
        button1 = ctk.CTkButton(self, text='Reload Data', command=self.reloadThread)
        button1.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        
        # Redirection buttons
        button2 = ctk.CTkButton(self, text='Goto NYSE', command=lambda: self.master.showPage('NYSE'))
        button2.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
        
        button3 = ctk.CTkButton(self, text='Goto Hedgeye', command=lambda: self.master.showPage('Hedgeye'))
        button3.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')
                
        

    def reloadThread(self):
        """
        Requests backend to fetch new data if the database is not updated with todays data.
        It will then display the page that the user was on. 
        Progress bar is started and will disappear when reload is finished. 
        """
        thread = Thread(target=self.master.initiateWebScrape, args=('NASDAQ',))
        thread.start()
        
        self.progress_bar.grid(row=2, column=0, columnspan=4, sticky='ew', padx=10)
        self.progress_bar.start()
        
        
    def checkAlerts(self, show_alert):
        """
        Displays an alert if any or all values for the 10-Day Breakaway Momentum, 20-Day Breakaway Momentum, 
        5-Day Advance/Decline Thrust (%), and/or 5-Day Up/Down Volume Thrust (%) go below or above a set threshold.\n
        Args:\n
            silent: If true, the function will check alerts without notifying user.
        """
        message = ''
        
        if self.data['10-Day Breakaway Momentum']:
            if self.data['10-Day Breakaway Momentum'] > 1.97:
                message += '10-Day Breakway Momentum passed above set threshold of 1.97\n\n'
        
        if self.data['20-Day Breakaway Momentum']:
            if self.data['20-Day Breakaway Momentum'] > 1.72:
                message += '20-Day Breakway Momentum passed above set threshold of 1.72\n\n'
            
        if self.data['5-Day Advance/Decline Thrust (%)']:
            if self.data['5-Day Advance/Decline Thrust (%)'] < 19.05:
                message += '5-Day Advance/Decline Thrust passed below set threshold of 19.05%\n\n'
                
        if self.data['5-Day Advance/Decline Thrust (%)']:
            if self.data['5-Day Advance/Decline Thrust (%)'] > 73.66:
                message += '5-Day Advance/Decline Thrust passed above set threshold of 73.66%\n\n'
            
        if self.data['5-Day Up/Down Volume Thrust (%)']:
            if self.data['5-Day Up/Down Volume Thrust (%)'] < 16.41:
                message += '5-Day Up/Down Volume Thrust passed below set threshold of 16.41%\n\n'
                
        if self.data['5-Day Up/Down Volume Thrust (%)']:
            if self.data['5-Day Up/Down Volume Thrust (%)'] > 77.88:
                message += '5-Day Up/Down Volume Thrust passed above set threshold of 77.88%\n\n'
                
        if show_alert:
            Popup(self).showInfo(message)
            
        if message != '':
            button4 = ctk.CTkButton(self, text='New Alerts', command=lambda: self.checkAlerts(show_alert=True), border_color='#D6544B', border_width=3, width=90)
        else:
            button4 = ctk.CTkButton(self, text='No Alerts', state='disabled', width=80)
            
        button4.grid(row=0, column=3, padx=10, pady=10, sticky='e')
        
        
    def reloadPage(self, target_date=None):
        """
        Refreshes the current page with updated information. It will save where you are
        on the page (what day and what ticker you are on).\n
        Args:\n
            target_date (str, optional): If not None, will refresh the page to display the tickers for that date. Defaults to None.
        """
        data = summonNasdaqData(date=target_date)
        self.data = data
        self.drawInteractiveWidget(data['Date'])
        self.drawTable(data)
        
        # This saves where you are on the page so the user doesnt lose where they are if the navigate to other pages
        self.master.pages['NASDAQ'][1] = data['Date']
        
        # Will silently check threshold alerts, if there are any it will color the border of the alert button red
        self.checkAlerts(show_alert=False)
        
              
    
    def dateAction(self, date):
        """
        If the user interacts with the date drop down, this function is called to manipulate the displayed page.\n
        Args:\n
            date (str): Date that was clicked on by user.
        """
        self.reloadPage(target_date=date)
    
    
    def drawInteractiveWidget(self, date_choice):
        """
        Draws the correct information on the display when the user interacts with it.\n
        Args:\n
            date_choice (str, optional): Date that was clicked on by user. Defaults to None.
        """
        # Date dropdown box     
        date_drop_down = ctk.CTkOptionMenu(self, values=self.dates, command=self.dateAction, anchor='center')
        if date_choice:
            date_drop_down.set(date_choice)
        date_drop_down.grid(row=1, column=3, padx=10, pady=10, sticky='w')
        
        
    def drawTable(self, data):
        """
        Updates shown table with data that is passed in.\n
        Args:\n
            data (dict): Data that is displayed on the table.
        """
        # Top left corner positions the label and table without adjusting it individually
        initrow = 4
        initcol = 0
        
        # Table label
        self.table_lable = ctk.CTkEntry(self, justify='center', height=40, font=(None, 20))
        self.table_lable.grid(row=(initrow - 1), column=initcol, columnspan=4, padx=10, pady=10, sticky='ew')
        self.table_lable.insert(ctk.END, 'Volumetric Data') 
          
        labels = ['Close (%)', 
            'Advancing Volume', 'Declining Volume', 
            'Total Volume', 'Volume Delta (%)',
            'Upside Day (%)', 'Downside Day (%)',
            'Advances', 'Declines', 'Net (Advances/Declines)',
            '10-Day Breakaway Momentum', '20-Day Breakaway Momentum',
            'Advance/Decline Ratio', 'Advance/Decline Thrust (%)',
            '5-Day Advance/Decline Thrust (%)', '5-Day Up/Down Volume Thrust (%)', 
            'New Highs', 'New Lows', 'Net (Highs/Lows)',
            '21-Day Average (Highs/Lows)', '63-Day Average (Highs/Lows)']

        # Setting style based on color mode
        style = ttk.Style()
        if self._get_appearance_mode() == 'dark':
            background_color = '#131e23'
            row_color = '#373737'
            row_color2 = '#4B4B4B'
            text_color = 'white'
            highlight_color = '#476D7C'
            style.configure('my.Treeview', rowheight=53, font=(None, 15), fieldbackground=background_color)
        else:
            background_color = '#E5E5E5'
            row_color = '#F7F7F7'
            row_color2 = '#D3D3D3'
            text_color = 'black'
            highlight_color = '#476D7C'
            style.configure('my.Treeview', rowheight=53, font=(None, 15), fieldbackground=background_color)
        
        style.map('my.Treeview', background=[('selected', highlight_color)], foreground=[('selected', 'white')])
        
        # Table tree
        self.table = ttk.Treeview(self, columns=('col1',), style='my.Treeview', show='tree')

        # Changes when date are changed
        for i, label in enumerate(labels):
            d = data[label]
            if i % 2 == 0:
                self.table.insert('', 'end', text=label, values=[d], tags='even')
            elif i % 2 != 0:
                self.table.insert('', 'end', text=label, values=[d], tags='odd')
                
        # Coloring the rows differently so the table is better contrasted
        self.table.tag_configure('even', background=row_color, foreground=text_color)
        self.table.tag_configure('odd', background=row_color2, foreground=text_color)
        self.table.column('col1', anchor='e')

        self.table.grid(row=initrow, column=initcol, columnspan=4, rowspan=4, padx=10, sticky='nsew')