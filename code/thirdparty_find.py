import requests
from bs4 import BeautifulSoup
import pandas as pd

# Target URL
url = "https://www.appbrain.com/stats/libraries/development-tools"

# Send HTTP request to the website
response = requests.get(url)

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all divs with the class 'td valign-middle'
divs = soup.find_all('div', class_='td valign-middle')

# Extract the text from the <a> tag within each div
class_td = []
for div in divs:
    a_tag = div.find('a')
    if a_tag:
        class_td.append(a_tag.text.strip())

# Save to a CSV file (changed from to_excel to to_csv)
df = pd.DataFrame(class_td, columns=['Development Tools'])
df.to_csv('output/development.csv', index=False)

print("Ad networks have been saved to development.csv")
