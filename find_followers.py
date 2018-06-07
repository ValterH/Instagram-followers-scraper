import sys
import json
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

args = sys.argv

if args[1] == '-u':
    uname = args[2]
else:
    sys.exit("Specify username")
if args[3] == '-p':
    pwd=args[4]
else:
    sys.exit("Specify password")
if args[5]== '-q':
    query_string = args[6]
    queries = query_string.replace(',',' ').split()
else:
    sys.exit("Specify queries")

baseurl = 'https://www.instagram.com/'
driver = webdriver.Chrome()
driver.get(baseurl + 'accounts/login/')
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']"))).send_keys(uname)
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']"))).send_keys(pwd)
js ="document.getElementsByTagName('button')[1].click();"
driver.execute_script(js)

searchbox = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Search']")))
followers = {}
for query in queries:
    driver.get(baseurl+query+'/')
    
    follow_ele = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "a[href='/"+query+"/followers/']"))
    )
    num = str(follow_ele.text)
    #print(num)
    ms = False
    ks = False
    dots = False
    if (num.find('m')>-1):
        ms = True
    if (num.find('k')>-1):
        ks = True
    if (num.find('.')>-1):
        dots = True
    num = ''.join(filter(str.isdigit, num))
    number = int(num)
    if ms:
        number = number * 1000000
    if ks:
        number = number * 1000
        if dots:
            number = number / 10
    #print(number)
    js = 'document.querySelectorAll("a[href=' + "'/" + query + "/followers/'" + ']")[0].click();'
    driver.execute_script(js)
    
    title_ele = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[contains(text(), 'Followers')]"))
    )
    List = title_ele.find_element_by_xpath(
        '..').find_element_by_tag_name('ul')
    List.click()
    num_of_shown_follow = len(List.find_elements_by_tag_name('li'))
    last_num = 0
    counter = 0
    while len(List.find_elements_by_tag_name('li')) < number-1:
        #print(str(last_num/number * 100)+"%")
        if len(List.find_elements_by_tag_name('li')) == last_num:
            counter += 1
        else:
            counter = 0
        if counter == 10:
            time.sleep(3600)
        last_num=len(List.find_elements_by_tag_name('li'))
        element = List.find_elements_by_tag_name('li')[-1]
        try:
            element.click()
            element.send_keys(Keys.SPACE)
        except Exception as e:
            time.sleep(0.1)
    tags = []
    for ele in List.find_elements_by_tag_name('li'):
        tags.append(ele.text.split('\n')[0])

    followers[query]=tags
driver.quit()
with open('followers.json', 'w') as file:
     file.write(json.dumps(followers))

sys.exit()
