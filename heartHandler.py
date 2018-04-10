import fbAPI
import Handler
import numpy
class heartHandler(Handler.Handler):
    def __init__(self, date):
        super().__init__(date)
        self.modifiers = ["activities-heart-intraday", "dataset"]
        self.metricTemplate = "activities/heart/date/DATE/1d/1min.json"
        self.metric = "activities/heart/date/%s/1d/1min.json" % self.date
        self.version = "1"
        self.plot_x = "time"
        self.plot_y = "value"
        self.table = "heartrate"
        # self.update()

    def getTitle(self):
        lastEntries = self.plotData[1][-10:]
        num = 0
        for i in lastEntries:
            num += i
        num /= 10
        return str("Last 10mins Avg: %sbpm" % num)
