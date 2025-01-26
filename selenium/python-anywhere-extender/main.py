from dotenv import load_dotenv, dotenv_values
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# CONSTANTS
load_dotenv()
config = dotenv_values(".env")

EMAIL = config.get("EMAIL_ADDRESS")
PASSWORD = config.get("PYTHON_ANYWHERE_PWD")
ENDPOINT = "https://www.pythonanywhere.com/login/"

# DRIVER
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    # Navigates to login page
    driver.get(ENDPOINT)

    wait.until(EC.title_contains("Login"))
    assert "Login" in driver.title, "Page title does not match expected: Login"

    # Login
    username_field = driver.find_element(By.NAME, value="auth-username")
    password_field = driver.find_element(By.NAME, value="auth-password")
    submit_button = driver.find_element(By.CSS_SELECTOR, value="button[type='submit']")

    assert username_field, "Username input field was not found"
    assert password_field, "Password input field was not found"
    assert submit_button, "Submit button was not found"

    username_field.send_keys(EMAIL)
    password_field.send_keys(PASSWORD)

    assert username_field.get_attribute("value") == EMAIL, "Username was not input correctly"
    assert password_field.get_attribute("value") == PASSWORD, "Password was not input correctly"

    submit_button.click()

    # Dashboard
    wait.until(EC.title_contains("Dashboard"))
    assert "Dashboard" in driver.title, "Page title does not match expected: Dashboard"

    tasks_navigation_button = driver.find_element(By.ID, value="id_tasks_link")
    assert tasks_navigation_button, "Tasks navigation button was not found"
    tasks_navigation_button.click()

    # Tasks
    wait.until(EC.title_contains("Tasks"))
    assert "Tasks" in driver.title, "Page title does not match expected: Tasks"

    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "extend_scheduled_task")))
    expiry_date = driver.find_element(By.CLASS_NAME, value="scheduled_tasks_expiry").text
    extend_expiry_button = driver.find_element(By.CLASS_NAME, value="extend_scheduled_task")

    assert expiry_date, "Expiry date data was not found"
    assert extend_expiry_button, "Extend expiry button was not found"

    extend_expiry_button.click()

    """
    TEST for tmr - want to check if there's a way to ensure it was successfully clicked:
    
    Add this to console to freeze (enter debugger) after clicking on the button:
        document.querySelector('button.extend_scheduled_task').addEventListener('click', () => {
            debugger;
        });
    
    - Could just check if the date is different. Would fail if run multiple times on the same day though.
    """
    # wait.until(lambda driver: extend_expiry_button.get_attribute("disabled") is not None)
    # assert extend_expiry_button.get_attribute("disabled") == "", "Button is not disabled after clicking"
    #
    # wait.until(lambda driver: extend_expiry_button.get_attribute("disabled") is None)
    # assert extend_expiry_button.get_attribute("disabled") is None, "Button is not enabled after clicking"

    new_expiry_date = driver.find_element(By.CLASS_NAME, value="scheduled_tasks_expiry").text

    assert new_expiry_date >= expiry_date, "Extension not successfully applied"

finally:
    driver.quit()
