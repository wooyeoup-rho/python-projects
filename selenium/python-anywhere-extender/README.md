# Selenium Python Anywhere Extender

Small **Selenium** project that automates extending the expiry date of a scheduled task on **PythonAnywhere**.

The woes of a free user.

## How it works
1. Script launches a Chrome browser and navigates to [PythonAnywhere](https://www.pythonanywhere.com/)
2. It logs into the user account (in an .env file)
3. It navigates to the 'Task' section
4. It waits for the task to load and presses the 'Extend expiry' button
5. It confirms updated expiry date and closes.

## Technologies used
- Python
- Selenium
- ChromeDriver / WebDriver