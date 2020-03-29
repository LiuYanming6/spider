import configparser
import csv
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def login(user, pwd):
    driver_path = r"../chromedriver.exe"
    driver = webdriver.Chrome(executable_path=driver_path)
    url = "http://km.cnki.net/foundation/home/login"
    driver.get(url)
    driver.implicitly_wait(10)  # 找不到时等待10秒

    driver.find_element_by_name('username').send_keys(user)
    driver.find_element_by_name('password').send_keys(pwd)
    driver.find_element_by_class_name('login-btn').click()

    # 退出登录后的dialog
    time.sleep(2)
    body = driver.find_element_by_tag_name("body")
    body.send_keys(Keys.ESCAPE)

    return driver


def search(driver, searchWord):
    print(searchWord)
    driver.find_element_by_xpath("//input[@placeholder='输入检索词']").send_keys("全域旅游")
    # use ChroPath Studio for chrome
    driver.find_element_by_xpath(
        '''//div[@class='search-panel']//button[@class='el-button mr20 btn-bluex el-button--primary']//span''') \
        .click()


def fetch(driver, writer):
    # driver.switch_to_frame(driver.find_element_by_tag_name('main'))
    # driver.switch_to.window()

    page_num = 0
    while 1:
        page_num += 1
        # /html/body/section/section/section/main/div/div[4]/div[1]
        # /html/body/section/section/section/main/div/div[4]/div[2]
        lines = driver.find_elements_by_xpath('/html/body/section/section/section/main/div/div[4]/div')
        print("正在处理第{%d}页 共{%d}条" % (page_num, len(lines)))
        if (len(lines) == 0):
            break
        for line in lines:
            name = line.find_element_by_class_name('colleci-top')
            aut = line.find_element_by_class_name("colleci-aut")
            summary = line.find_element_by_class_name("colleci-mid").find_elements_by_tag_name("span")[1].text
            keys = line.find_element_by_xpath("//p[@class='float-l']/span")

            writer.writerow([name.find_elements_by_tag_name('span')[0].text,# 主题
                             aut.find_elements_by_tag_name("span")[0].text,# 作者
                             aut.find_elements_by_tag_name("span")[1].text,# 日期
                             aut.find_elements_by_tag_name("span")[2].text,# 来源
                             keys.text, #关键字
                             summary])  # 摘要

        driver.find_element_by_xpath("//i[@class='el-icon el-icon-arrow-right']") \
            .click()  # 下一页


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('../config.ini')
    driver = login(config.get('okms', 'Username'), config.get('okms', 'password'))

    search(driver, config.get('okms', 'SearchWord'))
    time.sleep(10)
    file = open('okms.csv', 'w', newline='')
    writer = csv.writer(file, delimiter=',',
                        quotechar='|', quoting=csv.QUOTE_ALL)

    fetch(driver, writer)
