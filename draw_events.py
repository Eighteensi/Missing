# -*- coding:utf-8 -*-


import os, sys
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties



def get_flood_event(floodsFile):
    '''Get flood events id.
    '''
    events = []
    with open(floodsFile, "r") as floods:
        events = [flood.strip() for flood in floods if flood.strip()]
    return events


def get_file_data(src_file):
    '''Get data from src file.
    '''
    data = []
    with open(src_file, "r", encoding="utf8") as src:
        for line in src.readlines():
            arr = line.strip().split()
            if not len(arr):
                continue
            data.append(float(arr[3]))
    return data


def draw_events(events,srcDir=".\\"):
    '''Draw events result to pictures.
    '''
    for event in events:
        #qob = get_file_data(os.path.join(srcDir, event, "qobs.txt"))
        res = get_file_data(os.path.join(srcDir, event, "result.txt"))
        x = range(0, len(res))
        plt.figure(figsize=(10,6), dpi=80)        
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        #plt.plot(x, qob, label="实测", linestyle="-", color="blue")
        plt.plot(x, res, label="模拟", linestyle="--", color="orange")
        #plt.xticks(x[::1])
        plt.title("{}".format(event))
        plt.xlabel("时段（h）")
        plt.ylabel("流量（m3/s）")
        plt.legend()
        plt.savefig(os.path.join(srcDir, "result", "{}.png".format(event)))
                           
        
def analyse_events(events, dt, srcDir=".\\", warmup=0):
    '''Analys api simulation result.
    '''
    dcVal = []
    meaVol, simVol, volErr = [], [], []
    meaPeak, simPeak, peakErr = [], [], []
    meaHour, simHour, hourErr = [], [], []
    for event in events:
        qobFile = os.path.join(srcDir, event, "qobs.txt")
        resFile = os.path.join(srcDir, event, "result.txt")
        qob = [line.strip().split()[3] for line in open(qobFile, "r").readlines() if line.strip()]
        res = [line.strip().split()[3] for line in open(resFile, "r").readlines() if line.strip()]
        qob = [float(q) for q in qob[warmup:]]
        res = [float(r) for r in res[warmup:]]
        
        avQob = sum(qob)/len(qob)
        part1 = sum([pow(q-r, 2) for q, r in zip(qob, res)])
        part2 = sum([pow(q-avQob, 2) for q in qob])
        dcVal.append(1-part1/part2)

        meaVol.append(sum(qob)*0.36)
        simVol.append(sum(res)*0.36)
        volErr.append([simVol[-1]-meaVol[-1], (simVol[-1]-meaVol[-1])/meaVol[-1]])

        meaPeak.append(max(qob))
        simPeak.append(max(res))
        peakErr.append([simPeak[-1]-meaPeak[-1], (simPeak[-1]-meaPeak[-1])/meaPeak[-1]])

        meaHour.append(qob.index(meaPeak[-1]))
        simHour.append(res.index(simPeak[-1]))
        hourErr.append([simHour[-1]-meaHour[-1], 0])

    volPassPerc = len([err for err in volErr if abs(err[1])<0.201])/len(volErr)
    peakPassPerc = len([err for err in peakErr if abs(err[1])<0.201])/len(peakErr)
    hourPassPerc = len([err for err in hourErr if abs(err[0])<dt])/len(hourErr)
    avDC = sum(dcVal)/len(dcVal)
    anaFile = os.path.join(srcDir, "result", "analyse.txt")
    with open(anaFile, "w") as out:
        out.write("event\tMeasureVol(10^4m3)\tSimulateVol(10^4m3)\tErr\t "+
                  "DC\t" + "MeasurePeak(m3/s)\tSimulatePeak(m3/s)\tErr\t" +
                  "PeakTimeErr(h)\n")
        for i in range(0, len(events)):
            out.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
                events[i], meaVol[i], simVol[i], volErr[i][1],
                dcVal[i], meaPeak[i], simPeak[i], peakErr[i][1], hourErr[i][0]))
        out.write("PassPercent\t\t\t{}\t{}\t\t\t{}\t{}\n".format(
            volPassPerc, avDC, peakPassPerc, hourPassPerc))

        
if __name__ == "__main__":
    floods = ".\\floods.txt"
    events = get_flood_event(floods)
    draw_events(events)
    #analyse_events(events, 1)
