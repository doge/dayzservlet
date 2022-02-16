### This repository is unmaintained as of Feburary 16, 2022.

# DayZServlet
A python-flask implementation of the servlet used for the legacy versions of DayZ.

<sup>This has only been tested on version 0.46.124490.</sup>

### What does this do?
Older versions of DayZ Standalone make post/get requests to certain endpoints that relate to the saving, killing and creation of players. DayZServlet replicates the functions that these endpoints do in order to allow you to play legacy versions of DayZ with player saves. Instead of storing data in a MySQL database like how the game normally does it, I decided to use MongoDB as it is easier and faster to use.

| Endpoints                |
| ------------------------ |
| /DayZServlet/lud0/find   |
| /DayZServlet/lud0/load   |
| /DayZServlet/lud0/create |
| /DayZServlet/lud0/save   |
| /DayZServlet/lud0/queue  |
| /DayZServlet/lud0/kill   |

## Running DayZServlet
First, you wil need to configure `config.py` so it is setup with the credentials to your MongoDB instance.

Then, run these commands;

`pip install -r requirements.txt`

`python server.py`

Then, in your `init.sqf` file in your mission, add this line at the bottom;

`dbSelectHost "http://localhost:5000/DayZServlet/";`
