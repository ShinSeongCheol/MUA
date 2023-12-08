from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from sqlalchemy import MetaData


naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()
scheduler = APScheduler()


def create_app():
    app = Flask(__name__)
    app.config.from_envvar("APP_CONFIG_FILE")

    # ORM
    db.init_app(app)
    if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

    # 스케줄 설정
    scheduler.init_app(app)

    from mua.util.scheduler import updateWorld, updateWorldRank

    with app.app_context():
        db.create_all()

    # 월드 정보
    updateWorld()
    scheduler.start()

    from .views import main, user

    app.register_blueprint(main.bp)
    app.register_blueprint(user.bp)

    return app
