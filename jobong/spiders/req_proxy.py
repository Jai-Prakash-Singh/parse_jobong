import requests
from random import choice
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
		                        )


def main(link):
    #f = open("/home/desktop/mygoodproxy333.txt")
    f = open("/home/desktop/proxy5")
    pass_ip_list = f.read().strip().split("\n")    
    f.close()

    loop = True

    while loop is True:
        pass_ip = choice(pass_ip_list)
        pass_ip = pass_ip.strip()
        pass_ip = "vinku:india123@%s" %(pass_ip.strip())

 	try: 
            http_proxy = "http://" + pass_ip
            proxyDict = {"http"  :http_proxy}
            r = requests.get(link,  proxies=proxyDict)
            if r.status_code == requests.codes.ok:
                page = r.content
	        logging.debug(r.status_code)
	        loop = False

	except:
	    loop = True

    
    r.cookies.clear()
    r.close()
    return page



if __name__=="__main__":
    link = "http://docs.python-requests.org/en/latest/user/quickstart/#response-content"
    page = main(link)
    #print page
    
        
    

