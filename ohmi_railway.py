import json, pytz
from datetime import datetime

def get_data(line):
    data = get_all()

    if line == 'all':
        return data
    if line == 'main' or line == 'honsen':
        return data[:25]
    if line == 'yokaichi':
        result = data[27:]
        result.insert(0, data[12])
        return result
    if line == 'taga':
        result = data[25:27]
        result.insert(0, data[6])
        return result
    
    return []
    

def get_all():
    result = []
    stns_ko = ['마이바라','후지테크마에','토리이모토','히코네','히코네세리카와','히코네구치','타카미야','아마고','토요사토','에치가와','고카쇼','카와베노모리','요카이치','나가타니노','다이가쿠마에','교세라마에','사쿠라가와','아사히오츠카','아사히노','히노','미나쿠치마츠오','미나쿠치','미나쿠치이시바시','미나쿠치조난','키부카와','스크린','타가타이샤마에','신요카이치','타로보구마에','이치노베','히라타','무사','오미하치만']
    stns_ja = ['米原','フジテック前','鳥居本','彦根','ひこね芹川','彦根口','高宮','尼子','豊郷','愛知川','五箇荘','河辺の森','八日市','長谷野','大学前','京セラ前','桜川','朝日大塚','朝日野','日野','水口松尾','水口','水口石橋','水口城南','貴生川','スクリーン','多賀大社前','新八日市','太郎坊宮前','市辺','平田','武佐','近江八幡']

    trains = get_all_trains()

    for i, v in enumerate(stns_ko):
        result.append({
            'stn': {
                'ko': v,
                'ja': stns_ja[i]
            },
            'up': [],
            'down': []
        })
        for train in trains:
            if train['stn'] != v : continue
            result[i][train['dir']].append({
                'trainNo': train['no'],
                'terminal': train['terminal'],
                'type': train['type']
            })

    return result

def get_all_trains():
    # 평일/휴일에 맞는 시간표 읽어오기
    time = datetime.now(pytz.timezone('Asia/Seoul'))
    day = time.weekday()
    path = 'weekdays.json'
    if day == 5 or day == 6: path = 'weekends.json'
    with open('./timetable/' + path, 'r', encoding='utf-8') as f:
	    data = json.load(f)
    
    result = []
    now = time.hour * 60 + time.minute
    for no in data:
        tt = data[no]['time']

        # 아직 운행이 시작되지 않은 열차 걸러내기
        if now < t2m(tt[0]['t']): continue

        # 이미 운행이 끝난 열차 걸러내기
        if now > t2m(tt[-1]['t']): continue

        # 어느 역에 있는지 찾기
        location = None
        for n in range(len(tt) - 1, -1, -1):  # 뒤에서부터 찾기
            t = t2m(tt[n]['t'])
            if t == now:  # 지금이 시간표에 적힌 시간이라면 역에 있는 것으로 간주
                location = tt[n]['s']
                break
            if t < now:  # 지금이 시간표에 적힌 시간보다 미래라면 다음 역으로 표시
                location = tt[n + 1]['s']
                break

        # 50번 열차 빼고는 전부 보통 등급
        train_type = '보통'
        if no == '50' : train_type = '쾌속'

        # 열차번호로 상행/하행 구분하기
        direction = 'down'
        if int(no) % 2 == 0 : direction = 'up'

        result.append({
            'no': no,
            'stn': location,
            'terminal': data[no]['terminal'],
            'type': train_type,
            'dir': direction
        })
    
    return result



def t2m(time): #H:mm 형식으로 된 "시간을 자정으로부터 몇 분 지났는지"로 바꿔주는 함수
    t = time.split(':')
    return int(t[0]) * 60 + int(t[1])