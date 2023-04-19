from GUI_hedgeye import HedgeyePage
from GUI_nasdaq import NASDAQPage
from GUI_nyse import NYSEPage
from GUI_load import LoadingPage
from GUI_popup import Popup
from interface import updateDatabase
from customtkinter import set_appearance_mode, set_default_color_theme, CTk
from threading import Thread


set_appearance_mode('system')
set_default_color_theme('theme.json')

class MainApp(CTk):
    def __init__(self):
        super().__init__()
        
        # For correctly sizing the loading screen
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Initial screen size for the Hedgeye page
        self.geometry('1280x845')
        self.title('FIG')

        self.loading_page = LoadingPage(self)
        self.loading_page.grid(row=0, column=0, sticky='nsew')
        
        thread = Thread(target=self.initiateWebScrape, args=('Hedgeye',)) # Hedgeye is the first page to be shown
        thread.start()
    
    
    def createStashPages(self):
        # Create the interactive pages
        self.pages = {
            'Hedgeye': [HedgeyePage(self), None, None], # [PageObject, currect_date, current_ticker]
            'NASDAQ': [NASDAQPage(self), None], # [PageObject, currect_date]
            'NYSE': [NYSEPage(self), None] # [PageObject, currect_date]
        }
        
        # Stash the interactive pages
        for page in self.pages.values():
            page[0].grid_forget()
                    
      
    def showPage(self, requested_page): 
        """
        Master function that allows each interactive page to switch to a different interactive page.\n
        Stashes all pages and then displays the page that is specified.\n
        Args:\n
            page (string): Dictionary name of the page ('Hedgeye', 'NASDAQ', 'NYSE')\n
        """
        
        for page in self.pages.values():
            page[0].grid_forget()
        
        self.title(requested_page) # Change the page header
        saved_info_params = self.pages[requested_page][1:] # Parameters for reloadPage
        self.pages[requested_page][0].reloadPage(*saved_info_params) # Refresh that page with todays data
        self.pages[requested_page][0].progress_bar.grid_forget() # Stashes the loading bar for then `reload` is pressed
        self.pages[requested_page][0].grid(row=0, column=0, sticky='nsew')


    def initiateWebScrape(self, page):
        """
        Master function that grabs new information. Each page's `Reload` button calls this function.\n
        The page name that is passed in as a argument is the page that is shown after scrapping web data.\n
        Args:\n
            page (string): Dictionary name of the page ('Hedgeye', 'NASDAQ', 'NYSE')\n
        """
        popup = Popup(self)
        
        try:
            result = updateDatabase()
        except:
            popup.showError('A backend error occured. Call your son for support.')
            self.loading_page.destroy()
            self.showPage(page)
            return
            
        self.createStashPages()
        
        # WiFi error handling
        if type(result) == str:
            popup.showWarning(result)
            popup.showInfo('Reconnect the WiFi and press `Reload` to get updated information.')
            
        # Allows the user to see which websites are causing issues
        elif result[0] != 0 or result[1] != 0:
            for message in result:
                if type(message) == str:
                    popup.showWarning(message)
            popup.showInfo('To try again, press `Reload` to get updated information.')

        try:
            self.loading_page.destroy()
        except:
            pass
        finally:
            self.showPage(page)
            return


if __name__ == '__main__':  
    main_app = MainApp()
    main_app.mainloop()