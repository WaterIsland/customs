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

