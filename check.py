import requests
import csv
from tqdm import tqdm
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Suppress only the single InsecureRequestWarning from urllib3 needed to bypass SSL verification warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Read usernames from usernames.csv
usernames = []
with open('usernames.csv', mode='r') as file:
    reader = csv.reader(file)
    header = next(reader)  # Read the header row
    for row in reader:
        usernames.append(row[0])

# Limit to the first 10 usernames for testing
usernames = usernames[:10]

# Initialize a list to hold the username and rating information
user_ratings = []

# Base URL for user info API
user_info_base_url = "https://codeforces.com/api/user.info?handles="

# Fetch rating for each username with tqdm progress bar
for username in tqdm(usernames, desc="Fetching user ratings"):
    user_info_api_link = f"{user_info_base_url}{username}&checkHistoricHandles=false"
    try:
        user_response = requests.get(user_info_api_link, verify=False)
        user_data = user_response.json()
        if user_data["status"] == "OK":
            rating = user_data["result"][0].get("rating", "N/A")
            user_ratings.append({"username": username, "rating": rating})
        else:
            user_ratings.append({"username": username, "rating": "N/A"})
    except requests.exceptions.SSLError as e:
        print(f"SSL error for user {username}: {e}")
        user_ratings.append({"username": username, "rating": "Error"})
    except Exception as e:
        print(f"An error occurred for user {username}: {e}")
        user_ratings.append({"username": username, "rating": "Error"})

# Write to the existing usernames.csv file
with open('usernames.csv', mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["username", "rating"])
    writer.writeheader()
    for user_rating in user_ratings:
        writer.writerow(user_rating)

print(f"Usernames and ratings for the first 10 users have been written to usernames.csv")
