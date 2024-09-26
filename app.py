from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests, cv2, os
from time import sleep
from tqdm import tqdm
from datetime import datetime, timedelta

tomorrow = datetime.today() + timedelta(days=1)
tomorrowStr = tomorrow.strftime('%Y_%m_%d')
tomorrowTitle = tomorrow.strftime('%Y년 %m월 %d일')

# filename = f'{tomorrowStr}의 모든 것.md'
filename = f'{tomorrowStr}의 모든 것.html'

형식 = '''
<h2>내일의 모든 것</h2>
<h3>날씨 소식</h3>
<br />
<h4>YYYY년 MM월 DD일 X요일</h4>
<p>의 날씨 소식입니다.<p>
<br /><br />

<p>내일 오전의 날씨는 <strong>(흐리고 비 | 흐리고 한때 비 | 흐림 | 구름많음 | 맑음)</strong>입니다.</p>
<p>그리고 내일 오후의 날씨는 <strong>(흐리고 비 | 흐리고 한때 비 | 흐림 | 구름많음 | 맑음)</strong>입니다.</p>
<br />
<img src="YYYY_dd_mm.png" alt="weather_image" />

<br />
<hr />
<br />

<h3>내일 운세</h3>
<h4>띠별 운세</h4>

<table>
    <thead>
        <tr style="border-bottom: 1px solid e2e2e2; margin: 4px;">
            <td style="width: 15%; background: #094044; color: white; padding: 4px; text-align: center;">띠</td>
            <td style="width: 75%; background: #094044; color: white; padding: 4px; text-align: center;">내일 운세</td>
        </tr>
    </thead>
    <tbody>
        <tr style="border-bottom: 1px solid e2e2e2; margin: 4px;">
            <td style="padding: 4px; text-align: center">쥐띠</td>
            <td>{}</td>
        </tr>
        <!-- ... -->
    </tbody>
</table>
<br />
<h4>별자리 운세</h4>
<table>
    <thead>
        <tr style="border-bottom: 1px solid e2e2e2; margin: 4px;">
            <td style="width: 15%; background: #094044; color: white; padding: 4px; text-align: center;">별자리</td>
            <td style="width: 20%; background: #094044; color: white; padding: 4px; text-align: center;">날짜</td>
            <td style="width: 65%; background: #094044; color: white; padding: 4px; text-align: center;">내일 운세</td>
        </tr>
    </thead>
    <tbody>
        <tr style="border-bottom: 1px solid e2e2e2; margin: 4px;">
            <td style="padding: 4px; text-align: center">물병자리</td>
            <td style="padding: 4px; text-align: center">01월 20일 ~ 02월 18일</td>
            <td>{}</td>
        </tr>
        <!-- ... -->
    </tbody>
</table>
'''

def writeStyle():
    with open(filename, "w", encoding='utf-8') as file:
        file.write('''
<style>
table {
  border: 1px #a39485 solid;
  font-size: .9em;
  box-shadow: 0 2px 5px rgba(0,0,0,.25);
  width: 100%;
  border-collapse: collapse;
  border-radius: 5px;
  overflow: hidden;
}

th {
  text-align: left;
}
  
thead {
  font-weight: bold;
}
  
 td, th {
  padding: 1em .5em;
  vertical-align: middle;
}
  
 td {
  border-bottom: 1px solid rgba(255,255,255,.4);
}
  
 @media all and (max-width: 768px) {
    
  table, thead, tbody, th, td, tr {
    display: block;
  }
  
  th {
    text-align: right;
  }
  
  table {
    position: relative; 
    padding-bottom: 0;
    border: none;
    box-shadow: 0 0 10px rgba(0,0,0,.2);
  }
  
  thead {
    float: left;
    white-space: nowrap;
  }
  
  tbody {
    overflow-x: auto;
    overflow-y: hidden;
    position: relative;
    white-space: nowrap;
  }
  
  tr {
    display: inline-block;
    vertical-align: top;
  }
  
  th {
    border-bottom: 1px solid #a39485;
  }
  
  td {
    border-bottom: 1px solid #e5e5e5;
  }
  
  
  }
</style>

''')

def get날씨():
    week = ['월요일',
    '화요일',
    '수요일',
    '목요일',
    '금요일',
    '토요일',
    '일요일']

    title = '{} {}'.format(tomorrowTitle, week[tomorrow.weekday()])

    url = 'https://weather.naver.com/'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.set_window_size(1920, 1080)

    sleep(0.2)

    tomorrowBtn = driver.find_element(By.XPATH, '//*[@id="nation"]/ul/li[2]/button')
    driver.execute_script("arguments[0].click();", tomorrowBtn)
    map = driver.find_element(By.XPATH, '//*[@id="mapPanel"]')
    map.screenshot(f'./{tomorrowStr}_map1.png')

    afternoonBtn = driver.find_element(By.XPATH, '//*[@id="mapPanel"]/div[1]/button[3]')
    driver.execute_script("arguments[0].click();", afternoonBtn)
    map = driver.find_element(By.XPATH, '//*[@id="mapPanel"]')
    map.screenshot(f'./{tomorrowStr}_map2.png')

    오전날씨 = driver.find_element(By.XPATH, '//*[@id="weekly"]/ul/li[2]/div/div[2]/span[1]/span').text
    오전강수확률 = driver.find_element(By.XPATH, '//*[@id="weekly"]/ul/li[2]/div/div[2]/span[1]/strong/span[2]').text

    오후날씨 = driver.find_element(By.XPATH, '//*[@id="weekly"]/ul/li[2]/div/div[2]/span[2]/span').text
    오후강수확률 = driver.find_element(By.XPATH, '//*[@id="weekly"]/ul/li[2]/div/div[2]/span[2]/strong/span[2]').text

    최저기온 = driver.find_element(By.XPATH, '//*[@id="weekly"]/ul/li[2]/div/div[3]/strong/span[1]').text
    최고기온 = driver.find_element(By.XPATH, '//*[@id="weekly"]/ul/li[2]/div/div[3]/strong/span[3]').text

    imagePath = '{}.png'.format(tomorrowStr)

    image1Path = f'{tomorrowStr}_map1.png'
    image2Path = f'{tomorrowStr}_map2.png'

    image1 = cv2.imread(image1Path, cv2.IMREAD_COLOR)
    image2 = cv2.imread(image2Path, cv2.IMREAD_COLOR)

    if image1 is None or image2 is None:
        print('Image load failed')
        exit(0)

    merge_image = cv2.hconcat([image1, image2])

    cv2.imwrite(imagePath, merge_image)

    os.remove(image1Path)
    os.remove(image2Path)

    형식 = '''
<h2>내일의 모든 것</h2>
<h3>날씨 소식</h3>
<br />
<h4>{}</h4>
<p>의 날씨 소식입니다.<p>
<br /><br />

<p>내일 오전의 날씨는 <strong>{}</strong>입니다.</p>
<p>그리고 내일 오후의 날씨는 <strong>{}</strong>입니다.</p>
<br />
<p>오전 강수 확률은 <strong>{}</strong> 이고, 오후 강수 확률은 <strong>{}</strong> 입니다.</p>
<p>최저 기온 <strong>{}C</strong> 이고 최고 기온은 <strong>{}C</strong> 입니다.</p>
<br />

<img src="{}" alt="weather_image" />

<br />
<hr />
<br />
'''.format(
        title,
        오전날씨, 오후날씨, 
        오전강수확률.replace("강수확률\n", ""),
        오후강수확률.replace("강수확률\n", ""),
        최저기온.replace("최저기온\n", ""),
        최고기온.replace("최고기온\n", ""),
        imagePath
    )

    with open(filename, 'a', encoding='utf-8') as file:
        file.write(형식)

def get운세(운세, 날짜=None):
    url = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&qvt=0&query={} 운세'.format(운세)

    with requests.get(url) as response:
        if response.status_code != 200:
            print(response.status_code)
            exit(0)

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.select('#yearFortune > div.infors > div:nth-child(4) > div.detail._togglePanelSelectLink > p')
        if len(data) == 0:
            print("Data is Empty")
            print(data)
            exit(0)
        with open(filename, 'a', encoding='utf8') as file:
            if 날짜 == None:
                형식 = '''
        <tr style="border-bottom: 1px solid e2e2e2; margin: 4px;">
            <td style="padding: 4px; text-align: center">{}</td>
            <td>{}</td>
        </tr>
'''.format(운세, data[0].text)
            else:
                형식 = '''
        <tr style="border-bottom: 1px solid e2e2e2; margin: 4px;">
            <td style="padding: 4px; text-align: center">{}</td>
            <td style="padding: 4px; text-align: center">{}</td>
            <td>{}</td>
        </tr>
'''.format(운세, 날짜, data[0].text.replace(날짜, ""))
            file.write(형식)

    sleep(1.5)

def get운세s():
    띠s = ['쥐띠', '소띠', '호랑이띠', '토끼띠', '용띠', '뱀띠', '말띠', '양띠', '원숭이띠', '닭띠', '개띠', '돼지띠']
    별자리s = {
        '물병자리': '01월 20일 ~ 02월 18일',
        '물고기자리': '02월 19일 ~ 03월 20일',
        '양자리': '03월 21일 ~ 04월 19일',
        '황소자리': '04월 20일 ~ 05월 20일',
        '쌍둥이자리': '05월 21일 ~ 06월 21일',
        '게자리': '06월 22일 ~ 07월 22일',
        '사자자리': '07월 23일 ~ 08월 22일',
        '처녀자리': '08월 23일 ~ 09월 23일',
        '천칭자리': '09월 24일 ~ 10월 22일',
        '전갈자리': '10월 23일 ~ 11월 22일',
        '사수자리': '11월 23일 ~ 12월 24일', 
        '염소자리': '12월 25일 ~ 01월 19일'
    }

    with open(filename, 'a', encoding='utf8') as file:
        file.write('''
<h3>내일 운세</h3>
<h4>띠별 운세</h4>

<table>
    <thead>
        <tr style="border-bottom: 1px solid e2e2e2; margin: 4px;">
            <td style="width: 15%; background: #094044; color: white; padding: 4px; text-align: center;">띠</td>
            <td style="width: 75%; background: #094044; color: white; padding: 4px; text-align: center;">내일 운세</td>
        </tr>
    </thead>
    <tbody>
''')

    for 띠 in tqdm(띠s, desc="    띠 운세 크롤링...", mininterval=0.1):
        get운세(띠)
        
    with open(filename, 'a', encoding='utf8') as file:
        file.write('''
    </tbody>
</table>
<br />
<h4>별자리 운세</h4>
<table>
    <thead>
        <tr style="border-bottom: 1px solid e2e2e2; margin: 4px;">
            <td style="width: 15%; background: #094044; color: white; padding: 4px; text-align: center;">별자리</td>
            <td style="width: 24%; background: #094044; color: white; padding: 4px; text-align: center;">날짜</td>
            <td style="width: 61%; background: #094044; color: white; padding: 4px; text-align: center;">내일 운세</td>
        </tr>
    </thead>
    <tbody>
''')
    sleep(3)

    for 별자리, 날짜 in tqdm(별자리s.items(), desc="별자리 운세 크롤링...", mininterval=0.1):
        get운세(별자리, 날짜)

    with open(filename, 'a', encoding='utf-8') as file:
        file.write('''
    </tbody>
</table>
''')

if __name__ == "__main__":
    writeStyle()
    get날씨()
    get운세s()
