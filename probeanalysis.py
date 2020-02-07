import matplotlib.pyplot as plt
import numpy as np

TIME_INDEX = 1
INFO_INDEX = -1
PROBE_INDEX = 6
MAC_INDEX = 2


class Analyser:
    def __init__(self):
        self.x = []
        self.y = []

    def readCSV(self, filename):
        file = open(filename, 'r')
        return file

    def show(self):
        plt.plot(self.x, self.y)
        plt.show()

    def processData(self):
        pass

class ProbeAnalysis(Analyser):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.mac = {}
        self.wantedList = ["Raspberr_3f:48:74", "AVMAudio_42:d6:ff", "Sagemcom_9b:c2:74"]

    def processData(self):
        result = {}
        file = self.readCSV(self.filename)
        document = file.readlines()
        size = int(float(document[-1].split(",")[1][1:-1]))
        print(size)
        self.x = np.array(range(0, size + 1))
        for i in range(size):
            result[i] = []
        print(self.x)
        for line in document:
            line = line.split(',')
            if line[PROBE_INDEX][1:] == "Probe Request" and line[MAC_INDEX][1:-1] not in self.wantedList:
                key = int(float(line[TIME_INDEX][1:-1]))
                if key not in result.keys():
                    result[key] = []
                result[key] = result[key] + [line[MAC_INDEX]]
        self.y = [len(result[x]) for x in result.keys()]
        print(self.y)
        print(len(self.y))
        print(sum(self.y))
        #self.x = self.x[7200:10800]
        #self.y = self.y[7200:10800]
        self.x = self.x[:60]
        self.y = self.y[:60]


app = ProbeAnalysis("ingolstadt.csv")
app.processData()
app.show()
