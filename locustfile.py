import logging
from http import HTTPStatus

from locust import HttpUser, TaskSet, constant, task
from locust.exception import RescheduleTask

from sgdb.api.handlers import GameView
from sgdb.utils.testing import generate_games, url_for


class AnalyzerTaskSet(TaskSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.round = 0

    @staticmethod
    def make_dataset():
        games = generate_games(games_num=50)

        return games

    def request(self, method, path, expected_status, **kwargs):
        with self.client.request(method, path, catch_response=True, **kwargs) as resp:
            if resp.status_code != expected_status:
                resp.failure(f'expected status {expected_status}, '
                             f'got {resp.status_code}')
            logging.info(
                'round %r: %s %s, http status %d (expected %d), took %rs',
                self.round, method, path, resp.status_code, expected_status,
                resp.elapsed.total_seconds()
            )
            return resp

    def post_game(self, game):
        resp = self.request('POST', '/games', HTTPStatus.CREATED, json={**game})
        if resp.status_code != HTTPStatus.CREATED:
            raise RescheduleTask
        return resp.json()['data']['app_id']

    def get_game(self, app_id):
        url = url_for(GameView.URL_PATH, app_id=app_id)
        self.request('GET', url, HTTPStatus.OK,
                     name='/games/{app_id}/')

    def update_game(self, app_id):
        url = url_for(GameView.URL_PATH, app_id=app_id)
        self.request('PATCH', url, HTTPStatus.OK, name='/games/{app_id}/', json={"free": False})

    @task
    def workflow(self):
        self.round += 1
        dataset = self.make_dataset()

        for data in dataset:
            app_id = self.post_game(data)
            self.get_game(app_id)
            self.update_game(app_id)


class WebsiteUser(HttpUser):
    tasks = [AnalyzerTaskSet]
    wait_time = constant(1)
