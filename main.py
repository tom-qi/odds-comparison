import requests
from bs4 import BeautifulSoup
import schedule
import time
import pandas as pd

#TODO:
    # How can pandas match the players (and their respective odds) 
    # from oddstrader to the model?

    # Figure out how to standardize names and clean data from beautifulsoup if necessary

    # edge cases, tests, considerations. Create error assertions where necessary
        # 1. The AI model did not calculate odds for that player/prop
        # 2. a match from oddtrader is actually live
        # 3. Names incorrect
    
    # Create requirements.txt

    # Create test cases

    # explore https://the-odds-api.com/ integration. Unfortunately free model only allows 500 request/mo.

def check_spreadsheet_last_updated():
    # URL to download the spreadsheet
    # Procedure to get url was as follows
    # Click on the "generate-excel" request in the Network tab to open its details.
    # Headers: Look under the "Headers" tab to find the full URL of the request in the "Request URL" section.

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

# Function to convert probabilities into American odds
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
# TODO: I'll put this in a loop or something later

def extract_table_to_dataframe(url):
    # Retrieve the HTML content from the website
    response = requests.get(url)
    html_content = response.content

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find and parse the table. IDK how to find the table id.
    # gotta inspect element and find something like...
    # table = soup.find('table', {'id': 'table_id'})

# TODO:

    # Use pandas to read the table HTML into a DataFrame
    # df = pd.read_html(str(table))[0]

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

def calculate_edge(model_probability, best_odds):
    """
    Calculate the betting edge.

    :param model_probability: The probability of the outcome according to the model (as a decimal, e.g., 0.5 for 50%)
    :param best_odds: The best decimal odds available for the outcome
    :return: The calculated edge as a percentage. A positive edge suggests a bet with expected value above the bookmaker's odds.
    """
    decimal_odds = best_odds
    implied_probability = 1 / decimal_odds
    edge = (model_probability - implied_probability) * 100  # Convert to percentage
    
    return edge
