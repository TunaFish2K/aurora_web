from waitress import serve
from aurora_core import app 
import sys
try:
    ip,port=sys.argv[1].split(":",maxsplit=1)
except:
    print("参数错误！")
    print("例：")
    print(sys.argv[0],"127.0.0.1:8080")
else:
    serve(app=app)