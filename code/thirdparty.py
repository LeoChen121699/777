import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape and extract names from a given URL
def scrape_library_names(url, class_name):
    # Send HTTP request to the website with headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve {url}: {response.status_code}")
        return []
    
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all divs with the specified class
    divs = soup.find_all('div', class_=class_name)
    
    # Debugging: Print the first 5 divs to check the structure
    for div in divs[:5]:
        print(div.prettify())
    
    # Extract the text from the <a> tag within each div
    libraries = []
    for div in divs:
        a_tag = div.find('a')
        if a_tag:
            libraries.append(a_tag.text.strip())
    
    return libraries

# URLs
ad_networks_url = "https://www.appbrain.com/stats/libraries/ad-networks"
social_libs_url = "https://www.appbrain.com/stats/libraries/social-libs"
analytics_tools_url = "https://www.appbrain.com/stats/libraries/tag/analytics/android-analytics-libraries"

# Scraping the library names from the respective pages
ad_networks = scrape_library_names(ad_networks_url, 'td valign-middle')
social_libs = scrape_library_names(social_libs_url, 'td valign-middle')
analytics_tools = scrape_library_names(analytics_tools_url, 'td valign-middle')

# Determine the maximum length of the lists to avoid index errors
max_length = max(len(ad_networks), len(social_libs), len(analytics_tools))

# Extend lists to ensure they are the same length
ad_networks.extend([''] * (max_length - len(ad_networks)))
social_libs.extend([''] * (max_length - len(social_libs)))
analytics_tools.extend([''] * (max_length - len(analytics_tools)))

# Save to a CSV file with three columns
df = pd.DataFrame({
    'Ad Network': ad_networks,
    'Social Library': social_libs,
    'Analytics Tool': analytics_tools
})

df.to_csv('output/libraries_data.csv', index=False)

print("Data has been saved to libraries_data.csv")
