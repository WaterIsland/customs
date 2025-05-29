# -*- coding: utf-8 -*-
# Created on 2025/05/01
import multiprocessing
import time
import psutil
import inspect
import queue


#####
#
# StoppableProcess
#
# If a process calls terminate(), the process object will be stopped by inspector class.
#
#####
class StoppableProcess(multiprocessing.Process):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, daemon=False, timeout=None, priority=0):
        multiprocessing.Process.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs, daemon=daemon)
        self.__group    = group
        self.__target   = target
        self.__name     = name
        self.__args     = args
        self.__kwargs   = kwargs
        self.__daemon   = daemon
        self.__timeout  = timeout
        self.__priority = priority

    def start(self):
        super().start()

    def join(self):
        super().join(timeout=self.__timeout)

    def run(self):
        self.__target(*self.__args, **self.__kwargs)

    def terminate(self):
        super().terminate()

    def get_id(self):
        return self.pid

    def get_timeout(self):
        return self.__timeout
    
    def get_name(self):
        return self.__name
    
    def get_priority(self):
        return self.__priority
    

class MultiProcessManager():
    def __init__(self, accuracy=0.05, cpu_rate=0.5, logger=None, queue=None): 
        if (logger is None): raise Exception('[Exception] Please set logging instance.')
        self.__physical_cpu_core = int(psutil.cpu_count(logical=False)*cpu_rate)
        self.__logical_cpu_core  = int(psutil.cpu_count(logical=True)*cpu_rate)
        self.__accuracy = accuracy
        self.__logger   = logger
        self.__workers  = []
        self.__queue    = queue
        self.__logger.info('Success to init. ::: {}'.format(self.__class__.__name__))

    def __launch_new_process(self, pool, idx=-1):
        try:
            print('at __launch_new_process, pool: {}'.format(pool))
            print('at __launch_new_process, pool: {}'.format(self.__workers))
            self.__logger.info('at __launch_new_process, pool: {}'.format(pool))
            self.__logger.info('at __launch_new_process, self.__workers: {}'.format(self.__workers))
            launch = self.__workers.pop()
            #pool.append(launch)
            pool.insert(idx, launch)
            launch[1].start()
            print('Launch worker : {}'.format(launch))
            self.__logger.info('Launch worker : {}'.format(launch))
        except Exception as e:
            self.__logger.error('No worker processes : {}'.format(e))
            return -1
        return 0

    def run(self):
        # start() processes
        pool = []
        self.__logger.info('Launch worker processes ----------')
        for idx in range(self.__physical_cpu_core):
            ret = self.__launch_new_process(pool)
            if (ret < 0): break # No worker processes

        self.__logger.info('Odd worker processes ----------')
        for item in self.__workers:
            self.__logger.info('Launch worker : {}'.format(item))

        # Inspect multi-process
        self.__logger.info('Insprct worker processes ----------')
        start_time = time.perf_counter()
        while(True):
            time.sleep(self.__accuracy)

            end_time = time.perf_counter()
            diff_time = end_time - start_time
            print(f'Process execution time: {diff_time:.4f} seconds')
            self.__logger.debug(f'Process execution time: {diff_time:.4f} seconds')

            # Find had finished process
            finished = []
            for idx, ins in enumerate(pool):
                print('name: {}, is_alive: {}'.format(ins[1].get_name(), ins[1].is_alive()))
                self.__logger.debug('name: {}, is_alive: {}'.format(ins[1].get_name(), ins[1].is_alive()))
                if (ins[1].is_alive() is False):
                    ins[1].join()
                    finished.append(idx)
            
            # Remove had finished process and Launch new one
            for idx in finished:
                print('Pop ==> name: {}, is_alive: {}'.format(pool[idx][1].get_name(), pool[idx][1].is_alive()))
                self.__logger.debug('Pop ==> name: {}, is_alive: {}'.format(pool[idx][1].get_name(), pool[idx][1].is_alive()))
                pool.pop(idx) # Remove
                ret = self.__launch_new_process(pool, idx)
                if (ret < 0): break # No worker processes

            # Insert new process to empty queue
            if (len(pool) < self.__physical_cpu_core):
                cnt_of_empty = self.__physical_cpu_core - len(pool)
                for cnt in range(cnt_of_empty): self.__launch_new_process(pool, len(pool)+cnt-1)

            # Finish oneselves
            if (diff_time >= self.__inspector.get_timeout()):
                break
            
            try:
                # get data from manager Queue
                get_items = self.__queue.get(timeout=5)
                print('********** get_items : {}'.format(get_items))
                self.__logger.debug('********** get_items : {}'.format(get_items))

                from_val = get_items['from'] # From:run_dispatcher
                to_val   = get_items['to'] # To:MultiProcessManager.run                        
                tmp_ary = []
                if (from_val == 'run_dispatcher') and (to_val == 'MultiProcessManager.run'):
                    # generate process
                    pr_obj = StoppableProcess(
                          target   = get_items['function'] # r_val['function']
                        , name     = get_items['key']      # r_val['key']
                        , timeout  = get_items['timeout']  # r_val['timeout']
                        , priority = get_items['priority'] # r_val['priority']
                        , args     = (get_items['args'])   # r_val['args']
                    )
                    print('********** add worker: {}'.format(pr_obj))
                    self.__logger.debug('********** add worker: {}'.format(pr_obj))
                    self.add_worker([get_items['key'], pr_obj, get_items['priority']])
                    
                else:
                    # self.__queue.put(get_items, timeout=1) # restore queue?
                    pass

            except queue.Empty as e:
                print('Shared Queue is empty... go next loop...')
                self.__logger.error('Shared Queue is empty... go next loop...')

        # Terminate aliving processes
        self.__logger.info('Final check ----------')
        for ins in pool:
            if (ins[1].is_alive()):
                ins[1].terminate()
                ins[1].join()
            self.__logger.info('name: {}, is_alive: {}'.format(ins[1].get_name(), ins[1].is_alive()))

        self.__logger.info('Terminated check ----------')
        for ins in pool:
            self.__logger.info('name: {}, is_alive: {}'.format(ins[1].get_name(), ins[1].is_alive()))

    def set_inspector(self, instance=None):
        self.__inspector = instance

    #
    # workers format: [instance_name as string, instance as object, priority as int]
    #
    def set_workers(self, workers=[]):
        # Sort by priority as ASC
        #workers = sorted(workers, key=lambda x:x[2])
        sorted(workers, key=lambda x:x[2])
        self.__workers = workers
        print('[{}] self.__workers: {}'.format(inspect.currentframe().f_code.co_name, self.__workers))

    def get_workers(self):
        return self.__workers

    def add_workers(self, workers=[]):
        for worker in workers: self.__workers.append(worker)
        # Sort by priority as ASC
        #self.__workers = sorted(self.__workers, key=lambda x:x[2])
        sorted(self.__workers, key=lambda x:x[2])
        print('[{}] self.__workers: {}'.format(inspect.currentframe().f_code.co_name, self.__workers))

    def rm_workers(self):
        pass

    def set_worker(self, worker=None):
        self.__workers = worker

    def add_worker(self, worker=None):
        self.__workers.append(worker)
        # Sort by priority as ASC
        self.__workers = sorted(self.__workers, key=lambda x:x[2])
        sorted(self.__workers, key=lambda x:x[2])
        print('[{}] self.__workers: {}'.format(inspect.currentframe().f_code.co_name, self.__workers))

    def rm_worker(self):
        pass

