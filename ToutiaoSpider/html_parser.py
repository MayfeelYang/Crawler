# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import urlparse



class HtmlParser(object):
	def _get_group_urls(self, root_url, soup):
		group_urls = dict()
		#<a ga_event="news_recommend" class="item selected" href="/" data-node="category" data-category="__all__">
		#<span class="channel-tag">推荐</span></a>
		links = soup.find_all('a', class_ = "item")
		for link in links:
			new_url = link['href']
			new_full_url = urlparse.urljoin(root_url, new_url)
			group_urls[new_full_url] = link.find("span").get_text()
		print 'the length of group urls:', len(group_urls)
		#print group_urls
		return group_urls

	def _get_part_urls(self, page_url, soup):
		part_urls = set()
		#<a ga_event="click_feed_newstitle" class="link title" href="/group/6274815266204631297/" target="_blank" data-node="title">
		#	两个孩子溺水，父亲只救起自家孩子，被谴责他一句话让众人咋舌！
		#</a>
		links = soup.find_all('div', class_ = "title-box" )
		print links
		for link in links:
			new_url = link['href']
			new_full_url = urlparse.urljoin(page_url, new_url)
			part_urls.add(new_full_url)
		#print 'the length of new_urls:', len(new_urls)
		return part_urls

	def _get_new_urls(self, page_url, soup):
		new_urls = set()
		# /view/123.htm
		links = soup.find_all('a', href = re.compile(r"/group/\d+/"))
		for link in links:
			new_url = link['href']
			new_full_url = urlparse.urljoin(page_url, new_url)
			new_urls.add(new_full_url)
		#print 'the length of new_urls:', len(new_urls)
		return new_urls

	


	def _get_new_data(self, page_url, soup):
		res_data = {}
		res_data['url'] = page_url

		#<dd class="lemmaWgt-lemmaTitle-title"> <h1>Python</h1>
		title_node = soup.find('dd', class_ = "lemmaWgt-lemmaTitle-title").find("h1")
		res_data['title'] = title_node.get_text()
		#<div class="lemma-summary" label-module="lemmaSummary">
		summary_node = soup.find('div', class_ = "lema-summary")
		res_data['summary'] = summary_node.get_text()
		
		return res_data


	def parse(self, page_url, html_cont):
		if page_url is None or html_cont is None:
			return
		soup_slice = BeautifulSoup(html_cont, 'html.parser', from_encoding = 'utf-8')
		new_urls = self._get_new_urls(page_url, soup_slice)
		new_data = self._get_new_data(page_url, soup_slice)
		return new_urls, new_data

	def parse_part(self, page_url, html_cont):
		if page_url is None or html_cont is None:
			return
		soup_part = BeautifulSoup(html_cont, 'html.parser', from_encoding = 'utf-8')
		new_urls = self._get_part_urls(page_url, soup_part)
		return new_urls

	def parse_main(self, root_url, html_main_cont):
		if root_url is None or html_main_cont is None:
			return
		soup_group = BeautifulSoup(html_main_cont, 'html.parser', from_encoding = 'utf-8') 
		group_urls = self._get_group_urls(root_url, soup_group)
		return group_urls

	
