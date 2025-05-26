# -*- coding: utf-8 -*-
# Created on 2025/05/01
import logging
import multiprocessing

import cstmlogging as clog


def create_logger_for_multiprocess(log_queue: multiprocessing.Queue=None):
    logger = logging.getLogger(__file__)
    handler = logging.handlers.QueueHandler(log_queue)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


def call_multiprocess_wrapper(function=None, log_queue: multiprocessing.Queue=None, *args):
    logger = create_logger_for_multiprocess(log_queue)
    try:
        if (logger is None):
            raise Exception('No logger instance.')

    except Exception as e:
        return -1

    # create arguments
    arg_list = [logger]
    for item in args:
        arg_list.append(item)
    logger.info('arg_list: {}'.format(arg_list))
    
    function(arg_list) # call multiprocess function


import sys
import random
import time


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

#    f0(logger)


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

#    f0(logger)


#class MultiProcessDispatcher(multiprocessing.Process):
#    @staticmethod
#def run_dispatcher():
def run_dispatcher(*args):
    logger    = args[0][0]
    func_name = args[0][1]
    dispatched_workers = args[0][2]
    logger_leaf_queue = args[0][3]

    for i in range(2):
        time.sleep(5)
        logger.info('dispatched_workers: {}'.format(dispatched_workers))
        print('dispatched_workers: {}'.format(dispatched_workers))

        logger.info('Add again... ==> {} sec'.format(i))
        print('Add again... ==> {} sec'.format(i))
#            workers = []
        process_pool = {
              'f10': {'function': call_multiprocess_wrapper, 'args': (f1, logger_leaf_queue, 'f10'), 'timeout': 10, 'priority': 8}
            , 'f11': {'function': call_multiprocess_wrapper, 'args': (f1, logger_leaf_queue, 'f11'), 'timeout': 10, 'priority': 9}
            , 'f12': {'function': call_multiprocess_wrapper, 'args': (f1, logger_leaf_queue, 'f12'), 'timeout': 10, 'priority': 10}
            , 'f13': {'function': call_multiprocess_wrapper, 'args': (f1, logger_leaf_queue, 'f13'), 'timeout': 10, 'priority': 11}
            , 'f20': {'function': call_multiprocess_wrapper, 'args': (f2, logger_leaf_queue, 'f20', 3), 'timeout': 10, 'priority': 12}
            , 'f21': {'function': call_multiprocess_wrapper, 'args': (f2, logger_leaf_queue, 'f21', 3), 'timeout': 10, 'priority': 13}
            , 'f22': {'function': call_multiprocess_wrapper, 'args': (f2, logger_leaf_queue, 'f22', 3), 'timeout': 10, 'priority': 14}
            , 'f23': {'function': call_multiprocess_wrapper, 'args': (f2, logger_leaf_queue, 'f23', 3), 'timeout': 10, 'priority': 15}
        }
        for r_key, r_val in process_pool.items():
            pr_obj = cprcs.StoppableProcess(
                target   = r_val['function']
                , name     = r_key
                , timeout  = r_val['timeout']
                , priority = r_val['priority']
                , args     = r_val['args']
            )
            dispatched_workers.append([r_key, pr_obj, r_val['priority']])


import random
from customs import cstmprocess  as cprcs # need psutil


def set_workers(manager_obj=None, logger_root=None, logger_leaf=None):
    process_pool = {
        #random.randint(0, 100)
          'f10': {'function': call_multiprocess_wrapper, 'args': (f1, logger_leaf.get_queue(), 'f10'), 'timeout': 10, 'priority': 0}
        , 'f11': {'function': call_multiprocess_wrapper, 'args': (f1, logger_leaf.get_queue(), 'f11'), 'timeout': 10, 'priority': 1}
        , 'f12': {'function': call_multiprocess_wrapper, 'args': (f1, logger_leaf.get_queue(), 'f12'), 'timeout': 10, 'priority': 2}
        , 'f13': {'function': call_multiprocess_wrapper, 'args': (f1, logger_leaf.get_queue(), 'f13'), 'timeout': 10, 'priority': 3}
        , 'f20': {'function': call_multiprocess_wrapper, 'args': (f2, logger_leaf.get_queue(), 'f20', 3), 'timeout': 10, 'priority': 4}
        , 'f21': {'function': call_multiprocess_wrapper, 'args': (f2, logger_leaf.get_queue(), 'f21', 3), 'timeout': 10, 'priority': 5}
        , 'f22': {'function': call_multiprocess_wrapper, 'args': (f2, logger_leaf.get_queue(), 'f22', 3), 'timeout': 10, 'priority': 6}
        , 'f23': {'function': call_multiprocess_wrapper, 'args': (f2, logger_leaf.get_queue(), 'f23', 3), 'timeout': 10, 'priority': 7}
#        , 'dispatcher': {'function': call_multiprocess_wrapper, 'args': (run_dispatcher, logger_leaf.get_queue(), 'run_dispatcher', workers, create_logger_for_multiprocess(logger_leaf)), 'timeout': 10, 'priority': 999999}
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


    dispatcher_dict = {'dispatcher': {'function': call_multiprocess_wrapper, 'args': (run_dispatcher, logger_leaf.get_queue(), 'run_dispatcher', manager_obj.get_workers(), create_logger_for_multiprocess(logger_leaf)), 'timeout': 10, 'priority': 999999}}
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

    logger_root.info('Sorted worker processes queue ----------')
    for item in manager_obj.get_workers(): 
        logger_root.info('[Name, Process Instance, Priority] = {}'.format(item))

#    time.sleep(2)
#    logger_root.info('Add workers processes queue ----------')
#    manager_obj.add_worker(workers[0])
#    manager_obj.add_worker(workers[1])
#    manager_obj.add_worker(workers[2])

