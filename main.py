import requests
from bs4 import BeautifulSoup
import schedule
import time
import pandas as pd


def check_spreadsheet_last_updated():
    # URL from which to download the spreadsheet
    download_url = 'https://www.sports-ai.dev/api/generate-excel'

    # Send a HEAD request to get the headers only
    response = requests.head(download_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Check the last modified date in the headers
        last_modified = response.headers.get('Last-Modified')
        if last_modified:
            print(f"The spreadsheet was last updated on: {last_modified}")
            return last_modified
        else:
            print("No 'Last-Modified' header found.")
            return None
    else:
        print('Failed to access the spreadsheet.')
        return None


# Run the function to check the last updated time
last_updated = check_spreadsheet_last_updated()


def download_latest_spreadsheet():
    # URL of the page where the spreadsheet link is available
    url = 'https://www.sports-ai.dev/predictions'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the download link for the spreadsheet (this part depends on the
    # webpage structure) Example: download_link = soup.find('a', {'id':
    # 'spreadsheet-download-link'}).get('href')

    # Check if this is a new spreadsheet (you might store the last downloaded
    # file info and compare)

    # If it's a new file, download it
    # response = requests.get(download_link)
    # with open('path/to/save/spreadsheet.xlsx', 'wb') as file:
    #     file.write(response.content)
    # Update the info of the last downloaded file


def job():
    print("Checking for new spreadsheet...")
    download_latest_spreadsheet()


# Schedule the job every 1 hour (adjust as needed)
schedule.every(1).hours.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
