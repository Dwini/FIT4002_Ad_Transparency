from selenium.webdriver import Chrome, ChromeOptions
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time

EMAIL_ID = "john_doe_1998_14@gmail.com"

def slow_typing(element, text):
   for character in text:
      element.send_keys(character)
      time.sleep(0.3)

# Visit chrome://version/ and copy profile path in place of '<chrome user profile>'
options = ChromeOptions().add_argument("--user-data-dir=<chrome user profile>")

browser = Chrome("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe", chrome_options=options)
browser.get('http://gmail.com')

time.sleep(5)

# to accept cookie notification so that it doesn't interfere
"""cookie_cta = browser.find_element_by_id('accept-cookie-notification')
cookie_cta.click()"""

# Navigate to Signup Page
"""button = browser.find_element_by_id('signupModalButton')"""
button = browser.find_elements_by_xpath('//*[@id="ow284"]/div[2]')
button.click()

time.sleep(5)

# Fill user's full name
username = browser.find_element_by_id('user_fudll_name')
# username.send_keys('John Doe')
slow_typing(username, 'John Doe')

time.sleep(5)
# Fill user's email ID
email = browser.find_element_by_id('user_email_login')
slow_typing(email, EMAIL_ID)

time.sleep(5)
# Fill user's password
password = browser.find_element_by_id('user_password')

# Reads password from a text file because
# it's silly to save the password in a script.
with open('password.txt', 'r') as myfile:
       Password = myfile.read().replace('\n', '')
slow_typing(password, Password)

time.sleep(5)
# click on Terms and Conditions
toc = browser.find_element_by_name('terms_and_conditions')
toc.click()

# click on signup page
signupbutton = browser.find_element_by_id('user_submit')
signupbutton.click()

time.sleep(20)

browser.close()
