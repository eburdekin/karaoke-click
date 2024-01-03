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
    # NEED TO FIX IT SO SONG'S SINGER_ID IS CHECKED BEFORE THE SINGER IS ADDED TO SINGER LIST
    Singer.create_singer(singer_name, song_id)
    singer_id = Singer.get_singer_id(singer_name)
    Song.update_singer_id(song_id, singer_id)


def remove_song(singer_name):
    Singer.remove_singer_by_name(singer_name)
    # add methods to remove singer ID from song


def load_song():
    Song.load_next_song()


def pause_song():
    print("Pausing song.")


def view_queue():
    Song.get_queued()


def view_up_next():
    Singer.view()


# Methods for Songs
def view_all_songs():
    Song.get_all()


def get_songs_by_title(title):
    Song.get_by_title(title)


def get_songs_by_artist(artist):
    Song.get_by_artist(artist)


def get_songs_by_genre(genre):
    Song.get_by_genre(genre)


def add_new(title, artist, genre, lyrics):
    Song.add_new_song_to_library(title, artist, genre, lyrics)


def exit_program():
    print("Goodbye!")
    Song.drop_table()
    Singer.drop_table()
    exit()
