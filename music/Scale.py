import random

polyphony = 5
channel = 1
noteMin = 36
noteMax = 96
index = 0
microseconds = 0
samplesize = 20
analysize = samplesize - 1
root = 0
channel = 1
samples = [] * samplesize

threshold = 1.7
threshMin = 1.61
threshMax = 3.71
knobMin = 1
knobMax = 1024
root = 0
currScale = 0
scaleLen = 13
scaleCount = 5
polyphony = 5
currentMillis = 1
previousMillis = 0
scale = [
    [12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],    #Chromatic
    [7, 1, 3, 5, 6, 7, 10, 12],     #Major
    [7, 1, 3, 4, 6, 8, 9, 11],      #DiaMinor
    [7, 1, 2, 2, 5, 6, 9, 11],      #Indian
    [7, 1, 3, 4, 6, 8, 9, 11]       #Minor
]

class Message:
    def __init__(typ, val, vel, dur, per, chann):
        this.typ = typ
        this.value = val
        this.velocity = vel
        this.duration = dur
        this.period = per
        this.channel = chann

noteArray = []
controlMessage = None

def scaleSearch(note, scale, scalesize):
    for i in range(scalesize):
        if (note == scale[i]):
            return note
        else:
            if (note < scale[i]):
                return scale[i]
    return random.randint(0, 10)

def scaleNote(note, scale, root):
    scaled = note%12
    octave = note/12
    scalesize = scale[0]

    scaled = scaleSearch(scaled, scale, scalesize)
    scaled = (scaled + (12 * octave)) + root
    return scaled

def sample():
    if (index < samplesize):
        samples[index] = micros() - microseconds
        microseconds = samples[index] + microseconds
        index += 1

def map(x, fl, fh, tl, th):
    fd = fh - fl
    td = th - tl
    return tl + (((x - fl) / fd) * td)

def midiSerial(typ, channel, data1, data2):
    # Note type = 144
    # Control type = 176
    print("output to midi")

def setNote(value, velocity, duration, notechannel):
    for i in range(polyphony):
        if (not noteArray[i].velocity):
            noteArray[i] = new Message(0, value, velocity, currentMillis+duration, notechannel)
            midiSerial(144, channel, value, velocity)
        break

def setControl(type, value, velocity, duration):
    controlMessage = new Message(type, value, velocity, duration)

def checkNote():
    for i in range(polyphony):
        if (noteArray[i].velocity):
            if (noteArray[i].duration <= currentMillis):
                midiSerial(144, channel, noteArray[i].value, 0)
                noteArray[i].velocity = 0


def analyzeSample():
    averag = 0
    maxim = 0
    minim = 100000
    stdevi = 0
    delta = 0
    change = 0

    if (index == samplesize):
        sampanalysis = []
        for i in range (analysize):
            sampanalysis[i] = samples[i+1]
            if (sampanalysis[i] > maxim):
                maxim = sampanalysis[i]
            if (sampanalysis[i]< minim):
                minim = sampanalysis[i]
            averg += sampanalysis[i]
            stdevi += sampanalysis[i] * sampanalysis[i]
        
        averg = averg/analysize
        stdevi = Math.sqrt(stdevi/analysize - averg * averg)
        if (stdevi < 1):
            stdevi = 1.0
        delta = maxim - minim

        if (delta > (stdevi * threshold)):
            change = 1
        
        if change:
            dur = 150 + map(delta%127, 1, 127, 100, 2500)
            ramp = 3 + (dur%100)
            notechannel = random(1,5)

            setnote = map(averag%127, 1, 127, noteMin, noteMax)
            setnote = scaleNote(setnote, scale[currScale], root)

            setNote(setnote, 100, dur, channel)

            setControl(controlNumber, controlMessage.value, delta%127, ramp)
        index = 0
