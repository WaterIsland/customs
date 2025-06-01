# -*- conding: utf-8 -*-
# Created on 2025/05/01
import multiprocessing as mltprcs

from customs import cstmlogging  as clog
#from customs import cstmthread   as cthrd
from customs import cstmprocess  as cprcs # need psutil
#from customs import cstmdb       as cdb   # need pandas, pyodbc, sqlalchemy, urllib
from customs import cstmfunction as cfnc


ROOT_LOG_PATH       = 'log\\test_root.log'
PROCESS_LOG_PATH    = 'log\\test_leaf_process.log'
DISPATCHER_LOG_PATH = 'log\\test_leaf_dispatcher.log'


if __name__ == '__main__':
    with mltprcs.Manager() as manager:
        shrd_queue = manager.Queue()

        logger_root = clog.CustomLogging(file_name=ROOT_LOG_PATH)
        logger_leaf = clog.CustomLoggingForProcess(file_name=PROCESS_LOG_PATH)

        logger_leaf.start_logging()
        try:
            manager_obj = cprcs.MultiProcessManager(
                  accuracy = 1
                , cpu_rate = 0.5
                , logger   = logger_root
                , queue    = shrd_queue)
            cfnc.set_initial_workers(
                  manager_obj      = manager_obj
                , logger_root      = logger_root
                , process_log_path = PROCESS_LOG_PATH
                , dispach_log_path = DISPATCHER_LOG_PATH
                , shrd_queue       = shrd_queue
            )

            # Create inpector process
            logger_root.info('Created inspector processes ----------')
#            inspector_obj = cprcs.StoppableProcess(target=cprcs.MultiProcessManager.run, name='MultiProcessManager.run', timeout=1)
            inspector_obj = cprcs.StoppableProcess(target=cprcs.MultiProcessManager.run, name='MultiProcessManager.run', timeout=5)
#            inspector_obj = cprcs.StoppableProcess(target=cprcs.MultiProcessManager.run, name='MultiProcessManager.run', timeout=10)
#            inspector_obj = cprcs.StoppableProcess(target=cprcs.MultiProcessManager.run, name='MultiProcessManager.run', timeout=20)

            manager_obj.set_inspector(inspector_obj)
            logger_root.info('Launch multiprocess ----------')
            manager_obj.run()
        
        except Exception as e:
            logger_root.error(e)

        finally:
            logger_leaf.stop_logging()

        logger_root.info('End multiprocess _/_/_/_/_/_/_/_/_/_/')

