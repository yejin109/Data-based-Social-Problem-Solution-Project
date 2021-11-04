import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver import Chrome

# Generate Datetime
period_start = '20200101'
period_end = '20210831'
dates = pd.date_range(start=period_start, end=period_end)
date_idx = dates.strftime("%Y%m%d").tolist()

# Browser Driver 설정
direc = 'chromedriver.exe'
delay = 3
browser = Chrome(direc)
browser.implicitly_wait(3)

# 검색어 크롤링
search_key = '페미'
titles = []
addresses = []
for page in range(200):
    url = f'https://pann.nate.com/search/talk?q={search_key}&page={1+page}'
    browser.get(url)
    for link_idx in range(1, 10):
        try:
            link = browser.find_element_by_xpath(f'/html/body/div[2]/div[2]/div[2]/div[1]/div[3]/ul/li[{link_idx}]/div[1]/a')
            title = link.text
            address = link.get_attribute('href')
            titles.append(title)
            addresses.append(address)
        except:
            continue

titles = pd.DataFrame(titles, columns=['Title'])
addresses = pd.DataFrame(addresses, columns=['Aref'])
database = pd.concat([titles, addresses], axis=1)
database.to_csv('../data/nate_pan/link_nate_pan_key1.csv')

# 실시간
# key_realtime = 'total'
# https://pann.nate.com/talk/ranking?rankingType=total&page=1
# https://pann.nate.com/talk/ranking?rankingType=total&page=2

# 일간
# titles = []
# addresses = []
# for date in date_idx:
#     for page in range(1, 3):
#         url = f'https://pann.nate.com/talk/ranking/d?stdt={date}&page={page}'
#         browser.get(url)
#         for link_idx in range(1, 51):
#             try:
#                 link = browser.find_element_by_xpath(f'/html/body/div[2]/div[2]/div[3]/div[1]/div[2]/div[2]/ul/li[{link_idx}]/dl/dt/a')
#                 title = link.get_attribute('title')
#                 address = link.get_attribute('href')
#                 titles.append(title)
#                 addresses.append(address)
#             except:
#                 continue
#
# titles = pd.DataFrame(titles, columns=['Title'])
# addresses = pd.DataFrame(addresses, columns=['Aref'])
# database = pd.concat([titles, addresses], axis=1)
# database.to_csv('../data/nate_pan/database.csv')

# 댓글 가져오기
database = pd.read_csv('../data/nate_pan/link_nate_pan_key1.csv')
arefs = database['Aref']
comments = []
for aref_idx, aref in enumerate(arefs):
    start_time = time.time()
    comments_per_aref = []
    response = requests.get(aref)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        usertxts = soup.find_all('dd', {'class': 'usertxt'})
        for usertxt in usertxts:
            try:
                comment = usertxt.find('span').contents[0]
                comment = comment.replace('\n', '')
                comment = comment.replace('\t', '')
                comments_per_aref.append(comment)
            except:
                continue
    else:
        print(response.status_code)
    comments.append(comments_per_aref)
    print(f'Comments Number: {len(comments_per_aref)}')
    print(f'time : {time.time()-start_time}')
    if aref_idx % 100==0:
        print(f'{aref_idx}th DONE')

database_comments = pd.DataFrame(comments)
database_comments.to_csv('../data/nate_pan/comments_nate_pan_key1_raw.csv')
print()
