# VitalX - Web app!
My web app for recording historical health data


I have this configured on my linux laptop so it runs on boot. The idea being it opens up and I can quickly enter the details in from todays walk or last night's sleep. 


Future improvements will include getting this onto a linux virtual machine. 


## How it works
My docker compose yaml file is set to restart: unless-stopped for all services. When my laptop turns on and I log in, the docker services initialise and all of the containers spin up in the background. I've set chrome to sleep for 20 seconds before running the service to make sure it has enough time to bring everything up. There's also a health check to make sure the database is up and running so we don't run into a situation where the web app is up but it can't get the data from the database. 


## Docker Database
The database is now on Docker not on my laptop. 


# DO NOT RUN THIS SPECIFIC COMMAND - docker compose down -v
This will remove the databases. If you do this you will need to recreate the databases and then repopulate them from a backup. If this happens, to fix this you need to restore from one of the 2 backup options as you can see below. 


## Backups
I have configured this to automatically run daily backups of 2 kinds. CSV backups and a PG backup. the last entry of the day is the walk entry. After a walk is submitted it will create the backups and then I shut my laptop down. 


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
gunzip < backups/vitalx_backup_2026-08-16.sql.gz | docker exec -i vitalx_db psql -U postgres -d vitalx

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


## I've set chrome to autostart via this config file - nano ~/.config/autostart/vitalx.desktop - which has the below in:
[Desktop Entry]
Type=Application
Exec=bash -c "sleep 20 && google-chrome http://127.0.0.1:8050"
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=VitalX Auto Launch


## Weather API
The weather API (openmeteo) is set to run on an infinite loop. But this - on conflict (todays_date) do nothing; - makes sure that it only writes to the database once per day. 
    command: >
      sh -c "while true; do
        uv run python -m api.openmeteo.weather_api;
        sleep 86400;
      done"


## Notes
So I log in to my laptop and the web app opens straight away so I can type my details in. 

The UI layer is the dash app so it handles the layout, callbacks, user input and calling service functions. 
The service layer is the service.py and this is the logic for the app. New features go here.
The database layer handles loading the sql files, executing queries, fetching results etc

Once you make changes to the code, you need to restart your Docker containers to apply them with the below alias:
rstVX - (docker compose -f /home/marcus/Documents/VitalX/docker-compose.yml restart app && docker compose -f /home/marcus/Documents/VitalX/docker-compose.yml logs -f --tail=20 app')

Or, if you made changes to `docker-compose.yml` itself run this command:
docker compose up -d --build

I'm terrified of house fires (No idea why) so it's not on a raspberry pi but I am going to look into a Hetzner Linux VM and run all my web app stuff from a VM instead. For now my work around is auto run solutions. I'll wait till I have a few web apps before proceeding with this so there's a few work arounds until I get to this point. 

Author
Marcus Richardson





