from time import sleep
import time
import re 
import random
import shutil

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


area = input('検索する「エリア・駅」を入力して下さい。')
genre = input('検索する「店名・ジャンル」を入力して下さい。')
search_number = input('検索件数を入力して下さい。(半角数字)')
mail = input('送信先メールアドレスを入力して下さい。（半角英数字）')
#「エリア・駅」を検索
def search_area(area):
    search_area = driver.find_element(By.CSS_SELECTOR,'input#js-suggest-area')
    search_area.send_keys(area)
    sleep(1)
    #driver.find_element(By.CSS_SELECTOR,'button.p-search__button').click()
#「店名・ジャンル」を検索
def search_genre(genre):
    search_genre = driver.find_element(By.CSS_SELECTOR,'input#js-suggest-shop')
    search_genre.send_keys(genre)
    sleep(1)
    driver.find_element(By.CSS_SELECTOR,'button.p-search__button').click()
#住所を分割
def devide_address(address):
    matches = re.match('(.{2,3}?[都道府県])(.+?郡.+?[町村]\D+|.+?市.+?区\D+|.+?[市区町村]\D+)([0-9|-]+|[0-9|‐]+|[0-9|－]+)',address)
    return matches.groups
#正しいメールアドレスを取得
def correct_mail(mail):
    matche_mail = mail.replace('mailto:','')
    return matche_mail
#店舗名を取得
def get_shop_name():
    shop_name = driver.find_elements(By.CSS_SELECTOR,'p#info-name')
    if shop_name:
        shop_name = shop_name[0].text
        print(shop_name)
        return shop_name
    else:
        return ''
#電話番号を取得
def get_tel():
    tel = driver.find_elements(By.CSS_SELECTOR,'span.number')
    if tel:
        return tel[0].text
    else:
        return ''
#出力したcsvファイルをメールで送信
def send_mail(mail_address):
    from_email ='saijotaito.programming@gmail.com'
    if mail_address:
        to_email = mail_address
    else:
        to_email = 'saijotaito.programming@gmail.com'
    cc_mail = ''
    mail_title = 'レストラン検索結果'
    message = ''
    #MIMEMultipartクラスでMIMEオブジェクトを生成
    msg = MIMEMultipart()
    msg['Subject'] = mail_title
    msg['To'] = to_email
    msg['From'] = from_email
    msg.attach(MIMEText(message))
    #MIMEApplicationクラスで送付ファイルからオブジェクトを生成
    with open(r"test.csv","rb") as f:
        attachment = MIMEApplication(f.read())
        attachment.add_header("Content-Disposition", "attachment", filename="test.csv")
    #先ほど生成したMMIMEオブジェクトにアタッチ
    msg.attach(attachment)
    #サーバを指定してメールを送信
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587
    smtp_password = 'conqkrxjbsfavinf'
    server = smtplib.SMTP(smtp_host,smtp_port)
    server.starttls()
    server.login(from_email,smtp_password)
    server.send_message(msg)
    server.quit()

user_agent = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
                  ]

CHROME_DRIVER_PATH = r"C:\Users\taiha\Desktop\chromedriver\chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('--user-agent=' + user_agent[random.randrange(0, len(user_agent), 1)])
driver = webdriver.Chrome(executable_path=r"C:\Users\taiha\Desktop\chromedriver\chromedriver.exe",options=options)
driver.implicitly_wait(5)

url = 'https://www.gnavi.co.jp/'
driver.get(url)
sleep(3)
#検索関数の実行
search_area(area)
search_genre(genre)
sleep(3)

d_list = []
while True:
    containers = driver.find_elements(By.CSS_SELECTOR,'div.style_restaurant__SeIVn')
    print(len(containers))
    for i in range(len(containers)):
        print("="*30,i,"="*30)
        container = driver.find_elements(By.CSS_SELECTOR,'div.style_restaurant__SeIVn')[i]
        #container = containers[i]
#広告の店舗情報をスキップ
        pr = container.get_attribute('data-restaurant-pr')
        if pr:
            continue
        else:
            #店舗詳細ページに遷移
            container.find_element(By.CSS_SELECTOR,'a.style_titleLink__oiHVJ').click()
            sleep(3)
            shop_name = get_shop_name()
            tel = get_tel()
            mail = driver.find_elements(By.CSS_SELECTOR,'table.basic-table > tbody > tr:nth-of-type(12) > td > ul > li:nth-of-type(2) > a')
            if mail:
                mail = mail[0].get_attribute('href')
                mail = correct_mail(mail)
            else:
                mail = ''
        
            address = driver.find_elements(By.CSS_SELECTOR,'span.region')
            if address:
                address = address[0].text
                devided_address =  devide_address(address)
                prefecture = devided_address()[0]
                district = devided_address()[1]
                number = devided_address()[2]
                print(number)
            else:
                prefecture = ''
                district = ''
                number = ''
                    
            building = driver.find_elements(By.CSS_SELECTOR,'span.locality')
            if building:
                building = building[0].text
            else:
                building = ''
                
            web_site = driver.find_elements(By.CSS_SELECTOR,'a.go-off')
            if web_site:
                web_site = web_site[0].get_attribute('href')
            else:
                web_site = ''
                
            d_list.append({
                '店舗名':shop_name,
                '電話番号':tel,
                'メールアドレス':mail,
                '都道府県':prefecture,
                '市町村区':district,
                '番地':number,
                '建物名':building,
                'URL':web_site
            })

            print(len(d_list))
            if len(d_list) == int(search_number):
                break
            driver.back()
            sleep(3)
    if len(d_list) == int(search_number):
        break
    print('ページ遷移中')
    driver.find_element(By.CSS_SELECTOR,'ul.style_pages__Y9bbR > li:nth-of-type(10) > a').click()
    sleep(3)

df = pd.DataFrame(d_list)
df.to_csv('test.csv',index=None,encoding='utf-8-sig')

#source = r"C:\Users\taiha\Desktop\Final-Answer\1-2.csv"
#destination = r"C:\Users\taiha\Desktop\Final-Answer\Exercise_for_Pool\python\ex1_web_scraping\1-2.csv"
#shutil.move(source,destination)

driver.quit()
send_mail(mail)