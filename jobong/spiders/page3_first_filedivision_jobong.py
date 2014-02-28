import subprocess
import multiprocessing
import logging
from scrapy import cmdline
import time

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',)

# page3_first_filedivision_jobong.py page3_second_scrapy_jobong.py

num_fetch_threads = 100
enclosure_queue = multiprocessing.JoinableQueue()



def main3(i, q):
    for pth in iter(q.get, None):
        try:
            #cmdline.execute(['scrapy',  'runspider',  'page3_scrapy_myntra.py',  '-a',  'pth=%s' %(pth)])
            logging.debug(pth)
        except:
            f = open("again_use scrapy", "a+")
            print >>f, pth
            f.close()

        time.sleep(2)
        q.task_done()

    q.task_done()

            




def main2(output):
    procs = []

    for i in range(num_fetch_threads):
        procs.append(multiprocessing.Process(target=main3, args=(i, enclosure_queue,)))
        #worker.setDaemon(True)
        procs[-1].start()

    for pth in output:
        enclosure_queue.put(pth)

    print '*** Main thread waiting'
    enclosure_queue.join()
    print '*** Done'

    for p in procs:
        enclosure_queue.put(None)

    enclosure_queue.join()

    for p in procs:
        p.join()






def main():
    f = open("to_extract.txt")
    directory = f.read().strip()
    f.close()
 
    output = subprocess.check_output(["find",  directory,  "-name",  "*.docx"])
    output = output.strip().split("\n")
    
    length = len(output)
    
    val = length / 100

    mod = length % 100

    i = 0 
    for l in xrange(100, length, 100):
        l2 = l-100
	i = i+1
	p = multiprocessing.Process(name = i, target=main2, args=(output[l2: l],))
	p.start()
        logging.debug('Starting')
	p.join()

    p = multiprocessing.Process(name = "mod", target=main2, args=(output[mod: ], ))
    p.start()
    logging.debug('Starting')
    p.join()
         
    print "Finished everything...."
    print "num active children:", multiprocessing.active_children()

    
    

if __name__=="__main__":
    main()
