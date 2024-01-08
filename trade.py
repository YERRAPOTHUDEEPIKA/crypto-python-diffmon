# import webbrowser

# url = "https://trader.zebacus.com/login"
# webbrowser.open(url)

# from urllib.request import urlopen

# url = "https://trader.zebacus.com/login"
# web_url = urlopen(url)

# # You can now work with the 'web_url' object, for example, reading its content
# content = web_url.open()
# print(content)
# import webbrowser

# url = "https://trader.zebacus.com/login"
# webbrowser.open(url)


# Used to import the webdriver from selenium
from selenium import webdriver
import os
 
# Get the path of chromedriver which you have installed
def startBot(username, password, url):
    # Specify the path to the ChromeDriver executable
    chromedriver_path = r'D:\newbank\server\Scripts\chromedriver\chromedriver.exe'

    # Giving the path of chromedriver to selenium webdriver
    driver = webdriver.Chrome(executable_path=chromedriver_path)

    # Opening the website in Chrome.
    driver.get(url)

    # Find the id or name or class of
    # username by inspecting on username input
    email = driver.find_element_by_xpath("//input[@type='email']")
    email.send_keys(username)

    # Find the password by inspecting on password input
    password_input = driver.find_element_by_xpath("//input[@type='password']")
    password_input.send_keys(password)  # Provide your password here

    # Click on submit
    login_button = driver.find_element_by_css_selector("span:contains('Log In')")
    login_button.click()

# Driver Code
# Enter below your login credentials
username = "tester1@kappsoft.com"
password = "Qwert@123"

# URL of the login page of the site
# which you want to automate login.
url = "https://trader.zebacus.com/login"

# Call the function
startBot(username, password, url)
