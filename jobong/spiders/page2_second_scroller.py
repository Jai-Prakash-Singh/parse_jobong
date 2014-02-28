from urlparse import urlparse
import os 
import phan_proxy
from bs4 import BeautifulSoup
import sys
import logging 
import time

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)


def main2(bl):
    driver = phan_proxy.main(bl)

    page = driver.page_source
    #print page
    #print driver.current_url

    try:
        time.sleep(2)
        driver.find_element_by_id("jab-news").click()
        logging.debug("jab-news....")

    except:
        pass

    try:
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        logging.debug("scrolling... first")
        return driver

    except:
        logging.debug("repeating...")
        driver.delete_all_cookies()
        driver.quit()
        main2(bl)
        


def main(line):
    f = open("to_extract.txt")
    directory = f.read().strip()
    f.close()

    line = line.strip()
    
    line2 = line.split(",")

    ctlink = str(line2[1]).strip()

    cate  = str(line2[2]).strip()
    cate = cate.split("(")
    cate = cate[0].strip()

    brand = str(line2[-1]).strip()
    brand = brand.split("(")
    brand = brand[0].strip()

    #bl = str(line2[-2]).strip()
    bl = "http://www.jabong.com/men/shoes/casual-shoes/bacca-bucci/"

    parsed = urlparse(ctlink)
    fpth = parsed.path.replace("/new-products/", "")
    fpth = filter(None, fpth.split("/"))
    fpth = '/'.join(fpth)

    directory2 = "%s/%s/%s" %(directory, fpth, cate)

    try:
        os.makedirs(directory2)

    except:
        pass

    filename = "%s/%s.doc" % (directory2, brand)
    filename2 = "%s/%s.docx" % (directory2, brand)

    driver = main2(bl)
    
    height = 0
    loop = True

    while loop is True:
         logging.debug("scrolling...")
         time.sleep(1)
         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
         time.sleep(1)
         heightnow = driver.execute_script("return $(document ).height();")

	 if heightnow == height:
	     loop = False

	 else:
	     height = heightnow
	     loop = True
   
    page = driver.page_source
    
    soup = BeautifulSoup(page)

    tag_ul_product = soup.find("ul", attrs={"id":"productsCatalog"})

    if tag_ul_product:
        tag_a = tag_ul_product.find_all("a")

    else:
        tag_a = []


    f = open(filename, "a+")
    f2 = open(filename2, "a+")

    for al in tag_a:
        try:
	    parsed = urlparse(str(al.get("href")))
	    if parsed.netloc == "www.jabong.com":
	        print >>f, line, str(al.get("href")).strip()
		print >>f2, str(al.get("href")).strip()
	except:
	    pass


    f.close()
    f2.close()

    driver.delete_all_cookies()
    driver.quit()
    



if __name__=="__main__":
    line = "http://www.jabong.com/kids/clothing/girls-clothing/new-products/?source=topnav,http://www.jabong.com/kids/clothing/girls-clothing/girls-twin-sets/new-products/,Twin Sets (55),http://www.jabong.com/kids/clothing/girls-clothing/girls-twin-sets/n-xt-girls/new-products/,N-XT Girls(4)"
    main(line)




