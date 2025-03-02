BoardGameRental
About

Project for webaplication to rent boardgames Inspired to upgrade pyrkon's gamesroom app ;)

using postgressql to store data

to launch:

docker-compose build
docker-compose run web python manage.py migrate
optionally:
    docker-compose run web python manage.py collectstatic
docker-compose up 

