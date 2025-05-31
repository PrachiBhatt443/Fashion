from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time
import requests
from pathlib import Path

# Function to download an image
def download_image(url, save_path):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Image saved to {save_path}")
        else:
            print(f"Failed to download image: {url}")
    except Exception as e:
        print(f"Error downloading image: {e}")

# Initialize WebDriver
driver = webdriver.Firefox()

try:
    # Open Instagram
    driver.get("https://www.instagram.com")

    # Wait for username & password fields
    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "username")))
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "password")))

    # Enter login details
    username.clear()
    username.send_keys("ayush_singh_0417")  # Replace with your username
    password.clear()
    password.send_keys("ayushsingh12345679639")  # Replace with your password

    # Click the login button
    login_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    login_button.click()

    # Wait for login to complete
    time.sleep(10)

    # Handle 'Not Now' popup if it appears
    try:
        # not_now_button = WebDriverWait(driver, 5).until(
        #     EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))
        # )
        not_now_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and contains(text(), 'Not')]"))
        )
        not_now_button.click()
    except:
        print("No 'Not Now' button appeared.")

    # Search for a hashtag
    time.sleep(5) 
    # Wait for the search icon (targeting the span containing 'Search')
    search_icon = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Search']"))
    )
    search_icon.click()
    
    # Wait for the search input box to appear
    searchbox = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']"))
    )
    searchbox.clear()
    searchbox.send_keys("#cat")  # Change the hashtag as needed
    time.sleep(3)
    searchbox.send_keys(Keys.RETURN)
    time.sleep(2)
    searchbox.send_keys(Keys.RETURN)

    # Wait for the hashtag page to load
    time.sleep(5)

    # Create a folder to save images
    save_dir = Path("instagram_images/cat")
    save_dir.mkdir(parents=True, exist_ok=True)

    # Scrape images
    images_scraped = 0
    SCROLL_PAUSE_TIME = 3
    last_height = driver.execute_script("return document.body.scrollHeight")

    while images_scraped < 50:  # Limit the number of images
        # Find image elements
        # image_elements = driver.find_elements(By.XPATH, "//img[contains(@class, 'FFVAD')]")
        image_elements = driver.find_elements(By.XPATH, "//img[contains(@src, 'cdninstagram')]")

        for img in image_elements:
            try:
                img_url = img.get_attribute("src")
                if img_url:
                    # Save the image
                    save_path = save_dir / f"image_{images_scraped}.jpg"
                    if not save_path.exists():  # Avoid re-downloading
                        download_image(img_url, save_path)
                        images_scraped += 1
                        if images_scraped >= 50:
                            break
            except Exception as e:
                print(f"Error processing image: {e}")

        # Scroll down to load more images
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("Reached the end of the page.")
            break
        last_height = new_height

    print(f"Scraping completed. Total images scraped: 1924")

finally:
    driver.quit()
