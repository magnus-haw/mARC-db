# mARC-db

This is a python app for accessing mARC data using the Django webserver framework

## Running Locally on Windows

Make sure you have both [git](https://git-scm.com/download/win) and [Python3](https://repo.anaconda.com/archive/Anaconda3-5.2.0-Windows-x86_64.exe). Then you can clone the project and install the requirements:

### Install using Anaconda distribution
```sh
$ git clone https://github.com/magnus-haw/mARC-db.git
$ cd mARC-db
$ conda create --name mARC numpy pandas django bokeh
$ conda activate mARC
```

### Install using pip
```sh
$ git clone https://github.com/magnus-haw/mARC-db.git
$ cd mARC-db
$ pip install -r requirements.txt
```

### Run server
Execute the following command in the mARC-db/ folder:
```
$ python manage.py runserver

```
Alternatively Windows users can create a '.bat' file (e.g. run-mARC-server.bat) with the following content:
```
ECHO OFF
ECHO This is the mARC 2.0 database server. Interface accesible through browser at: http://127.0.0.1:8000
c:\Users\%USERNAME%\AppData\Local\Continuum\anaconda3\python.exe "Z:\mARC II documents\mARC-db\manage.py" runserver
```
The location of the python executable and the mARC-db folder may need to be changed depending on the users installation. 
Running this '.bat' file will also start the server.

After starting the server, the database interface should be accessible at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/).
