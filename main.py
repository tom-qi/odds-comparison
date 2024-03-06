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

    # link to the Excel was not immediately available...I will need to figure
    # out a way to get the url from response

    # If it's a new file, download it
    # response = requests.get(download_link)
    # with open('path/to/save/spreadsheet.xlsx', 'wb') as file:
    #     file.write(response.content)
    # Update the info of the last downloaded file


def download_latest_spreadsheet():
    # URL from which to download the spreadsheet
    download_url = 'https://www.sports-ai.dev/api/generate-excel'

    # Send a GET request to the URL
    response = requests.get(download_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Write the content of the response to a file
        with open('downloaded_spreadsheet.xlsx', 'wb') as file:
            file.write(response.content)
        print('Spreadsheet downloaded successfully.')
    else:
        print('Failed to download the spreadsheet.')


# Run the download function
download_latest_spreadsheet()

file_path = 'predictions.xlsx'
# Load the spreadsheet
df = pd.read_excel(file_path)

def probability_to_decimal_odds(probability):
    if probability == 0:
        return 0
    return round(1 / probability, 2)

# The function to convert probabilities into American odds
def probability_to_american_odds(probability):
    if probability >= 0.5:
        return round(-100 / (probability / (1 - probability)), 2)
    else:
        return round(100 / ((1 - probability) / probability), 2)

# Apply the functions to each of the columns F through I and add them to the DataFrame
def add_odds_column(spreadsheet):
    spreadsheet['N'] = spreadsheet['F'].apply(probability_to_american_odds)
    spreadsheet['O'] = spreadsheet['F'].apply(probability_to_decimal_odds)
    spreadsheet['P'] = spreadsheet['G'].apply(probability_to_american_odds)
    spreadsheet['Q'] = spreadsheet['G'].apply(probability_to_decimal_odds)
    spreadsheet['R'] = spreadsheet['H'].apply(probability_to_american_odds)
    spreadsheet['S'] = spreadsheet['H'].apply(probability_to_decimal_odds)
    spreadsheet['T'] = spreadsheet['I'].apply(probability_to_american_odds)
    spreadsheet['U'] = spreadsheet['I'].apply(probability_to_decimal_odds)
# I'll put this in a loop or something later

def extract_table_to_dataframe(url):
    # Retrieve the HTML content from the website
    response = requests.get(url)
    html_content = response.content

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find and parse the table. You will need to inspect the webpage to get the correct table identifier.
    # Example:
    # table = soup.find('table', {'id': 'table_id'})

    # Use pandas to read the table HTML into a DataFrame
    # Example if there's one table:
    # df = pd.read_html(str(table))[0]

    # If there are multiple tables, you'll need to find the correct one by index or condition
    # Example if there's more than one table:
    # dfs = pd.read_html(str(soup))
    # df = dfs[0]  # or whichever index the correct table is

    return df

odds_wta = extract_table_to_dataframe("https://www.oddstrader.com/wta/")
odds_atp = extract_table_to_dataframe("https://www.oddstrader.com/atp/")
def job():
    print("Checking for new spreadsheet...")
    download_latest_spreadsheet()


# Schedule the job every 1 hour (adjust as needed)
schedule.every(1).hours.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
