from GUI_settings import Settings
from interface import summonHedgeyeData
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkEntry, CTkComboBox, CTkProgressBar, END
from tkinter import ttk
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.dates as mdates
from threading import Thread
import matplotlib.pyplot as plt


class HedgeyePage(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Class globals
        self.data = None
        self.tickers = []
        self.progress_bar = CTkProgressBar(self, mode='indeterminate', width=200)
        
        # For the date selector
        self.dates = summonHedgeyeData(all_dates=True)
        self.dates.reverse() 
        
        # Manual configures to get spacing right
        self.grid_rowconfigure(2, minsize=25)
        self.grid_columnconfigure(7, minsize=350)
        
        # Page specifier
        page_title = CTkLabel(self, text="Daily Data", font=('', 40, 'bold'))
        page_title.grid(row=0, column=0, columnspan=2, sticky='w', pady=25, padx=10)
        
        # Reload data button
        button1 = CTkButton(self, text='Reload', command=self.reloadThread, font=('', 16))
        button1.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        
        # Redirection buttons
        button2 = CTkButton(self, text='NASDAQ', command=self.gotoNASDAQ, font=('', 16))
        button2.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')
        
        button3 = CTkButton(self, text='NYSE', command=self.gotoNYSE, font=('', 16))
        button3.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
        
        # Open settings
        button4 = CTkButton(self, text='Settings', command=self.openSettings, font=('', 16), width=100)
        button4.grid(row=0, column=7, padx=10, pady=10, sticky='e')
        
        # Date
        date_lable = CTkLabel(self, text='Date:', font=('', 17))
        date_lable.grid(row=1, column=3, padx=10, pady=10, sticky='e')
        
        # Ticker
        ticker_lable = CTkLabel(self, text='Ticker:', font=('', 17))
        ticker_lable.grid(row=1, column=5, padx=10, pady=10, sticky='e')
                
            

    def reloadThread(self):
        """Attemps to get new data from websites and store it in database.\n"""
        
        thread = Thread(target=self.master.initiateWebScrape, args=('Hedgeye',))
        thread.start()
        
        self.progress_bar.grid(row=0, column=1, columnspan=2)
        self.progress_bar.start()


    def gotoNASDAQ(self):
        """Changes page to the NASDAQ Power Play Results page.\n"""
        
        self.master.geometry('740x845')
        self.master.geometry(f'+490+140') # Shift
        self.master.showPage('NASDAQ')
        

    def gotoNYSE(self):
        """Changes page to the NYSE Power Play Results page.\n"""
        
        self.master.geometry('740x845')
        self.master.geometry(f'+490+140') # Shift
        self.master.showPage('NYSE')
        
    
    def openSettings(self):
        Settings(self.master)
        
        
    def reloadPage(self, target_date=None, target_tick=None):
        """
        Reloads all data on the page given that the user selects a different date or ticker to look at.\n
        Args:\n
            target_date (string, optional): Date that user chooses. Defaults to None.\n
            target_tick (string, optional): Ticker that user chooses. Defaults to None.\n
        """
        
        # Gets most recent information on startup because tdate and ttick are None
        data = summonHedgeyeData(date=target_date, ticker=target_tick)
                
        if len(data) > 1:
            self.data = data # For updating the 10s/2s spread and tickerAction function
            self.tickers = [d['Ticker'] for d in data[0:-1]] # Exclude the 10s/2s data
        
        # Display the first bout of data in the list
        self.drawTable(data[0])
        self.drawGraph(data[0]['Ticker'])
        self.drawInteractiveWidgets(self.tickers, data[0]['Description'], target_date, data[0]['Ticker'])
        
        # This saves where you are on the page so the user doesnt lose where they are if the navigate to other pages
        self.master.pages['Hedgeye'][1] = data[0]['Date']
        self.master.pages['Hedgeye'][2] = data[0]['Ticker']
        

        
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
        self.reloadPage(target_date=target_dict['Date'], target_tick=target_dict['Ticker'])
        
        
    def dateAction(self, date):
        """
        Changes the page accordingly when choosing a different date to look at.\n
        Takes in an event from the ComboBox.\n
        """
        
        self.reloadPage(target_date=date)
            
            
    def drawInteractiveWidgets(self, tickers, description, date_choice=None, ticker_choice=None):
        """
        Redraws the date and ticker combo boxes.\n
        Args:\n
            tickers (string)
            description (string):
            date_choice (string, optional): Date that user chooses. Defaults to None.
            ticker_choice (string, optional): Ticker that user chooses. Defaults to None.
        """

        # Date in entry box
        self.date_drop_down = CTkComboBox(self, values=self.dates, command=self.dateAction, width=140, justify='center', font=('', 14))
        if date_choice:
            self.date_drop_down.set(date_choice)
        self.date_drop_down.grid(row=1, column=4, pady=10, sticky='w')
        
        # Ticker in dropdown box
        self.ticker_drop_down = CTkComboBox(self, values=tickers, command=self.tickerAction, width=100, justify='center', font=('', 14))
        if ticker_choice:
            self.ticker_drop_down.set(ticker_choice)
        self.ticker_drop_down.grid(row=1, column=6, pady=10, sticky='w')
        
        # Description to the right of ticker dropdown
        self.description_lable = CTkLabel(self, text=description, font=('', 16))
        self.description_lable.grid(row=1, column=7, columnspan=3, pady=10, sticky='ew')
        
        
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
        self.table_lable = CTkEntry(self, font=('', 20), justify='center', height=40)
        self.table_lable.grid(row=(initrow - 1), column=initcol, columnspan=3, sticky='ew', pady=10)
        self.table_lable.insert(END, 'Range and Performance Data') 
          
        labels = ['Buy', 'Sell', 'Close', 'Range Asym - Buy (%)', 'Range Asym - Sell (%)', 'W/W Delta', 
                  '1-Day Delta (%)', '1-Week Delta (%)', '1-Month Delta (%)', '3-Month Delta (%)',
                  '6-Month Delta (%)', '1-Year Delta (%)']

        # Changing the style based on color mode
        style = ttk.Style()
        if self._get_appearance_mode() == 'dark':
            background_color = '#103248'
            row_color = '#373737'
            row_color2 = '#4B4B4B'
            text_color = 'white'
            highlight_color = '#476D7C'
            style.configure('my.Treeview', rowheight=53, font=(None, 20), borderwidth=1, fieldbackground=background_color)
        else:
            background_color = '#E5E5E5'
            row_color = '#F7F7F7'
            row_color2 = '#D3D3D3'
            text_color = 'black'
            highlight_color = '#476D7C'
            style.configure('my.Treeview', rowheight=53, font=(None, 20), borderwidth=1, fieldbackground=background_color)
            
        # Color change when clicking on the table
        style.map('my.Treeview', background=[('selected', highlight_color)], foreground=[('selected', 'white')])
        
        # Top row tree
        self.top_row = ttk.Treeview(self, columns=('col1',), style='my.Treeview', show='tree')
        # Stationary data, only changes when date changes
        self.top_row.insert('', 'end', text='10s/2s Spread (bps)', values=(self.data[-1]['10s/2s Spread (bps)']), tags='tt')
        self.top_row.tag_configure('tt', background=background_color, foreground=text_color)
        self.top_row.column('col1', anchor='e')
        self.top_row.grid(row=initrow, column=initcol, columnspan=3, sticky='nsew', pady=7)
        
        # Table tree
        self.table = ttk.Treeview(self, columns=('col1',), style='my.Treeview', show='tree')
        
        # Changes when ticker and date are changed
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

        self.table.grid(row=initrow, column=initcol, columnspan=3, rowspan=9, sticky='nsew', pady=73)


    def drawGraph(self, ticker):
        """
        Updates the graph given a specified ticker.\n
        Args:\n
            ticker (string): 'ABC...Z'.\n
        """
        # Top left of the table is where to specify location
        initrow = 4
        initcol = 0
        
        plt.rcParams['font.size'] = 12
        
        # Graph label
        self.graph_lable = CTkEntry(self, font=('', 20), justify='right', height=40)
        self.graph_lable.grid(row=(initrow - 1), column=initcol, columnspan=6, sticky='ew', padx=10)
        self.graph_lable.insert(END, 'Trade Price                  ')    
        
        
        # Setting color scheme
        if self._get_appearance_mode() == 'dark':
            face_color = '#103248'
            label_color = 'white'
            close_line_color = '#C1C1C1'
            grid_color = '#8F8F8F'
            
        else:
            face_color = '#E5E5E5'
            label_color = 'black'
            close_line_color = 'black'
            grid_color = 'black'
        

        fig = plt.Figure(figsize=(8, 6), tight_layout=True, facecolor=face_color)
        ax = fig.add_subplot(111)
        ax.set_facecolor(face_color)
        
        data = summonHedgeyeData(ticker=ticker)
        dates = [datetime.strptime(d['Date'], '%Y-%m-%d') for d in data[:-1]] # Exclude 10s/2s data        
        y1 = [d['Buy'] for d in data[0:-1]]
        y2 = [d['Sell'] for d in data[0:-1]]
        y3 = [d['Close'] for d in data[0:-1]]
        
        
        # ------------------------------------------------------------------------------------------------
        # Chops trend lines to show where data tracking has stopped for 7 days or longer
        
        index_ends = []
        index_starts = []

        for i in range(1, len(dates)):
            diff = (dates[i] - dates[i - 1]).days
            if diff >= 7:
                index_ends.append(i - 1)
                index_starts.append(i)            
        
        if len(index_ends) == 0:
            ax.plot_date(dates, y1, 'g^', label='Buy', linestyle='-')
            ax.plot_date(dates, y2, 'rv', label='Sell', linestyle='-')
            ax.plot_date(dates, y3, color=close_line_color, label='Close', linestyle='--', fmt='d')
            
        else:
            # First line segment
            ax.plot_date(dates[0:index_ends[0]], y1[0:index_ends[0]], 'g^', label='Buy', linestyle='-')
            ax.plot_date(dates[0:index_ends[0]], y2[0:index_ends[0]], 'rv', label='Sell', linestyle='-')
            ax.plot_date(dates[0:index_ends[0]], y3[0:index_ends[0]], color=close_line_color, label='Close', linestyle='--', fmt='d')
        
            # Any line segment after the first and before the final segment
            for i in range(1, len(index_ends)):
                ax.plot_date(dates[index_starts[i-1]:index_ends[i]], y1[index_starts[i-1]:index_ends[i]], 'g^', linestyle='-')
                ax.plot_date(dates[index_starts[i-1]:index_ends[i]], y2[index_starts[i-1]:index_ends[i]], 'rv', linestyle='-')
                ax.plot_date(dates[index_starts[i-1]:index_ends[i]], y3[index_starts[i-1]:index_ends[i]], color=close_line_color, label='Close', linestyle='--', fmt='d')
                
            # Final segment
            ax.plot_date(dates[index_starts[-1]:-1], y1[index_starts[-1]:-1], 'g^', linestyle='-')
            ax.plot_date(dates[index_starts[-1]:-1], y2[index_starts[-1]:-1], 'rv', linestyle='-')
            ax.plot_date(dates[index_starts[-1]:-1], y3[index_starts[-1]:-1], color=close_line_color, linestyle='--', fmt='d')
        
        # ------------------------------------------------------------------------------------------------

        for tick in ax.get_xticklabels():
            tick.set_rotation(30)
            
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.autoscale_view()
        ax.tick_params(colors=label_color, grid_color=grid_color)
        ax.set_xlabel('Date', color=label_color)
        ax.set_ylabel('Price', color=label_color)
        ax.legend()
        ax.grid(axis='y', color=grid_color)
        
        
        # Create the canvas and draw the plot
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()

        # Create the toolbar and add it to the window
        toolbar = CustomToolbar(canvas, self)
        toolbar.update()
        toolbar.grid(row=initrow - 1, column=initcol, columnspan=3, sticky='w', padx=20)
              
        canvas.get_tk_widget().grid(row=initrow, column=initcol, columnspan=6, rowspan=1, sticky='nsew', padx=10)
        
        
class CustomToolbar(NavigationToolbar2Tk):
    def __init__(self, canvas_, parent_):
        super(CustomToolbar, self).__init__(canvas_, parent_, pack_toolbar=False)
        self.config(background='#373737', highlightbackground='#373737', highlightcolor='#373737')
        self._message_label.config(foreground='white', background='#373737')