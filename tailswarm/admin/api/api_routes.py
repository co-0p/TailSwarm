import subprocess
from bottle import route, template, static_file


@route('/test/<word>')
def index(word):
    return template('<b>Hello {{word}}</b>!', word=word)

@route('/join')
def join(type):
    output = subprocess.run(
        ["docker", "swarm", "join-token", "worker"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout

    key = output.strip().split(" ")[-2]

    return {
        "join_token": key,
    }