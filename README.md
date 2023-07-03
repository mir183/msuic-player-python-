# Music Player Program (python)

This is a simple music player application implemented in Python using the `pygame` library for audio playback and the `tkinter` library for the user interface. It allows you to select a folder containing MP3 files and play them one by one.

## Requirements
- Python 3.11
- pygame library
- tkinter library
- mutagen library (for reading MP3 file metadata)
- PIL (Python Imaging Library) for working with images
- A folder containing all MP3 songs

## Setup and Usage
1. Install the required libraries:
(`pip install pygame`)
(`pip install tkinter`)
(`pip install mutagen`)
(`pip install Pillow`)
2. Place the Python script in a directory along with your music files (MP3 format) and all pngs with it.
3. Run the Python script `musicplayer.py`.
4. A window will open showing the current directory. Click on the "Select Folder" button to choose the directory containing your MP3 files.
5. Once the folder is selected, the list of MP3 files in that folder will be displayed in the listbox.
6. To play a song, select it from the list and click the "Play/Resume" button. The selected song will start playing.
7. While a song is playing, you can pause it by clicking the "Play/Resume" button again. Clicking it again will resume the playback.
8. The "Stop" button stops the currently playing song.
9. The "Next" and "Previous" buttons allow you to navigate to the next or previous song in the list and play it.
10. The progress label at the bottom displays the current position and the total duration of the currently playing song.
11. The player will automatically play the next song in the list once the current song finishes playing.

## Icons
The player uses custom icons for the buttons. You can replace the icon images (`play.png`, `pause.png`, `stop.png`, `next.png`, and `previous.png`) with your own icons of the same dimensions (50x50 pixels) if you wish to change the appearance. I had also provided the icons in my repo.

## Note
- The player uses `pygame.mixer.music` for audio playback, which means it can only play one song at a time.
- The player should handle most common MP3 files, but it might not support some less common or unusual formats.

## Known Issues
- If there are other MP3 files in the selected folder that are not listed in the player, they will not be playable using the player's controls. Only the MP3 files listed in the player can be played.
- The player's GUI may not handle very large song lists gracefully.
- Please note that I did this project alone, which means there might be several bugs! Pardon them; I will try to review the code later and add more functionality.

## Contributing
Contributions to this project are welcome. If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request on the project's GitHub repository.

Enjoy your music with the simple Python Music Player! If you have any questions or feedback, feel free to reach out to the developer<3.
