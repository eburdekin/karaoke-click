from models.playlist import Playlist
from models.song import Song
from data.default_songs import default_songs


class KaraokeMachine:
    def __init__(self):
        self.playlist = Playlist()


def add_song():
    print("Adding song.")


def load_song():
    print("Loading next song.")


def exit_program():
    print("Goodbye!")
    exit()
