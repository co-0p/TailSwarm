import subprocess
import json
import os

import click
import yaml


def simple_run_remote(cmd, node):
    run = subprocess.run(
        ['ssh',  "-o", "StrictHostKeyChecking=no", f'root@{node}', 'bash', '-c', f"'{cmd}'"]
    )
    return run.returncode

def run_remote(cmd, node):
    result = subprocess.run(
        ['ssh',  "-o", "StrictHostKeyChecking=no", f'root@{node}', 'bash', '-c', f"'{cmd}'"],
        capture_output=True, text=True, check=True
    )
    return result.stdout

def docker_remote(args, node):
    result = subprocess.run(
        args,
        capture_output=True, text=True, check=True,
        env={**os.environ, "DOCKER_HOST": f"ssh://root@{node}" }
    )
    return result.stdout

def get_self_environment():
    data = json.loads(subprocess.run(
        ["tailscale", "status", "--json"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout)
    for tag in data["Self"]["Tags"]:
        if tag.endswith("-environment"):
            return tag[4:]
    return None


def get_self_name():
    data = json.loads(subprocess.run(
        ["tailscale", "status", "--json"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout)
    return data["Self"]["HostName"]


def am_manager():
    data = json.loads(subprocess.run(
        ["docker", "info", "--format", "json"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout)
    my_address = data["Swarm"]["NodeAddr"]
    manager_addresses = data.get("Swarm", {}).get("RemoteManagers") or []
    for manager in manager_addresses:
        if my_address in manager["Addr"]:
            return True
    return False

def am_devmachine():
    result = subprocess.run(['tailscale', 'status', '--json'], capture_output=True, text=True)
    status_data = json.loads(result.stdout)
    return "tag:dev-machine" in status_data["Self"]["Tags"]

def get_tailswarm_config():
    with open('tailswarm.yml', 'r') as file:
        config = yaml.safe_load(file)
    return config

def get_nodes_in_environment(environment):
    result = subprocess.run(['tailscale', 'status', '--json'], capture_output=True, text=True)
    status_data = json.loads(result.stdout)
    # Find nodes with tags that match yaml environments
    nodes = set()
    for peer_id in status_data["Peer"]:
        peer = status_data["Peer"][peer_id]
        for tag in peer["Tags"]:
            if environment == tag.replace("tag:", ""):
                nodes.add(peer.get("HostName"))
    return nodes

def get_manager_nodes_in_environment(environment):
    result = subprocess.run(['tailscale', 'status', '--peers', '--json'],
                            capture_output=True, text=True, check=True)
    ts_status = json.loads(result.stdout)
    managers = set()
    for nodekey, peer_data in ts_status["Peer"].items():
        if f"tag:{environment}" in peer_data["Tags"]:
            output = run_remote("docker info --format '{{.Swarm.ControlAvailable}}'", peer_data["HostName"])
            if output.strip() == "true":
                managers.add(peer_data["HostName"])
    return managers

def get_current_tailnet_suffic():
    result = json.loads(subprocess.run(['tailscale', 'status', '--json'], capture_output=True, text=True).stdout)
    current_ts_suffix = result["CurrentTailnet"]["MagicDNSSuffix"].strip()
    return current_ts_suffix

def get_available_environments():
    # Find environments defined in yaml
    config = get_tailswarm_config()
    environment_names = set([key for key in config["environments"].keys()])
    # Find all nodes
    result = subprocess.run(['tailscale', 'status', '--json'], capture_output=True, text=True)
    status_data = json.loads(result.stdout)
    # Find nodes with tags that match yaml environments
    available_environments = set()
    for peer_id in status_data["Peer"]:
        peer = status_data["Peer"][peer_id]
        for tag in peer["Tags"]:
            env_name = tag.replace("tag:", "")
            if env_name in environment_names:
                available_environments.add(env_name)
    return available_environments

def get_all_node_labels(environment):
    manager_nodes = get_manager_nodes_in_environment(environment)
    if len(manager_nodes) == 0:
        click.echo("No manager nodes found")
        exit(1)

    cmd = "docker node ls -q | xargs docker node inspect --format json"
    response = json.loads(run_remote(cmd, manager_nodes.pop()))

    return { item["Description"]["Hostname"]: set(item["Spec"]["Labels"].keys()) for item in response }


