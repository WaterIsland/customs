# -*- conding: utf-8 -*-
# Created on 2025/05/01
import time
import multiprocessing as mltprcs

from customs import cstmlogging as clog
from customs import cstmthread  as cthrd
from customs import cstmprocess as cprcs # need psutil
from customs import cstmdb      as ctdb  # need pandas, pyodbc, sqlalchemy, urllib

'''
def dummy():
    pass

log_obj = clog.CustomLogging(file_name='log/test.log')

log_obj.log('INFO', 'TEST!!!!!')

#    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, deamon=True, logger=None):
#    def __init__(self, database: str='', script_name: str='', conn_type='connection', logger=None):
th_obj = cthrd.RaisableThread(target=dummy, name='dummy', args=(), logger=log_obj)
db_obj = ctdb.CustomDB(logger=log_obj)
'''


import sys


def f1(func_name: str='f1', log_queue: mltprcs.Queue=None):
    logger = clog.CustomLoggingForProcess.create_logger_for_multiprocess(log_queue)
    try:
        if (logger is None):
            raise Exception('No logger instance.')

    except Exception as e:
        return -1
    
    show_str = 'Start {} as {}'.format(sys._getframe().f_code.co_name, func_name)
    logger.info(show_str)
    print(show_str)
    for i in range(10):
        show_str = 'Process {} => {}:::{}'.format(sys._getframe().f_code.co_name, func_name, i)
        logger.info(show_str)
        print(show_str)
        time.sleep(1)
    show_str = 'End '+ sys._getframe().f_code.co_name
    logger.info(show_str)
    print(show_str)


def f2(func_name: str='f2', cnt: int = 1, log_queue: mltprcs.Queue=None):
    logger = clog.CustomLoggingForProcess.create_logger_for_multiprocess(log_queue)
    try:
        if (logger is None):
            raise Exception('No logger instance.')

    except Exception as e:
        return -1
    
    show_str = 'Start {} as {}'.format(sys._getframe().f_code.co_name, func_name)
    logger.info(show_str)
    print(func_name, show_str)
    for i in range(cnt):
        show_str = 'Process {} => {}:::{}'.format(sys._getframe().f_code.co_name, func_name, i)
        logger.info(show_str)
        print(show_str)
        time.sleep(1)
    show_str = 'End '+ sys._getframe().f_code.co_name
    logger.info(show_str)
    print(func_name, show_str)


def main():
    import random

    logger_root = clog.CustomLogging(file_name='log\\test_root.log')
    logger_leaf = clog.CustomLoggingForProcess(file_name='log\\test_leaf.log')
    manager_obj = cprcs.MultiProcessManager(accuracy=1, cpu_rate=0.5, logger=logger_root)

    logger_root.info('Start multiprocess _/_/_/_/_/_/_/_/_/_/')
    # Create worker processes
    logger_root.info('Created worker processes ----------')
    workers = []
    for idx in range(4):
        name = 'f1'+str(idx)
        pr_obj = cprcs.StoppableProcess(target=f1, name=name, timeout=10, priority=random.randint(0, 100), args=(name, logger_leaf.get_queue()))
         # workers format: [instance_name as string, instance as object, priority as int]
        workers.append([name, pr_obj, pr_obj.get_priority()])

    for idx in range(4):
        name = 'f2'+str(idx)
        pr_obj = cprcs.StoppableProcess(target=f2, name=name, timeout=10, priority=random.randint(0, 100), args=(name, 3, logger_leaf.get_queue()))
        # workers format: [instance_name as string, instance as object, priority as int]
        workers.append([name, pr_obj, pr_obj.get_priority()])
    manager_obj.set_workers(workers)

    logger_root.info('Sorted worker processes queue ----------')
    for item in manager_obj.get_workers(): 
        logger_root.info('[Name, Process Instance, Priority] = {}'.format(item))

    # Create inpector process
    logger_root.info('Created inspector processes ----------')
    inspector_obj = cprcs.StoppableProcess(target=cprcs.MultiProcessManager.run, name='MultiProcessManager.run', timeout=5)
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
else:
    print(__name__)
