# coding=utf-8
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from threading import Thread
from Queue import Queue

_BE_PROXY_QUEUE = Queue()
path = 'mt_proxy.txt'


class Consumer_Thread(Thread):
    def run(self):
        global _BE_PROXY_QUEUE
        while not _BE_PROXY_QUEUE.empty():
            p = _BE_PROXY_QUEUE.get()
            try:
                if test_useful(p):
                    with open(path, 'a') as f:
                        f.write(p + '\n')
            except Exception, e:
                print '[HERE]', e
                pass
            finally:
                _BE_PROXY_QUEUE.task_done()


def test_useful(proxy):
    print '[INFO] Testing proxy ', proxy, ' now...'
    try:
        proxies = {'http': proxy}
        requests.get('http://ip.cip.cc', timeout=20, proxies=proxies)
        print '[Congra] Successfully get one'
        return True
    except Exception, e:
        print e
        return False


def get_proxies_from_KDL(max_page):
    print '[Scrapy] Start Scrapying Proxies in KDL'

    base_url = 'http://www.kuaidaili.com/free/'
    options = ['intr/', 'inha/']

    p_pool = []

    print '===============\n', 'Scraping XICI DAILI' '\n===============\n'
    xici_page = 1

    while xici_page <= 3:
        #   xicidaili
        new_count = 0
        print 'PAGE', str(xici_page)
        xici_url = 'http://www.xicidaili.com/nt/' + str(xici_page)
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'}
        try:
            rx = requests.get(xici_url, timeout=15, headers=headers)
            bobj_2 = BeautifulSoup(rx.content.decode('utf-8'))
            sibs = bobj_2.findAll('table', {'id': 'ip_list'})[0].tr.next_siblings
        except Exception, e:
            try:
                print 'error 1:', e
                rx = requests.get(xici_url, timeout=15, headers=headers)
                bobj_2 = BeautifulSoup(rx.content.decode('utf-8'))
                sibs = bobj_2.findAll('table', {'id': 'ip_list'})[0].tr.next_siblings

            except Exception, e:
                print 'error 2', e
                break

        for sib in sibs:
            try:
                get_proxy = sib.findAll('td')[2].get_text() + ':' + sib.findAll('td')[3].get_text()
                p_pool.append(get_proxy)
                new_count += 1
            except AttributeError:
                pass
        print 'get ', new_count, ' proxies in page', xici_page
        xici_page += 1
    # 第几个分页面
    opt = 0
    while opt <= 1:
        page = 1
        print '===============\n', 'Scraping ', options[opt], '\n===============\n'
        while page < max_page:
            url = base_url + options[opt] + str(page) + '/'
            driver = webdriver.PhantomJS(
                executable_path=r"/root/csdn_spider/phantomjs-2.1.1-linux-x86_64/bin/phantomjs")
            #driver = webdriver.PhantomJS(executable_path=r'D:\phantomjs-2.1.1-windows\bin\phantomjs.exe')
            driver.get(url)
            print 'Sleep 0.7 sec...'
            time.sleep(0.7)
            bobj = BeautifulSoup(driver.page_source)
            driver.close()
            siblings = bobj.findAll(name='table', attrs={'class': 'table table-bordered table-striped'})[
                0].tbody.tr.next_siblings
            count = 0
            for sibling in siblings:
                try:
                    get_proxy = sibling.findAll(name='td')[0].get_text() + ':' + sibling.findAll(name='td')[
                        1].get_text()
                    p_pool.append(get_proxy)
                    count += 1
                except AttributeError:
                    pass
            print 'Get', str(count), 'proxy'
            page += 1
        opt += 1



    print '*****************************'
    print 'Finished! Get ', len(p_pool), ' useful proxies in total'
    return p_pool
    # with open('proxy_kdl.txt', 'w') as f:
    #    for p in p_pool:
    #        p = p + '\n'
    #        f.write(p)
    # print 'Successfully written in \'proxy_kdl.txt\''


def get_proxies_from_file():
    with open('proxy_kdl.txt', 'r') as f:
        return f.readlines()


def test_proxies_efficience(proxy):
    proxies = {'http': proxy}
    start = time.time()
    for i in range(3):
        r = requests.get('http://www.baidu.com', proxies=proxies)
        print i, '  ', r.text
    cost = time.time() - start
    print 'With Proxy: cost ', cost / 3, ' seconds'

    start = time.time()
    for i in range(3):
        r = requests.get('http://ip.cip.cc')
        print i, '  ', r.text
    cost = time.time() - start
    print 'Without Proxy: cost ', cost / 3, ' seconds'


def main():
    # 清空已有的文件
    with open(path, 'w') as f:
        f.write(time.ctime() + '\n')
        f.write('========================\n')
    global _BE_PROXY_QUEUE
    max_thread = 100
    threads = []
    # 2大页面，每个大页面3个分页
    pool = get_proxies_from_KDL(3)
    print 'uher2'
    for i in range(len(pool)):
        _BE_PROXY_QUEUE.put(pool[i])
    for i in range(max_thread):
        threads.append(Consumer_Thread())
    for i in range(max_thread):
        threads[i].start()
    # 陷入等待 线程不够 是因为线程没有死循环就退出
    _BE_PROXY_QUEUE.join()

    print '###########################################'
    print 'SUCCESS!'
    print '###########################################'


if __name__ == '__main__':
    main()
