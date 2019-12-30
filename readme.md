# Small applet for automatically creating and indexing customers/projects
## Setting up a development environment

- open folder in terminal
- create virtualenvironment `virtualenv venv`
- activate environment `source venv/bin/activate`
- install requirements `pip install -r requirements.txt`

## Bundle app into executable
- virtualenvironment must be activated
- python setup.py py2app
- you find the exectubale in subfolder dist
- you might need to change file permissions for the app. On mac you can open the app like a folder on right click.
 Then change the permissions for that folder and recursively for all subfolders.