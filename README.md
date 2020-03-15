# 3PlayerCouples
Original script by SpootyBiscuit 

Current usage:

- copy cybercouples to your noteskin folder (or you can change 3rd player noteskin in `sm.py`)
- create couples chart
- create doubles chart (for the third player)
- in your .sm file find and copy notes from your 3rd player chart
```
//--------------- dance-double - 3rdplayer ----------------
#NOTES:
     dance-double:
     3rdplayer:
     Beginner:
     1:
     0,0,0,0,0:
00000000        <----- COPY FROM HERE
00000000
00000000
00000000
,
00000000
.
.
.
00200020
00000000
00300030
00000000
;               <----- TIL END OF THE CHART
```
- now find the end of your couples chart
```
00200020
00000000
00300030
00000000
;
```
- replace the semicolon with `&` and paste your chart after it
```
00200020
00000000
00300030
00000000
&
00000000
00000000
00002002
00000000
```
- make sure that the chart ends with a semicolon
- ~~set your offset in `rich.py` file (in your offset is -0.030 enter 0.030)~~

- run the `rich.py`, it requires python 2 and some dependencies or something.
- set your offset and noteskin for the third player

# TODO
- Songs with variable BPM are not supported
- Make the chart automatically  generate from 1 couples chart and 1 doubles chart (instead of relying on the user to copy it)
- Convert it to Python 3
- a lot more
