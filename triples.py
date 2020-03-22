from sm import *
from sm_xml import XML
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter as tk
from tkinter import Tk
import sys
import os
import copy
import math  
noteSkin = "couplesp3"
noteSkin2 = "couplesp4"


def pause(str="<Press enter to peace out>"):
    input(str)


def peace(str):
    print(str)
    # pause()
    exit(0)


def usage():
    print("*** Usage: %s input.sm [output.sm] ***")
    print("(If no argument is given, output will be input-couples.sm)")
    # pause()
    exit(0)


def calcBPM(beat, bpms):
    time = 0
    currentBeat = 0
    for i in range(len(bpms)):
        if i+1 >= len(bpms):
            time += (beat-currentBeat)/(bpms[i][1]/60)
            return time
        else:
            if beat > bpms[i+1][0]:
                time += (bpms[i+1][0]-currentBeat)/(bpms[i][1]/60)
                currentBeat = bpms[i+1][0]
            else:
                time += (beat-currentBeat)/(bpms[i][1]/60)
                return time


def fancyWithXML(sm, output, noteskin, xml, xmlfile, fourPlayers, noteskin2):
    # KURNA OFFSET JAK JA GO NIE NAWIDZeKURNA OFFSET JAK JA GO NIE NAWIDZEKURNA OFFSET JAK JA GO NIE NAWIDZEKURNA OFFSET JAK JA GO NIE NAWIDZE
    noteSkinOffset = -0.002
    thirdPlayerOffset = 0.003
    attackTime = 0.002
    # KURNA OFFSET JAK JA GO NIE NAWIDZEKURNA OFFSET JAK JA GO NIE NAWIDZEKURNA OFFSET JAK JA GO NIE NAWIDZEKURNA OFFSET JAK JA GO NIE NAWIDZE

    bpms = sm.bpms
    stops = dict(sm.stops)

    couples = [[], [], [], [], [], []]
    couples2 = []
    fourPlayerCouples = {}

    thirdPlayerNotes = [[], [], [], [], [], []]
    if(fourPlayers == 0):
        for notes in sm.notes:
            if notes.type == "dance-double":
                if notes.difficulty == 'Beginner':
                    thirdPlayerNotes[0] = notes
                elif notes.difficulty == 'Easy':
                    thirdPlayerNotes[1] = notes
                elif notes.difficulty == 'Medium':
                    thirdPlayerNotes[2] = notes
                elif notes.difficulty == 'Hard':
                    thirdPlayerNotes[3] = notes
                elif notes.difficulty == 'Challenge':
                    thirdPlayerNotes[4] = notes
                else:
                    thirdPlayerNotes[5] = notes
            if notes.type == "dance-routine" and len(notes.layers) == 2:
                notes.type = "dance-double"
                if notes.difficulty == 'Beginner':
                    couples[0] = notes
                elif notes.difficulty == 'Easy':
                    couples[1] = notes
                elif notes.difficulty == 'Medium':
                    couples[2] = notes
                elif notes.difficulty == 'Hard':
                    couples[3] = notes
                elif notes.difficulty == 'Challenge':
                    couples[4] = notes
                else:
                    couples[5] = notes
        if thirdPlayerNotes != []:
            print("combining doubles chart with routine")

            for i in range(len(couples)):
                if(couples[i] != []):
                    couples[i].layers.append(thirdPlayerNotes[i].notes)
                    couples2.append(couples[i])
        else:
            if couples == []:
                peace(
                    "Error: There were no valid dance-routine charts found in the input file!")
        couples = copy.deepcopy(couples2)
    else:
        for notes in sm.notes:
            if notes.type == "dance-routine" and len(notes.layers) == 2:
                notes.type = "dance-double"
                if notes.name in fourPlayerCouples:
                    fourPlayerCouples[notes.name].layers.append(
                        notes.layers[0])
                    fourPlayerCouples[notes.name].layers.append(
                        notes.layers[1])
                else:
                    fourPlayerCouples[notes.name] = notes
        # couples = copy.deepcopy(fourPlayerCouples)
        couples = []
        for key, value in fourPlayerCouples.items():
            couples.append(value)

    new_stops = set()
    new_attacks = set()

    for notes in couples:
        # if(fourPlayers==1):
        #     notes = couples[notes]
        reds = notes.layers[0]
        blues = []
        yellows = []
        fourths = []

        # print(notes.layers[2])
        # print(sm.bpms[0][1])
        # print(sm.offset)
        # We want to add a stop gimmick wherever there is a blue note in any routine chart
        for b, n in notes.layers[1]:
            new_stops.add(b)
            blues.append((b+1.0/48, n))
        for b, n in notes.layers[2]:
            # TODO changing BPMs
            new_stops.add(b)
            new_stops.add(b+1.0/48)
            print(calcBPM(b, sm.bpms) - sm.offset)
            new_attacks.add(
                (calcBPM(b, sm.bpms) - sm.offset + thirdPlayerOffset  + noteSkinOffset, attackTime, noteskin)) # TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO 
            yellows.append((b+2.0/48, n))
        if(fourPlayers == 1):
            for b, n in notes.layers[3]:
                # TODO changing BPMs
                new_stops.add(b)
                new_stops.add(b+1.0/48)
                new_stops.add(b+2.0/48)
                print(calcBPM(b, sm.bpms) - sm.offset)
                new_attacks.add(
                    (calcBPM(b, sm.bpms) - sm.offset + thirdPlayerOffset*2 + noteSkinOffset, attackTime, noteskin2)) # TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO 
                fourths.append((b+3.0/48, n))

        # print(new_attacks)

        # print(reds)
        # print(blues)
        # print(yellows)

        combined = []

        combined = sorted(reds+blues+yellows+fourths, key=lambda l: l[0])

        notes.layers = [combined]

    new_stops = [x for x in new_stops]
    new_stops.sort()
    # print(new_stops)
    new_attacks = [x for x in new_attacks]
    new_attacks.sort()
    # print(new_attacks)

    bi = 1
    curbpm = bpms[0][1]
    for beat in new_stops:
        # Determine curbpm for the stop at "beat"
        while bi < len(bpms) and beat >= bpms[bi][0]:
            curbpm = bpms[bi][1]
            bi += 1

        nb = beat+1.0/48  # Beat plus one 192nd

        s = 60.0/curbpm/48+0.0005  # Time between 192nd notes
        ns = stops.get(beat, 0)
        ns += stops.get(nb, 0)
        ns += s
        ns =  ns   # New stop value one 192nd down
        s = s

        stops.update([(beat, -s), (nb, ns)])

    stops = [x for x in list(stops.items())]
    stops.sort()

    filteredStops = []

    
    currentBeat = 0
    for stop in stops:
        if(stop[0] > currentBeat):
            currentBeat = stop[0]
            searchForWarps = []
            lastStop = []
            for stop in stops:
                if stop[0] >= currentBeat and stop[0] < currentBeat+0.063:
                    if (stop[1] < 0):
                        searchForWarps.append(stop)
                    else:
                        lastStop = stop
            currentBeat = lastStop[0]
            toCompensate = 0.0
            i = False
            for warp in searchForWarps:
                if i:
                    filteredStops.append(
                        (warp[0], warp[1]+thirdPlayerOffset))
                    toCompensate += warp[1]+thirdPlayerOffset
                else:
                    filteredStops.append((warp[0], warp[1]))
                    toCompensate += warp[1]
                i = True
            filteredStops.append((lastStop[0], -toCompensate))

    sm.stops = filteredStops
    xml.attacks = new_attacks
    sm.notes = couples

    open(output, "wb").write(sm.barf("\r\n", 1, noteskin).encode())
    open(xmlfile, "wb").write(xml.barf("\r\n", 1, noteskin).encode())

    print('Conversion Done!')


fields = [['noteskin', 'couplesp3'], ['noteskin2', 'couplesp4']]


def fetch(entries, fourPlayers):
    for entry in entries:
        field = entry[0]
        text = entry[1].get()
        print(('%s: "%s"' % (field, text)))
        if field[0] == 'noteskin':
            global noteSkin
            noteSkin = entry[1].get()
        if field[0] == 'noteskin2':
            global noteSkin2
            noteSkin2 = entry[1].get()

    input = askopenfilename(filetypes=[("sm files", "*.sm")])
    xmlfile = askopenfilename(
        filetypes=[("xml files", "*.xml")], initialfile=[('default.xml')])
    output = asksaveasfilename(
        filetypes=[("sm files", "*.sm")], initialfile=[('output.sm')])

    try:
        sm_raw = open(input, "rb").read()
    except:
        peace("Error:  Cannot open %s" % input)

    sm = SM(input)
    xml = XML(xmlfile)
    fancyWithXML(sm, output, noteSkin, xml, xmlfile,
                 fourPlayers.get(), noteSkin2)
    # rich(sm, output, noteSkin)


def makeform(root, fields):
    entries = []
    for field in fields:
        row = tk.Frame(root)
        lab = tk.Label(row, width=15, text=field[0], anchor='w')
        v = tk.StringVar(root, value=field[1])
        ent = tk.Entry(row, textvariable=v)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries.append((field, ent))

    return entries


if __name__ == "__main__":
    # Tk().withdraw()
    #	if len(sys.argv) <= 1:
    #		usage()

    root = tk.Tk()
    ents = makeform(root, fields)
    root.bind('<Return>', (lambda event, e=ents: fetch(e)))
    fourPlayers = tk.IntVar()
    checkBoxer = tk.Checkbutton(
        root, text="4players", variable=fourPlayers, onvalue=1, offvalue=0)
    checkBoxer.pack(side=tk.LEFT, padx=5, pady=5)
    b1 = tk.Button(root, text='Run', command=(
        lambda e=ents, a=fourPlayers: fetch(e, a)))
    b1.pack(side=tk.LEFT, padx=5, pady=5)
    b2 = tk.Button(root, text='Quit', command=root.quit)
    b2.pack(side=tk.LEFT, padx=5, pady=5)
    root.mainloop()


#	if len(sys.argv) == 2:
#		if input.lower().endswith(".sm"):
#			output = input[:-3] + "-couples" + input[-3:]
#		else:
#			i = input.rfind(".")
#			if i == -1:
#				output = input + "-couples.sm"
#			else:
#				output = input[:i] + "-couples.sm"
#	else:
#		output = sys.argv[2]

#	if os.path.exists(output):
#		peace("Error:  Output file %s already exists!" % output)

#	if not os.path.exists(input):
#		peace("Error:  Input file %s does not exist!" % input)

    # open("asdf.txt", "wb").write(sm.barf("\r\n", 0))
    # print sm.barf("\r\n", 0)
