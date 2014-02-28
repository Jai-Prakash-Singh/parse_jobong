# -*- coding: latin-1 -*-
# -*- coding: iso-8859-15 -*-
# -*- coding: ascii -*-
# -*- coding: utf-8 -*-

from scrapy.spider import Spider
from scrapy.selector import Selector
from bs4 import BeautifulSoup
import time

#page3_scrapy_myntra.py , page3_filedivision_myntra.py 

class DmozSpider(Spider):
    name = "link_to_link"
    allowed_domains = ["jabong.com"]
 
    def __init__(self, pth = None):
       
        pthdoc = pth.strip()[:-1]
        
        pth2 = str(pth).strip().split("/")
         
        f = open(pthdoc)
	line = f.readline().strip()
	f.close()
        
	linelist = line.split(",")
	scat = linelist[2]
	scat = scat.split("(")
	scat = str(scat[0]).strip()
	self.subcat = scat

        self.catlink = linelist[-2]

	brand = str(pth2[-1]).strip()[:-5]
        brand = brand.split("(")
        brand = str(brand[0]).strip()
        self.brand = brand

        self.pth = pth        
        self.pth2 = pth2 = pth.strip().split("/")
        self.target = str(pth2[1]).strip()

	self.category = str(pth2[2]).strip()

        f = open(pth)
	avalurls = f.read().strip().split("\n")
        self.start_urls = map(str.strip, avalurls)
	f.close()
    

    def parse(self, response):
        #sel = Selector(response)
        #title = sel.xpath("/html/body/div/div[2]/section/div[2]/div/div/div[2]/div/div/h1/text()").extract()
        #title = 
        #try:
            link = response.url

            page = response.body 

	    soup = BeautifulSoup(page)
 
            title = soup.find("span", attrs={"id":"qa-title-product"})
            title = str(title.get_text()).strip()

            sp = soup.find("span", attrs={"itemprop":"price"})
            sp = "Rs. %s" %(str(sp.get_text()).strip())

            mrp = soup.find("span", attrs={"class":"striked-price fs14 c222 d-inline mt5"})

	    if mrp:
                mrp = str(mrp.get_text()).strip()

	    else:
	        mrp = sp 



            try:
                size = soup.find("ul", attrs={"id":"listProductSizes"})
                subsize = size.find_all("li")
            except:
                pass

            sizelist = []

	    for l in subsize:
	        sizelist.append(str(l.get_text()).strip())

	    size = str(sizelist)
            
            

            vender = seller  = soup.find("span", attrs={"id":"qa-prd-brand"})
            vender = str(vender.get_text()).strip()
 
            spec = soup.find("div", attrs={"id":"productInfo"})
            spec = str(spec).replace("\n", " ").replace("\t" ," ").replace("\r", " ").replace('"', "'")

            image = soup.find("li", attrs={"data-js-function":"setImage"})
            image = str(image.img.get("src")).strip()


	    sku = soup.find("td", attrs={"id":"qa-sku"}) 
            sku = str(sku.get_text()).strip()
      
	    target = self.target
	    category = self.category 
	    subcat  = self.subcat 
 	    brand   = self.brand 
            colour = "None"
            metatitle = "None"
            metadisc = "None"
            desc = "None"
            catlink = self.catlink      
   
            date = str(time.strftime("%d:%m:%Y"))
            status = "None"

            directory = '/'.join(self.pth2[:-1])

            filename = "%s/%s%s" %(directory , self.pth2[-1][:-5],  ".csv")
            f = open(filename, "a+")
	    print>>f,  ','.join([sku, title, catlink, sp, category, subcat, brand, image, mrp, 
	                colour, target, link, vender, metatitle, metadisc, size,
		        desc, spec, date, status])
            f.close()

            print[link, "ok"]


       # except:
       #    pass

        
