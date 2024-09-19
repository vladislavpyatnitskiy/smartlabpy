import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def smartlab_ticker(tickers, fields):
    """
    Scrape fundamental data for specified tickers and fields from smart-lab.ru.

    :param tickers: A list of ticker symbols (e.g., ["LKOH", "MAGN", "UPRO"]).
    :param fields: A list of fundamental data fields (e.g., ["market_cap"]).
    :return: DataFrame containing the scraped fundamental data for each ticker.
    """
    
    results = []
    
    for ticker in tickers:
        data_row = {'Ticker': ticker}
        
        for field in fields: # Format the URL with the ticker and field
            
            url = f"https://smart-lab.ru/q/shares_fundamental/?field={field}"
            response = requests.get(url)
            response.raise_for_status()  # Check for request errors
            
            # Find the first table and extract its rows
            table = BeautifulSoup(response.content,'html.parser').find('table')
            if not table:
                continue
            
            rows = table.find_all('tr')
            
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 3:
                    stock = re.sub(r'[\n\t]', '', cells[2].get_text()).strip()
                    value = re.sub(r'[\n\t]', '', cells[5].get_text()).strip()
                    
                    # If the ticker matches, store the value
                    if stock == ticker:
                        data_row[field.upper().replace("_", "/")] = value
                        break
        
        results.append(data_row)
    
    df = pd.DataFrame(results) # Convert the result list to a DataFrame
    
    # Ensure all columns are numeric where applicable
    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df.index = tickers # Set row names as tickers
    df = df.iloc[:, 1:] # Reduce first column
    
    return df

smartlab_ticker(["LKOH", "MAGN", "UPRO"], ["market_cap", "p_e", "p_s"]) # Test
