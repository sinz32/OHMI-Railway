import json

def read_csv(file_name):
	with open(file_name, 'r', encoding='utf-8') as f:
		data = f.read()
	data = data.strip()
	data = data.split('\n')
	for i, v in enumerate(data):
		data[i] = v.split(',')
	return data

# 중간에 열차번호가 바뀌는 열차 예외처리
# 평일과 휴일의 열차번호 및 왕복 횟수 등이 모두 일치
terminals = {
	'9800': '키부카와',
	'9802': '키부카와',
	'9804': '키부카와',
	'9806': '키부카와',
	'9808': '키부카와',
	'9810': '키부카와',
	'9600': '히노'
}

def csv2json(type):
	result = {}
	
	# 상행
	for line in ['타가선', '요카이치선', '본선']: # 본선으로 진입하는 열차들이 있으니, 본선을 나중에 읽어야 순서대로 추가됨
		data = read_csv(type + '상행_' + line + '.csv')

		for x in range(2, len(data[0])):
			no = data[0][x].strip()
			if no == '': continue
			if no not in result:
				result[no] = {
					'terminal': None,
					'time': []
				}
			for y in range(1, len(data)):
				data[y][x] = data[y][x].strip()
				if data[y][x] == '': continue
				if data[y][x] == '본선': continue
				if data[y][x] == '요카이치선': continue
				if data[y][x] == '타가선': continue
				result[no]['time'].append({
					's': data[y][1],
					't': data[y][x]
				})
	
	# 하행 - 어차피 한 번 돌리고 사용 안 할 소스이니, 소스가 중복되어도 신경쓰지 않음
	for line in ['본선', '요카이치선', '타가선']: # 본선에서 분기하는 열차들이 있으니, 본선 먼저 읽어야 순서대로 추가됨
		data = read_csv(type + '하행_' + line + '.csv')

		for x in range(2, len(data[0])):
			no = data[0][x].strip()
			if no == '': continue
			if no not in result:
				result[no] = {
					'terminal': None,
					'time': []
				}
			for y in range(1, len(data)):
				data[y][x] = data[y][x].strip()
				if data[y][x] == '': continue
				if data[y][x] == '본선': continue
				if data[y][x] == '요카이치선': continue
				if data[y][x] == '타가선': continue
				result[no]['time'].append({
					's': data[y][1],
					't': data[y][x]
				})
		
	# 행선지 추가
	for no in result:
		if no in terminals:
			result[no]['terminal'] = terminals[no]
		else:
			result[no]['terminal'] = result[no]['time'][-1]['s']
		
		
	with open(type + '.json', 'w', encoding='utf-8') as f:
		f.write(json.dumps(result, indent=4, ensure_ascii=False))

print('변환시작')
csv2json('평일')
print('평일 변환 끝')
csv2json('휴일')
print('휴일 변환 끝')

