from flask import Flask

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # ... configuration settings ...

    # 💥 Register the Blueprint from routes.py 💥
    from . import routes
    app.register_blueprint(routes.bp)
    
    return app