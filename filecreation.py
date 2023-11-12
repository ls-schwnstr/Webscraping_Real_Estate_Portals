import logging
import h5py
from datetime import datetime
from wggesucht import crawl_wg_gesucht
from immowelt import crawl_immowelt

# Configure logging
logging.basicConfig(filename='web_crawler.log', level=logging.INFO, format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

price_list, sqm_list, price_per_sqm_list, website_list = crawl_wg_gesucht()

price_list2, sqm_list2, price_per_sqm_list2, website_list2 = crawl_immowelt()

#price_list.extend(price_list2)
#sqm_list.extend(sqm_list2)
#price_per_sqm_list.extend(price_per_sqm_list2)
#website_list.extend(website_list2)


def file_creation():
    # Save the data to an HDF5 file
    file_name = "scraped_data.h5"
    current_datetime = datetime.now().strftime("%Y-%m-%d")

    with h5py.File(file_name, "a") as hf:
        # Check if the group for each website exists, and create it if it doesn't
        for website in website_list + website_list2:
            if website not in hf:
                hf.create_group(website)

        # Create a compound dataset for each website and date
        for website, prices, sqms, price_per_sqms in zip(website_list + website_list2,
                                                         [price_list, price_list2],
                                                         [sqm_list, sqm_list2],
                                                         [price_per_sqm_list, price_per_sqm_list2]):
            website_group = hf[website]

            if current_datetime in website_group:
                # If the group for the current date already exists, create a new dataset for the day
                current_len = len(website_group[current_datetime]["price"])
                new_len = current_len + len(prices)

                website_group[current_datetime].create_dataset("price", data=prices)
                website_group[current_datetime].create_dataset("square_meters", data=sqms)
                website_group[current_datetime].create_dataset("price_per_square_meter", data=price_per_sqms)
            else:
                # If the group for the current date doesn't exist, create it and datasets for the day
                data_group = website_group.create_group(current_datetime)
                data_group.create_dataset("price", data=prices)
                data_group.create_dataset("square_meters", data=sqms)
                data_group.create_dataset("price_per_square_meter", data=price_per_sqms)

    # Log the successful scrape
    for website in website_list + website_list2:
        logging.info(f"Scrape successful {website} for {current_datetime}")



if __name__ == "__main__":
    file_creation()
