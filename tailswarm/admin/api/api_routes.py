import subprocess
from lib.bottle import route, template, static_file


@route('/api/test/<word>')
def index(word):
    return template('<b>Hello {{word}}</b>!', word=word)

@route('/api/join')
def join(type):
    print(f"Request to join a {type}")
    return {   
        "join_command": subprocess.run(
            ["docker", "swarm", "join-token", "worker"], 
            capture_output=True,
            text=True,
            check=True,
        ).stdout,
    }