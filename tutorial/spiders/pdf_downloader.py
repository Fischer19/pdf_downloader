import scrapy
import numpy as np
from scrapy.http import Request

class PdfDownloader(scrapy.Spider):
	name = 'pdf_downloader'
	# links to the specific pages
	def __init__(self, source = "medrxiv", output = "pdf/"):
		self.source = source
		self.output = output

	def start_requests(self):
		start_urls = []
		for i in range(1):
			start_urls += ['https://connect.biorxiv.org/relate/content/181?page={}'.format(i + 1)]
		#target = getattr(self, 'target', None)
		#if target is not None:
		#	start_urls.append(target)
		#	print('---------------------')
		#	print(start_urls)
		for url in start_urls:
			print('---------------------')
			print(url)
			yield scrapy.Request(url, callback = self.parse)


	def parse(self, response):
		# selector of pdf file.
		if self.source == "medrxiv":
			selector = 'a[href*="medrxiv.org/cgi"]::attr(href)'
			text = response.css('a[href*="medrxiv.org/cgi"]::attr(title)').getall()
		else:
			selector = 'a[href*="biorxiv.org/cgi"]::attr(href)'
			text = response.css('a[href*="biorxiv.org/cgi"]::attr(title)').getall()
		hrefs = response.css(selector).getall()
		
		for i, href in enumerate(hrefs):
			if i % 2 == 1:
				continue
			print(text[i//2])
			yield Request(
				url=response.urljoin(href + "v1.full.pdf"),
				callback=self.save_pdf,
				#need to use meta keywords to pass the parameters
				meta = {'text': text[i//2]}
			)


	def save_pdf(self, response):
		""" Save pdf files """
		#path = response.css('a[href*="https://www.medrxiv.org/content"]::attr(href)').get()
		#path = response.url.split('/')[-1]
		#text = response.meta.get('text') + '.pdf'
		text = response.url.split('/')[-1]
		self.logger.info('Saving PDF %s', text);
		with open(self.output + text, 'wb') as file:
			file.write(response.body)