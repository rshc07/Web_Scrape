import os
import requests
import pandas as pd

# Paths for input Excel file
input_excel = r"C:\Users\HEMACHANDRAN RS\Python\Web_Scrap\.venv\Category_Pro.xlsx"

# Check if the input file exists
if not os.path.exists(input_excel):
    print(f"Error: The file '{input_excel}' does not exist. Please check the path and try again.")
    exit()

# Read the Excel file
df = pd.read_excel(input_excel)

# Check if required columns exist
required_columns = ["Product Name", "Category", "Actual Price", "Image URL"]
if not all(col in df.columns for col in required_columns):
    print("Error: Missing required columns in the Excel file. Ensure 'Product Name', 'Category', 'Actual Price', and 'Image URL' exist.")
    exit()

# Create the main directory for images
base_image_folder = r"C:\Users\HEMACHANDRAN RS\Python\Web_Scrap\product_images"
os.makedirs(base_image_folder, exist_ok=True)

# Loop through the Excel rows and process images
for index, row in df.iterrows():
    product_name = row["Product Name"]
    category = row["Category"]
    actual_price = row["Actual Price"]
    image_url = row["Image URL"]

    # Skip if no image URL
    if pd.isna(image_url) or image_url == "N/A":
        continue

    # Create category-specific folder
    category_folder = os.path.join(base_image_folder, category)
    os.makedirs(category_folder, exist_ok=True)

    # Format filename: {Product Name} - {Price}.jpg
    safe_product_name = product_name.replace(" ", "_").replace("/", "-")[:50]  # Replace spaces and limit length
    safe_price = str(actual_price).replace("₹", "").replace(",", "")  # Remove currency symbols and commas
    image_filename = f"{safe_product_name} - {safe_price}.jpg"
    image_path = os.path.join(category_folder, image_filename)

    try:
        # Download the image
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(image_path, "wb") as img_file:
                img_file.write(response.content)
            print(f"✅ Image saved: {image_path}")
        else:
            print(f"⚠️ Failed to download: {image_url}")

    except Exception as e:
        print(f"❌ Error downloading image for {product_name}: {e}")

print("✅ All images have been downloaded and categorized successfully!")
