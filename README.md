# constellatia
Constellatia is a simple audio visualizer built in Python.

You'll need to install 
<a href="https://www.pygame.org/wiki/GettingStarted">pygame</a> and 
<a href="http://pydub.com/">pydub</a>
in order for the visualizer to run.

## How to use
Simply run ``` python main.py ``` in the constellatia directory to start the visualizer.
You can determine what audio is played/visualized by setting ```FILENAME``` to the path to an audio file.
Currently, it runs immediately after processing, and will automatically stop after playing through the song.

This repo comes with some songs in the ```audio``` folder:
- <a href="https://www.youtube.com/watch?v=b6D6iGeEl1o">Deep Blue by The Midnight</a>
- <a href="https://www.youtube.com/watch?v=cnpqLWBrNw0">Missing by Orax</a>
- <a href="https://www.youtube.com/watch?v=9wCJPm19XYQ">Reckoner by Radiohead</a>
- <a href="https://www.youtube.com/watch?v=lpbJJmOJLz8">Something Memorable by Kn1ght</a>
- <a href="https://www.youtube.com/watch?v=VTJcLE_VVX8">They Might As Well Be Dead by Chris Christodoulou</a> 

as well as two test files, one of a sine wave and one of a square wave.

You can configure the visualizer before running by editing the config variables at the top of the file.

**note**: ```WINDOW_SIZE``` refers to the number of samples that are processed at a time (in other words, how many dots make up the wavy stuff),
NOT the size of the visualizer - ```SCREEN_WIDTH``` and ```SCREEN_HEIGHT``` determine that.
Controls:
- p: pause/unpause the visualizer and music
- q: prematurely end the visualizer
- r: start/stop recording

I **HIGHLY** discourage recording right now, since the current setup is super janky and I'm still working on it.
It will absolutely destroy your memory if you record for more than ~40 seconds.
However, if you do want to record, make sure the ```imgs``` folder is empty; otherwise, frames from previous recordings might get mixed in.
You can start recording right away by setting ```RECORDING = True```, or press r to toggle recordings as you like.
