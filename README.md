# TruView
The purpose of this project is to create a way to generate a way to analyze reviews of a product or service to see the numbers of people who say similiar things about it.

## Requirements
Python 3.6.x

## Setup:
#####It is recomended that you create a virtual environment for this.
To do this, run the following pip commands:

        pip install virtualenv
        virtualenv -p python3 truview_env
        source truview_env/bin/activate

----
* Clone this repository using git, or downloading the zip file.
* Enter into the project root directory


        cd trureview/
        
* Use Pip to install the requirements

		 pip install -r requirements.txt
		 python -m spacy.en.download all
		 
* Then use gunicorn to run the server

        gunicorn --worker-class gevent --timeout 120 trureview:app
    