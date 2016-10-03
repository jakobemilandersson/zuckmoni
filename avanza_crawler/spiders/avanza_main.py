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

class AvanzaSpider(scrapy.Spider):

	open('log.txt', 'w').close()
	
	name = "avanza_crawler"
	
	start_urls = [
		'https://www.avanza.se/aktier/lista.html',
	]
	

	def parse(self, response):
	
		def save_object(obj, filename):
			with open(filename, 'wb') as output:
				pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
				output.close()
			

		i = 0;
		j = 0;
		
		t2= response.xpath('//div[@class="tableScrollContainer"]')
		nT = t2.xpath('//table[@class="u-standardTable"]/tbody/tr/td/text()')
		
		t = response.xpath('//table[@class="u-standardTable"]')
		u = t.xpath('//tr[@class="row"]/td[@class="orderbookName"]/a[@class="ellipsis"]/text()').extract()
		
		u2 = t[0].xpath('//tr[@class="row"]/td[@class="orderbookName"]/a[@class="ellipsis"]/@href').extract()
		u3 = t[1].xpath('//tr[@class="row"]/td[@class="orderbookName"]/a[@class="ellipsis"]/@href').extract()
		u4 = t[2].xpath('//tr[@class="row"]/td[@class="orderbookName"]/a[@class="ellipsis"]/@href').extract()
		
		lists = []
		
		for n in range(0,100):		
			lists.append([])
			
		for nejm in u2:
			
			if(1):
				
			
				numm = nT[400+8*i].extract()
				numm2 = nT[401+8*i].extract()
				numm3 = nT[402+8*i].extract()
				numm4 = nT[403+8*i].extract()
				numm5 = nT[404+8*i].extract()
				numm6 = nT[405+8*i].extract()
				numm7 = nT[406+8 *i].extract()
				
				numm = re.sub('[^A-Za-z0-9,-]+', '', numm)
				numm2 = re.sub('[^A-Za-z0-9,-]+', '', numm2)
				numm3 = re.sub('[^A-Za-z0-9,-]+', '', numm3)
				numm4 = re.sub('[^A-Za-z0-9,-]+', '', numm4)
				numm5 = re.sub('[^A-Za-z0-9,-]+', '', numm5)
				numm6 = re.sub('[^A-Za-z0-9,-]+', '', numm6)
				numm7 = re.sub('[^A-Za-z0-9,-]+', '', numm7)

			
				nejm = re.sub('[^A-Za-z-]+', '', nejm[28:])
				
				lists[i].append(nejm)
				lists[i].append(numm)
				lists[i].append(numm2)
				lists[i].append(numm3)
				lists[i].append(numm4)
				lists[i].append(numm5)
				lists[i].append(numm6)
				lists[i].append(numm7)
				
				yield{
					'Agare' : lists[i][7],
					'Direktavk.%' : lists[i][6], 
					'P/E-tal' : lists[i][5],
					'Borsvarde MSEK' : lists[i][4],
					'1 ar %' : lists[i][3],
					'+/-%' : lists[i][2],
					'Senast' : lists[i][1],
					'Namn' : len(lists)
					
				}
				
				i+=1
				
				with open('log.txt', 'a') as f:
					f.write('---{0}---\n* Senast: {1}\n* +/-%: {2}\n* 1 år %: {3}\n* Börsvärde MSEK: {4}\n* P/E-tal: {5}\n* Direktavk.%: {6}\n* Ägare: {7}\n\n\n\n\n '.format(nejm, numm, numm2, numm3, numm4, numm5, numm6, numm7))
				
			j+=1
		
		
			
		now = datetime.datetime.now()
		
		newDir = 'avanza_crawler/lists/' + str(now)[:10] + '/'
		
		if not os.path.exists(newDir ):
			os.makedirs(newDir)
			
		fname = str(datetime.time(now.hour,now.minute,now.second)) + '.pk1'
		fname = fname.replace(':', '-')
		fname = newDir + fname
		
		save_object(lists, fname)
		
		yield Request(response.url, callback=self.parse, dont_filter=True)