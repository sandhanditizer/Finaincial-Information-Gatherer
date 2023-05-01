# Financial-Information-Gatherer (FIG)

## What it do baby:
This application was a project that I created for my father. Every morning he would spend about an hour collecting data from three different websites (hedgeye.com, www.wsj.com/market-data/stocks/marketsdiary, and finance.yahoo.com), putting them in their respective Excel files, and run some analysis. This is obviously a waste of time since this can be automated. So, this app does everything described above and displays all the information in either graphs, tables, or a combination of both.

## Downloads needed:
```bash
pip3 install python3 		# Don't actually do this just go to www.python.org/downloads/ and get a fresh version
pip3 install sqlalchemy 	# Database communications
pip3 install pysqlite3 		# Will be preinstalled if python3 exists on your device
pip3 install selenium  		# Web-scraping
pip3 install tk				# Tkinter GUI
pip3 install customtkinter 	# Newer version of tkinter GUI
pip3 install matplotlib		# Plotting
pip3 install tzlocal		# Time functions 
```

## Things to note - 1:
At the top of `GUI_app.py`, there is a shebang to indicate which interpreter should be used when executing a script I have for my computer. Since your interpreter will be in a different location I suggest that you change it to where `python3` is on your computer. You can still launch the app with the instructions I give below and this comment will not effect it. However, if you would like to create an automator file on Mac or executable script on Windows, then you need to change the interpreter location.
### Finding the correct path on Mac:
```bash
which python3
```
### Finding the correct path on Windows:
```PowerShell
where python
```

## Things to note - 2:
If you get a popup that says "Cannot grab risk range data from Hedgeye's website. Website page has changed to something unrecognizable." Then that means hedgeye has temporarily changed the page structure. Don't freak out, it will change back to the structure that allows data to be scraped from it. As long as it runs before 11am every morning then you will capture the data before they temperarily change the page structure.

## Having the right browser:
In `DataCollection/scrapeHedgeye.py` and `DataCollection/scrapeWSJ_Yahoo.py` the function `getDriver` will try to get drivers for Firefox or Chrome using selenium. If you do not have Firefox or Chrome installed, then please install one. Once a browser is installed, there is no further action needed. If there is a problem (rare) then look at seleniums documentation to get Firefox or Chrome to work. It might involve disabling a security feature. However, I did not have to change anything after downloading Firefox.

## Using the app:
Due to the fact that the data in my database is proprietary data from hedgeye.com, I am excluding the database and password, username, and user-agent data from `config.json` (this file is used to log into Hedgeye's website). I will be adding an example database that will allow you to interact with the app without seeing the proprietary data. If you would like to start collecting/viewing data from the websites specified above, follow the instructions below for creating the database with the correct schemas, getting a Hedgeye subscription, and creating the `config.json` file. If you choose to stay with the example database...
1. Check that the database filename in `DBControls/dbReadWrite.py` say `example_data.db` instead of `market_data.db`. It will be at the top of the file. 
2. Create a file in `DataCollection` named `config.json`. Copy and paste the contents for `config.json` below. No don't change anything, the app needs this file to exist to properly run. 
3. You will get an error popup telling you that it can't login to Hedgeye because you do not have access to the data (the config.json file is not set up with valid login data for hedgeye.com). That is okay, just acknowledge the popup and it will proceed to the main hedgeye page with fake data.

### Creating the SQLite database:
Create a sqlite database called `market_data.db` and store it in the `DBControls` file. Next, get an open-source universal database management tool that works with SQLite databases (I use the DBeaver Community edition which is free). Using a management tool like DBeaver, enter these tables into the database...
```sql
CREATE TABLE "Hedgeye" (
	"ID" INTEGER,
	"Date" TEXT,
	"Ticker" TEXT,
	"Description" TEXT,
	"Buy" REAL,
	"Sell" REAL,
	"Close" REAL,
	"Delta W/W" REAL,
	"1D Delta (%)" REAL,
	"1W Delta (%)" REAL,
	"1M Delta (%)" REAL,
	"3M Delta (%)" REAL,
	"6M Delta (%)" REAL,
	"1Y Delta (%)" REAL,
	"Range Asymmetry Buy (%)" REAL,
	"Range Asymmetry Sell (%)" REAL,
	PRIMARY KEY("ID" AUTOINCREMENT)
);

CREATE TABLE "NASDAQ" (
	"Date"	TEXT,
	"Advancing Volume" REAL,
	"Declining Volume" REAL,
	"Total Volume" REAL,
	"Change in Volume (%)" REAL,
	"Close (%)" REAL,
	"Upside Day (%)" REAL,
	"Downside Day (%)" REAL,
	"Advances" REAL,
	"Declines" REAL,
	"Net (Advances/Declines)" REAL,
	"10-Day Breakaway Momentum" REAL,
	"20-Day Breakaway Momentum" REAL,
	"Advance/Decline Ratio"	REAL,
	"Advance/Decline Thrust (%)" REAL,
	"5-Day Advance/Decline Thrust (%)" REAL,
	"5-Day Up/Down Volume Thrust (%)" REAL,
	"New Highs"	REAL,
	"New Lows" REAL,
	"Net (Highs/Lows)" REAL,
	"21-Day Average (Highs/Lows)" REAL,
	"63-Day Average (Highs/Lows)" REAL,
	PRIMARY KEY("Date")
);

CREATE TABLE "NYSE" (
	"Date" TEXT,
	"Advancing Volume" REAL,
	"Declining Volume" REAL,
	"Total Volume" REAL,
	"Change in Volume (%)" REAL,
	"Close (%)"	REAL,
	"Upside Day (%)" REAL,
	"Downside Day (%)" REAL,
	"Advances" REAL,
	"Declines" REAL,
	"Net (Advances/Declines)" REAL,
	"10-Day Breakaway Momentum" REAL,
	"20-Day Breakaway Momentum"	REAL,
	"Advance/Decline Ratio"	REAL,
	"Advance/Decline Thrust (%)" REAL,
	"5-Day Advance/Decline Thrust (%)" REAL,
	"5-Day Up/Down Volume Thrust (%)" REAL,
	"New Highs"	REAL,
	"New Lows" REAL,
	"Net (Highs/Lows)" REAL,
	"21-Day Average (Highs/Lows)" REAL,
	"63-Day Average (Highs/Lows)" REAL,
	PRIMARY KEY("Date")
);
```

### Getting a Hedgeye subscription:
To get data from hedgeye.com , you will need your own Hedgeye subscription.  
1. Goto `https://accounts.hedgeye.com/products`.  
2. Select one of the two pricing options for the Hedgeye Risk Manager subscription. This will give you access to the data that will be requested upon opening my application.  
3. Keep note of your username and password information.
4. Locate your user-agent data that is specific to your computer.   
4.a. Goto `https://www.whatismybrowser.com/detect/what-is-my-user-agent/`.  
4.b. Keep note of the user-agent information.

### Creating config.json:
If you are using the example database provided, make sure that `config.json` is in `DataCollection` and that the contents below are in the said file. If you have purchased a Hedgeye subscription, change the username, password, and user-agent fields.
```json
{
"Payload": 
	[{"username": "username-here", "password": "password-here"}], 
"Headers": 
	[{"user-agent": "user-agent-data-here"}]
}
```

## Running the program:
Run the program by executing
```bash
python3 GUI_app.py 
```
in the terminal or 
```bash
run GUI_app.py
```
in Ipython.