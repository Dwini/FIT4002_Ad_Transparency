import os

from driver.driver import create_driver, create_driver_with_proxy
from driver.session import get_session
from driver.location import set_location

def get_driver(position=None):
    driver = None
    if os.getenv('USE_PROXIES') != "1":
        driver = create_driver()
    else:
        driver = create_driver_with_proxy(position)

    set_location(driver, position)

    return driver