#Pahlavani
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
i = 1
# Make API requests and save data to the output CSV file
for index, row in dfR.iterrows():
    Address = row['address']
    URL = f"https://apilist.tronscanapi.com/api/account/analysis?address={Address}&type=0&start_timestamp=1514764800000&end_timestamp=1680508422169"

    try:
        response = requests.get(URL)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        
        api_data = response.json()
        #print(api_data)
        # Extract transaction_count values from the data
        trx_amount = [float(item["trx_amount"]) for item in api_data["data"]]
        usdt_amount = [float(item["usdt_amount"]) for item in api_data["data"]]
        price = [float(item["price"]) for item in api_data["data"]]

        if trx_amount:
            max_trx_amount = max(trx_amount)
            min_trx_amount = min(trx_amount)
            average_trx_amount = sum(trx_amount) / len(trx_amount)
        else:
            max_trx_amount = 0
            min_trx_amount = 0
            average_trx_amount = 0
        if usdt_amount:
            max_usdt_amount = max(usdt_amount)
            min_usdt_amount = min(usdt_amount)
            average_usdt_amount = sum(usdt_amount) / len(usdt_amount)
        else:
            max_usdt_amount = 0
            min_usdt_amount = 0
            average_usdt_amount = 0
        if price:
            max_price = max(price)
            min_price = min(price)
            average_price = sum(price) / len(price)
        else:
            max_price = 0
            min_price = 0
            average_price = 0

        dfR.at[index, 'max_trx_amount'] = max_trx_amount
        dfR.at[index, 'min_trx_amount'] = min_trx_amount
        dfR.at[index, 'average_trx_amount'] = average_trx_amount

        dfR.at[index, 'max_usdt_amount'] = max_usdt_amount
        dfR.at[index, 'min_usdt_amount'] = min_usdt_amount
        dfR.at[index, 'average_usdt_amount'] = average_usdt_amount

        dfR.at[index, 'max_price'] = max_price
        dfR.at[index, 'min_price'] = min_price
        dfR.at[index, 'average_price'] = average_price


        # Calculate max, min, and average
        #max_transaction_count = max(transaction_counts)
        #min_transaction_count = min(transaction_counts)
        #average_transaction_count = sum(transaction_counts) / len(transaction_counts)

        # Update values in the DataFrame
        #dfR.at[index, 'max_transaction_count'] = max_transaction_count
        #dfR.at[index, 'min_transaction_count'] = min_transaction_count
        #dfR.at[index, 'average_transaction_count'] = average_transaction_count

        
        # Save the updated DataFrame to the same CSV file
        dfR.to_csv(file_path, index=False)
        print(i)
        i += 1
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
