from geopy.geocoders import Nominatim
from time import sleep
import logging
import os

LOGGER = logging.getLogger()

def set_location(driver, location):
    """
    Sets driver location to given lat/lon values.
        driver: Selenium driver
        location: Dictionary of the form { 'lat': ..., 'lon': ... }
    """
    if os.getenv('CHANGE_LOCATION') != "1":
        return

    locator = Nominatim(user_agent="google")
    coordinates = "%f, %f" % (location['lat'], location['lon'])
    loc_info = locator.reverse(coordinates)
    LOGGER.info('Changing browser location...')
    LOGGER.info('Spoofing location: %s' % loc_info.raw['display_name'])

    # These are three different methods to spoof location
    driver.execute_cdp_cmd("Page.setGeolocationOverride", {
        "latitude": location['lat'],            # 32.585,       lat/lon for Warner Robins, 
        "longitude": location['lon'],           # -83.611,      Georgia, USA
        "accuracy": 100
    })
    driver.execute_script("window.navigator.geolocation.getCurrentPosition=function(success) {" +
        "var position = {\"coords\" : {\"latitude\": \"%s\",\"longitude\": \"%s\"}};" % (location['lat'], location['lon']) +
        "success(position);}")
    driver.execute_script("var positionStr=\"\";" +
        "window.navigator.geolocation.getCurrentPosition(function(pos){positionStr=pos.coords.latitude+\":\"+pos.coords.longitude});"+
        "return positionStr;")

    url = 'https://google.com/search?q=google'
    LOGGER.info('Opening: ' + url)
    driver.get(url)
    sleep(2)

    LOGGER.info('Clicking button to use precise location')
    try:
        location_btn = driver.find_elements_by_xpath('//a[@id="eqQYZc"]')[0]    # TODO: change how this works. id could change
        location_btn.click()
    except:
        LOGGER.warning('Could not click button')
        pass
    sleep(2)
    
    # Attempt to confirm location change
    try: 
        LOGGER.info('Location as seen by Google: %s' % driver.find_elements_by_xpath('//span[@id="Wprf1b"]')[0].text)
    except:
        LOGGER.warning('Could not confirm new location')
        LOGGER.warning('Assuming location changed successfully')