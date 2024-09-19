import requests
from bs4 import BeautifulSoup
import pandas as pd

def smartlab_info(url): # Current Stock Price Data
    """
    Scrapes current stock price data from the given URL.
    
    :param url: The URL of the webpage to scrape the stock price data.
    :return: A DataFrame containing ticker and price information.
    """
    
    # Send a request to the webpage
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors
    
    # Find the first table on the page and extract all rows ('tr' tags)
    table_rows = BeautifulSoup(response.content, 'html.parser').find_all('tr')
    
    stock_data = []
    
    # Iterate over the rows, starting from the second row (to skip the header)
    for row in table_rows[1:]:  # Skip the first row (header)
        cells = row.find_all('td')
        
        # Ensure the row contains enough data (e.g., 7 cells)
        if len(cells) >= 7: 
            
            # Append ticker and price to the stock_data list
            stock_data.append([cells[2].get_text(strip=True),
                               cells[6].get_text(strip=True)])
    
    # Create a DataFrame from the stock data
    return pd.DataFrame(stock_data, columns=["ticker", "price"])

smartlab_info("https://smart-lab.ru/q/shares/") # Test
