from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import time
import names
import random
from bot import Bot

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

class botCreator:
    def __init__(self, webdriver):
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
        self.webdriver = webdriver

        webdriver.get(
            'https://accounts.google.com/signup/v2/webcreateaccount?continue=https%3A%2F%2Fwww.google.com%2Fwebhp%3Fhl%3Den%26sa%3DX%26ved%3D0ahUKEwjbldiThc7pAhVQwzgGHbC3Bw0QPAgH&hl=en&dsh=S-1458628831%3A1590376291910546&gmb=exp&biz=false&flowName=GlifWebSignIn&flowEntry=SignUp')
        sleep(10)
        self.tab_entry(self)
        self.next(self)
        time.sleep(10)
        self.finalise(self)
        self.next(self)
        time.sleep(20)
        self.successful()

    def tabEntry(self):
        actions_create = ActionChains(self.webdriver)
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

    def next(self):
        actions_next = ActionChains(self.webdriver)
        actions_next = actions_next.send_keys(Keys.TAB)
        actions_next = actions_next.send_keys(Keys.TAB)
        actions_next.perform()

    def finalise(self):
        actions_finalise = ActionChains(self.webdriver)
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
