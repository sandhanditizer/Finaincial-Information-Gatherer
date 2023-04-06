from datetime import datetime
from selenium import webdriver
import re


def formatDate(date):
    date = date.strip()
    
    date_match = re.search(r'\d{1,2}/\d{1,2}/\d{2}', date)
    if date_match:
        date = date_match.group()
    
    
    formats = ['%B %d, %Y', '%A, %B %d, %Y', '%m/%d/%y', '%b %d, %Y']
    dt = None
    for f in formats:
        try:
            dt = datetime.strptime(date, f)
            break
        except ValueError:
            pass
    
    if dt is None:
        raise ValueError(f"Invalid date format: {date}.\n")

    # Return formatted date string in yyyy-mm-dd format
    return dt.strftime("%Y-%m-%d")



def getDriver(browser):
    """Creates a webdriver based off desired browser and returns the webdriver object"""
    if browser == 'Edge':
        options = webdriver.EdgeOptions()
        options.add_argument('-headless') # Prevents browser pop-up
        return webdriver.Edge(options=options)
    elif browser == 'Firefox':
        options = webdriver.FirefoxOptions()
        options.add_argument('-headless') # Prevents browser pop-up
        return webdriver.Firefox(options=options)
    else:
        raise ValueError('Available webdriver browsers are `Edge` and `Firefox`.\n')



def removeParentheses(string):
    return re.sub(r'\([^)]*\)', '', string).strip()



def extract(string):
    blocks = string.strip().split('\n\n\n\n')
    
    result = []
    for i in range(len(blocks)):
        if i != 0:
            pieces = blocks[i].lstrip('\n').split("\n")
            result.append({"Ticker": removeParentheses(pieces[0]).upper(), 
                           "Description": pieces[2].upper(), 
                           "Buy": float(pieces[4].replace(',', '')), 
                           "Sell": float(pieces[5].replace(',', '')), 
                           "Close": float(pieces[6].replace(',', ''))
                           })
    
    return result



def clean(data):
    """Removes characters from scraped data that should not be in the database"""
    for key in data:
        value = str(data[key])
        value = ''.join(filter(lambda x: x.isdigit() or x in ['-', '.'], value))
        if key == 'Date':
            data[key] = value
        else:
            data[key] = float(value)
        
    return data
