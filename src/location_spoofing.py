from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

if __name__ == '__main__':
    container_build = False

    # if this is running in the container, import and create virtual display.
    if len(sys.argv) > 1 and sys.argv[1] == '-c':
        container_build = True
        from pyvirtualdisplay import Display

        # set xvfb display since there is no GUI in container.
        display = Display(visible=0, size=(800, 600))
        display.start()

    # need to go to a web page so that bot can click on button to
    # use precise location
    driver.get('https://google.com/search?q=wikipedia')

    # set location as Warner Robins, Georgia, USA
    driver.execute_cdp_cmd("Page.setGeolocationOverride", {
        "latitude": 32.585,
        "longitude": -83.611,
        "accuracy": 100
    })

    # click button to use precise location
    driver.find_element_by_id('eqQYZc').click()

    # if this page centers at the spoofed location then success
    driver.get("https://www.google.com/maps")

    # close display if in container.
    if container_build == True:
        display.stop()
