[![codecov](https://codecov.io/gh/fras2560/InducedSubgraph/branch/main/graph/badge.svg?token=ZUB7EO8ESJ)](https://codecov.io/gh/fras2560/InducedSubgraph)

InducedSubgraph
===============

A web app that allows for the user to draw two graph G and H. It allows for the user to see if G contains an induced subgraph H.
Additional features such as coloring and checking graph properties were added. Check it out at [inducer]


Version
-----------

1.0

Dependencies
-----------

InducedSubgraph uses a number of open source projects:

* [Networkx] - NetworkX is a Python language software package for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks.
* [Flask] - Flask is a microframework for Python based on Werkzeug, Jinja 2 and good intentions.

Install Dependencies
-----------
```sh
	pip install -r requirements.txt
```

Start Server
-----------
```sh
	python run.py
```

Running Tests
-----------
```sh
	python -m unittest discover -s inducer/test
```

To run just a single test use:
```sh
	python -m unittest discover -s inducer/test -p <TEST_FILE_NAME>.py
```

Linting
-----------
This project uses flake8 for its linting. Any PR to master will check if there are any linting issues. It is recommended that one setups pep8 linting for their IDE / editor. To run the linter locally use
```sh
	pip install flake8
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 . --count --max-complexity=20 --max-line-length=127 --statistics --exclude=inducer/__init__.py
```


Contact
-----------
Feel free to contact me for ideas and help at [dallas.fraser.water@gmail.com]

License
----

MIT


[Networkx]:http://networkx.github.io/documentation/networkx-1.9/
[Flask]:http://flask.pocoo.org/
[inducer]:http://induced-subgraph.herokuapp.com/
[dallas.fraser.water@gmail.com]:mailto:dallas.fraser.water@gmail.com
