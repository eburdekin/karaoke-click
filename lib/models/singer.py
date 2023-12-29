class Singer:
    all = {}

    def __init__(self, name, id=None):
        self.id = id
        self.name = name
        self.songs = songs(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name) > 0:
            self._name = name

    def songs(self):
        return [song for song in Song.all if song.singer is self]
