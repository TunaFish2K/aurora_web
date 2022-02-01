from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from config import Config

bootstrap=Bootstrap()
login_manager=LoginManager()
login_manager.login_view='auth.login'
db=SQLAlchemy()

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)
    Config.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    

    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    from .server import server as server_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint,url_prefix="/auth")
    app.register_blueprint(server_blueprint,url_prefix="/server")
    
    app_ctx=app.app_context()
    app_ctx.push()
    db.create_all()
    from .models import User
    if db.session.query(User).filter_by(username=Config.ADMIN_NAME).count() <1:
        admin=User(username=Config.ADMIN_NAME,password=Config.ADMIN_PASSWORD)
        db.session.add(admin)
        db.session.commit()
    app_ctx.pop()
    return app