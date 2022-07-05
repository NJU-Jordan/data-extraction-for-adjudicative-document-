from selenium.webdriver import Chrome
import time
import datetime
import selenium
from selenium import webdriver

def mainPro(start, end):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')  # 设置option
    web = webdriver.Chrome(chrome_options=option)
    # web = Chrome()
    #当前日期
    cYear = datetime.datetime.now().year
    cMonth = datetime.datetime.now().month
    cDay = datetime.datetime.now().day

    #start date
    sYear = int(start[0: 4])
    sMonth = int(start[4: 6])
    sDay = int(start[6: 8])

    #end date
    eYear = int(end[0: 4])
    eMonth = int(end[4: 6])
    eDay = int(end[6: 8])

    #start button
    backYearButton = '/html/body/div[2]/div[1]/div/div[1]/button[1]'
    backMonthButton = '/html/body/div[2]/div[1]/div/div[1]/button[2]'
    forwardMonthButton = '/html/body/div[2]/div[1]/div/div[1]/button[4]'

    #end button
    backYearButton1 = '/html/body/div[3]/div[1]/div/div[1]/button[1]'
    backMonthButton1 = '/html/body/div[3]/div[1]/div/div[1]/button[2]'
    forwardMonthButton1 = '/html/body/div[3]/div[1]/div/div[1]/button[4]'
    #open the page
    web.get('https://anli.court.gov.cn/')
    time.sleep(1)
    #打开案例库
    web.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/ul/li[6]/a').click()
    time.sleep(2)
    #高级检索
    web.find_element_by_xpath('//*[@id="aljs"]/div/div[1]/div[2]/span').click()
    time.sleep(1)
    #start Data
    web.find_element_by_xpath('//*[@id="aljs"]/div/div[2]/div/form/div[5]/div/div[2]/div/div/div[1]/div/input').click()

    time.sleep(5)
#找起始日期
    while sYear < cYear:
        web.find_element_by_xpath(backYearButton).click()
        sYear += 1
        time.sleep(1)

    if sMonth < cMonth:
        while sMonth < cMonth:
            web.find_element_by_xpath(backMonthButton).click()
            sMonth += 1
            time.sleep(1)
    elif sMonth > cMonth:
        while sMonth > cMonth:
            web.find_element_by_xpath(forwardMonthButton).click()
            sMonth -= 1
            time.sleep(1)

    i = 2 + int(sDay / 7)
    if sDay%7 == 0:
        i -= 1
    time.sleep(1)
    break_flag = False
    pAddr = ''
    for i in range(i, 8):
        for j in range(1, 8):
            addr = f'/html/body/div[2]/div[1]/div/div[2]/table[1]/tbody/tr[{i}]/td[{j}]'
            #time.sleep(1)
            fDay = cDay
            if web.find_element_by_xpath(addr).text != '今天':
                #time.sleep(1)
                fDay = int(web.find_element_by_xpath(addr).text)
            if fDay == sDay:
                #time.sleep(1)
                break_flag = True
                pAddr = addr
                break

        if break_flag:
            break
    time.sleep(1)
    web.find_element_by_xpath(pAddr).click()
    time.sleep(1)

    # end Data
    web.find_element_by_xpath('//*[@id="aljs"]/div/div[2]/div/form/div[5]/div/div[2]/div/div/div[3]/div/input').click()

    time.sleep(1)
#找结束日期
    while eYear < cYear:
        time.sleep(1)
        web.find_element_by_xpath(backYearButton1).click()
        eYear += 1
        time.sleep(1)
    if eMonth < cMonth:
        while eMonth < cMonth:
            web.find_element_by_xpath(backMonthButton1).click()
            eMonth += 1
            time.sleep(1)
    elif eMonth > cMonth:
        while eMonth > cMonth:
            web.find_element_by_xpath(forwardMonthButton1).click()
            eMonth -= 1
            time.sleep(1)
    i = 2 + int(eDay / 7)
    if eDay % 7 == 0:
        i -= 1
    time.sleep(1)
    break_flag = False
    pAddr = ''
    for i in range(i, 8):
        for j in range(1, 8):
            addr = f'/html/body/div[3]/div[1]/div/div[2]/table[1]/tbody/tr[{i}]/td[{j}]'
            #time.sleep(1)
            fDay = cDay
            if web.find_element_by_xpath(addr).text != '今天':
                #time.sleep(1)
                fDay = int(web.find_element_by_xpath(addr).text)
            if fDay == eDay:
                #time.sleep(1)
                break_flag = True
                pAddr = addr
                break
        if break_flag:
            break
    time.sleep(1)
    web.find_element_by_xpath(pAddr).click()

    time.sleep(1)
    web.find_element_by_xpath('//*[@id="aljs"]/div/div[2]/div/form/div[9]/div/button[1]').click()
    time.sleep(3)

    #找对应时间内的案件告一段落，现在开始爬取案件
    try:
        textPath = '//*[@id="alk"]/div[2]/div/div[2]/div[2]/ul/li[1]/div[1]/div[1]'
        web.find_element_by_xpath(textPath).click()
        time.sleep(2)
    except selenium.common.exceptions.ElementNotInteractableException:
        textPath = '//*[@id="alk"]/div[2]/div/div[2]/div[2]/ul/li[1]/div[2]/div[1]'
        web.find_element_by_xpath(textPath).click()
        time.sleep(2)
    except :
        print("对应时间内没有案例")
        web.close()
        return

    time.sleep(2)
    #找到第一篇符合时间要求的案件后，比对时间，如果符合，爬取案件并点击下一篇；否则结束程序
    text = web.find_element_by_xpath('//*[@id="content"]').text
    time.sleep(1)
    name1 = web.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[1]/div[1]/div[2]/h2').text
    name = name1 + ".txt"
    print(name)
    time.sleep(1)
    list = str(text).split("\n")
    for i in range(0, 4):
        list.pop()
    text = "".join(list)
    f = open("text0.txt", encoding='utf-8', mode='a')
    f.write(text)
    f.write("\n")
    f.close()
    with open(name, mode="w", encoding="utf-8") as fi:
        fi.write(text)
    web.find_element_by_xpath('//*[@id="content"]/p/span[1]').click()
    time.sleep(1)
    count = 0

    while True:
        if count > 2:
            web.close()
            return
        Tdata = web.find_element_by_xpath('//*[@id="jbxx"]/div[2]/ul/li[6]/p').text
        time.sleep(1)
        itsTime = int(getTime(Tdata))
        if itsTime < int(start):
            count+=1
            continue
            # web.close()
            # return
        count = 0
        text = web.find_element_by_xpath('//*[@id="content"]').text
        name1 = str(web.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[1]/div[1]/div[2]/h2').text)
        name = name1 + ".txt"
        print(name)
        time.sleep(1)
        list = str(text).split("\n")
        for i in range(0, 4):
            list.pop()
        text = "".join(list)
        f = open("text0.txt", encoding='utf-8', mode='a')
        f.write(text)
        f.write("\n")
        f.close()
        with open(name, mode="w", encoding="utf-8") as fi:
            fi.write(text)
        web.find_element_by_xpath('//*[@id="content"]/p/span[1]').click()
        time.sleep(1)

def getTime(time):
    list = str(time).split("\n")
    if len(list) < 2:
        return "00000000"
    outcome = list[1].replace("-", "")
    return outcome
