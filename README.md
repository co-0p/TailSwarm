# TailSwarm

The TailSwarm cli is a tool to make working in a Docker Swarm + Tailscale infrastructure stack easy and declarative.

> Note: This is a very early release, probably not ready for production use. I am currently dogfooding it for my own project, but please be careful with it.
> Please assume that the cli or config interface could change.

You can find the latest build from the [GitHub releases section](https://github.com/co-0p/TailSwarm/releases).
Requirements, be on a nix machine with Python 3 installed.

Further documentation coming soon.

### The Opinionated Stack
- The `tailswarm` CLI and config file, as an abstraction layer lets you manage your Swarm declaratively and easily
- [Docker Swarm mode](https://docs.docker.com/engine/swarm/) to orchestrate containers on your nodes
- [Tailscale](https://tailscale.com/) to connect and discover nodes, segregate environments (testing, prod, etc.),
and streamline aspects of managing Swarm

### Why?

Docker Swarm Mode is an awesome tool, it is lighter and simpler than K8s, and is very approachable for anyone familiar with Docker.
It should have become the go-to tool for individuals or small teams who need to run a handful of containers on a handful of nodes.
In my opinion it has been held back for usability reasons, the functionality is all there, but to make it usable requires writing
a bunch of custom scripts and managing nodes manually, this is where it falls behind compared to newer options like Coolify, Kamal, etc.

But by supercharging it with Tailscale, a clean CLI, and a declarative yaml config file, we solve most of these issues and can easily manage
multienvironment projects with ease, and get to use a powerful battle tested orchestrator.

### Concepts

- We define a Tailscale tag for each environment `testing-environment`, `production-envrionment`, etc.
- We also define a tag for the developer's computer `dev-machine`, and for a CI job `ci-runner`
- Tailscale ACLs and SSH rules are set for the following:
  - Nodes with environment tags can access each other (but not by SSH)
  - `dev-machine` and `ci-runner` nodes can access all environment nodes (including by SSH)
- Swarm nodes connect over the Tailnet
- `tailswarm.yml` can be used to define Swarm labels to nodes, enable and disable stacks, and set environment variables
- `tailswarm` the cli uses the config file, the Tailscale cli, and Docker cli, to make everything simple 

One still needs to have a basic understanding of how Swarm works to make the most of things, but no long has to manage nodes individually with the CLI

### Todo List
- [ ] Compute changes before a deployment
- [ ] Status command
- [ ] Show logs command
- [ ] Make beautiful
- [ ] Cleaner interaction from both manager nodes and dev machines
- [ ] Command to copy files to a node
- [ ] Set swarm secrets
- [ ] Self upgrading script
- [ ] Create example repository