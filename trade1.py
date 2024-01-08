from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize the WebDriver without specifying the executable_path
driver = webdriver.Edge()

# URL of the login page
url = "https://trader.zebacus.com/login"

# Open the website in Microsoft Edge
driver.get(url)

# Find the username input and enter your email
username_field = driver.find_element(By.NAME, "email")
username_field.send_keys("tester1@kappsoft.com")

# Find the password input and enter your password
password_field = driver.find_element(By.NAME, "password")
password_field.send_keys("Qwert@123")

# Find the login button and click on it
login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')")
login_button.click()

# Add a delay to keep the browser open for manual inspection
time.sleep(120)  # Adjust the time as needed

# Close the WebDriver when you're done
driver.quit()