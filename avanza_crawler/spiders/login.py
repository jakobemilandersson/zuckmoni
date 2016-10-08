#-*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
import string
import re
import pickle
import datetime
import os
import time
import logging
import sys
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import TextResponse 
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class LoginSpider(scrapy.Spider):

	name = "login_crawler"
	
	start_urls = [
		'https://www.avanza.se/aktier/lista.html',
	]
	custom_settings = {
        'DOWNLOAD_DELAY' : '1'
    }
	
	
	def __init__(self):
	
		caps = DesiredCapabilities.FIREFOX
		caps["marionette"] = True
		profile = webdriver.FirefoxProfile()                                    
		profile.set_preference("dom.forms.number", False)                       
		self.driver = webdriver.Firefox(profile)
		#self.driver = webdriver.Firefox()
		
	def parse(self, response):
		self.driver.get(response.url)
		
		login_but = WebDriverWait(self.driver, 10).until(
					EC.visibility_of_element_located((By.XPATH, '/html/body/header/div/div/div/div/div[2]/button/span'))
				)
				
		login_but.click()
		time.sleep(2)
		
		mob_bankid_but = WebDriverWait(self.driver, 10).until(
					EC.visibility_of_element_located((By.XPATH, '//*[@id="pjaxContent"]/div/div/div/aside/div/div/div/div[1]/div/a'))
				)												
		
		mob_bankid_but.click()
		time.sleep(2)
		mob_bankid_but.click()
		time.sleep(2)
		
		person_nr = WebDriverWait(self.driver, 10).until(
					EC.visibility_of_element_located((By.XPATH, '//*[@id="pjaxContent"]/div/div/div/aside/div/div/div/div[1]/div/div/div/div/div[2]/input'))
				)
				

		time.sleep(1)
		
		person_nr.send_keys("9503296338")
		
		login = WebDriverWait(self.driver, 10).until(
					EC.visibility_of_element_located((By.XPATH, '//*[@id="pjaxContent"]/div/div/div/aside/div/div/div/div[1]/div/div/div/div/div[2]/button'))
				)
				
		login.click()
		self.logger.info((mob_bankid_but))
		time.sleep(10)
		self.driver.close()