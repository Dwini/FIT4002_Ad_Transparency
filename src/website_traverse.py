from google_adsense_scrape import getGoogleAds
from random import random, randint
from time import sleep
from selenium.webdriver import Chrome


# removes div's that cause obstruction
def clear_dialogs(driver):

    # we want to be tracked
    # agree to any cookie requests
    accept_cookies(driver)

    # TODO see if clicking main content will escape any popups

    dialogs = driver.find_elements_by_css_selector("[id*=dialog]")

    #TODO Can dialogs be encapsulated in classes?
    #dialogs_with_class = driver.find_elements_by_css_selector("[class*=dialog]")

    for dialog in dialogs:
        try:
            driver.execute_script("arguments[0].remove();", dialog)
        except:
            print('error in removing dialog')


def accept_cookies(driver):

    agree_buttons = driver.find_elements_by_xpath(
        "//button[contains(string(), 'Agree') or contains(string(), 'Allow') or contains(string(), 'Accept')] ")
    for button in agree_buttons:
        try:
            button.click()
            sleep(random.random())
        except:
            print('Failed to click a button')


def click_local_links(driver):

    local_links = driver.find_elements_by_xpath("// a[not(contains(href, 'http'))]")

    for i in range(len(local_links)):
        try:
            if(isElementClickable):
                i = randint(0, len(local_links) - 1)
                print(local_links[i].location_once_scrolled_into_view)
                local_links[i].click()
                break
        except:
            print('Failed to click local link')

def isElementClickable(element):


    # is element visible by styles
    if (not element.isDisplayed):
        return False
    return True

    #TODO check if behind anything
    #
    # # is the element behind another element
    boundingRect = element.rect
    #
    # // adjust coordinates to get more accurate results
    # const left = boundingRect.left + 1;
    # const right = boundingRect.right - 1;
    # const top = boundingRect.top + 1;
    # const bottom = boundingRect.bottom - 1;
    #
    # if (document.elementFromPoint(left, top) !== element ||
    #     document.elementFromPoint(right, top) !== element ||
    #     document.elementFromPoint(left, bottom) !== element ||
    #     document.elementFromPoint(right, bottom) !== element) {
    #     return false;
    # }
    #
    # return true;
    # `;
    #
    # return element.getDriver().executeScript(SCRIPT, element);


webdriver = "chromedriver.exe"
driver = Chrome(webdriver)
#options = driver.ChromeOptions()
#options.add_argument("--start-maximized")
#driver = Chrome(chrome_options=options)

urls = open('urls.txt', 'r')


def random_wait_and_scroll(driver):
    # random wait and scroll action
    for i in range(3):
        sleep(randint(1, 3))
        driver.execute_script("window.scrollTo(0," + str(randint(50, 2000)) + ")")
        sleep(randint(1, 3))

#prevent them from getting in the way of ads
def remove_header(driver):

    headers = driver.find_elements_by_xpath("//div[contains(@class, 'header')] | //header[@class]")
    #//header[@class]" or
    for header in headers:
        try:
            driver.execute_script("arguments[0].remove();", header)
        except:
            print('error in removing dialog')

def search_keywords(self, webdriver, db, scrapping = False):
    print('seting up profile')
    num_links_to_visit = 2

    # this sections is for collecting Ads
    session = HTMLSession()
    ad_list = []  # empty list to store ad details

    # Get Keywords
    keywords = bot.getSearchTerms()

    # Go through all keywords
    sleep(1)
    links = []
    for keyword in keywords:
        url = 'http://www.google.com/'
        # Search Keyword using text box
        webdriver.get(url)
        sleep(2)
        search_box = webdriver.find_element_by_xpath("//input[@name='q']")
        search_box.send_keys(keyword)
        sleep(2)
        search_box.send_keys(Keys.RETURN)
        r = session.get('https://google.com/search?q=' + keyword) # For collecting ads
        sleep(10)

        if scrapping:
            # Get the 4 ads at the top
            ads = r.html.find('.ads-ad')

            for ad in ads:
                ad_link = ad.find('.V0MxL', first=True).absolute_links  # link to landing page
                ad_link = next(iter(ad_link))  # need this since the result from above is set
                ad_headline = ad.find('h3.sA5rQ', first=True).text  # headline of the ad
                ad_copy = ad.find('.ads-creative', first=True).text  # ad copy
                ad_list.append([keyword, ad_link, ad_headline, ad_copy])  # append data row to list

                # save ad to database
                db.save_ad(self.bot.getUsername(), ad_link, ad_headline, ad_copy)

        # wait until shows result
        results = webdriver.find_elements_by_css_selector('div.g')

        # save site visit to database
        db.log_action(self.bot.getUsername(), url, ['search'], keyword)

        try:
            for _ in range(num_links_to_visit):
                new = True
                link = results[_].find_element_by_tag_name("a")
                href = link.get_attribute("href")
                for link in links:
                    if href == link:
                        new = False
                if new:
                    links.append(href)
        except:
            print()

    if scrapping:
        df_ads = pd.DataFrame(ad_list, columns=['keyword', 'ad_link', 'ad_headline', 'ad_copy'])

        # timestamp so we dont overwrite old CSVs
        ts = time.time()

        # write out to CSV for reference
        df_ads.to_csv('top-ads-' + str(ts) + '.csv')

        # todo: save to database instead
        # Selenium loop thru dataframe to save PNGs into "screenshots" folder
        for index, row in df_ads.iterrows():
            print('Index: ' + str(index) + ', Ad Link: ' + row['ad_link'])
            webdriver.get(row['ad_link'])

            # save site visit to database
            db.log_action(self.bot.getUsername(), row['ad_link'], ['visit'])

            sleep(2)
            webdriver.save_screenshot('screenshots/' + str(index) + '.png')
            # webdriver.get_screenshot_as_file(str(index) + '.png')

    for link in links:
        try:
            webdriver.get(link)

            # save site visit to database
            db.log_action(self.bot.getUsername(), link, ['visit'])

            sleep(10)
        except:
            print()

for url in urls:

    driver.get(url)
    sleep(randint(10, 15))

    #dialogues can get in the way of ads and scrolling
    clear_dialogs(driver)
    remove_header(driver)

    random_wait_and_scroll(driver)

    getGoogleAds(driver)

    click_local_links(driver)

    random_wait_and_scroll(driver)





