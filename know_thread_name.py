
import queue
from threading import Thread,current_thread
import warnings
warnings.filterwarnings("ignore")

logging.basicConfig(filename='logfile.log',level=logging.INFO,format='%(asctime)s %(threadName)s %(message)s ')

def do_work(item):
    try:
        print (current_thread().getName())

    except Exception as details:
        print (details)
        pass
    print (item)
    
 

def worker():
      while True:            
        item=q.get()
        do_work(item)
        q.task_done()
        
q=queue.Queue()
l=[13,26,77,99,101,4003]
for item in l:
      q.put(item)
 
 
for i in range (20):
    
    t=Thread(target=worker,name="child"+str(i))
    t.daemon=True
    t.start()
 
    
q.join()
