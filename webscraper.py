import pandas as pd
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from requests_html import HTMLSession
from time import sleep

class bot:
    def __init__(self, name, email, password, status):
        self.name = name
        self.email = email
        self.password = password
        self.status = status

def scrape_ads(bot, webdriver):
    session = HTMLSession()

    ad_list = [] #empty list to store ad details

    # Login
    webdriver.get('https://www.google.com/accounts/Login?hl=en&continue=http://www.google.com/')
    sleep(5)
    webdriver.find_element_by_id('identifierId').send_keys(bot.email)
    webdriver.find_element_by_xpath('//*[@id="identifierNext"]').click()
    sleep(5)
    webdriver.find_element_by_css_selector("input[type=password]").send_keys(bot.password)
    webdriver.find_element_by_id('passwordNext').click()
    sleep(5)

    # Get Keywords
    keywords = pd.read_csv(bot.status + '_keywords.csv', index_col =None, header=0 )
    # Go through all keywords
    sleep(1)
    for keyword in keywords.Keyword:
        """
        # Search Keyword using text box
        webdriver.get('http://www.google.com/')
        sleep(2)
        search_box = webdriver.find_element_by_xpath("//input[@name='q']")
        search_box.send_keys(keyword)
        sleep(2)
        search_box.send_keys(Keys.RETURN)
        sleep(2)
        page = webdriver
        """
        webdriver.get('https://google.com/search?q=' + keyword)
        r = session.get('https://google.com/search?q=' + keyword)
        sleep(2)
        # Get the 4 ads at the top
        ads = r.html.find('.ads-ad')

        for ad in ads:
            ad_link = ad.find('.V0MxL', first=True).absolute_links #link to landing page
            ad_link = next(iter(ad_link)) #need this since the result from above is set
            ad_headline = ad.find('h3.sA5rQ', first=True).text #headline of the ad
            ad_copy = ad.find('.ads-creative', first=True).text #ad copy
            ad_list.append([keyword, ad_link, ad_headline, ad_copy]) #append data row to list

    df_ads = pd.DataFrame(ad_list, columns = ['keyword', 'ad_link', 'ad_headline', 'ad_copy'])

    #timestamp so we dont overwrite old CSVs
    ts = time.time()
    #write out to CSV for reference
    df_ads.to_csv('top-ads-'+str(ts)+'.csv')

    #Selenium loop thru dataframe to save PNGs into "screenshots" folder
    for index, row in df_ads.iterrows():
        print('Index: ' + str(index) + ', Ad Link: ' + row['ad_link'])
        webdriver.get(row['ad_link'])
        webdriver.save_screenshot('screenshots/'+str(index)+'.png')

bot = bot('Phill', 'phillfranco44@gmail.com', 'pF1234()', 'democrat')
# Open chrome
webdriver = webdriver.Chrome(ChromeDriverManager().install())
scrape_ads(bot, webdriver)
