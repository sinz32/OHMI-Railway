from bs4 import BeautifulSoup
import requests, time, json

url = 'https://www.ohmitetudo.co.jp/railway/ride/timetable/honsen/'
# url = 'https://www.ohmitetudo.co.jp/railway/ride/timetable/yokaichi/'
# url = 'https://www.ohmitetudo.co.jp/railway/ride/timetable/taga/'

response = requests.get(url);
# print(response.text);
html = BeautifulSoup(response.text, 'html.parser')

def parse_timetable(url):
	if url == None: return []
	response = requests.get(url);
	# print(response.text);
	html = BeautifulSoup(response.text, 'html.parser')
	data = html.select('div#timetable')[0].select('div.mt-6')
	
	result = {
		'weekdays': [],
		'weekends': [],
	}
	# 평일
	for li in data[0].select('li.ekltip'):
		span = li.select('span')
		result['weekdays'].append(span[0].text);
	
	# 휴일
	for li in data[1].select('li.ekltip'):
		span = li.select('span')
		result['weekends'].append(span[0].text);
	
	print(result)
	return result


result = []
data = html.select('div.ridestation')[0].select('div.honsen_item')
first = True;
for datum in data:
	stn = datum.select('p.honsen_stationname')[0].text
	urls = datum.select('a')
	if 'http' not in urls[0].decode():
		print(urls[0].decode())
		print('http' not in urls[0].decode())
		urls.pop(0)

	if 'http' not in urls[-1].decode():
		print(urls[-1].decode())
		print('http' not in urls[-1].decode())
		urls.pop()
		
	urls[0] = urls[0]['href']
		
	if len(urls)==1: 
		if first:
			urls.append(None);
		else:
			urls.append(urls[0]);
			urls[0] = None;
	else:
		urls[1] = urls[1]['href']
	first = False;
	print(stn, urls)
	
	result.append({
		'stn': stn,
		'up': parse_timetable(urls[0]),
		'down': parse_timetable(urls[1])
	})
	
	time.sleep(3)

json_string = json.dumps(result, indent=4, ensure_ascii=False)
with open('timetable.json', 'w', encoding='utf-8') as f:
	f.write(json_string)

