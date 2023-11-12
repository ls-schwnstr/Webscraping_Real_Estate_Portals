import requests
from bs4 import BeautifulSoup
import numpy as np


def crawl_immowelt():
    # Initialize empty lists to store scraped data
    price_list = []  # To store prices
    sqm_list = []    # To store square meter values
    listings_count = 0  # To keep track of the number of listings

    # Loop through multiple pages of listings (pages 1 to 4)
    for i in range(1, 5):
        # Define the base URL and construct the search URL with page number
        base_url = "https://www.immowelt.de"
        search_url = f"/suche/muenchen-au-haidhausen/wohnungen/mieten?d=true&sd=DESC&sf=RELEVANCE&sp={i}"

        # Send an HTTP GET request to the Immowelt website
        response = requests.get(base_url + search_url)

        # Check if the response status code is 200 (indicating a successful request)
        if response.status_code == 200:
            # Fetch the page content and parse it with BeautifulSoup
            page = requests.get(base_url + search_url)
            soup = BeautifulSoup(page.content, 'html.parser')

            # Find all HTML elements which contain listing information
            listings = soup.find_all("div", class_="KeyFacts-073db")

            # Iterate through each listing to extract information
            for listing in listings:
                # Extract the price information from the listing
                price_div = listing.find("div", {"data-test": "price"})
                price = price_div.text.strip()

                # Remove the Euro sign (€) and dot separators from the price
                price = price.replace("€", "").replace(".", "")

                # Convert the cleaned price string to an integer and add it to the price list
                price = int(price)
                price_list.append(price)

                # Extract the square meter information from the listing
                sqm_div = listing.find("div", {"data-test": "area"})
                sqm = sqm_div.text.strip()

                # Remove the unit "m²" and convert the cleaned square meter string to an integer
                sqm = sqm.replace(" m²", "")
                sqm = int(float(sqm.split(',')[0]))
                sqm_list.append(sqm)

                # Increment the listings count
                listings_count += 1
        else:
            # Print an error message if the HTTP request is not successful
            print("Fehler beim Abrufen von immowelt")

    # Convert the lists to NumPy arrays for further analysis
    price_array = np.array(price_list)
    sqm_array = np.array(sqm_list)

    # Return the scraped data and the total number of listings processed
    return price_array, sqm_array, listings_count
