import fbAPI
import numpy as np
import time
import postgresHandler
import json

class Handler():
    def __init__(self, date):
        self.date = date
        self.table = ""
        self.metric = ""
        self.modifiers = []
        self.summary = []
        self.data = ""
        self.plot_x = ""
        self.plot_y = ""
        self.plotData = [[], []]
        self.fullLog = ""
        self.metricTemplate = ""
        self.minuteScale = 1
        self.version = 1
        self.pg = postgresHandler.pgSession()

    def getSummary(self):
        return self.summary


    def scale(self, scale):
        self.plotData = [[], []]
        start_minutes = scale[0] * 60
        end_minutes = scale[1] * 60
        self.data = self.fullLog
        for i in self.modifiers:
            self.data = self.data[i]

        for j in self.data:
            self.plotData[0].append(j[self.plot_x])
            self.plotData[1].append(j[self.plot_y])

        self.plotData[0] = self.plotData[0][start_minutes:end_minutes]
        self.plotData[1] = self.plotData[1][start_minutes:end_minutes]

    def changeDate(self,DATE):
        print(DATE)
        DATE = DATE.replace("/","-")
        self.date = DATE
        print(self.date)
        self.metric = self.metricTemplate.replace("DATE", DATE)
        self.update()

    def update(self):
        self.pg.openSession()
        exists = self.pg.checkEntryExists(self.date, self.table)

        if exists == True:
            if self.pg.checkIfComplete == True:
                print("PULLING OLD DATA")
                self.fullLog = self.pg.getEntry(self.date, self.table)
            else:
                print("PULLING NEW DATA")
                self.fullLog = fbAPI.getMetric(self.metric, self.version)
                self.pg.updateEntry(self.date, json.dumps(self.fullLog), self.table)
        else:
            self.pg.createEntry(self.date, json.dumps(self.fullLog), self.table )

        self.pg.closeSession()
