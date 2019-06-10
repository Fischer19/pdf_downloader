import scrapy

from scrapy.http import Request

class PdfDownloader(scrapy.Spider):
	name = 'pdf_downloader'
	# links to the specific pages
	#start_urls = ['https://graphreason.github.io/papers.html']
	def start_requests(self):
		start_urls = []
		target = getattr(self, 'target', None)
		if target is not None:
			start_urls.append(target)
			print('---------------------')
			print(start_urls)
		for url in start_urls:
			yield scrapy.Request(url)


	def parse(self, response):
		# selector of pdf file.
		selector = 'a[href$=".pdf"]::attr(href)'
		text = response.css('a[href$=".pdf"]::text').getall()
		for i, href in enumerate(response.css(selector).extract()):
			print(text[i])
			yield Request(
				url=response.urljoin(href),
				callback=self.save_pdf,
				#need to use meta keywords to pass the parameters
				meta = {'text': text[i]}
			)


	def save_pdf(self, response):
		""" Save pdf files """
		path = response.url.split('/')[-1]
		text = response.meta.get('text') + '.pdf'
		self.logger.info('Saving PDF %s', text);
		with open(text, 'wb') as file:
			file.write(response.body)