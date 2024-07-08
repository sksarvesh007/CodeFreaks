import requests
import csv

# API link
api_link = "https://codeforces.com/api/contest.ratingChanges?contestId=1983"

# Fetch the data
response = requests.get(api_link)
data = response.json()

# Extract usernames
usernames = [entry['handle'] for entry in data['result']]

# Save to CSV
csv_file = "usernames.csv"
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['username'])  # Write the header
    for username in usernames:
        writer.writerow([username])

print(f"Usernames have been saved to {csv_file}")
