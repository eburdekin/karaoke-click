from models.song import Song
from models.singer import Singer
from data.song_library import song_library


class KaraokeMachine:
    def __init__(self):
        self.queue = queue

    Song.create_table()
    Song.add_song_library()
    Singer.create_table()


# Methods for Queue
def add_song(song_id, singer_name):
    Singer.create_singer(singer_name, song_id)
    singer_id = Singer.get_singer_id(singer_name)
    Song.update_singer_id(song_id, singer_id)


def remove_song():
    pass


def load_song():
    print("Loading next song.")


def pause_song():
    pass


def view_queue():
    Song.get_queued()


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
