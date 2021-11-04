import time
import requests
from bs4 import BeautifulSoup
from bs4 import element
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
browser.implicitly_wait(2)

# # 검색어 크롤링
# search_key = '한남'
# titles = []
# addresses = []
# for page in range(200):
#     url = f'https://www.fmkorea.com/index.php?act=IS&is_keyword={search_key}&mid=home&where=document&page={page+1}'
#     browser.get(url)
#     for link_idx in range(1, 10):
#         try:
#             link = browser.find_element_by_xpath(f'/html/body/div[1]/div/div/div/div[3]/div/ul[3]/li[{link_idx}]/dl/dt/a')
#             title = link.text
#             address = link.get_attribute('href')
#             titles.append(title)
#             addresses.append(address)
#         except:
#             continue
#
# titles = pd.DataFrame(titles, columns=['Title'])
# addresses = pd.DataFrame(addresses, columns=['Aref'])
# database = pd.concat([titles, addresses], axis=1)
# database.to_csv('../data/FMkorea/link_FMkorea_key2.csv')

# 일간
# titles = []
# addresses = []
# for page in range(200):
#     url = f'https://www.fmkorea.com/index.php?mid=best&page={page}'
#     browser.get(url)
#     '/html/body/div[1]/div/div/div/div[3]/div/div[3]/div/div[3]/ul/li[1]/div/h3/a'
#     '/html/body/div[1]/div/div/div/div[3]/div/div[3]/div/div[3]/ul/li[10]/div/h3/a'
#     for link_idx in range(1, 21):
#         try:
#             link = browser.find_element_by_xpath(f'/html/body/div[1]/div/div/div/div[3]/div/div[3]/div/div[3]/ul/li[{link_idx}]/div/h3/a')
#             title = link.text
#             address = link.get_attribute('href')
#             titles.append(title)
#             addresses.append(address)
#         except:
#             continue
#
# titles = pd.DataFrame(titles, columns=['Title'])
# addresses = pd.DataFrame(addresses, columns=['Aref'])
# database = pd.concat([titles, addresses], axis=1)
# database.to_csv('../data/nate_pan/database.csv')
# print()

# 댓글 가져오기
database = pd.read_csv('../data/FMkorea/link_FMkorea_key2.csv')
arefs = database['Aref']
comments = []
for aref_idx, aref in enumerate(arefs):
    start_time = time.time()
    comments_per_aref = []
    browser.get(aref)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # 베댓
    best_comments = soup.find_all('li')
    for usertxt in best_comments:
        try:
            comment_div_one = usertxt.find_all('div')[1]
            comment_div_two = comment_div_one.find_all('div')
            if type(comment_div_two[0].contents[0]) == element.Tag:
                comments_per_aref.append(comment_div_two[0].contents[1])
            else:
                comments_per_aref.append(comment_div_two[0].contents[0])
        except IndexError:
            continue
    comments.append(comments_per_aref)
    print(f'Comments Number: {len(comments_per_aref)}')
    print(f'time : {time.time()-start_time}')
    if aref_idx % 100==0:
        print(f'{aref_idx}th DONE')
#
database_comments = pd.DataFrame(comments)
database_comments.to_csv('../data/FMkorea/comments_fmkorea_key2_raw.csv')
print()
