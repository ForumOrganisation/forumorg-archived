# forum-prod

This is the repository for the official website of [Forum Organisation](https://forum-prod.herokuapp.com).

## Getting Started

These instructions will get help get your own copy of the project running on your local machine for development and testing purposes.

### Prerequisites

To get your development environment running, you need

```
Python 2.7, pip, mongodb
```

### Installing

To install the necessary python dependencies

```
pip install -r requirements.txt
```

Before starting the application, launch a mongodb instance, and create a database named `heroku_lx65hjrq`.
Within the database, create a collection named `companies`.
Finally, set the environnement variable `MONDODB_URI` to its uri.

```
export MONGODB_URI=mongodb://localhost:27017/heroku_lx65hjrq (most of the times)
```

To get the project running, simply start the Flask server:

```
python ./runserver.py
```

## Stack

* [Python](https://www.python.org/) - Primary language for development
* [Mongodb](https://www.mongodb.com/) - Database platform

## Authors

* **Mehdi BAHA** - [mehdibaha](https://github.com/mehdibaha)
* **Juliette BRICOUT** - [jbricout](https://github.com/jbricout)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details