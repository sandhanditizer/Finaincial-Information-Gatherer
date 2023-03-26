from GUI_popup import Popup
from interface import summonHedgeyeData
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkEntry, CTkComboBox, END
from tkinter import ttk
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from threading import Thread
import matplotlib.pyplot as plt


class HedgeyePage(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Class globals
        self.data = None
        self.tickers = []
        
        # Manual configures to get spacing right
        self.grid_rowconfigure(2, minsize=25)
        self.grid_columnconfigure(7, minsize=350)
        
        # Page specifier
        pageTitle = CTkLabel(self, text="Hedgeye's Daily Data", font=('', 40))
        pageTitle.grid(row=0, column=0, columnspan=5, sticky='w', pady=25, padx=10)
        
        # Reload data button
        button1 = CTkButton(self, text='Reload', command=self.reloadThread, font=('', 16))
        button1.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        
        # Redirection buttons
        button2 = CTkButton(self, text='NASDAQ', command=self.gotoNASDAQ, font=('', 16))
        button2.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')
        
        button3 = CTkButton(self, text='NYSE', command=self.gotoNYSE, font=('', 16))
        button3.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
        
        # Date
        dateLable = CTkLabel(self, text='Date:', font=('', 17))
        dateLable.grid(row=1, column=3, padx=10, pady=10, sticky='e')
        
        # Ticker
        tickerLable = CTkLabel(self, text='Ticker:', font=('', 17))
        tickerLable.grid(row=1, column=5, padx=10, pady=10, sticky='e')
                
            

    def reloadThread(self):
        """Attemps to get new data from websites and store it in database.\n"""
        
        thread = Thread(target=self.master.initiateWebScrape, args=('Hedgeye',))
        thread.start()


    def gotoNASDAQ(self):
        """Changes page to the NASDAQ Power Play Results page.\n"""
        
        self.master.geometry('740x845')
        self.master.showPage('NASDAQ')
        

    def gotoNYSE(self):
        """Changes page to the NYSE Power Play Results page.\n"""
        
        self.master.geometry('740x845')
        self.master.showPage('NYSE')
        
        
    def reloadPage(self, date=None):
        """
        Gets specified data or most recent data from database.\n
        Args:\n
            date (string, optional): 'yyyy-mm-dd'. Defaults to None.\n
        """
        
        data = summonHedgeyeData(date=date)
        
        if data == []:
            Popup(self).showWarning(f'No data exists for {date}.')
            return
        
        self.data = data
        self.tickers = [d['Ticker'] for d in self.data[0:-1]] # Exclude the 10s/2s data
        
        # Display the first bout of data in the list
        self.drawInteractiveWidgets(self.data[0]['Date'], self.tickers, self.data[0]['Description'])
        self.drawTable(self.data[0])
        self.drawGraph(self.data[0]['Ticker'])

        
    def drawInteractiveWidgets(self, date, tickers, description, choice=None):
        """
        Updates the page when the user creates an event while using the page.\n
        Args:\n
            date (string): 'yyyy-mm-dd'.\n
            tickers (string): 'ABC...Z'.\n
            description (string): Description of ticker.\n
            choice (string, optional): Ticker selection. Defaults to None. Refer to the `tickerAction` function.\n
        """
        # Date in entry box
        self.dateEntry = CTkEntry(self, placeholder_text=f'{date}')
        self.dateEntry.bind('<Return>', self.dateAction)
        self.dateEntry.grid(row=1, column=4, pady=10, sticky='w')
        
        # Ticker in dropdown box
        self.tickerDropDown = CTkComboBox(self, values=tickers, command=self.tickerAction, width=100)
        if choice:
            self.tickerDropDown.set(choice)
        self.tickerDropDown.grid(row=1, column=6, pady=10, sticky='w')
        
        # Description to the right of ticker dropdown
        self.descriptionLable = CTkLabel(self, text=description, font=('', 16))
        self.descriptionLable.grid(row=1, column=7, columnspan=2, pady=10, sticky='ew')
        
        
    def findDictByTick(self, dlist, ticker):
        """Finds the specified ticker data in the list of dictionaries.\n"""
        
        for dict_item in dlist:
            if dict_item['Ticker'] == ticker:
                return dict_item
            
        return None # Not found
        
        
    def tickerAction(self, ticker):
        """
        Changes the page accordingly when choosing a different ticker to look at.\n
        Takes in an event from the ComboBox.\n
        """
        
        target_dict = self.findDictByTick(self.data, ticker)
        self.drawInteractiveWidgets(target_dict['Date'], self.tickers, target_dict['Description'], ticker)
        self.drawTable(target_dict)
        self.drawGraph(ticker=target_dict['Ticker'])
        
        
    def dateAction(self, _):
        """Changes the page accordingly when choosing a different date to look at.\n"""
        
        date = self.dateEntry.get()
        
        try:
            datetime.strptime(date, '%Y-%m-%d')
            self.reloadPage(date=date)
        except ValueError:
            Popup(self).showInfo('Date needs to be in the format: yyyy-mm-dd.')    
            
            
    def drawTable(self, data):    
        """
        Updates table with data passed in.\n
        Args:\n
            data (dict): Data to draw table.\n
        """
           
        # Top left of the table is where to specify location
        initrow = 4
        initcol = 6
        
        # Table label
        self.tableLable = CTkEntry(self, font=('', 20), justify='center', height=40)
        self.tableLable.grid(row=(initrow - 1), column=initcol, columnspan=2, sticky='ew', pady=10)
        self.tableLable.insert(END, 'Range and Performance Data') 
          
        labels = ['Buy', 'Sell', 'Close', 'Range Asym - Buy (%)', 'Range Asym - Sell (%)', 'W/W Delta', 
                  '1-Day Delta (%)', '1-Week Delta (%)', '1-Month Delta (%)', '3-Month Delta (%)',
                  '6-Month Delta (%)', '1-Year Delta (%)']

        # Table tree
        style = ttk.Style()
        style.configure('my.Treeview', rowheight=60, font=('', 20), background='white', foreground='black', bordercolor='black', borderwidth=1)
        style.map('my.Treeview', background=[('selected', 'grey')], foreground=[('selected', 'black')])
        self.table = ttk.Treeview(self, columns=('col1',), style='my.Treeview', show='tree')

        # Stationary data, only changes when date changes
        self.table.insert('', 'end', text='10s/2s Spread (bps)', values=(self.data[-1]['10s/2s Spread (bps)']), tags='tt')
        
        # Changes when ticker and date are changed
        for i, label in enumerate(labels):
            d = data[label]
            if i % 2 == 0:
                self.table.insert('', 'end', text=label, values=[d], tags='even')
            elif i % 2 != 0:
                self.table.insert('', 'end', text=label, values=[d], tags='odd')
                  
        # Coloring the rows differently so the table is better contrasted
        self.table.tag_configure('even', background='light grey', foreground='black')
        self.table.tag_configure('odd', background='white', foreground='black')
        self.table.tag_configure('tt', background='light blue', foreground='black')
        self.table.column('col1', anchor='e')

        self.table.grid(row=initrow, column=initcol, columnspan=2, rowspan=10, sticky='nsew')


    def drawGraph(self, ticker):
        """
        Updates the graph given a specified ticker.\n
        Args:\n
            ticker (string): 'ABC...Z'.\n
        """
        
        # Top left of the table is where to specify location
        initrow = 4
        initcol = 0
        
        # Graph label
        self.graphLable = CTkEntry(self, font=('', 20), justify='center', height=40)
        self.graphLable.grid(row=(initrow - 1), column=initcol, columnspan=6, sticky='ew', padx=10)
        self.graphLable.insert(END, 'Trade Price')    
        
        data = summonHedgeyeData(ticker=ticker)

        fig = plt.Figure(figsize=(8, 6))
        ax = fig.add_subplot(111)

        dates = [d['Date'] for d in data[0:-1]] # Exclude 10s/2s data
        y1 = [d['Buy'] for d in data[0:-1]]
        y2 = [d['Sell'] for d in data[0:-1]]
        y3 = [d['Close'] for d in data[0:-1]]
        
        
        # ------------------------------------------------------------------------------------------------
        # Chops trend lines to show where data tracking has stopped for 7 days or longer
        
        index_ends = []
        index_starts = []

        for i in range(1, len(dates)):
            diff = (datetime.strptime(dates[i], '%Y-%m-%d') - datetime.strptime(dates[i - 1], '%Y-%m-%d')).days
            if diff >= 7:
                index_ends.append(i - 1)
                index_starts.append(i)

        
        if len(index_ends) == 0:
            ax.plot(dates, y1, color='green', label='Buy')
            ax.plot(dates, y2, color='red', label='Sell')
            ax.plot(dates, y3, color='black', label='Close', linestyle='--')
            
        else:
            ax.plot(dates[0:index_ends[0]], y1[0:index_ends[0]], color='green', label='Buy')
            ax.plot(dates[0:index_ends[0]], y2[0:index_ends[0]], color='red', label='Sell')
            ax.plot(dates[0:index_ends[0]], y3[0:index_ends[0]], color='black', label='Close', linestyle='--')
        
            for i in range(1, len(index_ends)):
                ax.plot(dates[index_starts[i-1]:index_ends[i]], y1[index_starts[i-1]:index_ends[i]], color='green')
                ax.plot(dates[index_starts[i-1]:index_ends[i]], y2[index_starts[i-1]:index_ends[i]], color='red', label='Sell')
                ax.plot(dates[index_starts[i-1]:index_ends[i]], y3[index_starts[i-1]:index_ends[i]], color='black', label='Close', linestyle='--')
                
            ax.plot(dates[index_starts[-1]:-1], y1[index_starts[-1]:-1], color='green')
            ax.plot(dates[index_starts[-1]:-1], y2[index_starts[-1]:-1], color='red')
            ax.plot(dates[index_starts[-1]:-1], y3[index_starts[-1]:-1], color='black', linestyle='--')
        
        # ------------------------------------------------------------------------------------------------

        
        # Set x-ticks to every other date
        xticks = [dates[i] for i in range(0, len(dates), 2)]
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticks)

        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.legend()
        ax.grid(linestyle=':')

        # Rotate the dates on the x-axis
        fig.autofmt_xdate(rotation=55)

        self.fcan = FigureCanvasTkAgg(figure=fig, master=self)
        self.fcan.draw()
        self.fcan.get_tk_widget().grid(row=initrow, column=initcol, columnspan=6, rowspan=12, sticky='nsew', padx=10)