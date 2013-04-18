import string,threading,time

def thread_main(a):
    global count,mutex
    threadname = threading.currentThread().getName()

    for x in range(0,int(a)):
        mutex.acquire()
        count= count +1
        mutex.release()
        print threadname,x,count
        time.sleep(1)

def addcount():
    global count
    while count<10:
        count=count+1
        time.sleep(1)

def printcount():
    global count
    while count<10:
        print count
        time.sleep(2)

def test():
    global count
    count = 1
    add_thread = threading.Thread(target=addcount)
    print_thread = threading.Thread(target=printcount)

    add_thread.start()
    print_thread.start()


def main(num):
    global count,mutex
    threads = []
    count =1
    mutex = threading.Lock()
    for x in xrange(0,num):
        threads.append(threading.Thread(target=thread_main,args=(10,)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    while count<1000:
        print "current count =%s" % count

if __name__ =="__main__":
    #num =4 
    #main(4)
    test()
