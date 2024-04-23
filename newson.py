import requests
import time
from random import randint

def scrape_website(url):
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
        # Add more user agents as needed
    ]

    headers = {
        "User-Agent": user_agents[randint(0, len(user_agents) - 1)],
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Process the response content here

        return response.text

    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

# Example usage
url = "https://www.smartprix.com/laptops/msi-brand/price-below_80000"
html_content = scrape_website(url)
if html_content:
    print("Successfully scraped the website.")
else:
    print("Failed to scrape the website.")
