python3 -m coverage run -m unittest
python3 -m coverage report
python3 -m coverage html

flask --app app/api.py --debug run
python3 -m unittest app/api_tests/account_crud.py
