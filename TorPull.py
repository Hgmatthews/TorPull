import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import json
from urllib.parse import urljoin

# Directory where files will be downloaded
download_dir = os.path.abspath("downloads")

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set Chrome preferences for downloading files
chrome_prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", chrome_prefs)

# Add Tor proxy settings
chrome_options.add_argument('--proxy-server=socks5://127.0.0.1:9050')

# Set up the WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Ensure download directory exists
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Ask user for the URL
base_url = input("Please enter the base .onion URL: ").rstrip('/')
company_id = input("Please enter the company ID: ")

# Construct the API URL
api_url = f"{base_url}/companies/{company_id}/api/public/disclosures/{company_id}/dirs/"

# Function to download files
def download_files(url):
    try:
        # Use requests through Tor proxy
        proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
        
        print(f"Trying to access URL: {url}")
        response = requests.get(url, proxies=proxies, verify=False)
        response.raise_for_status()
        
        # Print raw response text for debugging
        print(f"Response content: {response.text[:500]}")  # Print first 500 characters
        
        # Check for JSON response
        content_type = response.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            try:
                data = response.json()
                if 'files' in data:
                    for file in data['files']:
                        file_url = urljoin(base_url, file['url'])
                        file_name = file['name']
                        print(f"Downloading: {file_name}")
                        
                        file_response = requests.get(file_url, proxies=proxies, verify=False)
                        file_response.raise_for_status()
                        
                        with open(os.path.join(download_dir, file_name), 'wb') as f:
                            f.write(file_response.content)
                        
                        print(f"Downloaded: {file_name}")
                
                if 'dirs' in data:
                    for dir in data['dirs']:
                        dir_url = urljoin(base_url, dir['url'])
                        print(f"Exploring directory: {dir['name']}")
                        download_files(dir_url)
            except json.JSONDecodeError:
                print("Error decoding JSON response")
        elif 'text/html' in content_type or 'text/plain' in content_type:
            print("Received HTML or plain text response")
            print(response.text)
        else:
            print("Unexpected content type. Not JSON, HTML, or plain text.")
        
    except requests.exceptions.SSLError as e:
        print(f"SSL Error occurred: {e}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while downloading: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Main execution
try:
    print(f"Accessing API endpoint: {api_url}")
    download_files(api_url)
    print("All downloads completed.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the browser
    driver.quit()
    print("Script completed.")
