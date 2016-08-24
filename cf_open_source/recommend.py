"""Recommend API.
"""
import numpy as np
import random
from catalog import SimpleCatalog

# TODO: implement classes: UserTasteModel.


class RecommendationEngine(object):

    def __init__(self, catalog=SimpleCatalog()):
        self.__catalog = catalog

    def train(self, ratings):
        raise NotImplementedError

    def train_partial(self, ratings):
        """The incremental training of models.
        """
        raise NotImplementedError

    def recommend(self, user_id=None, seed_track_ids=None):
        raise NotImplementedError

    def get_users(self, num=10):
        raise NotImplementedError

    def get_tracks(self, num=10):
        raise NotImplementedError


def predict_rating(user_taste_model, track):
    """
    :return rating: an integer from 1 to 5.
    """
    fea = extract_hidden_feature_from_track(track)
    return user_taste_model.predict(fea)


def predict_all_ratings(user_taste_model, catalog):
    """
    :return ratings: a dict mapping track_id to predicted rating.
    """
    ratings = dict(
        (track.id, predict_rating(user_taste_model, track))
        for track in catalog.tracks()
    )
    return ratings


def __rating_to_prob(rating):
    """Transform a rating of 1 to 5 to a non-negatie number proportational to
    its probability of being sampled.
    """
    # Exponential scale: one step higher in rating results in twice as much as
    # likely to be sampled.
    return float(2 ** rating)


def __sample_tracks_from_ratings(ratings, n, options):
    """
    :return track_ids: a list of string ids for tracks.
    """
    # TODO: allow filtering out certain track ids specified in `options`.
    track_ids_and_ratings = ratings.items()
    raw_rating_numbers = [x[1] for x in track_ids_and_ratings]
    probs = np.array(map(__rating_to_prob, raw_rating_numbers))
    probs = probs / max(probs.sum(), 1.)
    return np.random.choice([x[0] for x in track_ids_and_ratings],
        size=n, p=probs)


def recommend_n_tracks(catalog, user_taste_model, n, options):
    """Recommend n tracks from catalog based on user's taste model.

    :param catalog: a Catalog object.
    :param user_taste_model: a UserTasteModel object.
    :param n: the number of tracks to recommend.
    :return recommended_tracks: a list of Track objects.
    """
    ratings = predict_all_ratings(user_taste_model, catalog)
    sampled_track_ids = __sample_tracks_from_ratings(ratings, options)
    return [catalog[i] for i in sampled_track_ids]
