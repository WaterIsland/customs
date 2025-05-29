# -*- coding: utf-8 -*-
# Created on 2025/05/01
import sys
import random
import time
import logging
import inspect
import multiprocessing as mltprcs

from customs import cstmlogging as clog
from customs import cstmprocess as cprcs # need psutil


PROCESS_LOG_PATH = 'log\\test_leaf_process.log'


def create_logger_for_multiprocess(log_queue: mltprcs.Queue=None):
    logger = logging.getLogger(__file__+inspect.currentframe().f_code.co_name)
    handler = logging.handlers.QueueHandler(log_queue)
    if (handler not in logger.handlers):
        logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


#def f1(logger=None, func_name: str='f1'):
def f1(*args):
    func_name = args[0]

    try:
        logger = clog.CustomLogging(file_name=PROCESS_LOG_PATH)

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

    except Exception as e:
        logger.error(e)

    finally:
        pass


#def f2(logger=None, func_name: str='f2', cnt: int = 1):
def f2(*args):
    func_name = args[0]
    cnt       = args[1]

    try:
        logger = clog.CustomLogging(file_name=PROCESS_LOG_PATH)

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

    except Exception as e:
        logger.error(e)

    finally:
        pass


def run_dispatcher(*args):
    func_name  = args[0]
    shrd_queue = args[1]

    try:
        logger = clog.CustomLogging(file_name=PROCESS_LOG_PATH)

        logger.info('run_dispatcher: logger: {}, func_name: {}'.format(logger, func_name))

        for i in range(8):
            time.sleep(1)

            process_pool = {
                #  0: {'key': 'f10', 'function': f1, 'args': ('f10', ), 'timeout': 10, 'priority': 8}
                #, 1: {'key': 'f11', 'function': f1, 'args': ('f11', ), 'timeout': 10, 'priority': 9}
                #, 2: {'key': 'f12', 'function': f1, 'args': ('f12', ), 'timeout': 10, 'priority': 10}
                #, 3: {'key': 'f13', 'function': f1, 'args': ('f13', ), 'timeout': 10, 'priority': 11}
                #, 4: {'key': 'f20', 'function': f2, 'args': ('f20', 5), 'timeout': 10, 'priority': 12}
                #, 5: {'key': 'f21', 'function': f2, 'args': ('f21', 5), 'timeout': 10, 'priority': 13}
                #, 6: {'key': 'f22', 'function': f2, 'args': ('f22', 5), 'timeout': 10, 'priority': 14}
                #, 7: {'key': 'f23', 'function': f2, 'args': ('f23', 5), 'timeout': 10, 'priority': 15}
                  0: {'key': 'f10', 'function': f1, 'args': ('f10', ), 'timeout': 10, 'priority': random.randint(0, 100)}
                , 1: {'key': 'f11', 'function': f1, 'args': ('f11', ), 'timeout': 10, 'priority': random.randint(0, 100)}
                , 2: {'key': 'f12', 'function': f1, 'args': ('f12', ), 'timeout': 10, 'priority': random.randint(0, 100)}
                , 3: {'key': 'f13', 'function': f1, 'args': ('f13', ), 'timeout': 10, 'priority': random.randint(0, 100)}
                , 4: {'key': 'f20', 'function': f2, 'args': ('f20', 5), 'timeout': 10, 'priority': random.randint(0, 100)}
                , 5: {'key': 'f21', 'function': f2, 'args': ('f21', 5), 'timeout': 10, 'priority': random.randint(0, 100)}
                , 6: {'key': 'f22', 'function': f2, 'args': ('f22', 5), 'timeout': 10, 'priority': random.randint(0, 100)}
                , 7: {'key': 'f23', 'function': f2, 'args': ('f23', 5), 'timeout': 10, 'priority': random.randint(0, 100)}
            }

            print('Add new process... ==> {}'.format(process_pool[i]))
            logger.info('Add new process... ==> {}'.format(process_pool[i]))

            r_val = process_pool[i]
            try:
                shrd_queue.put('From:run_dispatcher', timeout=1)
                shrd_queue.put('To:MultiProcessManager.run', timeout=1)
                no_arg = 4+len(r_val['args'])
                shrd_queue.put(no_arg, timeout=1) # number of argument
                shrd_queue.put(r_val['function'], timeout=1)
                shrd_queue.put(r_val['key']     , timeout=1)
                shrd_queue.put(r_val['timeout'] , timeout=1)
                shrd_queue.put(r_val['priority'], timeout=1)
                for item in r_val['args']: shrd_queue.put(item, timeout=1)

            except BrokenPipeError as e:
                print('Shared Queue is broken... go next loop...')
                logger.error('Shared Queue is broken... go next loop...')
                logger.error(e)
    
    except Exception as e:
        logger.error(e)

    finally:
        pass


def set_workers(manager_obj=None, logger_root=None, logger_leaf=None, shrd_queue=None):
    process_pool = {
        #random.randint(0, 100)
          'f20': {'function': f2, 'args': ('f20', 3), 'timeout': 10, 'priority': 4}
#        , 'f21': {'function': f2, 'args': ('f21', 3), 'timeout': 10, 'priority': 5}
#        , 'f22': {'function': f2, 'args': ('f22', 3), 'timeout': 10, 'priority': 6}
#        , 'f23': {'function': f2, 'args': ('f23', 3), 'timeout': 10, 'priority': 7}
#        , 'f13': {'function': f1, 'args': ('f13', ), 'timeout': 10, 'priority': 3}
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

#    print('---------- logger_leaf: {}'.format(logger_leaf))
#    print('---------- shrd_queue: {}'.format(shrd_queue))
    #dispatcher_dict = {'dispatcher': {'function': call_multiprocess_wrapper, 'args': (run_dispatcher, logger_leaf.get_queue(), 'run_dispatcher', manager_obj.get_workers(), create_logger_for_multiprocess(logger_leaf)), 'timeout': 10, 'priority': 999999}}
    dispatcher_dict = {
        'dispatcher': {
              'function': run_dispatcher
            , 'args': (
                  'run_dispatcher'
                , shrd_queue
            )
            , 'timeout': 10
            , 'priority': 999999
        }
    }
    dispatcher = None
    for r_key, r_val in dispatcher_dict.items():
        pr_obj = cprcs.StoppableProcess(
              target   = r_val['function']
            , name     = r_key
            , timeout  = r_val['timeout']
            , priority = r_val['priority']
            , args     = r_val['args']
        )
        dispatcher = [r_key, pr_obj, r_val['priority']]
    manager_obj.add_worker(dispatcher)
#    shrd_dict['wrkr_list'] = workers#manager_obj.get_workers()

    logger_root.info('Sorted worker processes queue ----------')
    for item in manager_obj.get_workers(): 
        logger_root.info('[Name, Process Instance, Priority] = {}'.format(item))



