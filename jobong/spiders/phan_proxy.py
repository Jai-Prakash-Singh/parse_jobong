import logging
from selenium import webdriver
import logging
from  random  import choice
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities




logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )


def main(link):
    f2 = open("/home/desktop/proxy5")
    proxy_list = f2.read().strip().split("\n")
    f2.close()

    loop = True

    while loop is True:
        try:
            ip_port = choice(proxy_list).strip()

            logging.debug(ip_port)

            #user_pass = ip_port.split("@")[0].strip()
            user_pass = "vinku:india123"

            #prox = "--proxy=%s" % (ip_port.split("@")[1].strip())
            prox = "--proxy=%s" % (ip_port)

            service_args = [prox, '--proxy-auth='+user_pass, '--proxy-type=http', '--load-images=no']

            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:23.0) Gecko/20100101 Firefox/23.0")
            dcap["--disable-popup-blocking"] = "no"

            driver = webdriver.PhantomJS(service_args = service_args, desired_capabilities=dcap)
            driver.refresh()
            driver.get(link)
            
            if str(driver.current_url).strip() == "about:blank":
                loop = True

            else:
                loop = False

        except:
            pass

    return driver




if __name__=="__main__":
    link = "http://www.jabong.com/"
    main(link)
