from dateutil.parser import parse
import re


def reformatDate(date):
    """
    Uses the dateutil.parser to reformat any date into the format yyyy-mm-dd.\n
    Args:\n
        date (str): Date string of any format.\n
    Raises:\n
        ValueError: If the parser cannot format a date into yyyy-mm-dd.\n
    Returns:\n
        str: Date in the format yyyy-mm-dd.
    """
    date = date.strip() # Removes whitespace from leading an trailing edges
    try:
        dt = parse(date, ignoretz=True) # Ignores time zones
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid date format: {date}.")


def removeParentheseData(string):
    """Removes parentheses and anything inside of parentheses. Ex. '(ajsncn32 *#( jnsdc)' -> ''"""
    return re.sub(r'\([^)]*\)', '', string).strip()


def reformatData(data):
    """
    Takes raw data from Hedgeyes website and formats it into a dictionary of parsed data.\n
    Args:\n
        data (str): Raw website data.\n
    Returns:\n
        List(dict): Parsed and formated data.
    """
    blocks =  data.strip().split('\n\n\n\n') # Seperates data into a list of blocked data 
    blocks.reverse()
    blocks.pop() # Remove unwanted data
    
    result = []
    for i in range(len(blocks)):
        pieces = blocks[i].lstrip('\n').rstrip('\n').split('\n') # Remove newlines on either side and seperate further by newline chars
        print(pieces)
        result.append({
                'Ticker': removeParentheseData(pieces[0]).upper(), # Removes (BULLISH), (BEARISH), or (NEUTRAL) and make sures all letters are upper
                'Description': pieces[2].upper(), 
                'Buy': float(pieces[4]), 
                'Sell': float(pieces[5]), 
                'Close': float(pieces[6])
                    })
    return result


def cleanData(data):
    """
    Takes in raw data from WallStreet Journal and Yahoo Finance and ensures that the data does not contain anything but negatives and decimals.
    Skips over any key with 'Date'.\n
    Args:\n
        data (dict): Parsed raw website data.\n
    Returns:\n
        dict: Parsed cleaned website data.
    """
    for key, value in data.items():
        if key != 'Date':
            data[key] = float(''.join(filter(lambda x: x.isdigit() or x in ['-', '.'], str(value))))
        
    return data
