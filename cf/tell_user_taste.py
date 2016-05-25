"""
    tell_user_taste.py
    ~~~
    This module calculates user taste by listening history

    :auther: Alexander Z Wang
"""

def tell_user_taste(user_ID):
    """Get user taste from listening history

    :param user_ID: user id
    :return user_taste: description of user taste
    :rtype: string
    """

    user_rate = get_user_rate_front_end(user_ID)

    user_tags_tmp = dict()

    for track in user_rate:
        tags_data = get_track_lastfm_tags(track)
        for value in tags_data:
            if value[0] in user_tags_tmp:
                user_tags_tmp[value[0]] += user_rate[track] * value[1]
            else:
                user_tags_tmp[value[0]] = user_rate[track] * value[1]

    sorted_user_tags_tmp = sorted(user_tags_tmp.items(), key=operator.itemgetter(1))
    weight = 0
    k = min(len(sorted_user_tags_tmp), 5)
    for i in range(0,k):
        weight += sorted_user_tags_tmp[i][1]

    taste_output = ""
    for i in range(0,k):
        taste_output += sorted_user_tags_tmp[0] + "," + str(int(sorted_user_tags_tmp[i][1] * 100.0 / weight)) + "%" + " "
