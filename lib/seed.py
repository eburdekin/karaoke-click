from models.song import Song

Song.drop_table()
Song.create_table()
Song.add_song_library()
