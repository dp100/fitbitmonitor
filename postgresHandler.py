import psycopg2
import datetime, sys, fbAPI
from vaultClient import *

vault = vaultClient("http://172.17.0.1:8200", "jenkins", sys.argv[1])
PGdata = vault.get("postgres/data")

print(PGdata)

class pgSession():
    def __init__(self):
        self.conn = ""
        self.cur = ""

    def checkEntryExists(self,date,table):
        command = "SELECT datetime FROM %s WHERE datetime = '%s'"  % (table, date)
        self.cur.execute(command)
        if len(self.cur.fetchall()) != 0:
            print("Entry already exists, updating existing entry")
            return True
        else:
            print("Entry doesn't exist, creating new entry")
            return False
    # 
    # def newEntry(self,date,data,table):
    #     self.openSession()
    #     if self.checkEntryExists(date, table) == True:
    #
    #         else:
    #             self.updateEntry(date, data, table)
    #     else:
    #         self.createEntry(date, data, table)
    #     self.conn.commit()
    #     self.closeSession()

    def createEntry(self, date, data,table):
        command = "INSERT INTO %s (datetime, json) VALUES ('%s', '%s')" % (table,date,data)
        self.cur.execute(command)

    def updateEntry(self, date, data, table):
        command = "UPDATE %s SET json = '%s' WHERE datetime = '%s'" % (table, data, date)
        self.cur.execute(command)

    def getEntry(self, date, table):
        command = "SELECT json FROM %s WHERE datetime = '%s'"  % (table, date)
        self.cur.execute(command)
        return self.cur.fetchall()

    def checkIfComplete(self,date,table):
        entry = str(self.getEntry(date,table))
        if entry.__contains__("23:59:00"):
            return True
        else:
            return False


    def openSession(self):
        self.conn = psycopg2.connect(dbname=PGdata["name"], user=PGdata["user"], password=PGdata["password"], host=PGdata["host"], port=PGdata["port"])
        self.cur = self.conn.cursor()

    def closeSession(self):
        self.conn.close()
