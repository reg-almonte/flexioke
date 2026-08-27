1. Add a functionality to add "lyrics" to a song - add a button preferably to the Song Library songs, similar to "Play" and "+Queue" button. If the buttons seem to be too crowded, make a UI decision on your own to solve it.
2. The add lyrics will open a text field where the user can past the lyrics with time stamp, and a save button that will save the content as a text file (if a special extension is known for lyrics with timestamp, use it).
The expected format of the lyrics/timestamp is like this:
```text
[00:00.18] If I could be anybody, I would be you
[00:05.17] Maybe I'd understand the things that you do
[00:09.85] Stuck at a costume party, dressed in your shoes
```

3. Add a new separate page/tab for the karaoke player.
4. The karaoke page contains:
a. The Song Library, where user can search and queue or play a song. When play button is pressed while a song is currently playing, pause the music, warn the user that it will stop the current song. if he proceeds, the queued songs will remain, the new song will be played first.
b. The screen that displays the Lyrics associated to the song, synced to the music like a real karaoke. If there is no lyrics, simply display a message while still playing: 'No lyrics. You may upload in the upload page' or something like that. If there is a lyrics file with missing time stamp, simply display the lyrics with scroll bar.
c. The player contains Play/Pause, Skip to Next, Mute/Unmute Lead Vocals, Mute/Unmute Backing Vocals
d. The Playback Queue similar to version 1

If there are gaps, ask me during requirement refinement.