# -*- coding: utf-8 -*-
import url_manager, html_downloader, html_parser, html_outputer


class SpiderMain(object):
	def __init__(self):
		self.urls_group = url_manager.UrlManager()
		self.urls_slice = url_manager.UrlManager()
		self.downloader = html_downloader.HtmlDownloader()
		self.downloader_main = html_downloader.HtmlDownloader()
		self.parser = html_parser.HtmlParser()
		self.parser_main = html_parser.HtmlParser()
		self.outputer = html_outputer.HtmlOutputer()
		self.root_url = ""

	def _craw(self, url):
		html_cont = self.downloader.download(url)
		print html_cont
		new_urls = self.parser.parse_part(self.root_url, html_cont)
		print new_urls

	def craw_group(self, root_url):
		self.root_url = root_url
		html_main_cont = self.downloader_main.download(root_url)
		#print html_main_cont
		group_urls = self.parser_main.parse_main(root_url, html_main_cont)
		if group_urls is None or len(group_urls) == 0:
			return 
		for group_url in group_urls:
			print group_url
			self._craw(group_url)



		
	def craw1(self, url):
		count = 1
		self.urls.add_new_url(root_url)

		while self.urls.has_new_url():
			try:
				new_url = self.urls.get_new_url()
				print 'craw %d : %s' %  (count, new_url)
				html_cont = self.downloader.download(new_url)
				new_urls, new_data = self.parser.parse(new_url, html_cont)
				self.urls.add_new_urls(new_urls)
				self.outputer.collect_data(new_data)

				if count == 10:
					break;
				count += 1

			except Exception, e:
				print  'craw failed:' , str(e)
		self.outputer.output_html()


if __name__ == "__main__":
    root_url = "http://toutiao.com/"
    obj_spider = SpiderMain()
    #obj_spider.craw(root_url)
    obj_spider.craw_group(root_url)

