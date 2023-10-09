#Pahlavani
import pandas as pd
import requests
import sys
import datetime
import time

# Show progressbar
def progressbar(done, full=None, prefix="Downloaded"):
    if full is None:
        prog = (prefix + " " + str(done))
        sys.stdout.write('\r' + prog)
    else:
        prog = (prefix + " " + str(done) + "/" + str(full))
        sys.stdout.write('\r' + prog)

# Make a GET request to the API endpoint
UpTo = 20000
delay_in_seconds = 3
current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Format current datetime as string

for i in range(1, UpTo + 1):
    Cont = (i - 1) * 50
    URL = f"https://apilist.tronscanapi.com/api/account/list?sort=-balance&limit=50&start={Cont}"
    response = requests.get(URL)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Load JSON data from the response
        api_data = response.json()

        # Extract the list of dictionaries from the "accounts" key
        data = api_data.get("data", [])

        # Create a DataFrame from the extracted data
        df = pd.DataFrame(data)

        # Show progress and write to CSV file
        All = i * 50
        progressbar(All, UpTo * 50, "Downloaded")
        df.to_csv(f"outputf_{current_datetime}.csv", mode='a', header=True, index=True)

        # Add a delay every 3 iterations
        if i % 3 == 0 and i != UpTo:
            print(f"\nSleeping for {delay_in_seconds} seconds...")
            time.sleep(delay_in_seconds)
    else:
        print("Failed to retrieve data from the API. Status code:", response.status_code)
