import os
from flask_migrate import Migrate
from app import create_app, db
from app.models import User, Role, Permission

app = create_app(os.getenv('BLOG_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    """Make shell context"""
    return dict(db=db, User=User, Role=Role, Permission=Permission)


@app.cli.command()
def test():
    """Run unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
