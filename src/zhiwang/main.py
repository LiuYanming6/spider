# from ways import get_data
import csv
import time

from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from src.ocr.bdocr import client, options, get_file_content


def do_checkCode(driver):
    # # 验证码在定端, 所以要返回顶端
    body = driver.find_element_by_tag_name("body")
    body.send_keys(Keys.HOME)  # element exceptions.ElementNotInteractableException: Message: element not interactable
    # driver.find_element_by_id('backtop').click()
    time.sleep(1)

    path = 'checkcode.png'
    driver.save_screenshot(path)
    driver.save_screenshot("bak.png")

    element = driver.find_element_by_id('CheckCodeImg')  # 获取验证码元素
    left = element.location['x']
    top = element.location['y']
    right = element.location['x'] + element.size['width']
    bottom = element.location['y'] + element.size['height']
    print("%d %d %d %d" % (left, top, right, bottom))
    im = Image.open(path)
    # im = im.crop((left, top, right, bottom))  # 切割
    im = im.crop((619, 408, 750, 490))
    im.save(path)

    # 这是重新下载, 每次都不一样的,所以不能用
    # urlretrieve(element.get_attribute('src'), path)
    # 格式转换. http://www.pythonclub.org/modules/pil/convert-png-gif
    # im = Image.open(path)
    # transparency = im.info['transparency']
    # im.save('checkcode.png', transparency=transparency)

    # 百度ocr处理
    image = get_file_content('checkcode.png')
    # {'log_id': 1708842185825337341, 'direction': 0, 'words_result_num': 1, 'words_result': [{'words': '2XNT4', 'probability': {'variance': 0.0, 'average': 0.925741, 'min': 0.925741}}], 'language': 0}
    ret = client.basicGeneral(image, options)
    print(ret)

    driver.find_element_by_id("CheckCode").send_keys(ret['words_result'][0]['words'])
    driver.find_element_by_xpath("//input[@value='提交']").click()


driver_path = r"C:\chromedriver.exe"
driver = webdriver.Chrome(executable_path=driver_path)
url = "https://www.cnki.net/"
driver.get(url)
driver.implicitly_wait(10)

driver.find_element_by_id("txt_SearchText").send_keys("全域旅游")
searchBtn = driver.find_element_by_class_name("search-btn").click()
# /*
# 反爬虫机制
# 1 请求头反爬虫，这个也是最简单的，如果你不给定请求头，对方服务器就不会理你。需要设置的参数有User-Agent、Referer和Cookie
# 2 动态网页，利用Ajax技术使用js接口来传递数据
# iframe <iframe src='1.html' id='iframeResult'></iframe>
iframe = driver.find_element_by_id('iframeResult')
driver.switch_to.frame(iframe)

# 过滤条件
# driver.find_element_by_id("CJFQ").click()# 期刊
driver.find_element_by_link_text("中文文献").click()
time.sleep(3)  # 强制等待,切中文放在后会使切摘要不生效
driver.find_element_by_link_text("切换到摘要").click()
driver.find_element_by_link_text("相关度").click()
# driver.find_element_by_class_name("numNow").click()
# summary.click()

file = open('zhiWang.csv', 'w', newline='')
writer = csv.writer(file, delimiter=',',
                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
page_num = 1
while 1:
    # 一页d
    lines = driver.find_elements_by_class_name("GridRightColumn")
    print("正在处理第{%d}页 {%d}" % (page_num, len(lines)))
    if (len(lines) == 0):
        # 可能出现验证码
        do_checkCode(driver)
        time.sleep(3)
        continue
    for line in lines:
        # print(line)
        name = line.find_elements_by_tag_name('a')[0].text
        # print(name)
        author = line.find_elements_by_class_name('author')[0].text
        # print(author)
        journal = line.find_elements_by_tag_name('a')[1].text
        # print(journal)
        sammary = line.find_elements_by_tag_name('p')[0].text
        # print(sammary)
        # lable没有唯一,所以从上级开始匹配
        tim = line.find_element_by_xpath("//div[@class='DetailNum']/label").text
        # print(time.replace('发表时间：', ''))
        writer.writerow([name, author, journal, tim, sammary])

    # 下一页
    driver.find_elements_by_xpath("//div[@class='TitleLeftCell']/a")[-1].click()
    # driver.find_element_by_link_text("切换到摘要").click()
    page_num += 1
