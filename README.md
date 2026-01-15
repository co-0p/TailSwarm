# TailSwarm

Scripts and configs to make tailscale and docker swarm play nicely together. Docker Swarm is almost great, and Tailscale + some scripts can get it there.



## The Opinionated Stack
- Dockerswarm to run containers on your nodes
- Tailscale to manage and connect between nodes
- Github Actions and GitHub Container Registy
- `tailswarm` config files and CLI tool to set it up and make all the bits work nicely (requires Python3)
- Admin dashboard for monitoring, running commands, and managing nodes

## Quickstart

**Setting up first manager node**
1. Create a Tailscale account and new tailnet (don't try to use an existing one, Tailswarm will overwrite the settings). Also connect your dev machine to the tailnet.
2. Create a Tailscale API key for use in step 5
3. Create a GitHub Personal Access Token (Classic) for use in step 5 (wil xyz permissions)
4. On a fresh server or VM (running Ubuntu or Debain), run as root the following `curl -sfL http://example.com/tailswarm | bash -s -- init`
5. This will download and run the Tailswarm agent, which will set up Tailscale and Docker on the machine. Follow the directions as prompted.
	- Select environment (production, testing, staging, local, etc.)
	- Input Tailscale API key
	- Input Gihub Public-Access-Token (classic)

**Connecting additional nodes**

1. Visit the admin dashboard from a development machine on your tailnet. You can get this from the CLI with `tailswarm admin`
2. On a fresh server or VM (running Ubuntu or Debain), run as root the following `curl -sfL http://example.com/tailswarm | bash -s -- join`


## Concepts

- Manager nodes are a Docker Swarm concept, they control the goings on, there should always be an odd number of them, and in Tailswarm they also run an instance of the admin server.
- The admin server is a stateless web UI that is available to tag:dev-machines, and a REST server available to all other nodes within the environment.
- By default Tailswarm has the concepts of different environments "production", "staging", "testing", "local". You can add more. Make sure you add your development computers to the tailnet under "dev-machine", they don't need an environment tag.
- Tailswarm uses Tailscale tags and groups to isolate resources and permissions
- Be careful editing the `tailscale/policy.hujson` file, because there are hardcoded assumptions the rest of the system relies on.

## Using the CLI


## FAQ

- "Is it ready for production?"- Probably not
- "Why not use K8s?" - Yes, why not? K8s (or K3s or whatever) are great, but they can be a lot to manage, and there is a fair learning curve. If you have a good handle on Docker and Tailscale already, and you plan on managing a smallish number or nodes, then maybe TailSwarm makes sense.
- "Why not Kamal, Dokku, etc." - Again, all great and easy to use, but if you want some Docker Swarm features not supported then you make like to start with TailSwarm.
- "Isn't Docker Swarm dead" - Not really, it's true that it's not actively being developed much these days, but it's in a battle tested and robust state of maintanance. Many enterprises still use it so it's quite unlikely that Docker will cease support. 
- ""