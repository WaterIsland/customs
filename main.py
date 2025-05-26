# -*- conding: utf-8 -*-
# Created on 2025/05/01
import time
import multiprocessing as mltprcs

from customs import cstmlogging  as clog
from customs import cstmthread   as cthrd
from customs import cstmprocess  as cprcs # need psutil
from customs import cstmdb       as cdb   # need pandas, pyodbc, sqlalchemy, urllib
from customs import cstmfunction as cfnc


def main():
    logger_root = clog.CustomLogging(file_name='log\\test_root.log')
    logger_leaf = clog.CustomLoggingForProcess(file_name='log\\test_leaf.log')
    manager_obj = cprcs.MultiProcessManager(accuracy=1, cpu_rate=0.5, logger=logger_root)

    cfnc.set_workers(manager_obj, logger_root, logger_leaf)

    # Create inpector process
    logger_root.info('Created inspector processes ----------')
#    inspector_obj = cprcs.StoppableProcess(target=cprcs.MultiProcessManager.run, name='MultiProcessManager.run', timeout=1)
#    inspector_obj = cprcs.StoppableProcess(target=cprcs.MultiProcessManager.run, name='MultiProcessManager.run', timeout=5)
#    inspector_obj = cprcs.StoppableProcess(target=cprcs.MultiProcessManager.run, name='MultiProcessManager.run', timeout=10)
    inspector_obj = cprcs.StoppableProcess(target=cprcs.MultiProcessManager.run, name='MultiProcessManager.run', timeout=20)
    manager_obj.set_inspector(inspector_obj)
    logger_root.info('Launch multiprocess ----------')

    logger_leaf.start_logging()
    try:
        manager_obj.run()
    
    except Exception as e:
        logger_root.error(e)

    finally:
        logger_leaf.stop_logging()
    logger_root.info('End multiprocess _/_/_/_/_/_/_/_/_/_/')


if __name__ == '__main__':
    main()





'''
import threading

sum = 0
def increment():
    global sum
    for _i in range(100000):
        sum += 1

def main():
    threads = []
    for _i in range(10):
        threads.append(threading.Thread(target=increment))
    for i in range(10):
        threads[i].start()
    for i in range(10):
        threads[i].join()

    print(sum)

if __name__ == '__main__':
    main()
'''
    