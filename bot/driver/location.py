from geopy.geocoders import Nominatim
from time import sleep
import logging
import os

log = logging.getLogger()

def set_location_in_chrome(driver, location):
    log.info('Spoofing location in Chrome...')
    driver.execute_cdp_cmd('Page.setGeolocationOverride', {
        'latitude': location['lat'],            # 32.585,       lat/lon for Warner Robins,
        'longitude': location['lon'],           # -83.611,      Georgia, USA
        'accuracy': 100
    })
    driver.execute_script('window.navigator.geolocation.getCurrentPosition=function(success) {' +
        'var position = {"coords" : {"latitude": "%s","longitude": "%s"}};' % (location['lat'], location['lon']) +
        'success(position);' +
    '}')
    driver.execute_script(
        'var positionStr="";' +
        'window.navigator.geolocation.getCurrentPosition(function(pos){positionStr=pos.coords.latitude+":"+pos.coords.longitude});' +
        'return positionStr;'
    )

def check_location(driver):
    # Attempt to confirm location change
    url = 'https://google.com/search?q=google'
    log.info('Opening ' + url)
    driver.get(url)
    sleep(3)

    try:
        log.info('Location as seen by Google: %s' % driver.find_elements_by_xpath('//span[@id="Wprf1b"]')[0].text)
    except:
        log.warning('Could not confirm new location. Assuming location changed successfully')

"""
Sets driver location to given lat/lon values.
:param driver: Selenium driver
:param location: Dictionary of the form { 'lat': ..., 'lon': ... }
"""
def set_location(driver, location):
    locator = Nominatim(user_agent="google")
    coordinates = "%f, %f" % (location['lat'], location['lon'])
    loc_info = locator.reverse(coordinates)

    url = 'https://google.com/search?q=google'
    log.info('Opening ' + url)
    driver.get(url)
    sleep(3)

    log.info('Clicking button to use precise location')
    log.info('Spoofing Location: %s' % loc_info.raw['display_name'])
    try:
        # TODO: change how this works. id could change
        location_btn = driver.find_elements_by_xpath('//a[@id="eqQYZc"]')[0]
        location_btn.click()
    except:
        log.warning('Could not click button')
        pass

    check_location(driver)
