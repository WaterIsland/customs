# -*- conding: utf-8 -*-
# Created on 2025/05/01
import multiprocessing as mltprcs

from customs import cstmlogging  as clog
#from customs import cstmthread   as cthrd
from customs import cstmprocess  as cprcs # need psutil
#from customs import cstmdb       as cdb   # need pandas, pyodbc, sqlalchemy, urllib
from customs import cstmfunction as cfnc


if __name__ == '__main__':
    with mltprcs.Manager() as manager:
        shrd_queue = manager.Queue()

        logger_root = clog.CustomLogging(file_name='log\\test_root.log')
        logger_leaf = clog.CustomLoggingForProcess(file_name='log\\test_leaf.log')

        logger_leaf.start_logging()
        try:
            manager_obj = cprcs.MultiProcessManager(accuracy=1, cpu_rate=0.5, logger=logger_root, queue=shrd_queue)
            cfnc.set_workers(manager_obj, logger_root, logger_leaf, shrd_queue)

            # Create inpector process
            logger_root.info('Created inspector processes ----------')
#            inspector_obj = cprcs.StoppableProcess(target=cprcs.MultiProcessManager.run, name='MultiProcessManager.run', timeout=1)
#            inspector_obj = cprcs.StoppableProcess(target=cprcs.MultiProcessManager.run, name='MultiProcessManager.run', timeout=5)
#            inspector_obj = cprcs.StoppableProcess(target=cprcs.MultiProcessManager.run, name='MultiProcessManager.run', timeout=10)
            inspector_obj = cprcs.StoppableProcess(target=cprcs.MultiProcessManager.run, name='MultiProcessManager.run', timeout=20)

            manager_obj.set_inspector(inspector_obj)
            logger_root.info('Launch multiprocess ----------')
            manager_obj.run()
        
        except Exception as e:
            logger_root.error(e)

        finally:
            logger_leaf.stop_logging()

        logger_root.info('End multiprocess _/_/_/_/_/_/_/_/_/_/')


