from flask import Flask
import os

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )

    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 註冊 Blueprints
    from .routes.main import main_bp
    from .routes.auth import auth_bp
    from .routes.library import library_bp
    from .routes.search import search_bp
    from .routes.comic import comic_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(library_bp, url_prefix='/library')
    app.register_blueprint(search_bp, url_prefix='/search')
    app.register_blueprint(comic_bp, url_prefix='/comic')

    return app

def init_db():
    from flask import current_app
    import sqlite3
    db = sqlite3.connect(current_app.config['DATABASE'])
    with current_app.open_resource('../database/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    db.close()
