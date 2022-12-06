# purch-backend-api
Basic API for a purchasing and inventory application.

1. Update config.py for your database.

2. Create tables -- > flask blueprint_db db_create

3. Initialize flask migrate --> flask db init

4. run --> flask db upgrade

5. Seed database with provided data --> flask blueprint_db db_seed 

6. Run locally --> gunicorn -w 4 --bind 0.0.0:8005 wsgi::app
