#!/usr/bin/env python 

import logging
import phan_proxy
from bs4 import BeautifulSoup
import HTMLParser
import req_proxy
from bs4 import BeautifulSoup
from Queue import Queue
import threading
import time
from threading import Thread
import time
import os 
import sys
from urlparse import urlparse


num_fetch_threads = 20
enclosure_queue = Queue()

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

link_cl_ctxt_ccount = []




def main5(i, q):
    for line, f in iter(q.get, None):
    
        link = line[-2].strip()

        page = req_proxy.main(link)
        soup = BeautifulSoup(page)

        tag_brand  =  soup.find("div", attrs={"id":"facet_brand"})
        
        try:
            tag_a =  tag_brand.find_all("a")

        except:
            tag_a = []
        
        for l in  tag_a:
            try:
                brandlink = str(l.get("href")).strip()
                bramdname = str(l.get_text()).strip()
                print >>f,  "%s,%s,%s" %(','.join(line), brandlink, bramdname)

            except:
                pass

        time.sleep(i + 2)
        q.task_done()

    q.task_done()




def main4(link_cl_ctxt_ccount):
    procs = []

    f =  open("to_extract.txt")
    directory = f.read().strip()
    f.close()

    filename = "%s/%s" %(directory, "brandstoextract.txt")
    f = open(filename, "a+")
    

    for i in range(num_fetch_threads):
        procs.append(Thread(target=main5, args=(i, enclosure_queue,)))
        #worker.setDaemon(True)
        procs[-1].start()
    
    for line in link_cl_ctxt_ccount:
        enclosure_queue.put((line, f))

    print '*** Main thread waiting'
    enclosure_queue.join()
    print '*** Done'

    for p in procs:
        enclosure_queue.put(None)

    enclosure_queue.join()
    
    for p in procs:
        p.join()

    f.close()

 
def main3(i, q):
    for link in iter(q.get, None):
        page = req_proxy.main(link)
        soup = BeautifulSoup(page)

        tag_cat = soup.find_all("div", attrs={"class":"search-by-cat mt10 mb10 pl14 "})
    
        if tag_cat:
            cat_tag_a = tag_cat[0].find_all("a")

        else:
            cat_tag_a = []

        for cl in cat_tag_a:
            try:
                link_cl_ctxt_ccount.append([link, str(cl.get("href")).strip(), str(cl.get_text()).strip()])
                logging.debug((link, str(cl.get("href")).strip(), str(cl.get_text()).strip()))

            except:
                pass

        time.sleep(i + 2)
        q.task_done()

    q.task_done()




def main2(menu_links):
    procs = []

    for i in range(num_fetch_threads):
        procs.append(Thread(target=main3, args=(i, enclosure_queue,)))
        #worker.setDaemon(True)
        procs[-1].start()

    for link in menu_links:
        link.strip()
        enclosure_queue.put(link)
    
    print '*** Main thread waiting'
    enclosure_queue.join()
    print '*** Done'
    
    for p in procs:
        enclosure_queue.put(None)

    enclosure_queue.join()

    for p in procs:
        p.join()

    
    
     
def main():

    directory = "dir%s" %(time.strftime("%d%m%Y"))
    
    f = open("to_extract.txt", "w+")
    print >>f, directory
    f.close()

    f = open("extracted.txt", "a+")
    print >>f, directory
    f.close()

    try:
        os.makedirs(directory)

    except:
        pass


    link = "http://www.jabong.com"
    driver = phan_proxy.main(link)

    try:
        driver.find_element_by_id("jab-news").click()

    except:
        pass

    page = driver.page_source
    driver.close()
    soup = BeautifulSoup(page)

    tag_li = soup.find("li", attrs={"id":"qa-navigation0"})
    h = HTMLParser.HTMLParser()
    tag_li = h.unescape(str(tag_li))

    tag_li = tag_li.replace("\n", " ").replace("<!--",  " ").replace("-->", " ")

    soup = BeautifulSoup(tag_li)
    tag_a = soup.find_all("a")

    menu_links = []   
    
    for l in tag_a:
        try:
	    menulink = l.get("href")
            menu_links.append(menulink)
    
        except:
	    pass

    main2(menu_links)




if __name__=="__main__":
    main()
    #link_cl_ctxt_ccount = [['http://www.jabong.com/sports/sports-shoes/new-products/?source=topnav', 'http://www.jabong.com/men/clothing/mens-shirts/alessio69/', 'Football Shoes (1)']]
    main4(link_cl_ctxt_ccount)





