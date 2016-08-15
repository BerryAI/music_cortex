"""Load a sample user rating data, train a recommendation engine,
and see what tracks get recommended.
"""

import openacai as oa
from oa.data import get_example_ratings


example_ratings = get_example_ratings()

# engine = oa.RecommendaionEngine(catalog=SimpleCatalog())
engine = oa.RecommendaionEngine()
engine.train(ratings=exapmle_ratings)

one_user = engine.get_users()[0]
ratings = engine.get_ratings(user_id=one_user.id)
print ratings

# Recommend tracks for a user.
recommended_tracks = engine.recommend(user_id=one_user.id, n=10)
print recommended_tracks

# Recommend tracks based on seed tracks.
example_track_ids = [track.id for track in engine.tracks()[0:2]]
recommended_tracks = engine.recommend(seed_track_ids=example_track_ids, n=10)
print recommended_tracks
