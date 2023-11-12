import h5py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime


def calculate_average_price_per_sqm_and_listings(hdf5_file):
    website_data = {}  # Store data for each website

    # Open the HDF5 file
    with h5py.File(hdf5_file, "a") as hf:
        for website_name in hf:
            website_group = hf[website_name]
            website_dates = []  # Store dates for this website
            website_avg_prices = []  # Store average prices for this website
            website_listings = []  # Store listings count for this website
            print(f"Website: {website_name}")

            for date in website_group:
                if "_price" in date:
                    # Skip dataset names that end with "_price" (not date datasets)
                    continue

                price_data_name = f"{date}_price"
                listings_count_name = f"{date}_listings_count"

                if price_data_name not in website_group or listings_count_name not in website_group:
                    # Skip dates without both price and listings count data
                    continue

                price_data = website_group[price_data_name][:]
                listings_count = website_group[listings_count_name][()]

                sqm_data_name = f"{date}_square_meters"
                if sqm_data_name not in website_group:
                    # Skip dates without square meter data
                    continue

                sqm_data = website_group[sqm_data_name][:]

                # Convert the date string to a datetime object
                date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

                # Truncate the time portion of the datetime
                date = date.replace(hour=0, minute=0, second=0, microsecond=0)

                # Calculate the average price per square meter for the date
                if len(price_data) > 0 and len(sqm_data) > 0:
                    average_price_per_sqm = np.mean(price_data / sqm_data)
                    website_dates.append(date)
                    website_avg_prices.append(average_price_per_sqm)
                    website_listings.append(listings_count)
                    print(f"Date: {date}, Avg. Price/sqm: {average_price_per_sqm:.2f} EUR/sqm, Listings: {listings_count}")

            # Store the data for this website
            website_data[website_name] = (website_dates, website_avg_prices, website_listings)

    # Create two separate diagrams: one for price/sqm and one for listings count
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 10))

    for website_name, (dates, avg_prices, listings) in website_data.items():
        # Plot average price per square meter
        ax1.plot(dates, avg_prices, label=f"{website_name}", marker='o')
        ax1.set_ylabel("Avg Price per Sqm")
        ax1.set_title("Average Price per Sqm Over Time")

        # Plot listings count
        ax2.plot(dates, listings, label=f"{website_name}", marker='o')
        ax2.set_xlabel("Date")
        ax2.set_ylabel("Number of Listings")
        ax2.set_title("Number of Listings Over Time")

    # Set legend
    lines, labels = ax1.get_legend_handles_labels()
    ax1.legend(lines, labels, loc=0)

    # Format the date axis
    date_format = mdates.DateFormatter("%Y-%m-%d")
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_formatter(date_format)
    ax2.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax2.xaxis.set_major_formatter(date_format)

    plt.tight_layout()

    # Save the figure as an image
    plt.savefig("visualization.png")

    # Set y-axis limits
    ax1.set_ylim(0, 40)
    ax2.set_ylim(0, 70)

    # Show the figure
    plt.show()


if __name__ == "__main__":
    # Call the 'calculate_average_price_per_sqm_and_listings' function when the script is run
    hdf5_file = "scraped_data.h5"
    calculate_average_price_per_sqm_and_listings(hdf5_file)
