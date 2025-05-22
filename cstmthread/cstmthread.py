# -*- coding: utf-8 -*-
# Created on 2023/01/01
import threading
import ctypes
import time
import cstmlogging as clog


#####
#
# RaisableThread (StoppableThread)
#
# If it calls a method of raise_exception(), this thread object will be stopped.
# If thread use GIL resoruce, then it needs to implement functions in order to release resources correctly.
#
#####
class RaisableThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, daemon=True, logger=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, daemon=daemon, args=args, kwargs=kwargs)
        if (logger is None): raise Exception('[Ecception] Please set logget instance.')
        self.__group = group
        self.__target = target
        self.__name = name
        self.__args = args
        self.__kwargs = kwargs
        self.__daemon = daemon
        self.__logger = logger
        self.__logger.info('Success to init. ::: {}({}, {}, {})'.format(self.__class__.__name__, group, target, name))

    def start(self):
        super().start()

    def join(self, timeout: int=0):
        super().join(timeout)

    def run(self):
        self.__target(*self.__args, **self.__kwargs)

    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if (thread is self):
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        responce = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread_id), ctypes.py_object(SystemExit))
        if (responce == 1):
            self.__logger.info('Success in ransing exception.')
        elif (responce == 0):
            self.__logger.error('Failure in ransing exception.')
            ctypes.pyhonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread_id), 0)

    def inspect(self):
        if self.is_alive():
            self.raise_exception()
            for i in range(10):
                time.sleep(0.1)
                if self.is_alive():
                    self.__logger.info('Can stop thread. Waiting {} seconds.'.format(float(i)*0.1))
                    return 0
            self.__logger.error('Cannot stop thread.')
            raise Exception('Cannot stop thread.')

        else:
            self.__logger.info('Had stopped thread.')


if __name__ == '__main__':
    import sys
    import time
    import traceback

    def f1(logger=None):
        try:
            if (logger is None):
                raise Exception('No logger instance.')

        except Exception as e:
            return -1
        
        show_str = 'Start '+ sys._getframe().f_code.co_name
        logger.info(show_str)
        print(show_str)
        for i in range(10):
            show_str = 'Process {} => {}'.format(sys._getframe().f_code.co_name, i)
            logger.info(show_str)
            print(show_str)
            time.sleep(1)
        show_str = 'End '+ sys._getframe().f_code.co_name
        logger.info(show_str)
        print(show_str)


    def f2(cnt: int = 1, logger=None):
        try:
            if (logger is None):
                raise Exception('No logger instance.')

        except Exception as e:
            return -1

        show_str = 'Start '+ sys._getframe().f_code.co_name
        logger.info(show_str)
        print(show_str)
        for i in range(cnt):
            show_str = 'Process {} => {}'.format(sys._getframe().f_code.co_name, i)
            logger.info(show_str)
            print(show_str)
            time.sleep(1)
        show_str = 'End '+ sys._getframe().f_code.co_name
        logger.info(show_str)
        print(show_str)


    logger = clog.CustomLogging(file_name='log\\test.log')

    try:
        # It needs logger instance on each method as f1/f2
        #th_obj_xxx = RaisableThread(target=f1, name='f1', logger=logger, args=())
        #th_obj_yyy = RaisableThread(target=f2, name='f2', logger=logger, args=(10, ))
        # No problem
        th_obj1 = RaisableThread(target=f1, name='f1', logger=logger, args=(logger,))
        th_obj2 = RaisableThread(target=f2, name='f2', logger=logger, args=(10, logger))

        '''
        # Not parallel
        th_obj1.start()
        th_obj2.start()
        th_obj1.join(timeout=2)
        th_obj2.join(timeout=1)
        th_obj1.inspect()
        th_obj2.inspect()
        '''

        # Sirial
        th_obj1.start()
        th_obj1.join(timeout=2)
        th_obj1.inspect()

        th_obj2.start()
        th_obj2.join(timeout=6) # stop middle
        #th_obj2.join(timeout=11) # finish all
        th_obj2.inspect()

        '''
        # Adhoc launch -> Non stoppable
        th_obj1.run()
        th_obj2.run()
        '''
        raise Exception('Test Exception')

    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc())

