# VitalX - Web app!
My web app for recording historical health data. I created this because I wanted to push myself to go outside more and be healthier. I thought it would add an element of excitement and it did just that! It's incredible seeing the data accumulate daily. I can't wait to see my stats in 10 years!


I have this configured on my linux laptop so it runs on boot. The idea being it opens up and I can quickly enter the details in from todays walk or last night's sleep. Future goals are to get this onto a raspberry pi. I'll always be looking into networking options so I can access it from my phone from anywhere. 


## How it works
My docker compose yaml file is set to restart: unless-stopped for all services. When my laptop turns on and I log in, the docker services initialise and all of the containers spin up in the background. I've set chrome to sleep for 20 seconds before running the service to make sure it has enough time to bring everything up. There's also a health check to make sure the database is up and running so we don't run into a situation where the web app is up but it can't get the data from the database. 

Once it's on a pi I will just bring up the containers and leave them up. I'll only need to interact with it if there's an issue. 


## Docker Database
The database is now on Docker so I access the data by using docker exec commands in the terminal. 


## Backups
I have configured this to automatically run daily backups of 2 kinds. CSV backups and a PG backup. the last entry of the day is the walk entry. After a walk is submitted it will create the backups and then I shut my laptop down. 

Once this is on a pi I will be configuring the backups to run via the database instead of .py files. It's a workaround I've put in place until I have a pi. I have risk accepted that I don't fully understand the pg backup routine but it's working so i'm not concerned. 


# Restoring from back ups
## CSV backups

run the below to drop the database, create the database, create the schemas and then use the csv backup module to populate the databases via the csv

docker exec -it vitalx_db psql -U postgres -c "DROP DATABASE vitalx;"
docker exec -it vitalx_db psql -U postgres -c "CREATE DATABASE vitalx;"
docker exec -it vitalx_app uv run python -c "from vitalx.dbutils import create_schemas; create_schemas()"
docker exec -it vitalx_app uv run python -m src.vitalx.csv_backup

Then verify with the below command
docker exec -it vitalx_db psql -U postgres -d vitalx -c "
SELECT 'vitalx_walk' AS table_name, COUNT(*) FROM vitalx_walk
UNION ALL
SELECT 'vitalx_sleep', COUNT(*) FROM vitalx_sleep
UNION ALL
SELECT 'vitalx_streak', COUNT(*) FROM vitalx_streak
UNION ALL
SELECT 'weather', COUNT(*) FROM weather;
" 

and this to make sure the data is in the database

docker exec -it vitalx_db psql -U postgres -d vitalx -c "SELECT * FROM vitalx_walk;"

# PG Backups

run the below to drop the database, create the database, create the schemas and then use the pg backup module to populate the databases via the csv

docker exec -it vitalx_db psql -U postgres -c "DROP DATABASE vitalx;"
docker exec -it vitalx_db psql -U postgres -c "CREATE DATABASE vitalx;"
docker exec -it vitalx_app uv run python -c "from vitalx.dbutils import create_schemas; create_schemas()"
run the below on linux (Change the date in the file name to today):
gunzip < backups/vitalx_backup_2026-08-28.sql.gz | docker exec -i vitalx_db psql -U postgres -d vitalx
run the below on mac (Change the date in the file name to today):
gunzip -c backups/vitalx_backup_2026-08-28.sql.gz | docker exec -i vitalx_db psql -U postgres -d vitalx

Then verify with the below command
docker exec -it vitalx_db psql -U postgres -d vitalx -c "
SELECT 'vitalx_walk' AS table_name, COUNT(*) FROM vitalx_walk
UNION ALL
SELECT 'vitalx_sleep', COUNT(*) FROM vitalx_sleep
UNION ALL
SELECT 'vitalx_streak', COUNT(*) FROM vitalx_streak
UNION ALL
SELECT 'weather', COUNT(*) FROM weather;
" 

and this to make sure the data is in the database

docker exec -it vitalx_db psql -U postgres -d vitalx -c "SELECT * FROM vitalx_walk;"


## Whilst this is on my linux laptop, I've set chrome to autostart via this config file - nano ~/.config/autostart/vitalx.desktop - which has the below in:
[Desktop Entry]
Type=Application
Exec=bash -c "sleep 20 && google-chrome http://127.0.0.1:8050"
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=VitalX Auto Launch


## Weather API
The weather API (openmeteo) is set to run on an infinite loop. But this - on conflict (todays_date) do nothing; - makes sure that it only writes to the database once per day. Once this is on a pi i'll be able to adjust this with either a cron job or another solution. 

    command: >
      sh -c "while true; do
        uv run python -m api.openmeteo.weather_api;
        sleep 86400;
      done"


## Notes
So currently, I log in to my laptop and the web app opens after 20 seconds so I can type my details in. I enter my sleep details in a morning and my walk details in an evening. Once I enter my walk details, it takes automated backups. 

The UI layer is the dash app so it handles the layout, callbacks, user input and calling service functions. 
The service layer is the service.py and this is the logic for the app. New features go here.
The database layer handles loading the sql files, executing queries, fetching results etc

Once you make changes to the code, you need to restart your Docker containers to apply them with the below alias:
rstVX - (docker compose -f /home/marcus/Documents/VitalX/docker-compose.yml restart app && docker compose -f /home/marcus/Documents/VitalX/docker-compose.yml logs -f --tail=20 app')

Or, if you made changes to `docker-compose.yml` itself run this command:
docker compose up -d --build

# setting up
- make sure docker is installed on your device
- run uv sync
- run uv pip install -e .
- Make sure your .env file exists and looks like this
DB_USER=postgres
DB_PASSWORD=passwordhere
DB_HOST=localhost
DB_PORT=5432
DB_NAME=vitalx
- Make sure there's no native postgres instance running:
sudo lsof -i :5432 
if this returns entries run this
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/homebrew.mxcl.postgresql*.plist 2>/dev/null
then verify with the lsof command again to make sure nothings there
(I would recommend not having a native pg setup to keep things simple. databases are seamless in docker anyway.)
- Run docker compose up -d to bring the containers up. 
- Then run this to create the tables:
  uv run -m vitalx.dbutils
- Then follow either the csv or pg backup steps above
- then go to 127.0.0.1:8050 and you'll see your data


Author
Marcus Richardson
