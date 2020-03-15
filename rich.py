import os
import sys
from Tkinter import Tk
from tkFileDialog import askopenfilename, asksaveasfilename
from sm import *



def pause(str="<Press enter to peace out>"):
    raw_input(str)


def peace(str):
    print str
    # pause()
    exit(0)


def usage():
    print "*** Usage: %s input.sm [output.sm] ***"
    print "(If no argument is given, output will be input-couples.sm)"
    # pause()
    exit(0)


def rich(sm, output):
    ##KURNA OFFSET JAK JA GO NIE NAWIDZeKURNA OFFSET JAK JA GO NIE NAWIDZEKURNA OFFSET JAK JA GO NIE NAWIDZEKURNA OFFSET JAK JA GO NIE NAWIDZE
    #globalOfset = 0.024
    globalOfset = 0.030
    noteSkinOffset = 0.001
    thirdPlayerOffset = 0.003
    attackTime = 0.010
    ##KURNA OFFSET JAK JA GO NIE NAWIDZEKURNA OFFSET JAK JA GO NIE NAWIDZEKURNA OFFSET JAK JA GO NIE NAWIDZEKURNA OFFSET JAK JA GO NIE NAWIDZE

    bpms = sm.bpms
    stops = dict(sm.stops)

    couples = []
    couples3 = []
    for notes in sm.notes:
        if notes.type == "dance-routine" and len(notes.layers) == 2:
            notes.type = "dance-double"
            couples.append(notes)
        if notes.type == "dance-routine" and len(notes.layers) == 3:
            notes.type = "dance-double"
            couples3.append(notes)
    if couples3 != []:
        print "we doing some coll 3 player couples owo"
    else:
        if couples == []:
            peace(
                "Error: There were no valid dance-routine charts found in the input file!")

    # TODO: I could add a check for 64ths/192nds and print a warning...

    import copy
    couples = copy.deepcopy(couples3)

    new_stops = set()
    new_attacks = set()
    for notes in couples:
        reds = notes.layers[0]
        blues = []
        yellows = []

        print notes.layers[2]
        print sm.bpms[0][1]
        print sm.offset
        # We want to add a stop gimmick wherever there is a blue note in any routine chart
        for b, n in notes.layers[1]:
            new_stops.add(b)
            blues.append((b+1.0/48, n))
        for b, n in notes.layers[2]:
			# TODO changing BPMs
            new_stops.add(b+1.0/48)
            new_attacks.add((b/(sm.bpms[0][1]/60) - sm.offset +noteSkinOffset +globalOfset,attackTime))
            yellows.append((b+2.0/48, n))

        print new_attacks

        print reds
        print blues
        print yellows

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
				yi +=1 
			
        notes.layers = [combined]

    new_stops = [x for x in new_stops]
    new_stops.sort()
    print new_stops
    new_attacks = [x for x in new_attacks]
    new_attacks.sort()
    print new_attacks

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

    stops = [x for x in stops.items()]
    stops.sort()
    

    filteredStops = []
    lastWasWarp = False
    lastValue = 0.0
    removeNext = False
    doubleNext = False
    for i in stops:
        if removeNext:

            removeNext=False
            doubleNext = True
        elif doubleNext:
            doubleNext = False
            filteredStops.append((i[0],(i[1]-lastValue)))
        else:
            if lastWasWarp: 
                if i[1]<0:
                    filteredStops.append((i[0],i[1]+thirdPlayerOffset))
                    lastValue = i[1]+thirdPlayerOffset
                else:
                    filteredStops.append(i)
            else:
                filteredStops.append(i)

        if lastWasWarp:
            if i[1]<0:
                print '2 warpy owowowo'
                removeNext = True
                lastWasWarp = False
            else:
                lastWasWarp = False
            
        elif i[1]<0:
            lastWasWarp = True
        else:
            lastWasWarp = False
        # print i

    print "STOOOPKI TUTAJ: "
    print stops

    print "STOOOPKI2 TUTAJ: "
    print filteredStops

    sm.stops = filteredStops
    sm.attacks = new_attacks
    sm.notes = couples

    open(output, "wb").write(sm.barf("\r\n", 1))


if __name__ == "__main__":
    #Tk().withdraw()
#	if len(sys.argv) <= 1:
#		usage()
    input = askopenfilename(filetypes=[("sm files", "*.sm")])
    output = asksaveasfilename(
        filetypes=[("sm files", "*.sm")], initialfile=[('output.sm')])
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

    try:
        sm_raw = open(input, "rb").read()
    except:
        peace("Error:  Cannot open %s" % input)

    sm = SM(input)
    rich(sm, output)
    # open("asdf.txt", "wb").write(sm.barf("\r\n", 0))
    # print sm.barf("\r\n", 0)

			