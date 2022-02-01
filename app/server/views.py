from re import L
import flask
import sys,socket,threading,os

from flask_login import current_user, login_required
from . import server as server_blueprint
from .forms import *

class Server:
    def __init__(self,target_host,target_port,core="core",java="java") -> None:
        self.settings={"core":core,"java":java,"host":target_host,"port":target_port}
        self.is_linux=(sys.platform=="linux")
    def send(self,command:str):
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.connect((self.settings["host"],int(self.settings["port"])))
        com=command.encode(encoding="utf-8")
        sock.sendall(com)
        sock.close()
    def worker(self,directory:str,lst:str):
        os.chdir(directory)
        os.system(lst)
    def start(self):
        java=self.settings.get("java",None) or "java"
            
        j_max=self.settings.get("max",None) or ""
        j_min=self.settings.get("min",None) or ""   
        a="-Djline.terminal=jline.UnsupportedTerminal"
        b="-jar"
        try:
            name=self.settings["core"]
            #if not name.startswith('"') and not name.endswith('"'):
            #    name='"'+name+'"'
        except:
            return flask.redirect(flask.url_for("main.server"))
        path=os.path.dirname(os.path.abspath(name))+os.sep
        c="nogui"
        lst=" ".join([java,"-Xmx"+j_max,"-Xms"+j_min,a,b,name,c])
        print(lst)
        a=threading.Thread(target=self.worker,args=(path,lst))
        a.start()
        return flask.redirect(flask.url_for("main.server"))
    def _command(self,com):
        try:
            self.send(com)
        except Exception as e:
            print("error:",e)
        return flask.redirect(flask.url_for("main.server"))
    def _start(self):
        self.start()
        return flask.redirect(flask.url_for("main.server"))
    def _mset(self,key,value):
        self.settings[key]=value
        return flask.redirect(flask.url_for("main.server"))
    def _settings(self):
        return flask.jsonify(self.settings)
    def _properties(self):
        form=PropertiesEdit()
        if form.validate_on_submit():
            with open(os.path.dirname(os.path.abspath(self.settings["core"]))+os.sep+"server.properties","w+") as f: 
                f.write(form.edit.data)
            return flask.redirect(flask.url_for("server.mc_properties"))
        try:
            with open(os.path.dirname(os.path.abspath(self.settings["core"]))+os.sep+"server.properties","r+") as f: 
                form.edit.data=f.read()
        except FileNotFoundError:
            form.edit.data=""
        return flask.render_template("server/properties.html",user=current_user._get_current_object(),form=form)
c=Server(target_host="127.0.0.1",target_port="9028")
@server_blueprint.route("/command/<path:com>/")
@login_required
def mc_command(com):
    return c._command(com)
@server_blueprint.route("/start/")
@login_required
def mc_start():
    return c._start()
@server_blueprint.route("/stop/")
@login_required
def mc_stop():
    return flask.redirect(flask.url_for("server.mc_command",com="stop"))
@server_blueprint.route("/set/<key>/<path:value>/")
@login_required
def mc_set(key,value):
    return c._mset(key,value)
@server_blueprint.route("/settings/")
@login_required
def mc_settings():
    return c._settings()
@server_blueprint.route("/properties/",methods=["GET","POST"])
@login_required
def mc_properties():
    return c._properties()