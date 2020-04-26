from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from time import sleep, strftime
from random import randint

""" Can only use chrome 79"""
chromedriver_path = 'C:/Users/aiden/Downloads/chromedriver_win32/chromedriver.exe'
# Change this to your own chromedriver path!
webdriver = webdriver.Chrome(executable_path=chromedriver_path)
sleep(2)
webdriver.get('https://www.google.com')
sleep(3)

""" Need to finalise the finding of the element"""
search_box = webdriver.find_element_by_class_name("#tsf > div:nth-child(2) > div.A8SBwf > div.RNNXgb > div > div.a4bIc > input")
search_box.send_keys('democrat')

""" Need to finalise the finding of the element"""
button_search = webdriver.find_element_by_css_selector('#tsf > div:nth-child(2) > div.A8SBwf > div.FPdoLc.tfB0Bf > center > input.gNO89b')
button_search.click()
sleep(5)

first_link = webdriver.find_element_by_css_selector('#rso > div:nth-child(12) > div > div > div.jGGQ5e > div > a > div.PpBGzd.YcUVQe.MUxGbd.v0nnCb')
first_link.click()
