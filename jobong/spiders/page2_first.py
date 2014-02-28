import multiprocessing
import time
import logging
import page2_second_scroller

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)


num_fetch_threads = 100
#enclosure_queue = multiprocessing.Queue()
enclosure_queue = multiprocessing.JoinableQueue()


def main2(i, q):
    for line in iter(q.get, None):
        #print line
        try:
            page2_second_scroller.main(line)

        except:
           f = open("again_scroll.txt", "a+")
           print >>f, line
           f.close()

	time.sleep(2)
	q.task_done()

    q.task_done()


def main():
    f = open("to_extract.txt")
    directory = f.read().strip()
    f.close()

    filename = "%s/%s" %(directory, "brandstoextract.txt")
    
    f = open(filename)

    procs = []

    for i in range(num_fetch_threads):
        procs.append(multiprocessing.Process(target=main2, args=(i, enclosure_queue,)))
        #worker.setDaemon(True)
        procs[-1].start()

    for line in f:
        enclosure_queue.put(line)

    print '*** Main thread waiting'
    enclosure_queue.join()
    print '*** Done'

    for p in procs:
        enclosure_queue.put(None)

    enclosure_queue.join()
    
    for p in procs:
	p.join()

    f.close()



if __name__=="__main__":
    main()
   
    
    
    
