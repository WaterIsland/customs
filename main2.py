# -*- conding: utf-8 -*-
# Created on 2025/05/01
import time
import multiprocessing as mltprcs

from customs import cstmlogging  as clog
from customs import cstmthread   as cthrd
from customs import cstmprocess  as cprcs # need psutil
from customs import cstmdb       as cdb   # need pandas, pyodbc, sqlalchemy, urllib
from customs import cstmfunction as ctfnc
import customs


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


def f0(logger=None):
    logger.info('hogehoge')


#def f1(logger=None, func_name: str='f1'):
def f1(*args):
    logger    = args[0][0]
    func_name = args[0][1]
    logger.info('f1: logger: {}, func_name: {}'.format(logger, func_name))

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

    f0(logger)


#def f2(logger=None, func_name: str='f2', cnt: int = 1):
def f2(*args):
    logger    = args[0][0]
    func_name = args[0][1]
    cnt       = args[0][2]
    logger.info('f2: logger: {}, func_name: {}, cnt: {}'.format(logger, func_name, cnt))

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

    f0(logger)


def main():
    import random

    logger_root = clog.CustomLogging(file_name='log\\test_root.log')
    logger_leaf = clog.CustomLoggingForProcess(file_name='log\\test_leaf.log')
    manager_obj = cprcs.MultiProcessManager(accuracy=1, cpu_rate=0.5, logger=logger_root)

    process_pool = {
          'f10': {'function': ctfnc.call_multiprocess_wrapper, 'args': (f1, logger_leaf.get_queue(), 'f10'), 'timeout': 10, 'priority': random.randint(0, 100)}
        , 'f11': {'function': ctfnc.call_multiprocess_wrapper, 'args': (f1, logger_leaf.get_queue(), 'f11'), 'timeout': 10, 'priority': random.randint(0, 100)}
        , 'f12': {'function': ctfnc.call_multiprocess_wrapper, 'args': (f1, logger_leaf.get_queue(), 'f12'), 'timeout': 10, 'priority': random.randint(0, 100)}
        , 'f13': {'function': ctfnc.call_multiprocess_wrapper, 'args': (f1, logger_leaf.get_queue(), 'f13'), 'timeout': 10, 'priority': random.randint(0, 100)}
        , 'f20': {'function': ctfnc.call_multiprocess_wrapper, 'args': (f2, logger_leaf.get_queue(), 'f20', 3), 'timeout': 10, 'priority': random.randint(0, 100)}
        , 'f21': {'function': ctfnc.call_multiprocess_wrapper, 'args': (f2, logger_leaf.get_queue(), 'f21', 3), 'timeout': 10, 'priority': random.randint(0, 100)}
        , 'f22': {'function': ctfnc.call_multiprocess_wrapper, 'args': (f2, logger_leaf.get_queue(), 'f22', 3), 'timeout': 10, 'priority': random.randint(0, 100)}
        , 'f23': {'function': ctfnc.call_multiprocess_wrapper, 'args': (f2, logger_leaf.get_queue(), 'f23', 3), 'timeout': 10, 'priority': random.randint(0, 100)}
    }

    logger_root.info('Start multiprocess _/_/_/_/_/_/_/_/_/_/')
    # Create worker processes
    logger_root.info('Created worker processes ----------')
    workers = []
    for r_key, r_val in process_pool.items():
        pr_obj = cprcs.StoppableProcess(
              target   = r_val['function']
            , name     = r_key
            , timeout  = r_val['timeout']
            , priority = r_val['priority']
            , args     = r_val['args']
        )
        workers.append([r_key, pr_obj, r_val['priority']])
    manager_obj.set_workers(workers)

    logger_root.info('Sorted worker processes queue ----------')
    for item in manager_obj.get_workers(): 
        logger_root.info('[Name, Process Instance, Priority] = {}'.format(item))

    # Create inpector process
    logger_root.info('Created inspector processes ----------')
    inspector_obj = cprcs.StoppableProcess(target=cprcs.MultiProcessManager.run, name='MultiProcessManager.run', timeout=5)
#    inspector_obj = cprcs.StoppableProcess(target=cprcs.MultiProcessManager.run, name='MultiProcessManager.run', timeout=20)
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

