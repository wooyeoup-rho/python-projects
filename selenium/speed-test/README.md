# Selenium Internet Speed Complainer

Small **Selenium** project that tests the user's current internet speed and goes on X (previously Twitter) to rant about it.

## How it works
1. Script launches a Chrome browser and navigates to [Speedtest by Ookla](https://www.speedtest.net)
2. It starts the speed test and waits for it to finish, saving the reported upload and download speeds
3. It navigates to [X (goodbye Twitter)](x.com/) and logs in to the users account (from an .env file)
4. It drafts a complaint reporting the observed upload/download speed and tweets about it

## Technologies used
- Python
- Selenium
- ChromeDriver / WebDriver