# 3PlayerCouples
Original script by SpootyBiscuit 

Current usage:

1. copy cybercouples to your noteskin folder (or you can change 3rd player noteskin in `sm.py`)
2. create couples (routine) chart preferably in arrowvortex
3. create doubles chart (for the third player) with the same difficulty as routine
4. run the `rich.py`, it requires python 3
5. enter your globaloffset and set the noteskin for the third player and run

# TODO
- ~~Songs with variable BPM are not supported~~ variable BPMs work now!
- ~~Make the chart automatically  generate from 1 couples chart and 1 doubles chart (instead of relying on the user to copy it)~~
- ~~Convert it to Python 3~~ Done!
- ~~There is too little offset for p3 when there are no p2 notes ~~ Done too!
- ~~a lot more...~~ Maybe 4 player support in the future

# Extra stuff
- you can add multiple difficulties, by creating routine and doubles charts with the same difficulty 
- in `lua` folder, you can find pad change indicators with 3 player support. Originally made by WinDEU
  - Copy it to your song folder 
  - Add `#FGCHANGES:0.000=lua=1.000=0=0=1;` to your .sm file
  - To make managing these easier [here](https://docs.google.com/spreadsheets/d/1keiLYWV12BUKy3XMYToRJ262_lQhTySG4gbHvcclhBw/edit#gid=383139627) you can find a spreadsheet that automatically generates code for them
