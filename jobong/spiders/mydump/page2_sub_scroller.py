from selenium import webdriver
import logging
from  random  import choice
import time
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
from lxml import html
import os

logging.basicConfig(level=logging.DEBUG, format = '[%(levelname)s] (%(threadName)-10s) %(message)s')

# page2_scroller_myntra.py, page2_sub_scroller.py




def main3(driver):
    loop = True
    height = 0
    
    while loop  is True:
        driver.execute_script("window.scrollBy(0,-350)", "")
	logging.debug(("clicking ...", driver.current_url))
          
        try:
            driver.find_element_by_class_name("close").click()

        except: 
            driver.find_element_by_xpath("/html/body/div/div[2]/section/div[3]/div[2]/div/div[6]/a").click()
            logging.debug(("clicking ...", driver.current_url))
            time.sleep(1) 

	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	heightnow  = driver.execute_script("return $(document ).height();")

        logging.debug(heightnow)    
   
        if heightnow == height:
	    loop = False

	else:
	    height = heightnow




def main2(driver):
    height  = 0
    loop = True
    
    while loop is True:
        logging.debug("scrolling....")
        
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        heightnow  = driver.execute_script("return $(document ).height();")
        logging.debug(("height now: ", heightnow))
 
	if heightnow == height:
            try:
	        main3(driver)

            except:
	        pass
 
            loop = False

	else:
	    height = heightnow
	    



def maindriver(ip_port, bl):
    #user_pass = ip_port.split("@")[0].strip()
    user_pass = "vinku:india123"

    #prox = "--proxy=%s" % (ip_port.split("@")[1].strip())
    prox = "--proxy=%s" % (ip_port)

    service_args = [prox, '--proxy-auth='+user_pass, '--proxy-type=http', '--load-images=no']

    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:23.0) Gecko/20100101 Firefox/23.0")
    dcap["--disable-popup-blocking"] = "yes"

    driver = webdriver.PhantomJS(service_args = service_args, desired_capabilities=dcap)
    driver.refresh()
    driver.get(bl)

    if str(driver.current_url).strip() == "about:blank":
        return driver, None

    else:
        return  driver, "ok"


    

def main(mline):
    mline = mline.strip().encode("ascii", "ignore")
    line = mline.split(",")
    bl = line[-2].strip()
    
    f2 = open("/home/desktop/proxy5")
    proxy_list = f2.read().strip().split("\n")
    f2.close()

    loop = True

    while loop is True:
        try:
            ip_port = choice(proxy_list).strip()
            driver, status = maindriver(ip_port, bl)

            if status:
                loop = False

            else:
                driver.delete_all_cookies()
                driver.close()
        except:
            loop = True
              
    loop = True
    
    while loop is True:
        try:
            main2(driver)
  
            page = driver.page_source    

            soup = BeautifulSoup(page)

            tag_mk = soup.find_all("div", attrs={"id" : "mk-search-results"})  
            tag_a = tag_mk[0].find_all("a", attrs={"class":"clearfix"})
            
            if tag_a :
                loop = False

        except:
            pass 

        ip_port = choice(proxy_list).strip()
        driver.delete_all_cookies()
        driver.close()
        driver, status = maindriver(ip_port, bl)

        
    target = line[1].split("-")[0][1:].strip()
    category = line[1][1:].strip()
    subcategory = line[2].strip()
    brand = line[-1].split("[")[0].strip()

    f = open("to_extract.txt")
    topdir = f.read().strip()
    f.close()

    try:
        directory = "%s/%s/%s/%s/%s" %(topdir, target, category,  subcategory, brand)
        os.makedirs(directory)

    except:
        pass

    csvfilename = directory + "/" + brand + ".doc"
    linkfile = directory + "/" + brand + ".docx"

    f = open(csvfilename, "a+")
    f2 = open(linkfile, "a+")

    if not tag_a:
        f = open("linknotscrolled.txt", "a+")
        print >>f, str(mline)
        f.close()


    for l in tag_a:
        finallink =  "http://www.myntra.com%s" %(l.get("href").strip().encode("ascii", "ignore"))
        print >>f, ','.join([mline, finallink])
        print >>f2, finallink
        print mline, finallink
        print finallink

    f.close()
    f2.close()

    driver.delete_all_cookies()
    driver.close()    




if __name__=="__main__":
    line = "http://www.myntra.com/sale-women-accessories?nav_id=633&src=tn,/sale-women-accessories,Accessories,http://www.myntra.com/yelloe?src=lnb,yelloe [9]"
 
    #line = "http://www.myntra.com/sale-women-accessories?nav_id=633&src=tn,/sale-women-accessories,Accessories,http://www.myntra.com/men-casual-shirts?nav_id=7&src=tn,yelloe [9]"    
    main(line)
