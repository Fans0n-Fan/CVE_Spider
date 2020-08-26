import requests
from bs4 import BeautifulSoup
import json
a_url_set = []
result = []

list_url = "https://vulmon.com/searchpage?q=simatic+firmware"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
headers = {'User-Agent': user_agent}
while True:
	r = requests.get(list_url, headers=headers, timeout=5)
	if r.status_code == 200:
		break
content = r.text
soup = BeautifulSoup(content, 'lxml')
tag_a = soup.select('.header')
	#tag_a = soup.select.find_all("a",{"class":"header"})
	# print(tag_a)
for a in tag_a:
	a_url = a.get('href')
	# print(a_url)
	a_url_set.append(a_url)

a_url_set.pop(0)
a_url_set.pop(len(a_url_set)-1)

f_result = open('results.json', 'w')

for url in a_url_set:
	vuln_info = {}
	while True:
		r = requests.get("https://vulmon.com"+url, headers=headers, timeout=5)
		if r.status_code == 200:
			break
	content = r.text
	soup = BeautifulSoup(content, 'lxml')
	vuln_table = soup.select('div')
	vuln_name = soup.find('h1')
	vuln_n=vuln_name.text.strip()
	vuln_info["CVE"] = str(vuln_n)
	vuln_summry = soup.find('p')
	vuln_s=vuln_summry.text.strip()
	vuln_info["summry"] = str(vuln_s)

	f_result.write(json.dumps(vuln_info, ensure_ascii=False, indent=2))
	f_result.write('\n')
f_result.close()


