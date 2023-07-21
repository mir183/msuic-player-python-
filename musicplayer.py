import os
import pygame
import tkinter.filedialog as filedialog
from tkinter import Tk, Button, Label, Listbox, Scrollbar, StringVar, PanedWindow
from PIL import Image, ImageTk
from mutagen.mp3 import MP3

# Initialize Pygame mixer
pygame.mixer.init()

# Global variables
is_playing = False
is_paused = False
total_duration = 0
current_song = None

def select_folder():
    # Function to open a folder selection dialog and load songs from the selected folder.
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path.set(folder_selected)
        select_folder_button.grid_forget()
        load_songs()

def load_songs():
    # Function to load the list of MP3 songs from the selected folder.
    folder = folder_path.get()
    song_list.delete(0, 'end')
    for file in os.listdir(folder):
        if file.endswith('.mp3'):
            song_list.insert('end', file)
    song_list.config(width=20)  # Adjust the width as per your preference

def toggle_play(event=None):
    # Function to toggle between play and pause based on the current state.
    global is_playing, is_paused, paused_position

    if is_playing:
        # Pause the song
        pygame.mixer.music.pause()
        paused_position = pygame.mixer.music.get_pos()
        is_playing = False
        is_paused = True
        play_resume_button.config(image=play_icon)  # Update button image here
    else:
        if is_paused:
            # Resume the song from the paused position
            pygame.mixer.music.unpause()
            pygame.mixer.music.set_pos(paused_position / 1000)  # Set the position in seconds
            is_playing = True
            is_paused = False
            play_resume_button.config(image=pause_icon)  # Update button image here
        else:
            # Play a new song
            play_song()
            is_playing = True
            is_paused = False
            play_resume_button.config(image=pause_icon)  # Update button image here

def play_song():
    # Function to play the selected song.
    global current_song, total_duration, is_playing, is_paused

    is_playing = True
    is_paused = False

    # Get the selected song index
    selected_index = song_list.curselection()

    # Check if a song is selected
    if selected_index:
        selected_song = song_list.get(selected_index)
        song_path = os.path.join(folder_path.get(), selected_song)
        if current_song != song_path:
            pygame.mixer.music.load(song_path)
            current_song = song_path

        # Get the duration of the selected song
        song = MP3(song_path)
        total_duration = song.info.length

        pygame.mixer.music.play()
        play_resume_button.configure(image=pause_icon, command=toggle_play)

def stop_song():
    # Function to stop the currently playing song.
    global is_playing, is_paused

    pygame.mixer.music.stop()
    is_playing = False
    is_paused = False
    play_resume_button.configure(image=play_icon, command=toggle_play)
    progress_label["text"] = "0:00 - 0:00"

def update_progress():
    # Function to update the progress label with the current song's progress.
    if pygame.mixer.music.get_busy():
        current_time = pygame.mixer.music.get_pos() // 1000
        minutes = int(current_time // 60)
        seconds = int(current_time % 60)

        song_length = total_duration
        song_minutes = int(song_length // 60)
        song_seconds = int(song_length % 60)

        progress_label["text"] = f"{minutes:02d}:{seconds:02d} - {song_minutes:02d}:{song_seconds:02d}"
    elif is_playing:
        progress_label["text"] = "0:00 - 0:00"
    else:
        progress_label["text"] = "Paused"

    # If the song has finished playing, play the next song
    if not pygame.mixer.music.get_busy() and is_playing:
        play_next()

    root.after(1000, update_progress)  # Update every 1 second

def select_song(event):
    # Event handler for selecting a song from the list.
    play_song()

def play_next():
    # Function to play the next song in the list or loop back to the first song.
    next_song_index = song_list.curselection()[0] + 1
    if next_song_index >= song_list.size():
        next_song_index = 0  # Loop back to the first song

    song_list.selection_clear(0, 'end')
    song_list.activate(next_song_index)
    song_list.selection_set(next_song_index)
    play_song()

def play_previous():
    # Function to play the previous song in the list or play the last song if the current song is the first one.
    current_song_index = song_list.curselection()
    prev_song_index = current_song_index[0] - 1 if current_song_index else 0

    if prev_song_index < 0:
        prev_song_index = song_list.size() - 1  # Play the last song if the current song is the first one

    song_list.selection_clear(0, 'end')
    song_list.activate(prev_song_index)
    song_list.selection_set(prev_song_index)
    play_song()

# Create the main window
root = Tk()
root.title("Music Player")
root.geometry("330x500")  # Set the window size to 330x500, this size is suitable
root.resizable(False, False)  # Lock the window size, both in width and height

# Folder Selection
folder_path = StringVar()
folder_label = Label(root, textvariable=folder_path)
folder_label.grid(row=0, column=0)

select_folder_button = Button(root, text="Select Folder", command=select_folder)
select_folder_button.grid(row=0, column=1, padx=10, pady=10, sticky="nw")  # Place the button at the top-left corner

# PanedWindow for Song List
song_list_paned = PanedWindow(root, orient="vertical")
song_list_paned.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")
root.rowconfigure(1, weight=1)  # Allocate more space to the song list pane
root.columnconfigure(0, weight=1)  # Allocate more space to the song list pane

# Song List
song_list = Listbox(song_list_paned, selectbackground="gray", selectforeground="white")
song_list.pack(fill="both", expand=True)
song_list_paned.add(song_list)
song_list.bind("<<ListboxSelect>>", select_song)  # Bind the select_song function to the ListboxSelect event

# Scrollbar for Song List
scrollbar = Scrollbar(song_list)
scrollbar.pack(side="right", fill="y")
song_list.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=song_list.yview)

# Load icons before running the application
play_img = Image.open('play.png')
play_img = play_img.resize((50, 50), resample=Image.BICUBIC)
play_icon = ImageTk.PhotoImage(play_img)

pause_img = Image.open('pause.png')
pause_img = pause_img.resize((50, 50), resample=Image.BICUBIC)
pause_icon = ImageTk.PhotoImage(pause_img)

stop_img = Image.open('stop.png')
stop_img = stop_img.resize((50, 50), resample=Image.BICUBIC)
stop_icon = ImageTk.PhotoImage(stop_img)

next_img = Image.open('next.png')
next_img = next_img.resize((50, 50), resample=Image.BICUBIC)
next_icon = ImageTk.PhotoImage(next_img)

prev_img = Image.open('previous.png')
prev_img = prev_img.resize((50, 50), resample=Image.BICUBIC)
prev_icon = ImageTk.PhotoImage(prev_img)

# Play/Resume Button
play_resume_button = Button(root, image=play_icon, command=toggle_play)
play_resume_button.grid(row=2, column=1, padx=10, pady=10)

# Stop Button
stop_button = Button(root, image=stop_icon, command=stop_song)
stop_button.grid(row=2, column=2, padx=10, pady=10)

# Next Button
next_button = Button(root, image=next_icon, command=play_next)
next_button.grid(row=2, column=3, padx=10, pady=10)

# Previous Button
prev_button = Button(root, image=prev_icon, command=play_previous)
prev_button.grid(row=2, column=0, padx=10, pady=10)

# Progress Label
progress_label = Label(root, text="0:00 - 0:00")
progress_label.grid(row=3, column=0, columnspan=5)

# Start the update_progress function
root.after(1000, update_progress)

root.mainloop()
