from selenium import webdriver
import time
import openpyxl

try:
    wb = openpyxl.load_workbook('저장할 파일명')
    sheet = wb.active
except:
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.append(['vid_title', 'vid_uploader', 'c_author', 'content', 'like'])

driver = webdriver.Chrome('chromedriver.exe')

#댓글 수집할 영상 urls
urls = []

for url in urls:
    driver.get(url)
    time.sleep(3)
    vid_title = driver.find_element_by_css_selector('div#container h1.title yt-formatted-string').text
    vid_uploader = driver.find_element_by_css_selector('div.ytd-channel-name yt-formatted-string a.yt-formatted-string').text

    driver.execute_script("window.scrollBy(0, 400);")
    time.sleep(2)
    
    index = 0
    cc_index = 0
    n_of_comments_collected = 0
    
    # 아직 수집하지 않은 새 댓글 나타날 때까지 스크롤 (10번 시도해도 안 되면)
    while 1:
        scrollFailed = 0
        
        while 1:
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(3)
            comments = driver.find_elements_by_css_selector('div.ytd-comment-renderer div#main')
            
            if len(comments) == n_of_comments_collected:
                print('scroll failed')
                scrollFailed += 1
                if scrollFailed > 10:
                    break
            else:
                break
                
        # 더이상 스크롤이 불가할 때 이 url 내 수집 종료
        if scrollFailed > 10:
            break


        # 수집, 기록
        for comment in comments[index:]:
            # 채널이 댓글 단 경우 다른 선택자
            try:
                c_author = comment.find_element_by_css_selector('yt-formatted-string.ytd-channel-name').text
            except:
                c_author = comment.find_element_by_css_selector('a#author-text span').text

            #긴 댓글은 자세히 보기 눌러서 내용 수집
            try:
                comment.find_element_by_css_selector('paper-button#more').click()
                content = comment.find_element_by_css_selector('yt-formatted-string#content-text').text
            except:
                content = comment.find_element_by_css_selector('yt-formatted-string#content-text').text

            like = comment.find_element_by_css_selector('span#vote-count-middle').text

            if like == '':
                like = 0
            elif '천' in like:
                like = int(float(like[:-1]) * 1000)
            elif '만' in like:
                like = int(float(like[:-1]) * 10000)
            else:
                like = int(like)

            sheet.append([vid_title, vid_uploader, c_author, content, like])

        # 수집 후 인덱스 늘려주기
        n_of_comments_collected = len(comments)
        index = n_of_comments_collected


wb.save('저장할 파일명')

