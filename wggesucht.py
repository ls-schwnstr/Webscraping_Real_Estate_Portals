import requests
from bs4 import BeautifulSoup
import numpy as np


def crawl_wggesucht():
    # Initialize empty lists to store scraped data
    price_list = []      # To store prices
    sqm_list = []        # To store square meter values
    listings_count = 0  # To keep track of the number of listings

    seen_listings = set()  # Create a set to track seen listings and avoid duplicates

    for i in range(1, 5):
        # Define the base URL and construct the search URL with page number
        base_url = "https://www.wg-gesucht.de"
        search_url = "/wohnungen-in-Muenchen.90.2.1." + str(i - 1) + ".html?offer_filter=1&city_id=90" \
                     "&sort_order=0&noDeact=1&categories%5B%5D=2&ot%5B%5D=2116"
        response = requests.get(base_url + search_url)

        # Check if the response status code is 200 (indicating a successful request)
        if response.status_code == 200:
            # Fetch the page content and parse it with BeautifulSoup
            page = requests.get(base_url + search_url)
            soup = BeautifulSoup(page.content, 'html.parser')

            # Find all listings in the page
            listings = soup.find_all('div', class_='wgg_card offer_list_item')

            for listing in listings:
                # Extract the description of the listing
                description_element = listing.find('div', class_='col-xs-11')
                if description_element is not None:
                    description = description_element.get_text()

                    if "Au-Haidhausen" in description:
                        # Extract price and square meters information from the listing
                        price_sqm_element = listing.find('div', class_='printonly').div
                        if price_sqm_element:
                            # Split price and square meters values using '|' as separator
                            price, sqm = price_sqm_element.get_text().strip().split('|')
                            price = price.strip().split('&euro;')[0].strip()
                            sqm = sqm.strip().split('&sup2;')[0].strip()

                            # Convert price to an integer, removing currency symbol and formatting
                            price = int(price.split(' ')[0].replace("€", "").replace(".", ""))

                            # Convert square meter to an integer, removing unit symbol and formatting
                            sqm = int(sqm.split(' ')[0].replace("m²", ""))

                            # Check if this listing (price and sqm pair) has been seen before
                            listing_key = (price, sqm)
                            if listing_key not in seen_listings:
                                seen_listings.add(listing_key)  # Mark the listing as seen
                                price_list.append(price)         # Append the price to the list
                                sqm_list.append(sqm)             # Append the square meter value to the list
                                listings_count += 1

    # Convert the lists to NumPy arrays for further analysis
    price_array = np.array(price_list)
    sqm_array = np.array(sqm_list)

    # Return the scraped data and the total number of unique listings processed
    return price_array, sqm_array, listings_count
