from selenium.webdriver import Chrome, ChromeOptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import names
import random
import sys
from bot import Bot

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

class botCreator:
    def __init__(self):
        self.months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        self.gender = 'female' if random.randint(0, 1) else 'male'
        self.strFirstname = names.get_first_name(self.gender)
        self.strLastname = names.get_last_name()
        self.strUsername = self.strFirstname + '.' + self.strLastname + "." + str(random.randint(1000, 999999))
        self.strPassword = "Hi1234()"
        self.strDay = str(random.randint(0, 28))
        self.strMonth = random.choice(months)
        self.strYear = str(random.randint(1940, 2004))
        self.curBot = Bot(self.strFirstname, self.strLastname, self.strUsername, self.strPassword, self.gender)

        # todo: move this to app python file v
        options = webdriver.ChromeOptions()
        # need to replace argument with actual one we will be using
        options.add_argument(r"C:\Users\aiden\AppData\Local\Google\Chrome\User Data")
        browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        browser.get(
            'https://accounts.google.com/signup/v2/webcreateaccount?continue=https%3A%2F%2Fwww.google.com%2Fwebhp%3Fhl%3Den%26sa%3DX%26ved%3D0ahUKEwjbldiThc7pAhVQwzgGHbC3Bw0QPAgH&hl=en&dsh=S-1458628831%3A1590376291910546&gmb=exp&biz=false&flowName=GlifWebSignIn&flowEntry=SignUp')

        # define options.
        # print('setting options')
        # chrome_options = Options()
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--disable-dev-shm-usage')

        # print('building session')
        # browser = webdriver.Chrome(options=chrome_options)
        # print('session built succesfully')

        time.sleep(10)
        # to accept cookie notification so that it doesn't interfere
        """cookie_cta = browser.find_element_by_id('accept-cookie-notification')
        cookie_cta.click()"""
        # todo: move this to app python file ^

        self.tab_entry(browser)
        self.accountNext(browser)
        time.sleep(10)
        self.finalise(browser)
        self.personalNext(browser)
        time.sleep(20)
        browser.close()
        self.successful()

    def tabEntry(self, browser):
        actions_create = ActionChains(browser)
        firstname = browser.find_element_by_id('firstName')
        firstname.click()
        actions_create = actions_create.send_keys(self.bot.getFirstname())
        actions_create = actions_create.send_keys(Keys.TAB)
        actions_create = actions_create.send_keys(self.bot.getLastname())
        actions_create = actions_create.send_keys(Keys.TAB)
        actions_create = actions_create.send_keys(self.bot.getUsername())
        actions_create = actions_create.send_keys(Keys.TAB)
        actions_create = actions_create.send_keys(Keys.TAB)
        actions_create = actions_create.send_keys(self.bot.getPassword())
        actions_create = actions_create.send_keys(Keys.TAB)
        actions_create = actions_create.send_keys(self.bot.getPassword)
        actions_create.perform()

    def accountNext(self, browser):
        # click on next
        next = browser.find_element_by_id('accountDetailsNext')
        next.click()

    def personalNext(self, browser):
        # click on next
        next = browser.find_element_by_id('personalDetailsNext')
        next.click()

    def finalise(self, browser):
        actions_finalise = ActionChains(browser)
        phone = browser.find_element_by_id('phoneNumberId')
        phone.click()
        actions_finalise = actions_finalise.send_keys(Keys.TAB)
        actions_finalise = actions_finalise.send_keys(Keys.TAB)
        actions_finalise = actions_finalise.send_keys(self.bot.getBirthDay())
        actions_finalise = actions_finalise.send_keys(Keys.TAB)
        actions_finalise = actions_finalise.send_keys(self.bot.getBirthMonth())
        actions_finalise = actions_finalise.send_keys(Keys.TAB)
        actions_finalise = actions_finalise.send_keys(self.bot.getBirthYear())
        actions_finalise = actions_finalise.send_keys(Keys.TAB)
        actions_finalise = actions_finalise.send_keys(self.bot.getGender())
        actions_finalise.perform()

    def successful(self):
        #Need to finish adding new bots into the database
        # Insert some data.
        """query = "INSERT INTO Bots(name, score) VALUES (strFirstname, strLastname, strUsername, strPassword, day, month, year, gender)"
        await db.execute(query=query)"""