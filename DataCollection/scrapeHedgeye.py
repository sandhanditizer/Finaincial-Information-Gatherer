from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from DataCollection.helperFunctions import getDriver, extract, formatDate
import json


def login(hedgeye_driver):
    """
    Attemps to logs into the Hedgeye website.\n
    Args:\n
        hedgeye_driver (selenium.webdriver): Controller of webscrape process.\n
    Returns:\n
        selenium.webdriver: If success.\n
        string: If failure.\n
    """
    
    try:
        LOGIN_URL = 'https://accounts.hedgeye.com/users/sign_in'
        hedgeye_driver.get(LOGIN_URL)
        
        with open('DataCollection/config.json', 'r') as f:
            login_payload = json.load(f)

        # Finds the email and password fields, and enter login credentials
        email_field = hedgeye_driver.find_element(By.ID, 'user_email')
        email_field.send_keys(login_payload['Payload'][0]['username'])

        password_field = hedgeye_driver.find_element(By.ID, 'user_password')
        password_field.send_keys(login_payload['Payload'][0]['password'])

        # Submits the login form
        password_field.send_keys(Keys.RETURN)
        
        return hedgeye_driver
    except:
        return "Cannot log into Hedgeye's website."
    

def newestHedgeyeData():
    """
    Requests newest data from Hedgeye website and returns the data clean and formated.\n
    Returns:\n
        list: Data.\n
    """
    
    try:
        hedgeye_driver = login(getDriver('Firefox'))
    except:
        hedgeye_driver = login(getDriver('Edge'))
        
    if type(hedgeye_driver) == str:
        return hedgeye_driver # Login error

    try:
        HEDGEYE_TARGET_URL = 'https://app.hedgeye.com/feed_items/all?page=1&with_category=33-risk-range-signals'
        hedgeye_driver.get(HEDGEYE_TARGET_URL)
        
        # Make second request in case of error
        if hedgeye_driver.current_url != HEDGEYE_TARGET_URL:
            hedgeye_driver.get(HEDGEYE_TARGET_URL)
            
        # Waits a maximum of 30 seconds for the website to load correctly
        wait = WebDriverWait(hedgeye_driver, 30) 

        table = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="mid-col"]/div/div[1]/div/article/div/div[2]/table'))).get_attribute('textContent')
        date = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[starts-with(@id, "teaser_feed_item_")]/div[1]/time/span[2]'))).get_attribute('textContent')
    except:
        return "Cannot grab data from Hedgeye's website."
    finally:
        hedgeye_driver.quit()
        
    try:
        data = extract(table) # Formats data returns a list of dictionaries
    except:
        return "Cannot properly extract Hedgeye's table data."
    
    try:
        formated_date = formatDate(date)
    except:
        return "Cannot properly format Hedgeye's date data."
        
    data.append(formated_date)
    return data