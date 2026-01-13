# About `tailswarm_src` and how the CLI is built

`tailswarm_src` contains the scripts and internals for the tailswarm cli, it is written in python. Instead of dealing with builds and different OSs I've opted just to ship the python code and include the dependencies in the lib directory.

The `tailswarm` does little more than call the python scripts.

## Libraries
The Tailswarm CLI uses the following libs, I have included the libraries directly in a lib folder to avoid any need to install dependencies and perform or perform build steps.
- Click
- pyYAML
- requests