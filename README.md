# purch-backend-api
Basic API for a purchasing and inventory application.

1. Update config.py and create your database.

2. Initialize flask migrate --> flask db init

3. run --> flask db upgrade

4. Seed database with provided data --> flask blueprint_db db_seed 

5. Run locally --> gunicorn -w 4 --bind 0.0.0:8005 wsgi::app
