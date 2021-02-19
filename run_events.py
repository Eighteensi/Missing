# -*- coding:utf-8 -*-


import os



def get_events_id(floodsFile):
    '''Get flood events from 'floods.txt'.
    '''
    events = []
    with open(floodsFile, "r") as floods:
        events = [event.strip() for event in floods if event.strip()]
    return events


def run_events(events, srcDir=".\\"):
    '''Run hydrology events.
    '''
    exe = os.path.abspath(r".\\grdhm\\launcher.exe")
    dll = "grdhm"
    task = r".\\{}\\task.txt"
    params = "{} {} {}"
    for event in events:
        print(event, "runing...", end="\t")
        curTask = os.path.abspath(task.format(event))
        param = params.format(*[exe, dll, curTask])
        state = os.system(param)
        if not state:
            print("done")
        else:
            print("failed.")


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
    if not os.path.exists(os.path.join(srcDir, "result")):
        os.mkdir(os.path.join(srcDir, "result"))
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
    events = get_events_id(".\\floods.txt")
    run_events(events)
    analyse_events(events,1)
