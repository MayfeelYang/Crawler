# -*- coding: utf-8 -*-
import urllib2
class  HtmlDownloader(object):
	def download(self, url):
		if url is None:
			return None
		#这里的urllib2库使用的是最简单的方法，之后应该修调用一个更为强大的方法
		response = urllib2.urlopen(url)

		if response.getcode() != 200:
			return None
		return response.read()
		

		



