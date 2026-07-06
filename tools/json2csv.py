with open('timetable.json', 'r', encoding='utf-8') as f:
	data = json.load(f)


weekdays_up = []
weekdays_down = []
weekends_up = []
weekends_down = []

for datum in data:
	if 'up' in datum:
		weekdays_up.append(datum['stn']+',,'+(','.join(datum['up']['weekdays'])))
		weekends_up.append(datum['stn']+',,'+(','.join(datum['up']['weekends'])))
	if 'down' in datum:
		weekdays_down.append(datum['stn']+',,'+(','.join(datum['down']['weekdays'])))
		weekends_down.append(datum['stn']+',,'+(','.join(datum['down']['weekends'])))


with open('weekdays_up.csv', 'w', encoding='utf-8') as f:
	f.write('\n'.join(weekdays_up))
with open('weekends_up.csv', 'w', encoding='utf-8') as f:
	f.write('\n'.join(weekends_up))
with open('weekdays_down.csv', 'w', encoding='utf-8') as f:
	f.write('\n'.join(weekdays_down))
with open('weekends_down.csv', 'w', encoding='utf-8') as f:
	f.write('\n'.join(weekends_down))

