from models.song import Song
from models.singer import Singer

Singer.drop_table()
Singer.create_table()
Song.drop_table()
Song.create_table()
Song.add_song_library()
