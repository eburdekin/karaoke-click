from models.song import Song
from models.singer import Singer
from data.song_library import song_library


class KaraokeMachine:
    def __init__(self):
        self.queue = queue


# Methods for Queue
def add_song(song_id, singer_name):
    Singer.create_singer(singer_name, song_id)
    singer_id = Singer.get_singer_id(singer_name)
    Song.update_singer_id(song_id, singer_id)


def remove_song(singer_name):
    singer_id = Singer.get_singer_id(singer_name)
    song_id = Song.get_song_id(singer_id)
    Song.remove_singer_id(song_id)
    Singer.remove_singer_by_name(singer_name)


def load_song():
    Song.load_next_song()


def view_queue():
    Song.get_queued()


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


def remove_new(song_id):
    Song.remove_song_from_library(song_id)


def exit_program():
    print("Goodbye!")
    exit()
