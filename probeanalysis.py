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
        return  file.readlines()

    def show(self):
        plt.plot(self.x, self.y)
        plt.show()

    def processData(self):
        pass

class ProbeAnalysis(Analyser):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.mac = []
        self.wantedList = ["Raspberr_3f:48:74", "AVMAudio_42:d6:ff", "Sagemcom_9b:c2:74"]

    def isWildcard(self, inp):
        if len(inp) >= 2 and inp[1] == "Wildcard (Broadcast)":
            return True
        return False
    def processData(self):
        result = {}
        document = self.readCSV(self.filename)
        size = int(float(document[-1].split(",")[1][1:-1]))
        self.x = np.array(range(0, size + 1))
        for i in range(size):
            result[i] = []
        print(self.x)
        for line in document:
            line = line.split(',')
            wildcard = line[INFO_INDEX][:-2].split("=")

            if line[PROBE_INDEX][1:] == "Probe Request" and self.isWildcard(wildcard) and line[MAC_INDEX][1:-1] not in self.wantedList :

                key = int(float(line[TIME_INDEX][1:-1]))
                if key not in result.keys():
                    result[key] = []
                result[key] = result[key] + [line[MAC_INDEX][1:-1]]

                if line[MAC_INDEX][1:-1] not in self.mac:
                    self.mac.append(line[MAC_INDEX][1:-1]) #add mac_addr list

        return result

    def constructProbeAnalysis(self, result):
        self.y = [len(result[x]) for x in result.keys()]
        print(self.y)
        print(len(self.y))
        print(sum(self.y))
        #self.x = self.x[7200:10800]
        #self.y = self.y[7200:10800]
        #self.x = self.x[:60]
        #self.y = self.y[:60]

    def constructMacAnalysis(self, result):
        temp = []
        mac = []
        for i in result.keys():
            count = 0
            for j in result[i]:
                if j not in mac:
                    mac.append(j)
                    count = count + 1
            temp.append(count)
        self.y = temp

    def getMacNum(self):
        return self.mac


app = ProbeAnalysis("ingolstadt.csv")
result = app.processData()
app.constructMacAnalysis(result)
app.show()

