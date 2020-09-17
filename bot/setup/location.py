from geopy.geocoders import Nominatim
from time import sleep

def set_location(driver, location):
    """
    Sets driver location to given lat/lon values.
        driver: Selenium driver
        location: Dictionary of the form { 'lat': ..., 'lon': ... }
    """
    locator = Nominatim(user_agent="google")
    coordinates = "%f, %f" % (location['lat'], location['lon'])
    loc_info = locator.reverse(coordinates)
    print('>> Attempting to change browser location')
    print('\t>> Spoofing location: %s' % loc_info.raw['display_name'])

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

    # Click button to use precise location
    driver.get('https://google.com/search?q=google')
    sleep(2)
    try:
        location_btn = driver.find_elements_by_xpath('//a[@id="eqQYZc"]')[0]    # TODO: change how this works. id could change
        location_btn.click()
    except:
        pass
    sleep(2)
    
    # Attempt to confirm location change
    try: 
        print('\t>> Location as seen by Google: %s' % driver.find_elements_by_xpath('//span[@id="Wprf1b"]')[0].text)
    except:
        print('\t>> Could not confirm new location. Assuming location changed successfully')