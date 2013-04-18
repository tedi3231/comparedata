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

if __name__ =="__main__":
    num =4 
    main(4)
