from sm import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter as tk
from tkinter import Tk
import sys
import os
import copy
noteSkin = "couplesp3"
globalOffset = -0.030


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


def rich(sm, output, noteskin):
    # KURNA OFFSET JAK JA GO NIE NAWIDZeKURNA OFFSET JAK JA GO NIE NAWIDZEKURNA OFFSET JAK JA GO NIE NAWIDZEKURNA OFFSET JAK JA GO NIE NAWIDZE
    noteSkinOffset = 0.001
    thirdPlayerOffset = 0.003
    attackTime = 0.005
    # KURNA OFFSET JAK JA GO NIE NAWIDZEKURNA OFFSET JAK JA GO NIE NAWIDZEKURNA OFFSET JAK JA GO NIE NAWIDZEKURNA OFFSET JAK JA GO NIE NAWIDZE

    bpms = sm.bpms
    stops = dict(sm.stops)

    couples = [[], [], [], [], [], []]
    couples2 = []

    thirdPlayerNotes = [[], [], [], [], [], []]

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

    # TODO: I could add a check for 64ths/192nds and print a warning...

    couples = copy.deepcopy(couples2)

    new_stops = set()
    new_attacks = set()

    for notes in couples:
        reds = notes.layers[0]
        blues = []
        yellows = []

        # print(notes.layers[2])
        # print(sm.bpms[0][1])
        # print(sm.offset)
        # We want to add a stop gimmick wherever there is a blue note in any routine chart
        for b, n in notes.layers[1]:
            new_stops.add(b)
            blues.append((b+1.0/48, n))
        for b, n in notes.layers[2]:
            # TODO changing BPMs
            global globalOffset
            new_stops.add(b)
            new_stops.add(b+1.0/48)
            new_attacks.add(
                (calcBPM(b, sm.bpms) - sm.offset + noteSkinOffset - globalOffset, attackTime, noteskin))
            yellows.append((b+2.0/48, n))

        # print(new_attacks)

        # print(reds)
        # print(blues)
        # print(yellows)

        combined = []

        yi = ri = bi = 0  # Combine the red and blue layers
        while ri < len(reds) or bi < len(blues) or yi < len(yellows):
            if ri < len(reds) and bi < len(blues) and yi < len(yellows):
                if reds[ri][0] <= blues[bi][0]:
                    if reds[ri][0] <= yellows[yi][0]:
                        combined.append(reds[ri])
                        ri += 1
                    else:
                        combined.append(yellows[yi])
                        yi += 1
                else:
                    if blues[bi][0] <= yellows[yi][0]:
                        combined.append(blues[bi])
                        bi += 1
                    else:
                        combined.append(yellows[yi])
                        yi += 1
            elif ri < len(reds) and bi < len(blues):
                if reds[ri][0] <= blues[bi][0]:
                    combined.append(reds[ri])
                    ri += 1
                else:
                    combined.append(blues[bi])
                    bi += 1
            elif yi < len(yellows) and bi < len(blues):
                if yellows[yi][0] <= blues[bi][0]:
                    combined.append(yellows[yi])
                    yi += 1
                else:
                    combined.append(blues[bi])
                    bi += 1
            elif yi < len(yellows) and ri < len(reds):
                if yellows[yi][0] <= reds[ri][0]:
                    combined.append(yellows[yi])
                    yi += 1
                else:
                    combined.append(reds[ri])
                    ri += 1
            elif ri < len(reds):
                combined.append(reds[ri])
                ri += 1
            elif bi < len(blues):
                combined.append(blues[bi])
                bi += 1
            else:
                combined.append(yellows[yi])
                yi += 1

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

        nb = round(beat+1.0/48, 3)  # Beat plus one 192nd

        s = 60.0/curbpm/48+0.0005  # Time between 192nd notes
        ns = stops.get(beat, 0)
        ns += stops.get(nb, 0)
        ns += s
        ns = round(ns, 3)          # New stop value one 192nd down
        s = round(s, 3)

        stops.update([(beat, -s), (nb, ns)])

    stops = [x for x in list(stops.items())]
    stops.sort()

    filteredStops = []
    lastWasWarp = False
    lastValue = 0.0
    removeNext = False
    doubleNext = False
    for i in stops:
        if removeNext:

            removeNext = False
            doubleNext = True
        elif doubleNext:
            doubleNext = False
            filteredStops.append((i[0], (i[1]-lastValue)))
        else:
            if lastWasWarp:
                if i[1] < 0:
                    filteredStops.append((i[0], i[1]+thirdPlayerOffset))
                    lastValue = i[1]+thirdPlayerOffset
                else:
                    filteredStops.append(i)
            else:
                filteredStops.append(i)

        if lastWasWarp:
            if i[1] < 0:
                removeNext = True
                lastWasWarp = False
            else:
                lastWasWarp = False

        elif i[1] < 0:
            lastWasWarp = True
        else:
            lastWasWarp = False
        # print i

    sm.stops = filteredStops
    sm.attacks = new_attacks
    sm.notes = couples
    open(output, "wb").write(sm.barf("\r\n", 1, noteskin, globalOffset).encode())

    print('Conversion Done!')


fields = ['offset', '-0.030'], ['noteskin', 'couplesp3']


def fetch(entries):
    for entry in entries:
        field = entry[0]
        text = entry[1].get()
        print(('%s: "%s"' % (field, text)))
        if field[0] == 'offset':
            global globalOffset
            globalOffset = float(entry[1].get())
        elif field[0] == 'noteskin':
            global noteSkin
            noteSkin = entry[1].get()

    input = askopenfilename(filetypes=[("sm files", "*.sm")])
    output = asksaveasfilename(
        filetypes=[("sm files", "*.sm")], initialfile=[('output.sm')])

    try:
        sm_raw = open(input, "rb").read()
    except:
        peace("Error:  Cannot open %s" % input)

    sm = SM(input)
    rich(sm, output, noteSkin)


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
    b1 = tk.Button(root, text='Run', command=(lambda e=ents: fetch(e)))
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
