# -*- coding: utf-8 -*-
# Created on 2025/01/01
import os
import pandas as pd
import pyodbc
import sqlalchemy
import urllib
import re

import cstmlogging as clog


class CustomDB:
    def __init__(self, database: str='', script_name: str='', conn_type='connection', logger=None):
        if (logger is None): raise Exception('[Exception] Please set logger instance.')
        self.__database    = database
        self.__script_name = script_name
        self.__conn_type   = conn_type
        self.__logger      = logger
        self.__logger.info('Success to init. ::: {}({}, {}, {})'.format(self.__class__.__name__, database, script_name, conn_type))

    def create_connection_string_for_pyodbc(self, driver: str='SQL Server', server: str='', database: str='', user: str='', passwd: str='', script_name=''):
        self.__conn_str = 'Driver={%s};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s;APP=%s' % (driver, server, database, user, passwd, script_name)

    def create_connection_string_for_sqlalchemy(self, driver: str='SQL Server', server: str='', database: str='', user: str='', passwd: str='', script_name=''):
        self.create_connection_string_for_pyodbc(driver, server, database, user, passwd, script_name)
        self.__conn_str = urllib.parse.quote_plus(self.__conn_str)
        self.__conn_str = '%s+pyodbc:///?odbc_connect=%s' % (driver, self.__conn_str)

    def create_connection(self):
        if (self.__conn_type == 'connection'):
            try:
                self.__logger.info('App [{0}]: Creating the SQL connection to {1}'.format(self.__script_name, self.__database))
                self.__connection = pyodbc.connect(self.__conn_str, autocommit=False)
                self.__logger.info('App [{0}]: Success to create the connection for {1}'.format(self.__script_name, self.__database))

            except Exception as e:
                self.__logger.error(e)
                self.__logger.warning('App [{0}]: Fail to create the connection for {1}'.format(self.__script_name, self.__database))

        elif self.__conn_type == 'engine':
            try:
                self.__logger.info('App [{0}]: Creating the SQL connection to {1}'.format(self.__script_name, self.__database))
                self.__connection = sqlalchemy.create_engine(self.__conn_str)
                self.__logger.info('App [{0}]: Success to create the connection for {1}'.format(self.__script_name, self.__database))

            except Exception as e:
                self.__logger.error(e)
                self.__logger.warning('App [{0}]: Fail to create the connection for {1}'.format(self.__script_name, self.__database))

    def close_connection(self):
        try:
            self.__logger.info('App [{0}]: Disconnecting from {1}'.format(self.__script_name, self.__database))
            if   (self.__conn_type == 'connection'): self.__connection.close()
            elif (self.__conn_type == 'engine')    : self.__connection.dispose()
            self.__logger.info('App [{0}]: Success to disconnect from {1}'.format(self.__script_name, self.__database))

        except Exception as e:
            self.__logger.error(e)
            self.__logger.warning('App [{0}]: Fail to disconnect from {1}'.format(self.__script_name, self.__database))

    def get_db_connection(self):
        return self.__connection

    def get_cursor(self):
        self.__cursor = self.__connection.cursor()

    def close_cursor(self):
        if self.__cursor.fetchone != None: self.__cursor.close()

    def execute_query(self, query):
        try:
            self.__logger.info('App [{0}]: Executing a query on {1}'.format(self.__script_name, self.__database))
            results = None
            if (self.__conn_type == 'connection'):
                cursor = self.__connection.cursor()
                cursor.execute(query)
                resultes = cursor.fetchall()
                results_cols = [column[0] for column in cursor.description]
                results = pd.DataFrame.from_records(data=results, columns=results_cols)
                cursor.close()

            elif (self.__conn_type == 'engine'):
                results = self.__connection.execute(query)

            self.__logger.info('App [{0}]: Success to execute a query on {1}'.format(self.__script_name, self.__database))
            return results

        except Exception as e:
            self.__logger.error(e)
            self.__logger.warning('App [{0}]: Fail to execute a query on {1}'.format(self.__script_name, self.__database))

    def commit_query(self):
        try:
            self.__logger.info('App [{0}]: Commit a query on {1}'.format(self.__script_name, self.__database))
            self.__connectionn.commit()
            self.__logger.info('App [{0}]: Success to commit a query on {1}'.format(self.__script_name, self.__database))
            return 0

        except Exception as e:
            self.__logger.error(e)
            self.__logger.warning('App [{0}]: Fail to commit a query on {1}'.format(self.__script_name, self.__database))

        try:
            self.__logger.info('App [{0}]: Rollback a query on {1}'.format(self.__script_name, self.__database))
            self.__connectionn.rollback()
            self.__logger.info('App [{0}]: Success to rollback a query on {1}'.format(self.__script_name, self.__database))

        except Exception as e:
            self.__logger.error(e)
            self.__logger.warning('App [{0}]: Fail to rollback a query on {1}'.format(self.__script_name, self.__database))

        finally:
            return -1

