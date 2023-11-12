import requests
from bs4 import BeautifulSoup
import numpy as np
import re


def crawl_wohnungsboerse():
    # Initialize empty lists to store scraped data
    price_list = []          # To store prices
    sqm_list = []            # To store square meter values
    listings_count = 0      # To keep track of the number of listings

    # Loop through multiple pages of listings (pages 1 to 4)
    for i in range(1, 5):
        # Define the base URL and construct the search URL with page number
        base_url = "https://www.wohnungsboerse.net/"
        search_url = "searches/index?isSearch=1&country=DE&estate_marketing_types=miete%2C1&marketing_type=miete" \
                     "&estate_types%5B0%5D=1&cities%5B0%5D=Muenchen&districts%5B0%5D=Haidhausen&page=" + str(i)
        response = requests.get(base_url + search_url)

        # Check if the response status code is 200 (indicating a successful request)
        if response.status_code == 200:
            # Fetch the page content and parse it with BeautifulSoup
            page = requests.get(base_url + search_url)
            soup = BeautifulSoup(page.content, 'html.parser')

            # Find all HTML elements which contain listing information
            listings = soup.find_all("div", class_="p-4 sm:px-0 sm:pb-0 sm:col-span-6 lg:col-span-7")

            # Iterate through each listing to extract information
            for listing in listings:
                # Extract the price information from the listing
                price_element = listing.find("dd", class_="text-base font-bold", string=re.compile(r'€'))
                price_text = price_element.get_text(strip=True)

                # Extract numeric values from price_text and clean the price
                price = int(price_text.replace("€", "").replace(".", "").split(",")[0])

                # Append the cleaned price to the price list
                price_list.append(price)

                # Extract the square meter information from the listing
                sqm_element = listing.find("dd", class_="text-base font-bold", string=re.compile(r'm²'))
                sqm_text = sqm_element.get_text(strip=True)

                # Extract numeric values from sqm_text and clean the square meter
                sqm = int(sqm_text.replace("m²", "").replace(".", "").replace(",", ""))

                # Append the cleaned square meter value to the sqm list
                sqm_list.append(sqm)

                # Increment the listings count
                listings_count += 1
        else:
            # Print an error message if the HTTP request is not successful
            print("Error fetching data from the custom website")

    # Convert the lists to NumPy arrays for further analysis
    price_array = np.array(price_list)
    sqm_array = np.array(sqm_list)

    # Return the scraped data and the total number of listings processed
    return price_array, sqm_array, listings_count
