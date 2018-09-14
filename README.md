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

Paste the database file: db.sqlite3 into the mARC-db/ folder

### Run server
```
$ python manage.py runserver

```
Then the database interface should be accessible at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/).
