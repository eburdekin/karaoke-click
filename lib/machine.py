from models.__init__ import CONN, CURSOR

# from models.queue import Queue
from models.song import Song
from models.singer import Singer
from data.song_library import song_library


class KaraokeMachine:
    def __init__(self):
        self.queue = Queue()

    Song.create_table()
    Song.add_song_library()
    # Queue.create_table()
    Singer.create_table()


# Methods for Queue
def add_song(song_id, singer):
    Singer.create_singer(singer, song_id)
    # Queue.add_song_to_queue(song_id, singer)


def remove_song():
    pass


def load_song():
    print("Loading next song.")


def pause_song():
    pass


def view_queue():
    pass


def view_up_next():
    Singer.view()


# Methods for Songs
def get_all_songs():
    Song.get_all()


def get_songs_by_artist(artist):
    Song.get_by_artist(artist)


def get_songs_by_genre(genre):
    Song.get_by_genre(genre)


def exit_program():
    print("Goodbye!")
    Song.drop_table()
    # Queue.drop_table()
    exit()
