from flask_testing import TestCase
from MyApp import db
from MyApp import redis_store
from MyApp import create_app

app = create_app()


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object('config.development.Config')
        return app

    def setUp(self):
        from MyApp.models import ShortCodes
        db.create_all()
        redis_store.flushdb()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        redis_store.flushdb()
