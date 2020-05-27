from selenium.webdriver import Chrome, ChromeOptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import names
import random
#from config import keys
#from database import Database
import sys

months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

def slow_typing(element, text):
   for character in text:
      element.send_keys(character)
      time.sleep(0.3)

def tab_entry(browser, strFirstname, strLastname, strUsername, strPassword):
    actions_create = ActionChains(browser)
    firstname = browser.find_element_by_id('firstName')
    firstname.click()
    actions_create = actions_create.send_keys(strFirstname)
    actions_create = actions_create.send_keys(Keys.TAB)
    actions_create = actions_create.send_keys(strLastname)
    actions_create = actions_create.send_keys(Keys.TAB)
    actions_create = actions_create.send_keys(strUsername)
    actions_create = actions_create.send_keys(Keys.TAB)
    actions_create = actions_create.send_keys(Keys.TAB)
    actions_create = actions_create.send_keys(strPassword)
    actions_create = actions_create.send_keys(Keys.TAB)
    actions_create = actions_create.send_keys(strPassword)
    actions_create.perform()


def find_entry(browser, strFirstname, strLastname, strUsername, strPassword):
    # Fill user's full name
    firstname = browser.find_element_by_id('firstName')
    lastname = browser.find_element_by_id('lastName')
    # username.send_keys('John Doe')
    slow_typing(firstname, strFirstname)
    slow_typing(lastname, strLastname)

    time.sleep(5)
    # Fill user's email ID
    username = browser.find_element_by_id('username')
    slow_typing(username, strUsername)

    time.sleep(5)
    # Fill user's password
    # Had to use xpath for this as there is no id on the actual textbox
    password = browser.find_elements_by_xpath('//*[@id="passwd"]/div[1]/div/div[1]/input')
    slow_typing(password, strPassword)

    time.sleep(5)

    # Fill user's password
    password = browser.find_element_by_xpath('//*[@id="confirm-passwd"]/div[1]/div/div[1]/input')
    slow_typing(password, strPassword)

    time.sleep(5)

def account_next(browser):
    # click on next
    next = browser.find_element_by_id('accountDetailsNext')
    next.click()

def personal_next(broswer):
    # click on next
    next = browser.find_element_by_id('personalDetailsNext')
    next.click()

def finalise(browser, day, month, year, gender):
    actions_finalise = ActionChains(browser)
    phone = browser.find_element_by_id('phoneNumberId')
    phone.click()
    actions_finalise = actions_finalise.send_keys(Keys.TAB)
    actions_finalise = actions_finalise.send_keys(Keys.TAB)
    actions_finalise = actions_finalise.send_keys(day)
    actions_finalise = actions_finalise.send_keys(Keys.TAB)
    actions_finalise = actions_finalise.send_keys(month)
    actions_finalise = actions_finalise.send_keys(Keys.TAB)
    actions_finalise = actions_finalise.send_keys(year)
    actions_finalise = actions_finalise.send_keys(Keys.TAB)
    actions_finalise = actions_finalise.send_keys(gender)
    actions_finalise.perform()
"""
def successful(db, strFirstname, strLastname, strUsername, strPassword, day, month, year, gender):
    # Insert some data.
    query = "INSERT INTO Bots(name, score) VALUES (strFirstname, strLastname, strUsername, strPassword, day, month, year, gender)"
    await db.execute(query=query)
    """

if __name__ == '__main__':
    container_build = False

    # if this is running in the container, import and create virtual display.
    if len(sys.argv) > 1 and sys.argv[1] == '-c':
        container_build = True
        from pyvirtualdisplay import Display

        # set xvfb display since there is no GUI in container.
        display = Display(visible=0, size=(800, 600))
        display.start()

    #print('connecting to database')
    #db = Database()


    # Visit chrome://version/ and copy profile path in place of '<chrome user profile>'
    #options = ChromeOptions().add_argument("--user-data-dir=<chrome user profile>")
    #browser = Chrome("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe", chrome_options=options)
    
    options = webdriver.ChromeOptions()
    options.add_argument(r"C:\Users\aiden\AppData\Local\Google\Chrome\User Data")
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    browser.get('https://accounts.google.com/signup/v2/webcreateaccount?continue=https%3A%2F%2Fwww.google.com%2Fwebhp%3Fhl%3Den%26sa%3DX%26ved%3D0ahUKEwjbldiThc7pAhVQwzgGHbC3Bw0QPAgH&hl=en&dsh=S-1458628831%3A1590376291910546&gmb=exp&biz=false&flowName=GlifWebSignIn&flowEntry=SignUp')

    # define options.
    #print('setting options')
    #chrome_options = Options()
    #chrome_options.add_argument('--no-sandbox')
    #chrome_options.add_argument('--disable-dev-shm-usage')

    #print('building session')
    #browser = webdriver.Chrome(options=chrome_options)
    #print('session built succesfully')

    time.sleep(10)
    # to accept cookie notification so that it doesn't interfere
    """cookie_cta = browser.find_element_by_id('accept-cookie-notification')
    cookie_cta.click()"""

    gender = 'female'
    if random.randint(0,1):
        gender = 'male'
    strFirstname = names.get_first_name(gender)
    strLastname = names.get_last_name()
    strUsername = strFirstname + '.' + strLastname + "." + str(random.randint(1000, 999999))
    strPassword = "Hi1234()"
    tab_entry(browser, strFirstname, strLastname, strUsername, strPassword)
    account_next(browser)
    time.sleep(10)
    strDay = str(random.randint(0, 28))
    strMonth = random.choice(months)
    strYear = str(random.randint(1940, 2004))
    finalise(browser, strDay, strMonth, strYear, gender[0])
    personal_next(browser)
    time.sleep(20)

    browser.close()

    # close display if in container.
    if container_build == True:
        display.stop()
