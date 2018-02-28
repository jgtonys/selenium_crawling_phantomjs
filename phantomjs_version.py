#-*- coding:utf-8 -*-
#joonggonara crawling program. 2017-11-03
#python3.4, selenium, phantomjs, beautifulsoup



from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import sys
import codecs

def spider(f):
    keyword = input("input the keyword you are looking for : ") #keyword input
    n = int(input("number of pages you are looking for : "))  #pages input
    start = time.time()
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
    driver.implicitly_wait(3)
    driver.get('http://cafe.naver.com/joonggonara')
    #driver.set_window_size(2000,5000)
    driver.find_element_by_id('topLayerQueryInput').send_keys(keyword)								#inputing keyword in search box
    search_button_element = driver.find_element_by_css_selector("form[name='frmBoardSearch'] a")	#search!
    search_button_element.click()

    #convert frame
    iframe_element = driver.find_element_by_css_selector("iframe#cafe_main")						#reload iframe
    driver.switch_to_frame(iframe_element)															#move to the new frame
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')

    #searching board
    for i in range(n):
        css_selector_page = "table.Nnavi a"															#paging buttons
        page_buttons= driver.find_elements_by_css_selector(css_selector_page)
        page_buttons[i].click()
        css_selector_title = "td.board-list "														#board title
        title_elements_2 = driver.find_elements_by_css_selector("td.board-list")
        driver.save_screenshot("/scshot/s"+str(i)+".png")
        for title_element_2 in title_elements_2:
            #https://r12a.github.io/apps/encodings/ 
            title_text = title_element_2.text.encode("cp1252").decode("euc-kr")						#encoding..problem
            f.write(title_text+"\n")
            href_text = title_element_2.find_element_by_css_selector('a').get_attribute('href')
            f.write(href_text+"\n")
            print(title_text)
    driver.switch_to_default_content()																#원래html로 돌아간다.
    print("finished")
    end = time.time()
    print(end-start)

if __name__=="__main__":
    f = codecs.open("ouput.txt",'w')
    spider(f)
    f.close()
