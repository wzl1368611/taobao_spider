import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
import json, re
import requests

chrome_options = Options()
chrome_options.add_argument('--window-size=1500,1366')
driver = webdriver.Chrome(options=chrome_options)
# driver = webdriver.Chrome()

import csv

# 保存每次登陆的cookie
cookies = {}


# 登陆步骤
def login():
    # driver=webdriver.Chrome()
    # 请求网页

    # driver.get(url)
    # 查找id
    # loginBtn=driver.find_element_by_id('nav-login')
    # loginBtn.click()
    driver.get("https://login.taobao.com/member/login.jhtml?")
    time.sleep(5)
    for handle in driver.window_handles:  # 方法二，始终获得当前最后的窗口
        driver.switch_to.window(handle)
    # 输入账号密码
    user = 'asdsdasddfas'
    # 输入你的密码
    passwd = 'asdaffsdda'
    # id="fm-login-id"
    # id="fm-login-password"
    input_user = driver.find_element_by_id('fm-login-id')
    input_user.send_keys(user)
    time.sleep(5)
    input_pwd = driver.find_element_by_id('fm-login-password')
    input_pwd.send_keys(passwd)
    time.sleep(5)
    # class="fm-button fm-submit password-login"
    login_btn = driver.find_element_by_class_name('fm-button.fm-submit.password-login')
    login_btn.click()
    time.sleep(5)
    print('登录成功')
    for handle in driver.window_handles:  # 方法二，始终获得当前最后的窗口
        driver.switch_to.window(handle)

    # 获取淘宝的cookie值是多少，然后在去爬取后台订单

    # search()
    '''
    <a href="//www.taobao.com/" target="_top">
                        
                        <span>淘宝网首页</span>
                    </a>
    '''
    # //*[@id="J_SiteNavHome"]
    # links  = driver.find_elements_by_xpath('//*[@id="J_SiteNavHome"]/div/a')

    # sreach_window=driver.current_window_handle
    # driver.switch_to_window(driver.window_handles[1])

    # links = driver.find_elements_by_xpath('//ul[@class="site-nav-bd-r"]/li[@class="site-nav-menu.site-nav-home"]/div/a')[0]
    # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.weibo-login')))
    # redirectUrl=links.get_attribute('href')


def select_orders():
    login()
    time.sleep(5)
    # driver.get('https://i.taobao.com/my_taobao.htm?nekot=YWExOTc3ODQwODYx1603467566808')
    driver.get('https://i.taobao.com/my_taobao.htm?')

    for handle in driver.window_handles:  # 方法二，始终获得当前最后的窗口
        driver.switch_to.window(handle)

    time.sleep(5)
    for dictx in driver.get_cookies():
        cookies[dictx['name']] = dictx['value']


def get_orders(my_cookie):
    print('cookie是-----------------------------------------------------------------')
    print(my_cookie)
    data_lists = []
    url = 'https://buyertrade.taobao.com/trade/itemlist/asyncBought.htm?action=itemlist/BoughtQueryAction&event_submit_do_query=1&_input_charset=utf8'
    headers = {
        'authority': 'buyertrade.taobao.com',
        'method': 'POST',
        'path': '/trade/itemlist/asyncBought.htm?action=itemlist/BoughtQueryAction&event_submit_do_query=1&_input_charset=utf8',
        'scheme': 'https',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-length': '33',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://buyertrade.taobao.com',
        'referer': 'https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm?spm=a21wu.241046-cn.1997525045.2.41cab6cblZG2lP',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    broswer_cookie = '_samesite_flag_=true; cookie2=1e84f3524c032f4df0432ada158a26bf; t=5cf8c0e2ad4d179a63b35c5c7891206b; _tb_token_=78be6b64e38ee; cna=OeUZGFs+4zUCARsm/kyjLoC1; xlly_s=1; lgc=aa1977840861; dnk=aa1977840861; tracknick=aa1977840861; _cc_=V32FPkk%2Fhw%3D%3D; mt=ci=-1_0; thw=cn; l=eBNjyvycOp4Nymx2KO5a-urza77OPIOfcrVzaNbMiInca6M1TF6EkNQV3kFB7dtjit5fcLxlmtmRRRnkPfULRKOvjLhCPlUOrip6Je1..; isg=BIyMXzx3P00cmSsxYQd2da4YXeq-xTBv7FlXqeZMvTfKcSR7JNFY_2zDEXjJP2jH; tfstk=c7wcBQspDSlfsnhuOtMbvWnNL97da1CqlRyzU8yS9p8uG_2r0sDHaB7RBg0YoRd1.; sgcookie=E100IdRpkNGakaNfftr4YJC5xz%2BRA2YRYhQdCDjzZ4qit93PHfwfk3pasX40xn5frGp9ufWu7PvJyBWQdhro%2BmboSw%3D%3D; unb=1081686429; uc1=pas=0&cookie15=U%2BGCWk%2F75gdr5Q%3D%3D&cookie14=Uoe0bk1nmCgwNg%3D%3D&cookie21=VT5L2FSpdet1FS8C2gIFaQ%3D%3D&cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D&existShop=false; uc3=lg2=Vq8l%2BKCLz3%2F65A%3D%3D&nk2=AnDVLVDQ74FuN5%2Bf&id2=UoH38lxlrMGVoQ%3D%3D&vt3=F8dCufJDy7NARwl837k%3D; csg=5ea4c88d; cookie17=UoH38lxlrMGVoQ%3D%3D; skt=63157293cb5ae614; existShop=MTYwMzQ2ODk5MQ%3D%3D; uc4=nk4=0%40AJshdHhcHunBX3daT3SZEmgGH3VUv8Q%3D&id4=0%40UOnojfZl0YaV%2B%2BEAtPeFlNUMvpFW; _l_g_=Ug%3D%3D; sg=196; _nk_=aa1977840861; cookie1=BxUEep3zFLIewQ9V3tWAOxmrjWZRAQAsUvVRNDTjAK8%3D'
    broswer_headers = {
        'authority': 'i.taobao.com',
        'method': 'GET',
        'path': '/my_taobao.htm?nekot=YWExOTc3ODQwODYx1603467566808',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'referer': 'https://login.taobao.com/member/login.jhtml?',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
    }
    # 'cookie':my_cookie,
    for i in range(1, 3):

        form_data = {
            'pageNum': i,
            'pageSize': 15,
            'prePageNo': 2
        }
        res = requests.post(url, headers=headers, cookies=my_cookie, data=form_data)
        print('################################')
        print(res.text)
        json_date = res.json()
        with open('tao_order.txt', 'a') as f:
            f.write(json.dumps(json_date))
        # 终于取出数据了，！！！！！！！！！！！！！！！
        # order_number=json_date['mainOrders'][0]['id']   #  订单号: 1295072208095682964

        # post_type=json_date['mainOrders'][0]['payInfo']['postType']     # 自动充值 (支付方式)
        # acture_fee=json_date['mainOrders'][0]['payInfo']['actualFee']   # 实际价格
        # seller_nick=json_date['mainOrders'][0]['seller']['nick']    # 销售店名
        # status_ok=json_date['mainOrders'][0]['statusInfo']['operations']['text']   #交易状态 充值成功   
        # date=json_date['mainOrders'][0]['orderInfo']['createDay']            # 订单日期

        # quantity=json_date['mainOrders'][0]['subOrders']['quantity']        # 数量
        # title=json_date['mainOrders'][0]['subOrders']['itemInfo']['title']  # 主题是
        print('##################################')
        print(json_date['mainOrders'])
        for item in json_date['mainOrders']:
            data_list = {}
            # item=json.loads(item)
            order_number = repr(str(item['id']))  # 订单号: 1295072208095682964

            # post_type=item['payInfo']['postType']     # 自动充值 (支付方式)
            acture_fee = item['payInfo']['actualFee']  # 实际价格
            seller_nick = item['seller']['nick']  # 销售店名
            status_ok = item['statusInfo']['text']  # 交易状态 充值成功
            date = item['orderInfo']['createDay']  # 订单日期

            quantity = item['subOrders'][0]['quantity']  # 数量
            title = item['subOrders'][0]['itemInfo']['title']  # 主题是

            data_list['date'] = date
            data_list['seller_nick'] = seller_nick
            data_list['title'] = title
            data_list['order_number'] = order_number
            data_list['acture_fee'] = acture_fee
            data_list['quantity'] = quantity

            data_list['status_ok'] = status_ok
            # data_list['post_type']=post_type

            data_lists.append(data_list)
            print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
            print(order_number)
            print(acture_fee)
            print(seller_nick)
            print(status_ok)
            print(date)
            print(quantity)
            print(title)
    return data_lists


def search():
    login()
    try:
        driver.get('https://www.taobao.com')  # 跳转到首页

        # driver.switch_to.window(driver.window_handles[2]) #方法一，注意window_handles[2]变成了2

        for handle in driver.window_handles:  # 方法二，始终获得当前最后的窗口
            driver.switch_to.window(handle)

        # driver.get('https://www.taobao.com/?spm=a1z02.1.1581860521.1.elblhO')
        # 搜索框输入宝贝地址
        # id="q" name="q"
        search_content = driver.find_element_by_id('q')
        time.sleep(5)
        # 直 接 搜 索 电 饭 煲
        key = input('请输入爬取的的商品名称：')
        # key = '电饭煲'
        search_content.send_keys(key)
        # 搜索框按钮
        # class='submit icon-btn-search'
        search_btn = driver.find_element_by_class_name('btn-search.tb-bg')
        search_btn.click()
        time.sleep(5)

        for handle in driver.window_handles:  # 方法二，始终获得当前最后的窗口
            driver.switch_to.window(handle)
        time.sleep(5)
        print('获取第一页的数据')
        get_data()
        # 获取总页数
        total = driver.find_element_by_xpath('//*[@id="mainsrp-pager"]/div/div/div/div[1]').text
        total = re.sub(r',|，', '', total)
        print(total)
        totalnum = int(re.compile(r'(\d+)').search(total).group(1))
        return totalnum
    except TimeoutError as e:
        search()

    # return driver.current_url


# 淘宝网登陆界面
# https://login.taobao.com/member/login.jhtml?


def save():
    content = json.dumps(dict_lists, ensure_ascii=False, indent=2)
    # 把全局变量转化为json数据
    with open("taobao.json", "a+", encoding="utf-8") as f:
        f.write(content)
        print("json文件写入成功")

    with open('taobao.csv', 'w', encoding='utf-8', newline='') as f:
        # 表头
        title = dict_lists[0].keys()
        # 声明writer
        writer = csv.DictWriter(f, title)
        # 写入表头
        writer.writeheader()
        # 批量写入数据
        writer.writerows(dict_lists)
    print('csv文件写入完成')


dict_lists = []


# 执行操作步骤
def get_data():
    lists = driver.find_elements_by_xpath('//*[@id="mainsrp-itemlist"]/div/div/div[1]//div/div[2]')
    print('列表的大小为：', len(lists))
    for i in range(44):
        dict_list = {}
        price = driver.find_elements_by_xpath('.//div[@class="row row-1 g-clearfix"]/div/strong')[i].text
        amount = driver.find_elements_by_xpath('.//div[@class="row row-1 g-clearfix"]/div[@class="deal-cnt"]')[i].text
        # row row-2 title
        itemName = driver.find_elements_by_xpath('.//div[@class="row row-2 title"]/a')[i].text
        # row row-3 g-clearfix
        shop = driver.find_elements_by_xpath('.//div[@class="row row-3 g-clearfix"]/div[@class="shop"]/a/span[2]')[
            i].text
        location = driver.find_elements_by_xpath('.//div[@class="row row-3 g-clearfix"]/div[@class="location"]')[i].text
        # //*[@id="mainsrp-itemlist"]/div/div/div[1]/div[37]/div[2]/div[3]/div[1]/a/span[2]

        print('店名是：', shop)
        print('价格是：', price)
        print('销量是：', amount)
        print('地址是：', location)
        print('产品名称是：', itemName)
        dict_list['price'] = price
        dict_list['amount'] = amount
        dict_list['itemName'] = itemName
        dict_list['shop'] = shop
        dict_list['location'] = location
        dict_lists.append(dict_list)
        time.sleep(1)


# https://s.taobao.com/search?
# initiative_id=tbindexz_20170306&ie=utf8
# &spm=a21bo.2017.201856-taobao-item.2&sourceId=tb.index&search_type=item
# &ssid=s5-e&commend=all&imgfile=&q=%E7%94%B5%E9%A5%AD%E7%85%B2&suggest=history_1
# &_input_charset=utf-8&wq=&suggest_query=&source=suggest&bcoffset=3
# &ntoffset=3&p4ppushleft=1%2C48&s=44

# https://s.taobao.com/search?q=%E7%94%B5%E9%A5%AD%E7%85%B2&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&bcoffset=3&ntoffset=3&p4ppushleft=1%2C48&s=44


# 实现翻页功能
# 
def next_page():
    totalnum = search()  # 获取总页数的值，并且调用search获取第一页数据
    print('##################################')
    print(totalnum)
    num = 1  # 首先进来的是第1页，共100页，所以只需要翻页99次#初始为1，因为我第一页已经获取过数据了
    while num != 3:  # 这里我偷懒只爬取了3页
        # while num != totalnum - 1:    #首先进来的是第1页，共100页，所以只需要翻页99次
        print("第%s页:" % str(num + 1))
        driver.get('https://s.taobao.com/search?q=电饭煲&s={}'.format(44 * num))
        # 用修改s属性的方式翻页
        driver.implicitly_wait(10)
        # 等待10秒
        get_data()  # 获取数据
        time.sleep(3)
        num += 1  # 自增


# 爬取后台数据
def run():
    login()
    data_orders = get_orders(cookies)
    save_orders(data_orders)


# 主要内容      # 获取商品详情
def main_product():
    # url = 'https://login.taobao.com/member/login.jhtml?spm=a231o.13503973.1997563269.1.7f3768edKxXZmY&f=top'
    # login()
    next_page()
    save()


def save_orders(data_lists):
    content = json.dumps(data_lists, ensure_ascii=False, indent=2)
    # 把全局变量转化为json数据
    with open("taobao_order_new_new.json", "a+", encoding="utf-8") as f:
        f.write(content)
        print("json文件写入成功")

    with open('taobao_order_new_new.csv', 'w', encoding='utf-8', newline='') as f:
        # 表头
        title = data_lists[0].keys()
        # 声明writer
        writer = csv.DictWriter(f, title)
        # 写入表头
        writer.writeheader()
        # 批量写入数据
        writer.writerows(data_lists)
    print('csv文件写入完成')


def main_orders():
    select_orders()
    data_001 = get_orders(cookies)
    save_orders(data_001)


# 主程序入口
if __name__ == '__main__':
    # main()
    # select_orders()
    # data_001 = get_orders(cookies)
    # save_orders(data_001)

    choice = int(input('请选择：爬取商品信息请输入1：爬取订单请输入2：'))
    print(choice)
    if choice == 1:
        main_product()
    else:
        main_orders()
