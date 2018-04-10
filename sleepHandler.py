import fbAPI
import Handler
import numpy
class sleepHandler(Handler.Handler):
    def __init__(self, date):
        super().__init__(date)
        self.modifiers = ["sleep",0,"levels","data"]
        self.metricTemplate = "sleep/date/DATE.json"
        self.metric = "sleep/date/%s.json" % self.date
        self.version = "1.2"
        self.plot_x = "dateTime"
        self.plot_y = "level"
        self.table = "sleep"
        # self.update()
        # self.summary = self.fullLog["summary"]

    def getSummary(self):
        self.stages = []
        self.update()
        try:
            self.summary = self.fullLog["sleep"][0]["levels"]["summary"]
            for i in self.summary:
                self.stages.append(self.summary[i]["minutes"])
        except Exception:
            print("No sleep logs")
        return self.stages



    def scale(self, scale):
        self.plotData = [[], []]
        self.data = self.fullLog
        value = 0
        for i in self.modifiers:
            self.data = self.data[i]

        for j in self.data:

            self.plotData[0].append(j[self.plot_x].split("T")[1].split(".")[0])
            if j[self.plot_y] == "deep":
                value = 3
            elif j[self.plot_y] == "light":
                value = 2
            elif j[self.plot_y] == "rem":
                value = 1
            elif j[self.plot_y] == "wake":
                value = 0
            self.plotData[1].append(value)

    def getTitle(self):
        return "Sleep Logs"
