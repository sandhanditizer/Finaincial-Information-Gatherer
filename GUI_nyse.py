from GUI_popup import Popup
from interface import summonNyseData
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkEntry, CTkProgressBar, CTkComboBox, END
from tkinter import ttk
from threading import Thread


# Go to the file `GUI_nasdaq.py` to view functionality comments.

class NYSEPage(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.data = None
        self.progress_bar = CTkProgressBar(self, mode='indeterminate', width=150)
        self.dates = summonNyseData(all_dates=True)
        self.dates.reverse()
        
        self.grid_rowconfigure(2, minsize=25)
        self.grid_columnconfigure(3, minsize=100)
        
        # Page specifier
        page_title = CTkLabel(self, text='Power Play Results', font=('', 40, 'bold'))
        page_title.grid(row=0, column=0, columnspan=5, sticky='w', pady=25, padx=10)
        
        # Reload data button
        button1 = CTkButton(self, text='Reload', command=self.reloadThread, font=('', 16))
        button1.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        
        # Redirection buttons
        button2 = CTkButton(self, text='NASDAQ', command=self.gotoNASDAQ, font=('', 16))
        button2.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
        
        button3 = CTkButton(self, text='Hedgeye', command=self.gotoHedgeye, font=('', 16))
        button3.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')
        
        # Check alerts button
        button4 = CTkButton(self, text='Alerts', command=self.checkAlerts, font=('', 16), width=80)
        button4.grid(row=0, column=4, padx=10, pady=10, sticky='e')
        
        # Date
        date_lable = CTkLabel(self, text='Date:', font=('', 17))
        date_lable.grid(row=1, column=3, padx=10, pady=10, sticky='e')
                
        

    def reloadThread(self):
        thread = Thread(target=self.master.initiateWebScrape, args=('NYSE',))
        thread.start()
                
        self.progress_bar.grid(row=0, column=2, columnspan=3)
        self.progress_bar.start()
        

    def gotoNASDAQ(self):
        self.master.geometry('740x845')
        self.master.showPage('NASDAQ')
        
        
    def gotoHedgeye(self):
        self.master.geometry('1280x845')
        self.master.showPage('Hedgeye')
        
        
    def reloadPage(self, target_date=None):
        data = summonNyseData(date=target_date)        
        self.data = data
        self.drawInteractiveWidget(data['Date'])
        self.drawTable(data)
    
    
    def checkAlerts(self):
        message = ''
        
        if self.data['10-Day Breakaway Momentum'] > 1.97:
            message += '10-Day Breakway Momentum\n(PASSED ABOVE THRESHOLD OF 1.97)\n\n'
            
        if self.data['20-Day Breakaway Momentum'] > 1.72:
            message += '20-Day Breakway Momentum\n(PASSED ABOVE THRESHOLD OF 1.72)\n\n'
            
        if self.data['5-Day Advance/Decline Thrust (%)'] < 19.05:
            message += '5-Day Advance/Decline Thrust\n(PASSED BELOW THRESHOLD OF 19.05%)\n\n'
        if self.data['5-Day Advance/Decline Thrust (%)'] > 73.66:
            message += '5-Day Advance/Decline Thrust\n(PASSED ABOVE THRESHOLD OF 73.66%)\n\n'
            
        if self.data['5-Day Up/Down Volume Thrust (%)'] < 16.41:
            message += '5-Day Up/Down Volume Thrust\n(PASSED BELOW THRESHOLD OF 16.41%)\n\n'
        if self.data['5-Day Up/Down Volume Thrust (%)'] > 77.88:
            message += '5-Day Up/Down Volume Thrust\n(PASSED ABOVE THRESHOLD OF 77.88%)\n\n'
            
        popup = Popup(self)
        if message != '':
            popup.showInfo(message)
        else:
            popup.showInfo('No new alerts')
              
    
    def dateAction(self, date):
        self.reloadPage(target_date=date)
    
    
    def drawInteractiveWidget(self, date_choice):       
        # Date in entry box        
        self.date_drop_down = CTkComboBox(self, values=self.dates, command=self.dateAction, width=140, justify='center', font=('', 14))
        if date_choice:
            self.date_drop_down.set(date_choice)
        self.date_drop_down.grid(row=1, column=4, padx=10, pady=10, sticky='w')
        
        
    def drawTable(self, data):          
        initrow = 4
        initcol = 0
        
        # Table label
        self.table_lable = CTkEntry(self, font=('', 20), justify='center', height=40)
        self.table_lable.grid(row=(initrow - 1), column=initcol, columnspan=6, sticky='ew', padx=10, pady=10)
        self.table_lable.insert(END, 'Volumetric Data') 
          
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

        # Table tree
        style = ttk.Style()
        style.configure('my.Treeview', rowheight=60, font=('', 20), background='white', foreground='black', bordercolor='black', borderwidth=1)
        style.map('my.Treeview', background=[('selected', 'grey')], foreground=[('selected', 'black')])
        
        self.table = ttk.Treeview(self, columns=('col1',), style='my.Treeview', show='tree')

        for i, label in enumerate(labels):
            d = data[label]
            if i % 2 == 0:
                self.table.insert('', 'end', text=label, values=[d], tags='even')
            elif i % 2 != 0:
                self.table.insert('', 'end', text=label, values=[d], tags='odd')
                
        self.table.tag_configure('even', background='light grey', foreground='black')
        self.table.tag_configure('odd', background='white', foreground='black')
        self.table.column('col1', anchor='e')

        self.table.grid(row=initrow, column=initcol, columnspan=6, rowspan=4, sticky='nsew', padx=10)