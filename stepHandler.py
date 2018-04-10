import fbAPI
import Handler
import numpy
class stepHandler(Handler.Handler):
    def __init__(self, date):
        super().__init__(date)
        self.modifiers = ["activities-steps-intraday", "dataset"]
        self.metricTemplate = "activities/steps/date/DATE/1d/1min.json"
        self.metric = "activities/steps/date/%s/1d/1min.json" % self.date
        self.version = "1"
        self.plot_x = "time"
        self.plot_y = "value"
        self.table = "steps"
        # self.update()

    def getTitle(self):
        return str("Total: %s Steps" % self.fullLog["activities-steps"][0]["value"])
