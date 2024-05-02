from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
import json

url ='https://tku.schroll.edu.tw/eMis/tmw0020.aspx'
results = []
#with open('d:\engineer\Project\worm\cookies_jar.json') as f:
#    cookies = json.load(f)

driver = webdriver.Chrome()
driver.get(url)

#for cookie in cookies:
#    driver.add_cookie(cookie)
#driver.refresh()

#第一頁面

p1 = driver.find_element(By.LINK_TEXT, "查詢課程資料(含歷年)")
ActionChains(driver).click(p1).perform()
#第二頁面
#select_element = driver.find_element(By.NAME, 'DropDownList1')#選擇學年學期
#select1 = Select(select_element)



select1 = Select(driver.find_element(By.NAME, 'DropDownList1'))#選擇學年學期
select1.select_by_value('1052')#每個選項的編號為學年+學期,例112年上學期為1121,112年下學期則為1122.

select2 = Select(driver.find_element(By.NAME, 'DropDownList2'))#選擇課程
select2.select_by_value('1')# 1 為"所有課程"之選項代號

select3 = Select(driver.find_element(By.NAME, 'DropDownList3'))#選擇學院
select3.select_by_value('%')# % 為"所有學院"之選項代號

select4 = Select(driver.find_element(By.NAME, 'DropDownList4'))#選擇系所
select4.select_by_value('*')# * 為"全部"之選項代號

select5 = Select(driver.find_element(By.NAME, 'DropDownList5'))#選擇年級
select5.select_by_value('*')# * 為"全部"之選項代號

search = driver.find_element(By.NAME, 'Button1')#找到查詢紐
search.click()#按下查詢紐

#nextpage_top =driver.find_element(By.NAME, 'Button2')#頁面最上方的 '下一頁' 按鈕  
lists =[]
while True:
    row = driver.find_elements(By.TAG_NAME, 'tr')
    for i in row:
        j = i.find_elements(By.TAG_NAME, 'td')
        if len(j)>10:
            grade_th = j[0].text        #年級
            class_id = j[2].text        #開課序號
            sub_id = j[3].text          #科目編號
            class_nid = j[6].text       #班別
            ER_id = j[8].text           #選必修
            credit = j[9].text          #學分
            #group = j[10].text         #群別
            sub_name = j[11].text       #科目名稱
            teacher_name = j[13].text   #教師名稱
            list = {
                'Grade_th': grade_th,
                'Class_ID': class_id,
                'Sub_ID':   sub_id,
                'Class_NID':class_nid,
                'ER_ID':    ER_id,
                'Credit':   credit,
                #'Group':    group,
                'Sub_Name': sub_name,
                'Teacher':  teacher_name,
            }
            lists.append(list)
    nextpagebut = driver.find_element(By.NAME, 'Button4')#頁面最下方的 '下一頁' 按鈕
    if nextpagebut.get_attribute('disabled'):
        print('end')
        with open('d:\engineer\Project\worm\LIST\s1052.csv','a',encoding='utf-8') as f:
            json.dump(lists,f,indent=2,sort_keys=True,ensure_ascii=False)
        break
    else:
        nextpagebut.click()
    
#for txt in txts:
#    gradeth = txt.find_element(By.CLASS_NAME) #年級
#    class_id = #開課序號
#    sub_id = #科目編號
#    class_nid = #班別
#    ER_id = #選必修
#    credit = #學分
#    group = #群別



time.sleep(20)
driver.close()
