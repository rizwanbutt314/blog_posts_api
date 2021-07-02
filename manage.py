import unittest

from app.main import create_app, load_routes

app = create_app('prod')

app.app_context().push()

# Load API routes
api = load_routes(app)


@app.cli.command("test")
def run_test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    app.run()
