from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import re
import time

driver=webdriver.Chrome(executable_path='C:/Users/avin/Downloads/chrome/chromedriver.exe')

class Amazon(object):
	def __init__(self,item_list):
		self.amazon_url="https://www.amazon.com"
		self.item_list=item_list
		self.driver=webdriver.Chrome(executable_path='C:/Users/avin/Downloads/chrome/chromedriver.exe')
		#self.driver.get(self.amazon_url)
	
	def search_items(self):
		for item in self.item_list:
			self.driver.get(self.amazon_url)
			search_input = self.driver.find_element_by_id("twotabsearchtextbox")
			search_input.send_keys(item)
			time.sleep(2)
			search_button = self.driver.find_element_by_xpath('//*[@id="nav-search"]/form/div[2]/div/input')
			search_button.click()
			time.sleep(2)
			
item=["Headphones"]
test=Amazon(item)
test.search_items()