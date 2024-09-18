import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def imoex_stocks(url): # Data Frame of IMOEX Stocks Returns
    """
    Scrapes IMOEX daily returns of stocks data from the given URL.
    
    :param url: The URL of the webpage to scrape the IMOEX stock returns.
    :return: A DataFrame containing the company names and percentage changes.
    """
    
    response = requests.get(url) # Send a request to the webpage
    response.raise_for_status()  # Check for request errors
    
    # Parse the HTML content and extract table data from the webpage
    table_rows = BeautifulSoup(response.content, 'html.parser').find_all('tr')
    
    stock_data = []
    
    for row in table_rows: # Iterate over each row in the table
      
        cells = row.find_all('td')
        
        if len(cells) > 7:  # Ensure there are enough cells in the row
          
            company = cells[1].get_text(strip=True)
            
            # Clean and format the percentage change
            change = re.sub(r'[^\d\.\-\+]', '', cells[6].get_text(strip=True))
            
            change = change.replace('+', '')  # Remove the plus sign if present
            
            try:
                change = float(change)  # Convert to float
                
            except ValueError:
              
                continue  # Skip row if conversion fails
            
            # Add company and % data to the list
            stock_data.append([company, change])
    
    # Create a DataFrame from the stock data
    return pd.DataFrame(stock_data, columns=["Компания", "%"])

imoex_stocks("https://smart-lab.ru/q/index_stocks/IMOEX/") # Test
