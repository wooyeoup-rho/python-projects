from dotenv import load_dotenv, dotenv_values
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random

# CONSTANTS
load_dotenv()
config = dotenv_values(".env")

USERNAME = config.get("TWITTER_USERNAME")
PASSWORD = config.get("TWITTER_PASSWORD")
SPEEDTEST_ENDPOINT = "https://www.speedtest.net"
TWITTER_ENDPOINT = "https://x.com/i/flow/login"

# DRIVER
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 60*3)

try:
    # Speed Test
    driver.get(SPEEDTEST_ENDPOINT)

    wait.until(EC.title_contains("Speedtest by Ookla"))

    ## Starts the test
    start_button = driver.find_element(By.CLASS_NAME, value="start-button")
    assert start_button, "Start button was not found"

    start_button.click()

    ## Waits for test to finish
    wait.until(EC.url_contains("result"))

    download_speed = driver.find_element(By.CLASS_NAME, value="download-speed").text
    upload_speed = driver.find_element(By.CLASS_NAME, value="upload-speed").text

    assert download_speed, "Download speed result text was not found"
    assert upload_speed, "Upload speed result text was not found"

    # Twitter (X)
    driver.get(TWITTER_ENDPOINT)

    ## Login
    wait.until(EC.element_to_be_clickable((By.NAME, "text")))
    user_input = driver.find_element(By.NAME, value="text")
    assert user_input, "User input field was not found"
    user_input.send_keys(USERNAME)

    next_button = driver.find_element(By.XPATH, value="//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]")
    assert next_button, "Next button was not found"
    next_button.click()

    wait.until(EC.visibility_of_element_located((By.NAME, "password")))
    password_input = driver.find_element(By.NAME, value="password")
    password_input.send_keys(PASSWORD)

    login_button = driver.find_element(By.CSS_SELECTOR, value="button[data-testid='LoginForm_Login_Button']")
    assert login_button, "Login button was not found"
    login_button.click()

    ## Home
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='tweetTextarea_0']")))

    tweet_input = driver.find_element(By.CSS_SELECTOR, value="div[data-testid='tweetTextarea_0']")
    tweet_input.click()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[aria-label='Everyone can reply']")))

    tweet_input.send_keys(f"Hey Generic Internet Provider, why is my internet speed {download_speed}down/{upload_speed}up when I pay for {random.randint(1, 1000)}up/{random.randint(1,1000)}down???")

    post_button = driver.find_element(By.CSS_SELECTOR, value="button[data-testid='tweetButtonInline']")
    assert post_button, "Post button was not found"
    post_button.click()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-testid='toast']")))

finally:
    driver.quit()