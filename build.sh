rm -rf dist
python setup.py sdist
twine upload dist/* -u $PYPI_USERNAME -p $PYPI_PASSWORD
