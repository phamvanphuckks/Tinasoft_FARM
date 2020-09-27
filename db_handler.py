import sqlite3    as sql
import constant   as CONSTANT
import time, logging

from datetime  import datetime


logging.basicConfig(filename='logs\\error_code.log',level=logging.INFO)

class DataBase():
    def __init__(self):
        try:
            self.path = "databases\\DB_OF_SFARM.db"
            self.con  = sql.connect(self.path)
            self.cur  = self.con.cursor()
        except:
            logging.info('db_handler, __init__ : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))            

    def creat_table(self, place):
        try:
            table_name = "data_of_"+ str(place) + "_"+ datetime.now().strftime("%d_%m_%Y")
            with self.con:
                cmd = "CREATE TABLE IF NOT EXISTS " + table_name + '''(
                    stt         INTEGER     PRIMARY KEY AUTOINCREMENT,
                    node        INTEGER     NULL,
                    name        TEXT        NULL,
                    id          TEXT        NULL,
                    value       TEXT        NULL,
                    RF_signal   TEXT        NULL,
                    battery     TEXT        NULL,
                    time        TEXT        NULL, 
                    syn         TEXT        NULL)
                    '''
                self.cur.execute(cmd)
        except:
            logging.info('db_handler, creat_table : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def insert_data_nongtraiG00(self, place, syn):
        try:
            table_name = "data_of_"+ str(place) + "_"+ datetime.now().strftime("%d_%m_%Y")
            with self.con:
                cmd = "CREATE TABLE IF NOT EXISTS " + table_name + '''(
                    stt         INTEGER     PRIMARY KEY AUTOINCREMENT,
                    node        INTEGER     NULL, 
                    name        TEXT        NULL,
                    id          TEXT        NULL,
                    value       TEXT        NULL,
                    RF_signal   TEXT        NULL,
                    battery     TEXT        NULL,
                    time        TEXT        NULL, 
                    syn         TEXT        NULL)
                    '''
                self.cur.execute(cmd)

                cmd = "INSERT INTO " + table_name + " (node,name,id,value,RF_signal,battery,time,syn) VALUES(?,?,?,?,?,?,?,?)"
                for i in range(1, 15):
                    if(i == 11): i = 21
                    elif(i == 12): i = 23
                    elif(i == 13): i = 25
                    elif(i == 14): i = 32

                    self.cur.execute(cmd, ( str(CONSTANT.DATA_G00["NODE"+str(i)]["node"]), str(CONSTANT.DATA_G00["NODE"+str(i)]["name"]), 
                    str(CONSTANT.DATA_G00["NODE"+str(i)]["id"]), str(CONSTANT.DATA_G00["NODE"+str(i)]["value"]), 
                    str(CONSTANT.DATA_G00["NODE"+str(i)]["RF_signal"]), str(CONSTANT.DATA_G00["NODE"+str(i)]["battery"]),
                    str(CONSTANT.DATA_G00["NODE"+str(i)]["time"]),  syn)
                    
                )
        except:
            logging.info('db_handler, insert_data_nongtraiG00 : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def insert_data_nongtraiG01(self, place, syn):
        try:
            table_name = "data_of_"+ str(place) + "_"+ datetime.now().strftime("%d_%m_%Y")
            with self.con:
                cmd = "CREATE TABLE IF NOT EXISTS " + table_name + '''(
                    stt         INTEGER     PRIMARY KEY AUTOINCREMENT,
                    node        INTEGER     NULL,
                    name        TEXT        NULL,
                    id          TEXT        NULL,
                    value       TEXT        NULL,
                    RF_signal   TEXT        NULL,
                    battery     TEXT        NULL,
                    time        TEXT        NULL, 
                    syn         TEXT        NULL)
                    '''
                self.cur.execute(cmd)

                cmd = "INSERT INTO " + table_name + " (node,name,id,value,RF_signal,battery,time,syn) VALUES(?,?,?,?,?,?,?,?)"
                for i in range(11, 25):
                    if(i == 21): i = 22
                    elif(i == 22): i = 24
                    elif(i == 23): i = 26
                    elif(i == 24): i = 33

                    self.cur.execute(cmd, (str(CONSTANT.DATA_G01["NODE"+str(i)]["node"]),str(CONSTANT.DATA_G01["NODE"+str(i)]["name"]), 
                    str(CONSTANT.DATA_G01["NODE"+str(i)]["id"]), str(CONSTANT.DATA_G01["NODE"+str(i)]["value"]), 
                    str(CONSTANT.DATA_G01["NODE"+str(i)]["RF_signal"]), str(CONSTANT.DATA_G01["NODE"+str(i)]["battery"]),
                    str(CONSTANT.DATA_G01["NODE"+str(i)]["time"]),  syn)
                )
        except:
            logging.info('db_handler, insert_data_nongtraiG01 : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def insert_data_Relay(self, place, syn):
        try:
            table_name = "data_of_"+ str(place) + "_"+ datetime.now().strftime("%d_%m_%Y")
            with self.con:
                cmd = "CREATE TABLE IF NOT EXISTS " + table_name + '''(
                    stt         INTEGER     PRIMARY KEY AUTOINCREMENT,
                    node        INTEGER     NULL,
                    name        TEXT        NULL,
                    id          TEXT        NULL,
                    value       TEXT        NULL,
                    RF_signal   TEXT        NULL,
                    battery     TEXT        NULL,
                    time        TEXT        NULL, 
                    syn         TEXT        NULL)
                    '''
                self.cur.execute(cmd)

                cmd = "INSERT INTO " + table_name + " (node,name,id,value,RF_signal,battery,time,syn) VALUES(?,?,?,?,?,?,?,?)"
                for i in range(27, 32):
                    self.cur.execute(cmd, (str(CONSTANT.DATA_G01["NODE"+str(i)]["node"]),str(CONSTANT.DATA_G01["NODE"+str(i)]["name"]), 
                    str(CONSTANT.DATA_G01["NODE"+str(i)]["id"]), str(CONSTANT.DATA_G01["NODE"+str(i)]["value"]), 
                    str(CONSTANT.DATA_G01["NODE"+str(i)]["RF_signal"]), str(CONSTANT.DATA_G01["NODE"+str(i)]["battery"]),
                    str(CONSTANT.DATA_G01["NODE"+str(i)]["time"]),  syn)
                )
        except:
            logging.info('db_handler, insert_data_Relay : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def insert_data_row(self, place, node, name, id, value,  RF_signal, battery, time, syn):
        try:
            table_name = "data_of_"+ str(place) + "_"+ datetime.now().strftime("%d_%m_%Y")
            with self.con:
                cmd = "CREATE TABLE IF NOT EXISTS " + table_name + '''(
                    stt         INTEGER     PRIMARY KEY AUTOINCREMENT,
                    node        INTEGER     NULL,
                    name        TEXT        NULL,
                    id          TEXT        NULL,
                    value       TEXT        NULL,
                    RF_signal   TEXT        NULL,
                    battery     TEXT        NULL,
                    time        TEXT        NULL, 
                    syn         TEXT        NULL)
                    '''
                self.cur.execute(cmd)

                cmd = "INSERT INTO " + table_name + " (node,name,id,value,RF_signal,battery,time,syn) VALUES(?,?,?,?,?,?,?,?)"
    
                self.cur.execute(cmd, (str(node), str(name),str(id), str(value), str(RF_signal), str(battery), str(time),  str(syn)))
        except:
            logging.info('db_handler, insert_data_row : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    # Xóa tất cả các table trong database;
    def get_table_name(self):
        try: 
            with self.con:
                tables = list(self.cur.execute(
                        "select name from sqlite_master where type is 'table' "))
            return tables
        except:
            logging.info('db_handler, get_table_name : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def Delete_all_tb(self):
        try:
            with self.con:
                tables = list(self.cur.execute(
                    "select name from sqlite_master where type is 'table'"))
                for i in tables :
                    if(i != "('sqlite_sequence',)"):
                        cmd = ';'.join(["DROP TABLE IF EXISTS %s" % i])
                    else:
                        pass
                self.cur.executescript(cmd)
                self.con.commit()
        except:
            logging.info('db_handler, Delete_all_tb : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        


