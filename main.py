import requests
from bs4 import BeautifulSoup
import time

# Set headers to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Base URL with dynamic page number
base_url = "https://xxxxxxxxxxxxxxxxx={}"

page = 1  # Start from page 1

while True:
    url = base_url.format(page)
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve page {page}. Status code: {response.status_code}")
        break  # Stop if the request fails

    soup = BeautifulSoup(response.content, "html.parser")

    # Find all product containers on the current page
    product_containers = soup.find_all("div", class_="product details product-item-details")

    # If no products found, stop the loop (end of pagination)
    if not product_containers:
        print("No more products found. Stopping pagination.")
        break

    for product in product_containers:
        # Extract product name
        product_name_tag = product.find("h5", class_="product name product-item-name")
        product_name = product_name_tag.get_text(strip=True) if product_name_tag else "N/A"

        # Extract actual price
        special_price_tag = product.find("span", class_="special-price")
        actual_price = special_price_tag.find("span", class_="price").get_text(strip=True) if special_price_tag else "N/A"

        # Extract original price
        old_price_tag = product.find("span", class_="old-price")
        original_price = old_price_tag.find("span", class_="price").get_text(strip=True) if old_price_tag else "N/A"

        print(f"Product Name: {product_name}")
        print(f"Actual Price: {actual_price}")
        print(f"Original Price: {original_price}")
        print("-" * 50)

    page += 1  # Move to the next page
    time.sleep(2)  # Sleep to avoid getting blocked
