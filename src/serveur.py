
from flask import Flask
from flask import request


app = Flask(__name__)



#methode d'extinction de serveur depuis le browser -> a utiliser que si on reste sur du local
#sinon regarder 
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

@app.route("/")
def hello():
    return "Hello, World!"