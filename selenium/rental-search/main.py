import pandas
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime

# CONSTANTS
LISTING_ENDPOINT = "https://rentals.ca/"
SEARCH_LOCATION = "Montreal"

# DRIVER
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

try :
    # Home Page
    driver.get(LISTING_ENDPOINT)
    wait.until(EC.title_contains("Rentals.ca"))

    container = driver.find_element(By.CLASS_NAME, "navbar-main__search")
    driver.execute_script("arguments[0].style.display = 'block';", container)
    assert container.get_attribute("style") == "display: block;", "Container display was not set to block"

    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "search-control__input")))
    address_input = driver.find_element(By.CLASS_NAME, value="search-control__input")

    address_input.click()
    address_input.send_keys(SEARCH_LOCATION)

    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "search-main__result-name")))
    address_input.send_keys(Keys.RETURN)

    # Listing
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "listing-card-container")))

    type_button = driver.find_element(By.XPATH, value="//button[text()='Type ']")
    assert type_button, "Type filter button was not found"
    type_button.click()

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[title='All Apartments']")))
    apartments_button = driver.find_element(By.CSS_SELECTOR, value="label[title='All Apartments']")
    apartments_button.click()

    wait.until(EC.url_contains("/all-apartments"))

    # Gets listing information
    listing_cards = driver.find_elements(By.CLASS_NAME, value="listing-card-container")
    listing_titles = []
    listing_prices_lower = []
    listing_prices_upper = []
    listing_links = []

    for listing in listing_cards:
        title = listing.find_element(By.CLASS_NAME, value="listing-card__title")
        listing_titles.append(title.text)

        price = listing.find_element(By.CLASS_NAME, value="listing-card__price")
        cleaned_price = price.text.replace("$", "").replace(" ", "").split("-")
        listing_prices_lower.append(cleaned_price[0])
        if len(cleaned_price) == 2:
            listing_prices_upper.append(cleaned_price[1])
        else:
            listing_prices_upper.append("-")

        link = listing.find_element(By.CLASS_NAME, value="listing-card__details-link")
        listing_links.append(link.get_attribute("href"))

    today = datetime.strftime(datetime.today(), "%Y-%m-%d")
    dates = [today] * len(listing_titles)

    data_dict = {
        "timestamp": dates,
        "property_name": listing_titles,
        "price_lower": listing_prices_lower,
        "price_upper": listing_prices_upper,
        "url": listing_links
    }
    data_frame = pandas.DataFrame(data_dict)
    data_frame.to_csv("data.csv")

finally:
    driver.quit()