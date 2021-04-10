#Agents in Improvisational Live Coding

The computational tool provided in this repository is to be used in the Extempore live coding environment.

The following are the requirements which must be install before using this tool: 
- [Python](https://www.python.org/downloads/) 
- [pip](https://www.makeuseof.com/tag/install-pip-for-python/)
- [Extempore](https://extemporelang.github.io/docs/overview/install/)
- [VS Code Editor](https://code.visualstudio.com/download) 

Set Up:
1. Install the python dependencies by running `pipenv install` from the commandline within the 'Artefacts' directory
2. Install the text editor extension with `code --install-extension vscode-extempore-0.0.9.vsix`

Using to the agent: 
1. Activate the virtual environment with `pipenv shell`
2. run the agent script with `python agent.py`. You will see the agent "listening for messages..."
3. Open your text editor and, once the Extempore setup code is compiled, enter the command 'Hello Agent' into the command pallete. This will connect you to localhost on port 5005.
4. When promted for the control setting, enter `1` to connect to the suggestive agent or `2` to connect to the assertive agent.
5. To request a change to a new pattern, move your cursor within the scope of the pattern and hit `ctr`+`m`.
6. To request a change to the pattern which is currently in the agent's memory, hit `ctr`+`x`.