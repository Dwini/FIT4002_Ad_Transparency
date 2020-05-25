from selenium.webdriver import Chrome, ChromeOptions
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

EMAIL_ID = "john_doe_1998_14"

def slow_typing(element, text):
   for character in text:
      element.send_keys(character)
      time.sleep(0.3)

def tab_entry(browser):
    actions = ActionChains(browser)
    firstname = browser.find_element_by_id('firstName')
    firstname.click()
    actions = actions.send_keys('John')
    actions = actions.send_keys(Keys.TAB)
    actions = actions.send_keys('Doed')
    actions = actions.send_keys(Keys.TAB)
    actions = actions.send_keys('John1234Doed')
    actions = actions.send_keys(Keys.TAB)
    actions = actions.send_keys(Keys.TAB)
    actions = actions.send_keys('hi1234()')
    actions = actions.send_keys(Keys.TAB)
    actions = actions.send_keys('hi1234()')
    actions.perform()

def find_entry(browser):
    # Fill user's full name
    firstname = browser.find_element_by_id('firstName')
    lastname = browser.find_element_by_id('lastName')
    # username.send_keys('John Doe')
    slow_typing(firstname, 'John')
    slow_typing(lastname, 'Doe')

    time.sleep(5)
    # Fill user's email ID
    username = browser.find_element_by_id('username')
    slow_typing(username, EMAIL_ID)

    time.sleep(5)
    # Fill user's password
    # Had to use xpath for this as there is no id on the actual textbox
    password = browser.find_elements_by_xpath('//*[@id="passwd"]/div[1]/div/div[1]/input')
    slow_typing(password, 'hi1234()')

    time.sleep(5)

    # Fill user's password
    password = browser.find_element_by_xpath('//*[@id="confirm-passwd"]/div[1]/div/div[1]/input')
    slow_typing(password, 'hi1234()')

    time.sleep(5)

# Visit chrome://version/ and copy profile path in place of '<chrome user profile>'
"""options = ChromeOptions().add_argument("--user-data-dir=<chrome user profile>")

browser = Chrome("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe", chrome_options=options)
"""
options = webdriver.ChromeOptions()
options.add_argument(r"C:\Users\aiden\AppData\Local\Google\Chrome\User Data")
browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
browser.get('https://accounts.google.com/signup/v2/webcreateaccount?continue=https%3A%2F%2Fwww.google.com%2Fwebhp%3Fhl%3Den%26sa%3DX%26ved%3D0ahUKEwjbldiThc7pAhVQwzgGHbC3Bw0QPAgH&hl=en&dsh=S-1458628831%3A1590376291910546&gmb=exp&biz=false&flowName=GlifWebSignIn&flowEntry=SignUp')

time.sleep(10)
# to accept cookie notification so that it doesn't interfere
"""cookie_cta = browser.find_element_by_id('accept-cookie-notification')
cookie_cta.click()"""
tab_entry(browser)
time.sleep(10)
# click on next
next = browser.find_element_by_id('accountDetailsNext')
next.click()

time.sleep(20)



browser.close()
