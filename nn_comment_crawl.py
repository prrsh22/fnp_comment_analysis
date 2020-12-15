from selenium import webdriver
import time
import openpyxl

try:
    wb = openpyxl.load_workbook('저장할 파일명')
    sheet = wb.active
except:
    wb = openpyxl.Workbook()
    sheet = wb.active
    # 댓글 작성자 ****으로 마스킹 되어 있어 굳이 수집하지 않음
    sheet.append(['news_title', 'news_uploader', 'content', 'like', 'dislike'])

driver = webdriver.Chrome('chromedriver.exe')


urls = ['수집할 댓글 페이지 리스트']

for url in urls:
    driver.get(url)
    time.sleep(3)
    news_title = driver.find_element_by_css_selector('h3#articleTitle').text
    news_uploader = driver.find_element_by_css_selector('div.article_header img').get_attribute('title')

    #최근 기사의 경우
    n_of_comments = int(driver.find_element_by_css_selector('span.u_cbox_info_txt').text)
    #옛날 기사의 경우
    #n_of_comments = int(driver.find_element_by_css_selector('span.u_cbox_count').text)
    
    n_of_comments_collected = 0

    while (n_of_comments_collected < n_of_comments):

        comments_now_seen = driver.find_elements_by_css_selector('div.u_cbox_area')
        for comment in comments_now_seen[n_of_comments_collected:]:

            #삭제, 규정위반 댓글 스킵
            try:
                content = comment.find_element_by_css_selector('span.u_cbox_contents').text
                like = int(comment.find_element_by_css_selector('em.u_cbox_cnt_recomm').text)
                dislike = int(comment.find_element_by_css_selector('em.u_cbox_cnt_unrecomm').text)
                sheet.append([news_title, news_uploader, content, like, dislike])
                n_of_comments_collected += 1

            except:
                continue

        try:
            driver.find_element_by_css_selector('div.u_cbox_paginate a').click()
        except:
            break

        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")



wb.save('저장할 파일명')