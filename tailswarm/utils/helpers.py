import subprocess
import json


def get_self_environment():
    data = json.loads(subprocess.run(
        ["tailscale", "status", "--json"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout)
    for tag in data["Self"]["Tags"]:
        if tag.endswith("-environment"):
            return tag
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
        if manager["Addr"].contains(my_address):
            return True
    return False


def get_manager_address():
    data = json.loads(subprocess.run(
        ["docker", "info", "--format", "json"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout)
    
    managers = data.get("Swarm", {}).get("RemoteManagers", [])
    if not managers:
        return None
    
    manager_addr = managers[0]["Addr"]
    ip = manager_addr.split(':')[0].strip()
    return ip


def get_manager_name():
    manager_address = get_manager_address()
    if not manager_address:
        return None
    
    result = json.loads(subprocess.run(
        ['tailscale', 'whois', '--json', manager_address],
        capture_output=True,
        text=True
    ).stdout)
    name = result.get('Machine', {}).get('Name')
    return name
