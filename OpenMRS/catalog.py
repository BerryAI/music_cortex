"""Music catalog: track data management.
"""
from copy import deepcopy


class Track(object):
    """A class that manages data about a single track.
    """

    @classmethod
    def fields(Track):
        return ['id', 'title', 'artist', 'streaming_url']

    def __init__(self, track_data={}, source=None):
        """
        :param track_data: dict. Must include an `id`. Should contain `title`,
            'artist', 'streaming_url', and optionally `cover_photo_url` etc.
        """
        for field in Track.fields():
            assert field in track_data, ('track_data needs to have an "%s"' %
                                         field)
        self.__data = deepcopy(track_data)

    def __str__(self):
        return '{title}, by {artist}'.format(
            title=self['title'], artist=self['artist'])

    @property
    def id(self):
        """Read-only property."""
        return self.__data['id']

    @property
    def title(self):
        return self.__data.get('title')

    @property
    def artist(self):
        return self.__data.get('artist')

    @property
    def streaming_url(self):
        return self.__data.get('streaming_url')

    def __getitem__(self, key):
        return self.__data.get(key)


class Catalog(object):
    """A class that supports looking up a Track object by id.
    """

    def get_track_by_id(self, id):
        """
        Given an id, return a Track object.
        """
        raise NotImplementedError

    def __getitem__(self, id):
        """The [] operator.
        """
        return self.get_track_by_id(id)

    def get_track_ids(self, offset=0, limit=10):
        """
        Return all track ids, with results paginated.
        """
        raise NotImplementedError

    def tracks(self, offset=0, limit=None):
        """
        Return all tracks.
        """
        for track_id in self.get_track_ids(offset, limit):
            yield self[track_id]

    @property
    def name(self):
        return 'catalog'


class SimpleCatalog(Catalog):
    """
    A simple catalog class that stores all tracks as a dictionary in memory.
    To make it scalable to a large collection of tracks in a database or
    retrievable through web service, please implement inherit `Catalog`
    and override `get_track_by_id()`.
    """
    def __init__(self, tracks):
        """
        :param tracks: a list of Track objects or dicts.
        """
        self.__tracks = {}
        for track in tracks:
            if type(track) is dict:
                track = Track(track)
            self.__tracks[track.id] = track

    def get_track_by_id(self, id):
        return self.__tracks.get(id)

    def get_track_ids(self, offset=0, limit=10):
        if limit is None:
            end = None
        else:
            end = offset + limit
        return self.__tracks.keys()[offset:end]

    @property
    def name(self):
        return 'simple catalog'


class AcaiCatalog(Catalog):
    """A catalog that retrieves tracks from ACAI game service.
    """
    pass


class SpotifyCatalog(Catalog):
    """A catalog based on spotify web API using your spotify developer account.
    """
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

    def get_track_by_id(self, id):
        pass
