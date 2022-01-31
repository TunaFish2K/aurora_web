import os,definition,uuid

basedir=os.path.abspath(os.path.dirname(__name__))
env_prefix="AURORA_CORE:"
dirs={
    "database":"database"
}
CONFIG=definition.JsonConfig("config.json",init={
    "SECRET_KEY":"hard to guess string",
    "DATABASE_URI":"sqlite:///"+os.path.join(basedir,"db.sqlite"),
    "ADMIN_NAME":"!admin",
    "ADMIN_PASSWORD":"admin_pass_123456",
    "BACKGROUND_URI":"https://acg.toubiec.cn/random.php"
},auto_writeback=True)

class Config:
    SECRET_KEY=os.environ.get(env_prefix+"SECRET_KEY") or CONFIG.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_DATABASE_URI=os.environ.get(env_prefix+"DARABASE_URI") or CONFIG.get("DATABASE_URI")
    ADMIN_NAME=os.environ.get(env_prefix+"ADMIN_NAME") or CONFIG.get("ADMIN_NAME")
    ADMIN_PASSWORD=os.environ.get(env_prefix+"ADMIN_PASSWORD") or CONFIG.get("ADMIN_PASSWORD")
    BACKGROUND_URI=os.environ.get(env_prefix+"BACKGROUND_URI") or CONFIG.get("BACKGROUND_URI")
    @staticmethod
    def init_app(app):
        pass
    