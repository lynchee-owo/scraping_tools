import requests
import json
import html
import time

# Load existing data
with open("formattedDb.json", "r") as read_file:
    data = json.load(read_file)

calls = 0
# Process each coin
for coin in data:
    if calls >= 15:
        # Write the updated data back to the file before going to sleep
        with open("formattedDb.json", "w") as write_file:
            json.dump(data, write_file, indent=4)
        # wait for 80 seconds before the next cycle
        time.sleep(80)
        calls = 0

    # Call coingecko API to get coin info
    if coin['API id'] != "" and coin['API id'] != []:
        if coin['description'] == "":
            calls += 1
            print(calls)
            response = requests.get(f"https://api.coingecko.com/api/v3/coins/{coin['API id']}")
            coin_info = response.json()

            # Extract and clean up description
            if 'description' in coin_info:
                html_desc = coin_info['description']['en']
                clean_desc = html.unescape(html_desc)
                if clean_desc != "":
                    coin['description'] = clean_desc
                else:
                    coin['description'] = "description not available"
            else:
                print("no description: ", coin['API id'])
        else:
            continue
    else:
        coin['description'] = ""

# Write the updated data back to the file one last time after all coins have been processed
with open("formattedDb.json", "w") as write_file:
    json.dump(data, write_file, indent=4)