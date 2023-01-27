# unbxd_team7
E-commerce website assignment <br>
Assignment briefing: https://docs.google.com/document/d/1x1ZnGbpnZDiuCTA8oWP1pvXK1Hdzw8XUlDzdjw5zQKM/edit?usp=sharing <br>
Design document: https://docs.google.com/document/d/1Mp1Vo7OnLveeC7cfIkHc3Lhp2cZCQvZFSeLbucDRczY/edit?usp=sharing <br>



# VENV setup 
1. Creating a new vent
    1. Python -m venv <venv-name>
    2. Source <venv-name>/bin/activate
2. freeze the pip requirements
    1. pip freeze > requirements.txt
3. (venv) pip install Flask redis flask_caching requests
    1. export FLASK_APP=app.py
    2. export FLASK_ENV=development

# Docker setup
1. Docker build
    1. docker compose up -d --build
    2. docker compose up
    3. docker compose down
2. ‘docker ps’ to list all runing containers


* NOTE
1. use docker image names instead of localhost in app.py connection with the postgres database
2. Ports used => make changes accordingly in the js files and app.py
    1. flask : 5002
    2. database : 5432
    3. database UI : 8080
    4. redis : 6379