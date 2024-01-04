# Helper functions for cli.py, accessing Song/Singer classes

from models.song import Song
from models.singer import Singer
from data.song_library import song_library

# Your Playlist


def add_song_to_playlist(song_id, singer_name):
    Singer.create_singer(singer_name, song_id)
    singer_id = Singer.get_singer_id(singer_name)
    Song.update_singer_id(song_id, singer_id)


def remove_song_from_playlist(singer_name):
    singer_id = Singer.get_singer_id(singer_name)
    song_id = Song.get_song_id(singer_id)
    Song.remove_singer_id(song_id)
    Singer.remove_singer_by_name(singer_name)


def load_song():
    Song.load_next_song()


def view_all_playlist():
    Song.get_all_playlist()


# Song Library


def view_all_library():
    Song.get_all_library()


def view_library_by_title(title):
    Song.get_library_by_title(title)


def view_library_by_artist(artist):
    Song.get_library_by_artist(artist)


def view_library_by_genre(genre):
    Song.get_library_by_genre(genre)


def view_library_by_id(_id):
    Song.get_library_by_id(_id)


def add_song_to_library(title, artist, genre, lyrics):
    Song.add_to_library(title, artist, genre, lyrics)


def remove_song_from_library(song_id):
    Song.remove_from_library(song_id)


# Exit


def exit_program():
    print("Goodbye!")
    exit()
