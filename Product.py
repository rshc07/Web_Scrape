import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Set headers to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Base URL with dynamic page number
base_url = "https://xxxxxxxxxxxxxxxxx={}"
page = 1  # Start from page 1

# List to store product data
product_list = []

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

        # Extract image URL
        product_top = product.find_previous("div", class_="product-top")  # Go back to find product image
        image_tag = product_top.find("img", class_="img-responsive product-image-photo img-thumbnail lazy") if product_top else None
        image_url = image_tag["data-original"] if image_tag and "data-original" in image_tag.attrs else "N/A"

        # Append to list
        product_list.append({
            "Product Name": product_name,
            "Actual Price": actual_price,
            "Original Price": original_price,
            "Image URL": image_url
        })

    print(f"Page {page} scraped successfully.")
    page += 1  # Move to the next page
    time.sleep(2)  # Sleep to avoid getting blocked

# Convert data to a DataFrame and save as Excel
df = pd.DataFrame(product_list)
df.to_excel("products.xlsx", index=False)

print("Data successfully saved to products.xlsx")
