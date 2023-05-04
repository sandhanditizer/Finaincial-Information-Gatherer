from GUI_settings import Settings
from interface import summonHedgeyeData
import customtkinter as ctk
from tkinter import ttk
from datetime import datetime
from threading import Thread
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


class HedgeyePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Class globals
        self.data = None
        self.tickers = []
        self.progress_bar = ctk.CTkProgressBar(self, mode='indeterminate', indeterminate_speed=0.5)
        
        # For the date selector
        self.dates = summonHedgeyeData(all_dates=True)
        self.dates.reverse()
        
        # Page specifier
        page_title = ctk.CTkLabel(self, text="Daily Data", font=(None, 40, 'bold'))
        page_title.grid(row=0, column=0, columnspan=2, padx=10, pady=20,  sticky='w')
        
        # Reload data button
        button1 = ctk.CTkButton(self, text='Reload Data', command=self.reloadThread)
        button1.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
        
        # Redirection buttons
        button2 = ctk.CTkButton(self, text='Goto NASDAQ', command=lambda: self.master.showPage('NASDAQ'))
        button2.grid(row=1, column=1, padx=10, pady=10, sticky='ew')
        
        button3 = ctk.CTkButton(self, text='Goto NYSE', command=lambda: self.master.showPage('NYSE'))
        button3.grid(row=1, column=2, padx=10, pady=10, sticky='ew')
        
        # Open settings
        button4 = ctk.CTkButton(self, text='Credential Settings', command=self.openSettings, width=160)
        button4.grid(row=0, column=8, padx=10, pady=10, sticky='e')
        
        # Month separator       
        self.grid_split_seg_buttons = ctk.CTkSegmentedButton(self, values=['No Y-Grid', 'M', '3M', '6M', '1Y'], command=self.setGrid)
        self.grid_split_seg_buttons.set('No Y-Grid')
        self.grid_split_seg_buttons.grid(row=0, column=5, columnspan=4, padx=10, pady=10, sticky='w')
                
            

    def reloadThread(self):
        """
        Requests backend to fetch new data if the database is not updated with todays data.
        It will then display the page that the user was on. 
        Progress bar is started and will disappear when reload is finished. 
        """
        thread = Thread(target=self.master.initiateWebScrape, args=('Hedgeye',))
        thread.start()
        
        self.progress_bar.grid(row=2, column=0, columnspan=10, padx=10, sticky='ew')
        self.progress_bar.start()
        
    
    def openSettings(self):
        """
        Displays settings widget. Will self close if a change is made.
        """
        Settings(self.master)
        
        
    def reloadPage(self, target_date=None, target_tick=None):
        """
        Refreshes the current page with updated information. It will save where you are
        on the page (what day and what ticker you are on).\n
        Args:\n
            target_date (str, optional): If not None, will refresh the page to display the tickers for that date. Defaults to None.\n
            target_tick (str, optional): If not None, will refresh the page to display that ticker. Defaults to None.
        """
        # If target_date and target_tick == None -> data = most recent data from db
        data = summonHedgeyeData(date=target_date, ticker=target_tick)
                
        if len(data) > 1:
            self.data = data # For updating the 10s/2s spread and tickerAction function
            self.tickers = [d['Ticker'] for d in data[0:-1]] # Excludes the 10s/2s data
        
        # Display the first bout of data in the list
        self.drawTable(data[0])
        self.drawGraph(data[0]['Ticker'])
        self.drawInteractiveWidgets(self.tickers, data[0]['Description'], target_date, data[0]['Ticker'])
        
        # This saves where you are on the page which allows you to navigate to other pages or press `reload` without losing your spot
        self.master.pages['Hedgeye'][1] = data[0]['Date']
        self.master.pages['Hedgeye'][2] = data[0]['Ticker']
        

    def findDictByTick(self, list_of_dictionaries, ticker):
        """
        Finds the associated ticker data in the list of dictionaries given the ticker name.\n
        Args:\n
            list_of_dictionaries (list): List of all tickers and their associated data for X day.\n
            ticker (str): Ticker name that you want data for.\n
        Returns:\n
            dict: If ticker is found it returns its associated data. Else it returns None.\n
        """
        for dict_item in list_of_dictionaries:
            if dict_item['Ticker'] == ticker:
                return dict_item
            
        return None # Not found
        
        
    def tickerAction(self, ticker):
        """
        If the user interacts with the ticker drop down, this function is called to manipulate the displayed page.\n
        Args:\n
            ticker (str): Ticker that was clicked on by user.
        """
        target_dict = self.findDictByTick(self.data, ticker)
        self.reloadPage(target_date=target_dict['Date'], target_tick=target_dict['Ticker'])
        
        
    def dateAction(self, date):
        """
        If the user interacts with the date drop down, this function is called to manipulate the displayed page.\n
        Args:\n
            date (str): Date that was clicked on by user.
        """
        self.reloadPage(target_date=date)
            
            
    def drawInteractiveWidgets(self, tickers, description, date_choice=None, ticker_choice=None):
        """
        Draws the correct information on the display when the user interacts with it.\n
        Args:\n
            tickers (list): List of all tickers that are associated with X day. 
            description (str): Full company name that is represented by the ticker.\n
            date_choice (str, optional): Date that was clicked on by user. Defaults to None.\n
            ticker_choice (str, optional): Ticker that was clicked on by user. Defaults to None.
        """
        # Description to the right of ticker dropdown
        description_lable = ctk.CTkLabel(self, text=description, anchor='center')
        description_lable.grid(row=1, column=5, columnspan=4, padx=10, pady=10, sticky='ew')
        
        # Ticker dropdown box
        ticker_drop_down = ctk.CTkOptionMenu(self, values=tickers, command=self.tickerAction, anchor='center')
        if ticker_choice:
            ticker_drop_down.set(ticker_choice)
        ticker_drop_down.grid(row=1, column=4, padx=10, pady=10, sticky='ew')
        
        # Date dropdown box
        date_drop_down = ctk.CTkOptionMenu(self, values=self.dates, command=self.dateAction, anchor='center')
        if date_choice:
            date_drop_down.set(date_choice)
        date_drop_down.grid(row=1, column=3, padx=10, pady=10, sticky='ew')   
        
        
    def setGrid(self, _):
        self.drawGraph(ticker=self.master.pages['Hedgeye'][2])
        
        
    def drawTable(self, data):    
        """
        Updates shown table with data that is passed in.\n
        Args:\n
            data (dict): Data that is displayed on the table.
        """
        # Top left corner positions the label and table without adjusting it individually
        initrow = 4
        initcol = 6
        
        # Table label   
        self.table_lable = ctk.CTkEntry(self, justify='center', height=50, font=(None, 20))
        self.table_lable.grid(row=(initrow - 1), column=initcol, columnspan=3, pady=10, sticky='ew')
        self.table_lable.insert(ctk.END, 'Range and Performance Data') 
          
        labels = ['Buy', 'Sell', 'Close', 'Range Asym - Buy (%)', 'Range Asym - Sell (%)', 'W/W Delta', 
                  '1-Day Delta (%)', '1-Week Delta (%)', '1-Month Delta (%)', '3-Month Delta (%)',
                  '6-Month Delta (%)', '1-Year Delta (%)']

        # Changing the style based on color mode
        style = ttk.Style()
        if self._get_appearance_mode() == 'dark':
            background_color = '#131e23'
            row_color = '#373737'
            row_color2 = '#4B4B4B'
            text_color = 'white'
            highlight_color = '#304a54'
            style.configure('my.Treeview', rowheight=53, font=(None, 15), fieldbackground=background_color)
        else:
            background_color = '#E5E5E5'
            row_color = '#F7F7F7'
            row_color2 = '#D3D3D3'
            text_color = 'black'
            highlight_color = '#476D7C'
            style.configure('my.Treeview', rowheight=53, font=(None, 15), fieldbackground=background_color)
            
        # Color change when clicking on the table
        style.map('my.Treeview', background=[('selected', highlight_color)], foreground=[('selected', 'white')])
        
        # Top row tree
        self.top_row = ttk.Treeview(self, columns=('col1',), style='my.Treeview', show='tree')
        # Stationary data, only changes when date changes
        self.top_row.insert('', 'end', text='10s/2s Spread (bps)', values=(self.data[-1]['10s/2s Spread (bps)']), tags='tt')
        self.top_row.tag_configure('tt', background=background_color, foreground=text_color)
        self.top_row.column('col1', anchor='e')
        self.top_row.grid(row=initrow, column=initcol, columnspan=3, pady=(0, 5), sticky='nsew')
        
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

        self.table.grid(row=initrow, column=initcol, columnspan=3, rowspan=9, pady=62, sticky='nsew')


    def drawGraph(self, ticker):
        """
        Displays the close data for the specified ticker.\n
        Args:\n
            ticker (str): Close data that will be shown for this ticker.
        """
        # Top left corner positions the label and table without adjusting it individually
        initrow = 4
        initcol = 0
                
        # Graph label
        self.graph_lable = ctk.CTkEntry(self, justify='right', height=50, font=(None, 20))
        self.graph_lable.grid(row=(initrow - 1), column=initcol, columnspan=6, padx=10, sticky='ew')
        self.graph_lable.insert(ctk.END, 'Trade Price View                 ')    
        
        # Setting color scheme based on color mode of computer
        if self._get_appearance_mode() == 'dark':
            face_color = '#131e23'
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
        
        # Gets the data to be plotted
        data = summonHedgeyeData(ticker=ticker)
        dates = [datetime.strptime(d['Date'], '%Y-%m-%d') for d in data[:-1]] # Excludes 10s/2s data        
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
        # This chunk of code below is for splitting up the y-axis grid lines for the segment_button
        
        month_starts = []
        grid_type = self.grid_split_seg_buttons.get()
        if grid_type == 'No Y-Grid':
            ax.yaxis.grid(False)
        elif grid_type == 'M':
            for month in range(1, 13):
                month_dates = [d for d in dates if d.month == month]
                if month_dates:
                    month_starts.append(min(month_dates))
        elif grid_type == '3M':
            for month in range(1, 13, 3):
                month_dates = [d for d in dates if d.month in range(month, month+3)]
                if month_dates:
                    month_starts.append(min(month_dates))
        elif grid_type == '6M':
            for month in range(1, 13, 6):
                month_dates = [d for d in dates if d.month in range(month, month+6)]
                if month_dates:
                    month_starts.append(min(month_dates))
        elif grid_type == '1Y':
            prev_year = None
            for month in range(1, 2):
                month_dates = [d for d in dates if d.month == month]
                if month_dates:
                    month_start = min(month_dates)
                    if prev_year is None or month_start.year != prev_year:
                        month_starts.append(month_start)
                        prev_year = month_start.year
        
        for month_start in month_starts: 
            ax.axvline(month_start, linestyle='-', color=grid_color, zorder=-1, linewidth=0.8)
                
        # ------------------------------------------------------------------------------------------------
            
        for tick in ax.get_xticklabels():
            tick.set_rotation(30)
            
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%b-%d'))
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
        toolbar = CustomToolbar(canvas, self, self._get_appearance_mode())
        toolbar.update()
        toolbar.grid(row=initrow - 1, column=initcol, columnspan=3, padx=20, sticky='w')
              
        canvas.get_tk_widget().grid(row=initrow, column=initcol, columnspan=6, rowspan=1, padx=10, sticky='nsew')
        
        
class CustomToolbar(NavigationToolbar2Tk):
    def __init__(self, canvas_, parent_, color_mode):
        super(CustomToolbar, self).__init__(canvas_, parent_, pack_toolbar=False)
        
        if color_mode == 'light':
            color = 'gray85'
            fcolor = 'black'
        else:
            color = '#373737'
            fcolor = 'white'
        self.config(background=color, highlightbackground=color, highlightcolor=color, cursor='none')
        self._message_label.config(foreground=fcolor, background=color, font=(None, 16))