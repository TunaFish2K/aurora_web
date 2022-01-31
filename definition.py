import json,os
from typing import Any
class JsonConfig:
    def __init__(self,filename:str,init:dict,auto_writeback:bool=False) -> None:
        self.filename=os.path.realpath(filename)
        self.auto_writeback=auto_writeback
        with open(self.filename,"w+") as f:
            self.config=f.read()
        if self.config:
            self.config=json.loads(self.config)
        else:
            self.config=init.copy()
            self.restore()
    def set(self,key:str,value:Any):
        self.config[key]=value
        if self.auto_writeback:
            with open(self.filename,"w") as f:
                f.write(json.dumps(self.config))
    def get(self,key:str):
        try:
            return self.config[key]
        except KeyError:
            return None
    def restore(self):
        with open(self.filename,"w") as f:
            f.write(json.dumps(self.config))
    def sync(self):
        with open(self.filename,"w+") as f:
            self.config=f.read()
        if self.config:
            self.config=json.loads(self.config)
        else:
            self.config={}