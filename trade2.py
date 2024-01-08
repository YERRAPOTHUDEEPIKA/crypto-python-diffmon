from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set the path to the Edge WebDriver executable
edge_driver_path = r"D:\newbank\server\Scripts\msedgedriver.exe"

# Initialize the WebDriver with the specified service and options
driver = webdriver.Edge(executable_path=edge_driver_path)

# URL of the login page of the site you want to automate login.
url = "https://trader.zebacus.com/login"

# Open the website in Microsoft Edge
driver.get(url)

# Wait for the email input to be visible
email = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//input[@type='email']"))
)
email.send_keys("tester1@kappsoft.com")

# Wait for the password input to be visible
password = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//input[@type='password']"))
)
password.send_keys("Qwert@123")

# Find and click the "Log In" button
log_in = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[text()='Log In']"))
)
log_in.click()

# Find and click the "Trade" button
trade = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "(//div[@class='flex items-center justify-between'])[4]"))
)
trade.click()

# Close the WebDriver when you're done
driver.quit()