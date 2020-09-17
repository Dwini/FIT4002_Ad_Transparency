from time import sleep
import random
import base64
import logging

LOGGER = logging.getLogger()

def isElementClickable(self, element):
    # is element visible by styles
    if (not element.is_displayed()):
        return False
    return True

    # TODO check if behind anything
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


def full_page_screenshot(driver, url):
    original_size = driver.get_window_size()
    required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    driver.set_window_size(required_width, required_height)
    # elem.screenshot('/pageScreenshot/' + url + '.png')  # avoids scrollbar

    try:

        with open('pageScreenshots/' + str(random.randint(0, 10000)) + '.png', 'wb+') as fh:
            fh.write(base64.b64decode(driver.get_screenshot_as_base64()))

        LOGGER.info('printed full page')
    except:
        LOGGER.error('Full page screenshot failed')

    driver.set_window_size(original_size['width'], original_size['height'])


def random_wait_and_scroll(driver):
    # random wait and scroll action
    LOGGER.info('Waiting for page to load...')
    for i in range(3):
        sleep(random.randint(1, 3))
        driver.execute_script("window.scrollTo(0," + str(random.randint(50, 2000)) + ")")
        sleep(random.randint(1, 3))

if __name__ == '__main__':
    print('test')