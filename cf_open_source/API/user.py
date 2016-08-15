"""
    user.py
    ~~~
    This module provides all API for users

    :auther: Alexander Z Wang
"""

from sklearn.neural_network import MLPClassifier


def train_user_taste_model(track_hidden_features, user_ratings):
    """Get user taste model for prediction

    :param track_hidden_feature: hidden feature matrix of listened tracks
    :param user_rating: user rating vector of listened tracks
    :return user_model: user taste model classifiers
    :rtype: classifiers
    """

    user_model = MLPClassifier(
        hidden_layer_sizes=(5,), max_iter=3000, alpha=1e-2,
        algorithm='sgd', verbose=False, tol=1e-4, random_state=1,
        learning_rate_init=.01, activation='tanh')
    user_model.fit(track_hidden_features, user_ratings)

    return user_model


def predict_rating(user_model, track_hidden_features):
    """predict user rating score by user model

    :param user_model: user taste model classifiers
    :param track_hidden_features: hidden feature matrix of to be predicted
    :return prediction: predicted user rating score
    :rtype: list
    """

    prediction = user_model.predict(track_hidden_features)
    prediction = prediction.tolist()

    return prediction
