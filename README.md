
## Setup
The first thing to do is to clone the repository:
``` bash
$ git clone https://github.com/Hassan-Ahmadi/online_shop.git
$ cd online_shop
```

Create a virtual environment to install dependencies in and activate it:
``` bash
$ virtualenv2 --no-site-packages .venv
$ source .venv/bin/activate
```

Then install the dependencies:

``` bash
(venv)$ pip install -r requirements.txt
```

Once pip has finished downloading the dependencies:
``` bash
# For the first time run
(venv)$ python manage.py migrate

# create a super user
(venv)$ python manage.py createsuperuser
```

## Run
To run the project after completing the setup:

``` bash
(venv)$ python manage.py runserver

```