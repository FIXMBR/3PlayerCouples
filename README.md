# 3PlayerCouples
Original script by SpootyBiscuit 

[demo](https://youtu.be/gzuTTFQaElw)

# Warning
There is an issue with this method. It depends on your globalOffset, so anyone who wants to play your chart would have to convert it themselves

# Current usage:

[Downloads](https://github.com/FIXMBR/3PlayerCouples/releases/)

1. copy couplesp3 to your noteskin folder (or you can change 3rd player noteskin in the UI)
2. create couples (routine) chart preferably in arrowvortex
3. create doubles chart (for the third player) with the same difficulty as routine
  - backup your sm file before conversion, any file specified as an output will be overwritten, and your original - "source" charts will be lost
4. run `triples.exe` or`rich.py` - it requires python 3
5. enter your globaloffset and set the noteskin for the third player and run
6. make sure the output file is the only .sm file in song folder, also you probably need to restart nITG

# TODO
- ~~Songs with variable BPM are not supported~~ variable BPMs work now!
- ~~Make the chart automatically  generate from 1 couples chart and 1 doubles chart (instead of relying on the user to copy it)~~
- ~~Convert it to Python 3~~ Done!
- ~~There is too little offset for p3 when there are no p2 notes~~ Done too!
- ~~a lot more...~~ Maybe 4 player support in the future

# Extra stuff
- you can add multiple difficulties, by creating routine and doubles charts with the same difficulty 
- in `lua` folder, you can find pad change indicators with 3 player and multiple difficulties support. Originally made by WinDEU
  - Copy it to your song folder 
  - Add `#FGCHANGES:0.000=lua=1.000=0=0=1;` to your .sm file
  - To make managing these easier [here](https://docs.google.com/spreadsheets/d/1keiLYWV12BUKy3XMYToRJ262_lQhTySG4gbHvcclhBw/edit#gid=383139627) you can find a spreadsheet that automatically generates code for them
  - paste generated code into your desired difficulty
