import json

from scrapy import Spider, Request
import logging


class Coursera(Spider):
	name = 'coursera'
	coursera_link = 'https://www.coursera.org' 
	page_number = 1
	page_count = 5
	start_urls = [
			'https://www.coursera.org/courses'
	]

	def start_requests(self):
		for url in self.start_urls:
			if url == 'https://www.coursera.org/courses':
				new_url = url+'?page={page}&index=prod_all_products_term_optimization'.format(page=self.page_number)
				self.log(new_url)
				yield Request(new_url, callback=self.parse_courses)

	def parse_courses(self,response):
		# if self.page_number == 1:
		# 	total_courses = response.css('.rc-NumberOfResultsSection span::text').extract_first()
			# count = int([int(s) for s in total_courses.split() if s.isdigit()][0]/10)+1
			# self.page_count = count
		courses = response.css('.anchor-wrapper')
		#main > div > div > div.rc-SearchTabs > div > div.tab-contents > div > div > div > div > ul
		#main > div > div > div.rc-SearchTabs > div > div.tab-contents > div > div > div > div > ul > li:nth-child(1)
		#main > div > div > div.rc-SearchTabs > div > div.tab-contents > div > div > div > div > ul > li:nth-child(2) > div > div > a > div
		#main > div > div > div.rc-SearchTabs > div > div.tab-contents > div > div > div > div > ul > li:nth-child(1) > div > div > a > div > div.cds-69.card-info.css-0.cds-71.cds-grid-item > h2

	# //*[@id="main"]/div/div/div[1]/div/div[2]/div/div/div/div/ul/li[1]/div/div/a/div/div[2]/h2
	# 	response.css('div.rc-SearchTabs div div.tab-contents div div div div').xpath('//ul').xpath('//div/div/a/div/div[2]').xpath('//h2').get()
		#main > div > div > div.rc-SearchTabs > div > div.tab-contents > div > div > div > div > ul > li:nth-child(1) > div
		for course in courses:
			name = course.css('.headline-1-text::text').extract_first()
			image = course.css('.product-photo::attr(src)').extract_first()
			category = course.css('.product-type-row ._1d8rgfy3::text').extract_first()
			rating = course.css('.ratings-text::text').extract_first()
			enrollment = course.css('.enrollment-number::text').extract_first()
			university = course.css('.m-b-1s::text').extract_first()
			difficulty = course.css('span.difficulty::text').extract_first()
			link = self.coursera_link + course.css('.rc-DesktopSearchCard::attr(href)').extract_first()
			with open("temp.json", "w") as temp:
				json.dump({'name':name,'image':image,'category':category,'rating':rating,'enrollment':enrollment,'university':university,'difficulty':difficulty,'link':link}, temp)
			yield {'name':name,'image':image,'category':category,'rating':rating,'enrollment':enrollment,'university':university,'difficulty':difficulty,'link':link}
		#main > div > div > div.rc-SearchTabs > div > div.tab-contents > div > div > div > div > ul > li:nth-child(1) > div > div > a > div > div.cds-69.card-info.css-0.cds-71.cds-grid-item
		if self.page_number < self.page_count:
			self.page_number += 1
			next_page = 'https://www.coursera.org/courses?page={page}&index=prod_all_products_term_optimization'.format(page=self.page_number)
			yield response.follow(next_page, callback=self.parse_courses)
