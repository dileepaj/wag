# Welcome to WAG

## How to start development

### Step 1: Install pip

    	$ sudo apt-get install python-pip

### Step 2: Install MongoDB

#### For Ubuntu
	
    	$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
    
    	$ echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list

    	$ sudo apt-get update
    	
    	$ sudo apt-get install -y mongodb-org

#### For Windows
	
#### Download the MSI file and install
	https://www.mongodb.com/download-center?jmp=docs
	
#### Installation Instructions
	https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/
	
### Step 3: Installing dependencies
navigate into the git repo directory and type the following:

    $ pip install -r requirements.txt
    
### Step 4: Install PDFKIt

#### For Ubuntu

	https://pypi.python.org/pypi/pdfkit
	
#### For Windows

	http://wkhtmltopdf.org/downloads.html

This will install all python dependencies.


### Step 8: All done! Now run the development server

    ~/home/wag$ python runserver.py

Hack away! :D
