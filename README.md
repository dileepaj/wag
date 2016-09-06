# Welcome to WAG

## How to start development
### Step 1: Install pip

    $ sudo apt-get install python-pip

### Step 2: Install MongoDB
	
    $ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10
    
    $ echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/10gen.list

    $ sudo apt-get update

    $ sudo apt-get install mongodb-10gen


### Step 3: Installing dependencies
navigate into the git repo directory and type the following:

    $ pip install -r requirements.txt

This will install all python dependencies.


### Step 8: All done! Now run the development server

    ~/home/wag$ python runserver.py

Hack away! :D