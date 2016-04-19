import urllib2
import cookielib

url = "https://www.baidu.com"

print 'first method'
response1 = urllib2.urlopen(url)
#返回值为200时，证明获取成功
print response1.getcode()
content = response1.read()
print 'the length of content:', len(content)


print 'second method'
request = urllib2.Request(url)
#request.add_data('a', '1')
request.add_header('User-Agent', 'Mozilla/5.0')
response2 = urllib2.urlopen(request)
print response2.getcode()
content = response2.read()
print 'the length of content:', len(content)



print 'third method'
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
response3 = urllib2.urlopen(url)
print response3.getcode()
content = response3.read()
print 'the length of content:', len(content)
print cj
