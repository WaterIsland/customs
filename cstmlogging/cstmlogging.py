# -*- coding: utf-8 -*-
# Created on 2022/01/01
import os
import logging
import logging.handlers
import multiprocessing


#####
# Logging for single process
#####
class CustomLogging():
    def __init__(self, file_name: str='log/logger.log', log_level=logging.DEBUG, rotation=14, when='D', interval=1, cnt=5, utc=False):
        # Set logging configuration
        self.__logger = logging.getLogger(__name__+self.__class__.__name__)
        self.__logger.setLevel(log_level)

        # Force file creation
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
    
        # To avoid muliple same logging istance initializing
        self.__trfl_handler = logging.handlers.TimedRotatingFileHandler(
              filename    = file_name
            , when        = when
            , interval    = interval
            , backupCount = cnt
            , utc         = utc
        )
        if not self.__logger.hasHandlers():
            self.__logger.addHandler(self.__trfl_handler)

        formatter = logging.Formatter(
              fmt     = '%(asctime)s [%(levelname)s] %(message)s'
            , datefmt = '%Y/%m/%d %H:%M:%S'
        )
        self.__trfl_handler.setFormatter(formatter)
        self.log_level = log_level
    
    def get_logger(self)   : return self.__logger
    def get_log_level(self): return self.log_level
    
    # Extended logging functions
    def log(self, log_level: str, msg: str):
        log_level = str.lower(log_level)
        if   log_level == 'debug'    : self.__logger.debug(msg)
        elif log_level == 'dbg'      : self.__logger.debug(msg)
        elif log_level == 'info'     : self.__logger.info(msg)
        elif log_level == 'inf'      : self.__logger.info(msg)
        elif log_level == 'error'    : self.__logger.error(msg)
        elif log_level == 'err'      : self.__logger.error(msg)
        elif log_level == 'warning'  : self.__logger.warning(msg)
        elif log_level == 'warn'     : self.__logger.warning(msg)
        elif log_level == 'fatal'    : self.__logger.fatal(msg)
        elif log_level == 'ftl'      : self.__logger.fatal(msg)
        elif log_level == 'critical' : self.__logger.critical(msg)
        elif log_level == 'crtcl'    : self.__logger.critical(msg)

    # Default logging functions
    def debug   (self, msg: str): self.__logger.debug(msg)
    def info    (self, msg: str): self.__logger.info(msg)
    def error   (self, msg: str): self.__logger.error(msg)
    def warning (self, msg: str): self.__logger.warning(msg)
    def fatal   (self, msg: str): self.__logger.fatal(msg)
    def critical(self, msg: str): self.__logger.critical(msg)

#####
# Logging for multiprocess
#
# Please call Constractor -> start_logging() -> stop_logging()
#####
class CustomLoggingForProcess(multiprocessing.Process):
    def __init__(self, file_name: str='log/logger_pdp_process.log', log_level=logging.DEBUG, rotation=14, when='D', interval=1, cnt=5, utc=False):
        # Set logging configuration
        self.__logger = logging.getLogger(__name__+self.__class__.__name__)
        self.__logger.setLevel(log_level)

        # Force file creation
        os.makedirs(os.path.dirname(file_name), exist_ok=True)

        file_formattar = logging.Formatter(
              fmt     = '%(asctime)s [%(levelname)s] %(message)s'
            , datefmt = '%Y/%m/%d %H:%M:%S'
        )
        self.__trfl_handler = logging.handlers.TimedRotatingFileHandler(
              filename    = file_name
            , when        = when
            , interval    = interval
            , backupCount = cnt
            , utc         = utc
        )
        self.__trfl_handler.setFormatter(file_formattar)
        self.__logger.addHandler(self.__trfl_handler)
        self.__queue = multiprocessing.Manager().Queue()
        self.__listener = logging.handlers.QueueListener(self.__queue, self.__trfl_handler)

        self.__logger.addHandler(self.__trfl_handler)

    def start_logging(self): self.__listener.start()
    def stop_logging(self) : self.__listener.stop()

    def get_listener(self) : return self.__listener
    def get_queue(self)    : return self.__queue
    def get_logger(self)   : return self.__logger
    def get_log_level(self): return self.log_level
    
    # Extended logging functions
    def log(self, log_level: str, msg: str):
        log_level = str.lower(log_level)
        if   log_level == 'debug'    : self.__logger.debug(msg)
        elif log_level == 'dbg'      : self.__logger.debug(msg)
        elif log_level == 'info'     : self.__logger.info(msg)
        elif log_level == 'inf'      : self.__logger.info(msg)
        elif log_level == 'error'    : self.__logger.error(msg)
        elif log_level == 'err'      : self.__logger.error(msg)
        elif log_level == 'warning'  : self.__logger.warning(msg)
        elif log_level == 'warn'     : self.__logger.warning(msg)
        elif log_level == 'fatal'    : self.__logger.fatal(msg)
        elif log_level == 'ftl'      : self.__logger.fatal(msg)
        elif log_level == 'critical' : self.__logger.critical(msg)
        elif log_level == 'crtcl'    : self.__logger.critical(msg)

    # Default logging functions
    def debug   (self, msg: str): self.__logger.debug(msg)
    def info    (self, msg: str): self.__logger.info(msg)
    def error   (self, msg: str): self.__logger.error(msg)
    def warning (self, msg: str): self.__logger.warning(msg)
    def fatal   (self, msg: str): self.__logger.fatal(msg)
    def critical(self, msg: str): self.__logger.critical(msg)

    def listener(self, logger=None):
        while True:
            logger.handle(self.get_queue().get())

    def worker(logger=None):
        for i in range(3):
            logger.info("message #{}".format(i))

    @staticmethod
    def create_logger_for_multiprocess(log_queue: multiprocessing.Queue=None):
        logger = logging.getLogger(__file__)
        handler = logging.handlers.QueueHandler(log_queue)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        return logger

if __name__ == '__main__':
    import time

    log_obj1 = CustomLogging(file_name='log/test_normal.log')
    log_obj1.log('INFO', 'info test')
    log_obj1.error('error test')

    time.sleep(2)
    log_obj2 = CustomLoggingForProcess(file_name='log/test_pdp.log')
    log_obj2.start_logging()
    log_obj2.log('INFO', 'info test')
    log_obj2.error('error test')
    log_obj2.stop_logging()


