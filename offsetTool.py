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


def rich(sm, output, noteskin):
    new_attacks = set()
    for attack in sm.attacks:
        chartOffset = sm.params['GLOBALOFFSET'][0]
        new_attacks.add(
            (float(attack[0])+float(chartOffset)-globalOffset, float(attack[1]), noteskin))
    new_attacks = [x for x in new_attacks]
    new_attacks.sort()
    sm.attacks = new_attacks
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
