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

class NewAvanzaSpider(scrapy.Spider):

	open('log.txt', 'w').close()
	
	name = "new_avanza_crawler"
	
	start_urls = [
		'https://www.avanza.se/aktier/lista.html',
	]
	
	def __init__(self):	                      
		self.driver = webdriver.PhantomJS()
		#self.driver = webdriver.Firefox()
		
	def parse(self, response):
		self.driver.get(response.url)
		
		now = datetime.datetime.now()
		
		def stock_market_closed():
			if((now.hour >= 17 and now.minute >= 30) or (now.hour <= 9 and now.minute <= 00)):
				return True
				
			else:
				return False
				
		def save_object(obj, filename):
			with open(filename, 'wb') as output:
				pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
				output.close()
			
		#if(stock_market_closed()):
		#	sys.exit()
		
		##### LOGGA IN #######

		
		
		
		##### ------- ######
		
		i = 0;
		j = 0;
		
		##### VISA ALLA SVENSKA ######
		toggle = WebDriverWait(self.driver, 10).until(
					EC.visibility_of_element_located((By.XPATH, '//span[@data-ng-show="vm.selectedListLabel"]'))
				)
				
		toggle.click()
		time.sleep(0.5)
		toggle_all = WebDriverWait(self.driver, 10).until(
				EC.visibility_of_element_located((By.XPATH, '//li[@data-ng-click="vm.toggleAllMarketLists(landObject)"]'))
			)
			
		toggle_all.click()
		time.sleep(0.5)
		
		##### ------------------ ######
		
		resp = TextResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
		
		t2= resp.xpath('//div[@class="tableScrollContainer"]')
		nT = t2.xpath('//table[@class="u-standardTable"]/tbody/tr/td/text()')
		
		t = resp.xpath('//table[@class="u-standardTable"]')
		u = t.xpath('//tr[@class="row"]/td[@class="orderbookName"]/a[@class="ellipsis"]/text()').extract()
		
		u2 = t[0].xpath('//tr[@class="row"]/td[@class="orderbookName"]/a[@class="ellipsis"]/@href').extract()
		
		lists = []
		
		for n in range(0,780):
			lists.append([])
			
			
		for n in range(1,9):
		
			
			i = 0
			resp = TextResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
			
			t = resp.xpath('//table[@class="u-standardTable"]')
			
			u2 = t[0].xpath('//tr[@class="row"]/td[@class="orderbookName"]/a[@class="ellipsis"]/@href').extract()
			
			t2= resp.xpath('//div[@class="tableScrollContainer"]')
			nT = t2.xpath('//table[@class="u-standardTable"]/tbody/tr/td/text()')	
			
			for nejm in u2:
					
				if(1):
					try:
						numm = nT[400+8*i].extract()
					except IndexError:
						numm = -1
						break
					
					
					#numm2 = nT[401+8*i].extract()
					#numm3 = nT[402+8*i].extract()
					#numm4 = nT[403+8*i].extract()
					#numm5 = nT[404+8*i].extract()
					#numm6 = nT[405+8*i].extract()
					#numm7 = nT[406+8*i].extract()
					
					numm = re.sub('[^A-Za-z0-9,-]+', '', numm)
					numm = re.sub('[^0-9]+', '.', numm)	
					#numm2 = re.sub('[^A-Za-z0-9,-]+', '', numm2)
					#numm3 = re.sub('[^A-Za-z0-9,-]+', '', numm3)
					#numm4 = re.sub('[^A-Za-z0-9,-]+', '', numm4)
					#numm5 = re.sub('[^A-Za-z0-9,-]+', '', numm5)
					#numm6 = re.sub('[^A-Za-z0-9,-]+', '', numm6)
					#numm7 = re.sub('[^A-Za-z0-9,-]+', '', numm7)

					try:
						p = float(numm)
					except:
						continue
						
					nejm = re.sub('[^A-Za-z-]+', '', nejm[28:])
					
					
					lists[j].append(nejm)
					lists[j].append(numm)
				#	lists[j].append(numm2)
				#	lists[j].append(numm3)
				#	lists[j].append(numm4)
				#	lists[j].append(numm5)
				#	lists[j].append(numm6)
				#	lists[j].append(numm7)
					
					
					yield{
						'Senast' : lists[j][1],
						'Namn' : lists[j][0]
							
					}
					
					i+=1
					
			
					with open('log.txt', 'a') as f:
						f.write('---{0}---\n* Senast: {1}\n\n\n' .format(nejm, numm))
					
				j+=1
			
			if (numm == -1 or numm == ''):
				break
			
			i = 0
				
			next_button = WebDriverWait(self.driver, 10).until(
					EC.visibility_of_element_located((By.XPATH, '//button[@data-ng-click="vm.goToNextPage()"]'))
				)
				
			next_button.click()
			time.sleep(0.5)
			
			

		lists2 = filter(None, lists)
		newDir = 'avanza_crawler/lists3/' + str(now)[:10] + '/'
		
		if not os.path.exists(newDir ):
			os.makedirs(newDir)
			
		fname = str(datetime.time(now.hour,now.minute,now.second)) + '.pk1'
		fname = fname.replace(':', '-')
		fname = newDir + fname
		
		save_object(lists2, fname)
		
		yield Request(response.url, callback=self.parse, dont_filter=True)