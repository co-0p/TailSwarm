# TailSwarm 🐳🐝

Scripts and configs to make tailscale and docker swarm play nicely together. Docker Swarm is almost great, and Tailscale + some scripts can get it there.

## The Opinionated Stack
- Dockerswarm to run containers on your nodes
- Tailscale to manage and connect between nodes
- `tailswarm` config files and CLI tool to set it up and make all the bits work nicely (requires Python3)

# Using it

## Deploying
When you run `tailswarm deploy --environment testing-environment`, the cli will look at your `tailswarm.yaml` file,
and deploy what you have defined inside of the defined environment. Stacks are compose files located at `dockerswarm/stacks`

**Remember:** Stacks are deployed to the swarm before the deploy labels are changed, and deploy labels are not changed atomically.

# TODO
- Compute changes
- Deploy single stack
- Status
- Show logs
- Make pretty
- Promote from dev machine
- Command to copy files to a node
- Set a secret
- Self upgrade