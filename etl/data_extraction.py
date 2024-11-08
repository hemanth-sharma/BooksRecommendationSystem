"""
Data Extraction process
Extracting data from Goodreads.com
Data format : 
    Author:
    Title:
    Description:
    page_count:
    book_id:
    etc.


Extract data and save it in a file.
The saved data is in goodreads_books_clean.json    
"""


import asyncio
import pandas as pd
import time
from etl.data_scrapper import run_data_scrapper


if __name__ == "__main__":
    start_time = time.time()
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_data_scrapper())
    except RuntimeError as e:
        if 'This event loop is already running' in str(e):
            books_data = asyncio.run(run_data_scrapper())
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")



