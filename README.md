# Financial-Information-Gatherer (FIG)

## What it do baby:
This application was a project that I created for my father. Every morning he would spend about an hour collecting data from three different websites, putting them in their respective Excel files, and run some analysis. This is obviously a waste of time since this can be automated. So, this app does everything described above and displays all the information in either graphs, tables, or a combination of both.

## Downloads needed:
```bash
pip3 install sqlalchemy  
pip3 install pysqlite3 # Will be preinstalled if python3 exists on your device
pip3 install selenium  
pip3 install tkinter
pip3 install customtkinter  
pip3 install matplotlib
pip3 install tzlocal
```

## Choosing which browser to silently complete web scraping:
In `DataCollection/scrapeHedgeye.py` and `DataCollection/scrapeWSJ_Yahoo.py` the function `getDriver` defaults to a 'Firefox' driver, but if it fails then it will try an 'Edge' driver. If you do not have Firefox or Edge installed, then please install one or the other. If there is a problem you will get the appropriate error message in your terminal. Once Firefox or Edge is installed, there is no further action needed.

## Credentialing and database creation:
Due to the fact that the data in my database is proprietary data from hedgeye.com, I am excluding the database and the `config.json` data that my program uses to log into Hedgeye's website. I will be adding an example database so that you can interact with the app without seeing the proprietary data. If you would like to see data from hedgeye.com, follow the instructions below for creating the database with the correct tables, getting a Hedgeye subscription, and editing the config.json file. If you choose to stay with the example database, you will get an error popup telling you that it cant login to Hedgeye because you do not have access to the data. That is okay, just acknowledge the popup and it will proceed to the main hedgeye page with fake data.

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
### Getting a Hedgeye subscription and editing config.json:
To run this application, you will need your own Hedgeye subscription so that way you can legally get the data from their website.  
1. Goto `https://accounts.hedgeye.com/products`.  
2. Select one of the two pricing options for the Hedgeye Risk Manager subscription. This will give you access to the data that will be requested upon opening my application.  
3. Keep note of your username and password when you are prompted to make one.
4. Locate your user-agent data that is specific to your computer.   
4.a. Goto `https://www.whatismybrowser.com/detect/what-is-my-user-agent/`.  
4.b. Keep note of the user-agent information.
5. Navigate to `DataCollection/config.json`. The username, password, and user-agent data will be empty.
6. Fill in the username, password, and user-agent data in the correct spots.

If you bought a Hedgeye subscription and correctly edited the config.json file. The application will work and begin collecting data. Your database obviously will not be populated with data so you need to run the app (shown below) every trading day to populating the database.

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