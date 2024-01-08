from selenium import webdriver

url = "https://trader.zebacus.com/login"
username = "tester1@kappsoft.com"
password = "Qwert@123"

# Set up the Chrome web driver
driver = webdriver.Chrome()

# Open the website
driver.get(url)

# Find the username and password input fields and the login button
username_field = driver.find_element_by_name("username")  # Replace with the actual name or id of the username input field
password_field = driver.find_element_by_name("password")  # Replace with the actual name or id of the password input field
login_button = driver.find_element_by_name("submit")  # Replace with the actual name or id of the login button

# Enter the username and password
username_field.send_keys(username)
password_field.send_keys(password)

# Click the login button
login_button.click()

# Optionally, you can add a delay to ensure the page has loaded or see the result before the browser closes
import time
time.sleep()  # Wait for 5 seconds

# Close the browser
driver.quit()
