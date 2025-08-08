import os
from flask_injector import inject
from providers.MongoProvider import MongoProvider
from providers.UserProvider import UserProvider

data_provider = MongoProvider()
user_provider = UserProvider()


@inject
def create_user(steamUser):
    return user_provider.create_user(steamUser)

@inject
def read_game_by_title(gameTitle):
    game = data_provider.read_game_by_title(gameTitle)
    print(game)
    return data_provider.read_game_by_title(gameTitle)

@inject
def read_all_games():
    return data_provider.read_all_games()

@inject
def update_user(updateUser):
    return user_provider.update_user(updateUser)

@inject
def delete_user(deleteUser):
    return user_provider.delete_user(deleteUser)


def basic_auth(username, password, required_scopes=None):
    if username == os.environ.get('ADMIN_USERNAME', 'admin') and password == os.environ.get('ADMIN_PASSWORD', 'password'):
        return {'sub': 'admin'}
    # optional: raise exception for custom error response
    return None
