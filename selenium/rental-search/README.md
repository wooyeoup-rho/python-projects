# Selenium Rental Search Automation

Small **Selenium** project that scrapes the apartment rental information for a particular area and creates a .csv with the relevant information.

## How it works
1. Script launches a Chrome browser and navigates to a rental listing site (currently [Rentals.ca](https://rentals.ca/))
2. It enters the city in the input form
3. It applies the necessary filters and waits for the information to update
4. It scrapes the data in the first page of results
5. Uses [pandas](https://pandas.pydata.org) to create a .csv containing the results

## Technologies used
- Python
- Selenium
- ChromeDriver / WebDriver
- pandas