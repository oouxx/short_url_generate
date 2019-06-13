import unittest

import coverage
from flask_cors import CORS
from flask_script import Manager

from MyApp import create_app, db

app = create_app()
manager = Manager(app)
CORS(app, resouces='/*')
COV = coverage.coverage(
    branch=True,
    include='./*',
    omit=[
        './tests/*'
    ]
)
COV.start()


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('./tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


@manager.command
def recreate_db():
    """重建数据库"""
    db.drop_all()
    # 要导入model,会自动收集创建
    db.create_all()
    db.session.commit()


@manager.command
def test():
    """运行测试"""
    tests = unittest.TestLoader().discover('./tests', pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == "__main__":
    manager.run()
