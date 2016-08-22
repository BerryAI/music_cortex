"""Run this script to retrieve user ratings from ACAI game and save it to file.
"""
import sys
from os import path
import json
CMD = path.dirname(path.realpath(__file__))
sys.path.append(path.join(CMD, '../read_game_data'))
from acai_game import get_user_rate_dict

ratings = get_user_rate_dict()
json.dump(ratings,
          open(path.join(CMD, '../data/acai_game_user_ratings.json'), 'w'))
