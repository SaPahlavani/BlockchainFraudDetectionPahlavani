import pandas as pd
import requests
import datetime
import time

# Load data from the CSV file
file_path = "outputf_2023-10-09_06-17-17.csv"
dfR = pd.read_csv(file_path)

# Lists to store transaction count values
max_transaction_counts = []
min_transaction_counts = []
average_transaction_counts = []

# Make API requests and save data to the output CSV file
for index, row in dfR.iterrows():
    Address = row['address']
    URL = f"https://apilist.tronscanapi.com/api/account/analysis?address={Address}&type=4&start_timestamp=1514764800000&end_timestamp=1680508422169"

    try:
        response = requests.get(URL)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        
        api_data = response.json()

        # Extract transaction_count values from the data
        transaction_counts = [item["transaction_count"] for item in api_data["data"]]

        # Calculate max, min, and average
        max_transaction_count = max(transaction_counts)
        min_transaction_count = min(transaction_counts)
        average_transaction_count = sum(transaction_counts) / len(transaction_counts)

        # Update values in the DataFrame
        dfR.at[index, 'max_transaction_count'] = max_transaction_count
        dfR.at[index, 'min_transaction_count'] = min_transaction_count
        dfR.at[index, 'average_transaction_count'] = average_transaction_count

        
        # Save the updated DataFrame to the same CSV file
        dfR.to_csv(file_path, index=False)
        time.sleep(1)  # Add a delay to avoid rate limiting (1 request per second)
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Request Exception:", err)



print("\nData download and save complete.")
