from models.__init__ import CONN, CURSOR
from models.queue import Queue
from models.song import Song
from data.song_library import song_library


class KaraokeMachine:
    def __init__(self):
        self.queue = Queue()

    Song.create_table()
    Song.add_song_library()


def add_song():
    print("Adding song.")


def remove_song():
    pass


def load_song():
    print("Loading next song.")


def pause_song():
    pass


def get_all_songs():
    Song.get_all()


def exit_program():
    print("Goodbye!")
    exit()
