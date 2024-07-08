import requests
from bs4 import BeautifulSoup

with open('website.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

pagination = soup.find('div', class_='pagination')
page_numbers = [int(span['pageindex']) for span in pagination.find_all('span', class_='page-index')]
highest_page_number = max(page_numbers)

profiles = []

for page in range(1, highest_page_number + 1):
    page_url = f'https://codeforces.com/contestRegistrants/1983/page/{page}'
    
    # Fetch and parse the HTML content of the page
    response = requests.get(page_url)
    if response.status_code == 200:
        page_html = response.text
        page_soup = BeautifulSoup(page_html, 'html.parser')
        
        # Extract all Codeforces profiles from the page
        for link in page_soup.find_all('a', href=True):
            href = link['href']
            if '/profile/' in href:
                profiles.append(href)
    else:
        print(f"Failed to retrieve page {page}. Status code: {response.status_code}")

# Remove duplicates
profiles = list(set(profiles))

# Step 3: Save the profiles to a text file
with open('codeforces_profiles.txt', 'w', encoding='utf-8') as file:
    for profile in profiles:
        file.write(f"{profile}\n")

print(f"Profiles have been extracted from page 1 to {highest_page_number} and saved to codeforces_profiles.txt.")
